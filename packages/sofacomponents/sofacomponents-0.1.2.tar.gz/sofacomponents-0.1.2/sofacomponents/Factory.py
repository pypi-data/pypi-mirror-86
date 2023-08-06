from .lib.base_component import sofa_component

try:
    from .lib.generated_classes import BaseSofaComponents
except ModuleNotFoundError as e:
    import os
    if "SOFA_SRC" in os.environ:
        from .lib.parse_sofa_sources import parse_sources
        parse_sources(os.environ["SOFA_SRC"])
        from .lib.generated_classes import BaseSofaComponents
    else:
        print("ERROR: You need to parse the sofa sources. Either run sofacomponents.parse_sources(<path-to-sources>) or export SOFA_SRC=<path-to-sources>")
        raise e


class SofaFactory(BaseSofaComponents):
    def __init__(self, debug=False):
        self._defaults = dict()
        if debug:
            self._defaults.update({"printLog": True})

    def __getattr__(self, item):
        @sofa_component
        def _defcomp(self, **kwargs):
            return item

        return lambda **kw: _defcomp(self, **kw)
