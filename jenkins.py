#!/usr/bin/python

from errbot import BotPlugin, botcmd, arg_botcmd
import jenkins
import time



class JENKINS(BotPlugin):
    """
    Very simple JENKINS plugin
    """

    def __init__(self, *args, **kwargs):
        super(JENKINS, self).__init__(*args, **kwargs)
        self.server = jenkins.Jenkins('', username='', password='')
       

    @botcmd
    def jenkins_list_jobs(self, msg, args):
        """
        List jenkins jobs.
        """
        yield  "Your task is now processing..."
        jobs = self.server.get_jobs()
        max_length = max([len(job['name']) for job in jobs])
        yield self.send_card(
                    title='Jenkins jobs',
                    in_reply_to=msg,
                    body=('\n'.join(
          ['{2})  <{1}|{0}> '.format(job['name'].ljust(max_length), job['url'], (counter + 1)) for counter, job in
          enumerate(jobs)]).strip())
                   
                )

    def _get_job_url(self, job_name):
        jobs = self.server.get_jobs()
        for job in jobs:
          if job['name'] == job_name:
            return job['url']
        return None
        

    @botcmd
    def list_running_jenkins_job(self, msg, args):
        """
        List running jenkins jobs.
        """
        yield  "I will ask for the current running builds list!"
        jobs = [job for job in self.server.get_jobs() if 'anime' in job['color']]
        jobs_info = [self.server.get_job_info(job['name']) for job in jobs]
        if not jobs_info:
         yield "There is no running jobs!"
        else:
         yield self.send_card(
                    title='Jenkins running jobs',
                    in_reply_to=msg,
                    body=('\n\n'.join(
            ['<{1}|{0}>\n{2}'.format(job['name'], job['lastBuild']['url'], job['healthReport'][0]['description']) for
             job in jobs_info]).strip())

                )


    @arg_botcmd('job_name', type=str)
    def execute_jenkins_job(self, msg, job_name=None):
        """
        execute jenkins job.
        """
        try:
         url = self._get_job_url(job_name)
         if url:
          yield  'Please wait job is being executed, use below url to check the progress.\n{0}'.format(
                                                          url)
        
         last_build_number = self.server.get_job_info('{0}'.format(job_name))['lastCompletedBuild']['number']
         new_build_number = self.server.get_job_info('{0}'.format(job_name))['lastCompletedBuild']['number']
         self.server.build_job('{0}'.format(job_name))
         while new_build_number == last_build_number:
             time.sleep(2)
             new_build_number = self.server.get_job_info('{0}'.format(job_name))['lastCompletedBuild']['number']
         output=self.server.get_build_console_output('{0}'.format(job_name), new_build_number)
         yield self.send_card(
                    title='{0}#Build_{1}'.format(job_name,new_build_number),
                    in_reply_to=msg,
                    body="{0}".format(output)

                )

        except jenkins.NotFoundException:
         yield "Sorry, I can't find the job. Typo maybe?"

                



