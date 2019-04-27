from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic


class VimModel(Model):
    topic = SystemInfoTopic
    vim_configs = fields.List(fields.String())
