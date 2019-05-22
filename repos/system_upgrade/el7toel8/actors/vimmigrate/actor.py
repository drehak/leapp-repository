from leapp.actors import Actor
from leapp.libraries.common.reporting import report_generic
from leapp.models import Report, VimModel
from leapp.tags import ApplicationsPhaseTag, IPUWorkflowTag

from os import access, W_OK

class VimMigrate(Actor):
    """
    Actor for adding two directives into vim configuration files to simulate 
    the same behavior as vim-7.4 has.
    """

    name = 'vim_migrate'
    consumes = (VimModel,)
    produces = (Report,)
    tags = (ApplicationsPhaseTag, IPUWorkflowTag)

    """ Macros for adding into configuration file"""
    _changes = [
                'let skip_defaults_vim=1',
                'set t_BE='
              ]


    def insert_string(self, string, path):
        """
        Insert string into a file

        :param str string: string which will be inserted
        :param str path: string representing path
        """

        if not access(path, W_OK):
            raise OSError('File {} does not have writing permissions.'.format(path))

        try:
            with open(path, 'a') as f:
                f.write(string + '\n')
        except IOError:
            raise IOError('Error during writing to file {}.'.format(path))

    def process(self):
        for configs_list in self.consume(VimModel):
            if not configs_list:
                self.log.info('Vim configuration files will not be migrated, no Vim configuration files exists.')
            else:
                for vim_config in configs_list.vim_configs:
                    for change in _changes:
                        try:
                            self._insert_string(change, vim_config)
                        except (OSError, IOError) as error:
                            raise StopActorExecutionError(error)

                report_generic(
                                title='Vim was migrated',
                                summary='Changed strings were added into configuration files to ensure behavior from Vim 7.4',
                                severity='low'
                              )
