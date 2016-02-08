"""
extractor.mark
==============

Extractor that extracts swagger spec from *marked* view.

"""
from .base import Extractor


class MarkExtractor(Extractor):
    def get_mark(self, view):
        """Get mark object from view function."""
        return getattr(view, '_swag', {})

    def extract_others(self, view, ctx: dict):
        return self.get_mark(view)
