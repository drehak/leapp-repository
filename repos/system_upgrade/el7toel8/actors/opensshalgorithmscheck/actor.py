from leapp.actors import Actor
from leapp.libraries.actor import library
from leapp.models import Report, OpenSshConfig
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class OpenSshAlgorithmsCheck(Actor):
    """
    OpenSSH configuration does not contain any unsupported cryptographic algorithms.

    Check the values of Ciphers and MACs in OpenSSH server config file and warn
    about removed algorithms which might cause the server to fail to start.
    """
    name = 'open_ssh_algorithms'
    consumes = (OpenSshConfig,)
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        library.process(self.consume(OpenSshConfig))
