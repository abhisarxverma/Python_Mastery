# Library_management_system/__init__.py
"""
Library Management System Package
Provides core functionality for managing books, users, and transactions.
"""

# Import key modules for easier access
from .library import Library
from .Commandline import cli_utilities

# Define package-level variables if needed
__version__ = "1.0.0"
__all__ = ["Library", "cli_utilities"]
