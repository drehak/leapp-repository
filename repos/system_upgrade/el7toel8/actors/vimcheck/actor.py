from leapp.actors import Actor
from leapp.libraries.common.reporting import report_generic
from leapp.libraries.common.rpms import has_package
from leapp.models import InstalledRedHatSignedRPM, Report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class VimCheck(Actor):
    """
    Check if vim-minimal or vim-enhanced is installed and if so, inform about planned actions.
    """

    name = 'vim_check'
    consumes = (InstalledRedHatSignedRPM,)
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        vim_pkgs = ['vim-minimal', 'vim-enhanced']
        if any(has_package(InstalledRedHatSignedRPM, pkg) for pkg in vim_pkgs):
            # NOTE: informational message about planned fixes during IPU
            report_generic(
                title='Vim configuration files will be migrated',
                summary=('Either /etc/virc (for vi) or /etc/vimrc (for vim and gvim) configuration'
                         ' files exist. Vim changed default configuration and default behavior of'
                         ' copy/paste. The configuration in those files will be automatically migrated'
                         ' during the in-place upgrade to keep the behavior as it was in Vim 7.4.'),
                severity='low'
            )
