import sys
import traceback
from pprint import PrettyPrinter




__all__ = ['PRINT', 'getPPrintStr', 'print_exception']
debug = __debug__

class NoStringWrappingPrettyPrinter(PrettyPrinter):
    """
        https://stackoverflow.com/questions/31485402/can-i-make-pprint-in-python3-not-split-strings-like-in-python2
        https://stackoverflow.com/a/31485450/9530917
    """
    @classmethod
    def Create(cls): return cls(indent=4, sort_dicts=False)

    # noinspection PyProtectedMember, PyUnresolvedReferences
    def _format(self, o, *args):
        if isinstance(o, (str, bytes, bytearray)):
            width = self._width
            self._width = sys.maxsize
            try:
                super()._format(o, *args)
            finally:
                self._width = width
        else:
            super()._format(o, *args)

pp = NoStringWrappingPrettyPrinter.Create()

def PRINT(title: str, *args, _pp: PrettyPrinter = None, use_double_quotes: bool = True, **kwargs):
    """
    :param title: message to start the print, to make it easier to find it.
    :type title: str
    :param o: object to be serialized
    :type o: any
    :param _pp: any PrettyPrinter inpmentation. provide your own to customize the output.
    :type _pp: PrettyPrinter
    :param use_double_quotes: use double quotes (") instead of the default single quotes (')
    :type use_double_quotes:
    :return: formatted string of the passed object
    :rtype: str
    """
    if not debug: return
    print(f"\n ---------------- {title} ---------------- \n\r")
    print(getPPrintStr(dict(args=args, kwargs=kwargs), _pp=_pp, use_double_quotes=use_double_quotes))



def getPPrintStr(o: any, *, _pp: PrettyPrinter = None, use_double_quotes: bool = True) -> str:
    """
    :param o: object to be serialized
    :type o: any
    :param _pp: any PrettyPrinter inpmentation. provide your own to customize the output.
    :type _pp: PrettyPrinter
    :param use_double_quotes: use double quotes (") instead of the default single quotes (')
    :type use_double_quotes:
    :return: formatted string of the passed object
    :rtype: str
    """
    s = (_pp or pp).pformat(o)
    if use_double_quotes: s = s.replace("'", '"')
    return s



def print_exception(e: Exception):
    if not debug: return
    traceback.print_exception(type(e), e, e.__traceback__)
