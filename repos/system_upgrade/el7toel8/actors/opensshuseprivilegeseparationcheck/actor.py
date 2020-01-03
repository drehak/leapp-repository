from leapp.actors import Actor
from leapp.libraries.actor import library
from leapp.models import Report, OpenSshConfig
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class OpenSshUsePrivilegeSeparationCheck(Actor):
    """
    UsePrivilegeSeparation configuration option was removed.

    Check the value of UsePrivilegeSeparation in OpenSSH server config file
    and warn about its deprecation if it is set to non-default value.
    """
    name = 'open_ssh_use_privilege_separation'
    consumes = (OpenSshConfig, )
    produces = (Report, )
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        library.process(self.consume(OpenSshConfig))
