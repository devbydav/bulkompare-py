from PySide2 import QtWidgets

VERSION = "0.1.0"

ABOUT = f"""CsvComparator v{VERSION}

Logiciel sous license GPL

Developpé par David C

Librairies :
PySide2, Qt pour Python
Numpy
Pandas
Pydantic

Icons made by Freepik from www.flaticon.com"""


def show_about(logo):
    """Show the about dialog"""

    msg_box = QtWidgets.QMessageBox()
    msg_box.setWindowTitle("A propos")
    msg_box.setText(ABOUT)
    msg_box.setIconPixmap(logo)
    msg_box.exec_()
