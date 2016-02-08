"""
extractor
=========

Extract path info from flask application.

"""
from .base import Extractor
from .mark import MarkExtractor

__all__ = ['Extractor', 'MarkExtractor']
