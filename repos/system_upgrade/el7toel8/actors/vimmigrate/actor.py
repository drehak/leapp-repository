from leapp.actors import Actor
from leapp.libraries.actor import library
from leapp.libraries.common.reporting import report_with_remediation
from leapp.libraries.common.rpms import has_package
from leapp.models import Report, InstalledRedHatSignedRPM
from leapp.tags import ApplicationsPhaseTag, IPUWorkflowTag


class VimMigrate(Actor):
    """
    Modify Vim configuration files to keep the the same behavior as vim-7.4 has.
    """

    name = 'vim_migrate'
    consumes = (InstalledRedHatSignedRPM,)
    produces = (Report,)
    tags = (ApplicationsPhaseTag, IPUWorkflowTag)

    def process(self):
        error_list = []

        for [pkg, config_file in library.vim_configs.items() if has_package(InstalledRedHatSignedRPM, pkg)]:
            try:
                library.update_config(config_file)
            except (OSError, IOError) as error:
                self.log.warning('Cannot modify the {} config file.'.format(config_file))
                error_list.append((config_file, error))
        if error_list:
            report_with_remediation(
                title='The Vim configuration has not been updated',
                summary=('The files below has not been modified (error message included):'
                         ''.join(['    - {}: {}'.format(err[0], err[1]) for err in error_list])),
                remediation=('If you want keep original behaviour of vim, append the following lines'
                             ' into those files:\n    {}'.format('    \n'.join(library.new_macros))),
                severity='medium'
            )
            return
