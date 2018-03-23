import sys,MyClass
from PyQt5.QtWidgets import QApplication# 导入相应的包


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w=MyClass.MyClass()
    sys.exit(app.exec_())
