from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic


class VimModel(Model):
    """
    Represents facts about Vim configuration, explicitly
    paths to configuration files.

    Attribute vim_configs can be 'None' or can contain list of
    strings representing full path to Vim configuration files.
    """

    topic = SystemInfoTopic
    """List of strings representing full paths to configuration files"""
    vim_configs = fields.List(fields.String())
