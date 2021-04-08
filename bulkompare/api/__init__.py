import pathlib
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = pathlib.Path(sys._MEIPASS)
else:
    bundle_dir = pathlib.Path(__file__).parent.parent
