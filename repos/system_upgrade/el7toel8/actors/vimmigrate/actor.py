from leapp.actors import Actor
from leapp.libraries.common.reporting import report_generic
from leapp.models import Report, VimModel
from leapp.tags import ApplicationsPhaseTag, IPUWorkflowTag


class VimMigrate(Actor):
    """
    Actor for adding two directives into vim configuration files to simulate 
    the same behavior as vim-7.4 has.
    """

    name = 'vim_migrate'
    consumes = (VimModel,)
    produces = (Report,)
    tags = (ApplicationsPhaseTag, IPUWorkflowTag)
    changes = [
                'let skip_defaults_vim=1',
                'set t_BE='
              ]


    def insert_string(self, string, path):
        """
        insert_string

        Insert string into a file

        parameters:
        - string - string
        - path - string

        returns boolean
        """

        try:
            with open(path, 'a') as f:
                f.write(string + '\n')
                return True
        except IOError:
            return False

    def process(self):
        for configs_list in self.consume(VimModel):
            if configs_list == []:
                self.log.info('Vim configuration files will not be migrated, no Vim configuration files exists.')
            else:
                for vim_config in configs_list.vim_configs:
                    for change in changes:
                        result = self.insert_string(change, vim_config)
                        if result is False:
                            raise StopActorExecutionError('Vimmigrate actor was not able to open configuration file {}'.format(vim_config))

                report_generic(
                                title='Vim was migrated.',
                                summary='Changed strings were added into configuration files to ensure behavior from Vim 7.4.',
                                severity='low'
                              )
