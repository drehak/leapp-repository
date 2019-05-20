from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic


class VimModel(Model):
    """
    Class VimModel

    Attributes:
    - topic
    - vim_configs - list of strings which are full paths to found vim configuration files.
    """

    topic = SystemInfoTopic
    vim_configs = fields.List(fields.String())
