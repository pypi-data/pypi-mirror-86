from __future__ import absolute_import, division, print_function

import os

# Asencis Python bindings
# API docs at https://asencis.com/documentation
# Authors:
# Michael Roberts <michael@asencis.com>

__title__ = "asencis"
__version__ = "0.1.1"
__author__ = "asencis Ltd"
__license__ = "MPL 2.0"
__copyright__ = "2020 asencis, Ltd"

# API resources
from asencis.resources import *

Datasets = Dataset()
Domains = Domain()
Prefixes = Prefix()
Quantities = Quantity()
