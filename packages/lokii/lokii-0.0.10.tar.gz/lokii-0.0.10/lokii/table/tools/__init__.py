from .faker import FakerTool
from .random import RandomTool
from .context import ContextTool
from .constant import ConstantTool
from .param import ParamTool
from .string.join import JoinTool
from .string.slugify import SlugifyTool

tools = {
    'constant': ConstantTool(),
    'param': ParamTool(),
    'context': ContextTool(),
    'faker': FakerTool(),
    'random': RandomTool(),
    'string.join': JoinTool(),
    'string.slugify': SlugifyTool(),
}
