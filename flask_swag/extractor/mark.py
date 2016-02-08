"""
extractor.mark
==============

Extractor that extracts swagger spec from *marked* view.

"""
from .base import Extractor


class MarkExtractor(Extractor):
    def get_mark(self, view):
        """Get mark object from view function."""
        return getattr(view, '_swag', {}).copy()

    def extract_others(self, view, ctx: dict):
        mark = self.get_mark(view)
        mark.pop('parameters', None)
        mark.pop('responses', None)
        return mark

    def build_parameters(self, view, param_info, ctx: dict) -> list:
        mark = self.get_mark(view)
        parameters = super().build_parameters(view, param_info, ctx)
        parameters.extend(mark.get('parameters', []))
        return parameters

    def extract_responses(self, view, ctx: dict):
        mark = self.get_mark(view)
        if 'responses' not in mark:
            return super().extract_responses(view, ctx)
        return mark['responses']
