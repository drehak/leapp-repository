from leapp.actors import Actor
from leapp.libraries.common.reporting import report_generic
from leapp.models import InstalledRedHatSignedRPM, VimModel, Report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag



class VimCheck(Actor):
    """
    Actor for checking if vim is installed and if vimrc file exists.
    """

    name = 'vim_check'
    consumes = (InstalledRedHatSignedRPM,)
    produces = (Report, VimModel)
    tags = (ChecksPhaseTag, IPUWorkflowTag)
    vimconfigs = {
                    'vim-minimal': '/etc/virc',
                    'vim-enhanced': '/etc/vimrc'
                 }

    def _checkconfigs(self, packages_dict):
        """
        Vim project has two configs - /etc/virc for vi and /etc/vimrc for vim.
        This method appends respective configuration filename into list according to
        installed Vim packages.

        :param dict packages_dict: dictionary of name of Vim rpms plus boolean as key
        if it is installed or not

        Returns list of strings, which represents full paths to vim configuration
        files.
        """
        configs = []

        for package in packages_dict:
            if packages_dict[package] is True:
                configs.append(vimconfigs[package])

        return configs

    def process(self):
        """return value"""
        vim_configs = []
        """ dictionary indicating which vim rpms are installed"""
        _installed_vim = {
                          'vim-minimal': False,
                          'vim-enhanced': False
                        }

        installed_vim_pkgs = _installed_vim.keys()
        for rpms in self.consume(InstalledRedHatSignedRPM):
            for pkg in rpms.items:
                if pkg.name in installed_vim_pkgs:
                    _installed_vim[pkg.name] = True

        vim_configs = self._checkconfigs(_installed_vim)

        if len(vim_configs) > 0:
            report_generic(
                            title='Vim configuration files will be migrated',
                            summary='Either /etc/virc (for vi) or /etc/vimrc (for vim and gvim) \
                                     configuration files exist. Vim changed default configuration \
                                     and default behavior of copy/paste, migration will put directives \
                                     into configuration files for setting behavior as it was in Vim 7.4',
                            severity='low'
                          )
        else:
            self.log.info('Vim configuration files do not exist. Vim is not installed or configuration files are removed.')
            vim_configs = []

        self.produce(VimModel(vim_configs=vim_configs))

