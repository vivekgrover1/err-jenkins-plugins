#!/ur/bin/python

from errbot import BotPlugin, botcmd
import jenkins


class JENKINS(BotPlugin):
    """
    Very simple JENKINS plugin
    """

    def __init__(self, *args, **kwargs):
        super(JENKINS, self).__init__(*args, **kwargs)
        self.server = jenkins.Jenkins('http://ec2-13-232-108-34.ap-south-1.compute.amazonaws.com:8080/', username='', password='')
       


    @botcmd
    def jenkins_list_jobs(self, msg, args):
        """
        List jenkins jobs.
        """
        if self._is_instance_permitted(id):
            i = self.ec2.instances.filter(InstanceIds=[id]).start()
            response = "Instance {} started".format(self._get_instance_name(instance))
        else:
            response = "Instance not in permitted list. Use `aws addpermission ID` command."
        return response
