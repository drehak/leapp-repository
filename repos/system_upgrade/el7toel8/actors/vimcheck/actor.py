from leapp.actors import Actor
from leapp.libraries.common.reporting import report_generic
from leapp.models import InstalledRedHatSignedRPM, VimModel, Report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag

vimconfigs = {
              'vim-minimal': '/etc/virc',
              'vim-enhanced' : '/etc/vimrc'
              }

changes = [
            'let skip_defaults_vim=1',
            'set t_BE='
          ]



class VimCheck(Actor):
    """
    Actor for checking if vim is installed and if vimrc file exists.
    """

    name = 'vim_check'
    consumes = (InstalledRedHatSignedRPM,)
    produces = (Report, VimModel)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def checkconfigs(self, packages_dict):
      """
      checkconfigs

      Vim project has two configs - /etc/virc for vi and /etc/vimrc for vim.
      This method appends respective configuration filename into list according to
      installed Vim packages.

      parameters:
      - packages_dict - dictionary

      returns list of strings
      """
      configs = []

      for package in packages_dict:
        if packages_dict[package] == True:
          configs.append(vimconfigs[package])

      return configs

    def process(self):
      vim_configs = []
      installed_vim = {
                        'vim-minimal' : False,
                        'vim-enhanced' : False
                      }

      for rpms in self.consume(InstalledRedHatSignedRPM):
        for pkg in rpms.items:
          if pkg.name == 'vim-minimal':
            installed_vim['vim-minimal'] = True
          elif pkg.name == 'vim-enhanced':
            installed_vim['vim-enhanced'] = True
          else:
            continue

      vim_configs = self.checkconfigs(installed_vim)

      if len(vim_configs) > 0:
        report_generic(
                        title='Vim configuration files will be migrated.',
                        summary='Either virc or vimrc exists - it needs to be migrated.',
                        severity='low'
                      )
      else:
        report_generic(
                        title='Vim configuration files do not exist.',
                        summary='Vim is not installed or configuration files are removed.',
                        severity='low'
                      )
        vim_configs = []

      self.produce(VimModel(vim_configs=vim_configs))

