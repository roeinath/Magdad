# encoding: utf-8

"""
Exceptions used with python-docx_for_docm.

The base exception class is Pythondocx_for_docmError.
"""


class Pythondocx_for_docmError(Exception):
    """
    Generic error class.
    """


class InvalidSpanError(Pythondocx_for_docmError):
    """
    Raised when an invalid merge region is specified in a request to merge
    table cells.
    """


class InvalidXmlError(Pythondocx_for_docmError):
    """
    Raised when invalid XML is encountered, such as on attempt to access a
    missing required child element
    """
