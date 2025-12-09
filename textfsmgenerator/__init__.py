"""Top-level module for textFSM Generator.

- allow end-user to create template or test script on GUI application.
"""

from textfsmgenerator.core import ParsedLine
from textfsmgenerator.core import TemplateBuilder
from textfsmgenerator.core import NonCommercialUseCls
from textfsmgenerator.config import version
from textfsmgenerator.config import edition

__version__ = version
__edition__ = edition

__all__ = [
    'ParsedLine',
    'TemplateBuilder',
    'NonCommercialUseCls',
    'version',
    'edition',
]
