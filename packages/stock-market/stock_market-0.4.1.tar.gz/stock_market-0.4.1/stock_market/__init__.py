
# -*- coding: utf-8 -*-

# Try to use declare namespace, but if that failes, use pkgutil
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    import pkgutil
    pkgutil.extend_path(__path__, __name__)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
