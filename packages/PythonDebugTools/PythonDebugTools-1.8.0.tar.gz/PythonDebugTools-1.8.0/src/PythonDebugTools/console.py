import sys
import traceback
from pprint import PrettyPrinter




__all__ = ['PRINT', 'getPPrintStr', 'print_exception']
debug = __debug__

class NoStringWrappingPrettyPrinter(PrettyPrinter):
    @classmethod
    def Create(cls): return cls(indent=4, sort_dicts=False)

    # noinspection PyProtectedMember, PyUnresolvedReferences
    def _format(self, o, *args):
        if isinstance(o, str):
            width = self._width
            self._width = sys.maxsize
            try:
                super()._format(o, *args)
            finally:
                self._width = width
        else:
            super()._format(o, *args)

pp = NoStringWrappingPrettyPrinter.Create()

def PRINT(title: str, *args, _pp: PrettyPrinter = None, **kwargs):
    if not debug: return
    print(f"\n ---------------- {title} ---------------- \n\r")
    (_pp or pp).pprint(dict(args=args, kwargs=kwargs))



def getPPrintStr(o: any, *, _pp: PrettyPrinter = None) -> str: return (_pp or pp).pformat(o)



def print_exception(e: Exception):
    if not debug: return
    traceback.print_exception(type(e), e, e.__traceback__)
