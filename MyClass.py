import Mygui,os
import calendar
import datetime
from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QColorDialog,QHeaderView,QAbstractItemView,QFrame,QApplication,QLineEdit,QMessageBox
from PyQt5.QtCore import Qt,QDate,QSize   # 导入相应的包
from PyQt5.QtGui import QColor,QFont,QIcon,QPixmap,QKeyEvent
from Mysqlite import ReadSqlite,ReadSqliteDayColor,WriteSqlite,DeleteSqlite,ReadSqliteEventColor
from MyAES import decrypt_oralce,encrypt_oracle
from MyDataClass import WeekDay,ColorDay
from threading import Thread

from matplotlib import rcParams
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class MyClass(QMainWindow):

    NameDB='.\\Source\\test.db'
    key='pg'
    ColorCanChange='#5555ff'
    ColorDateDefault='#e5e5e5'
    ColorFontDefault='#bcbcbc'
    IdAll=[]
    # e5e5e5
    Green = ["#81ff81", "#22fe27", "#70ad47"]

    Yellow = ["#ffff00"]

    Blue = ["#00ffff", "#8ea9db"]
    Delight = ["#ccffff"]
    Pink = ["#fff2cc", "#ffcc99", "#ff603b"]

    Tired = ["#ffd966", "#ffc000"]

    Red = ["#ff0000"]
    Fucked = ["#969696", "#595959", "#333333"]

    ColorList1 = Green
    ColorList2 = Yellow
    ColorList3 = Blue+Delight+Pink
    ColorList4 = Tired
    ColorList5 = Red+Fucked

    ColorPaint1 = ColorList1[1]
    ColorPaint2 = ColorList2[0]
    ColorPaint3 = ColorList3[0]
    ColorPaint4 = ColorList4[1]
    ColorPaint5 = ColorList5[0]

    c1 = [0] * 5
    c2 = [0] * 8

    C1=[]
    C2=[]
    C3=[]
    C4=[]
    C5=[]

    colors1 = ["#00da00", "#dada00", "#00b8b8", "#ffaa00", "#da0000"]
    colors2 = ["#22fe27", "#ffff00", "#00ffff", "#ccffff", "#fff2cc", "#ffc000", "#ff0000", "#969696"]

    SliderValue=0
    year = QDate.currentDate().year()
    month = QDate.currentDate().month()
    day = QDate.currentDate().day()
    sbit_first=0
    def __init__(self, parent=None):
        super(MyClass,self).__init__(parent)
        self.ui=Mygui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        # self.showFullScreen()#全屏显示
        # self.showMaximized()

        self.AllHide()
        # self.login()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#列宽自动适应
        # self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)#行高

        self.KeyInit()
        self.ui.tableWidget.setFrameShape(QFrame.NoFrame)  # 无边框显示
        self.ui.textEdit.setFrameShape(QFrame.NoFrame)  # 无边框显示
        self.ui.widget.setStyleSheet("border-image: url(./Source/2.jpg);")
        self.ui.menuBar.setStyleSheet("background-image: url(./Source/2.jpg);color: white")
        self.ui.statusbar.setStyleSheet("background-image: url(./Source/2.jpg);color: white")
        self.ui.textEdit.setStyleSheet("border-image: url(./Source/paper1.jpg);")
        self.ui.textEdit.setFont(QFont("楷体", 12))
        # self.setWindowTitle('Once Upon A Time')
        self.setWindowTitle('34枚金币时间管理')
        icon = QIcon()
        icon.addPixmap(QPixmap("./Source/Calender.ico"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        # self.ui.horizontalLayout_13.setGeometry(QRect(20, 20, 491, 311))
        # self.ui.widget.setStyleSheet("background-image: url(2.jpg);")#图片平铺
        # self.ui.statusbar.hide()
        #信号槽连接

        self.ui.radioButton_3.setChecked(True)
        self.ui.radioButton_3.toggled.connect(self.Radio3)
        self.ui.radioButton_2.toggled.connect(self.Radio2)
        self.ui.radioButton.toggled.connect(self.Radio1)
        self.ui.pushButton.clicked.connect(self.TableCombine)
        self.ui.pushButton_2.clicked.connect(self.TableClear)
        self.ui.toolButton.clicked.connect(self.ColorSelect)

        self.ui.pushButton_3.clicked.connect(self.Color0)
        self.ui.pushButton_4.clicked.connect(self.Color1)
        self.ui.pushButton_5.clicked.connect(self.Color2)
        self.ui.pushButton_6.clicked.connect(self.Color3)
        self.ui.pushButton_7.clicked.connect(self.Color4)
        self.ui.pushButton_8.clicked.connect(self.Color5)

        self.ui.pushButton_9.clicked.connect(self.DataSave)
        self.ui.pushButton_10.clicked.connect(self.BackToToday)

        self.ui.tableWidget.itemClicked.connect(self.SelectClear1)
        self.ui.tableWidget_2.itemClicked.connect(self.SelectClear2)

        self.ui.dateEdit.dateChanged.connect(self.ResetDate)
        self.ui.comboBox.currentIndexChanged.connect(self.ButtonColorChange1)
        self.ui.comboBox_2.currentIndexChanged.connect(self.ButtonColorChange2)
        self.ui.comboBox_3.currentIndexChanged.connect(self.ButtonColorChange3)
        self.ui.comboBox_4.currentIndexChanged.connect(self.ButtonColorChange4)
        self.ui.comboBox_5.currentIndexChanged.connect(self.ButtonColorChange5)
        self.ui.verticalScrollBar.valueChanged.connect(self.ScrollBarSet)

        self.TableInit(7,34)
        self.TableItemInit(7,34)
        self.ui.pushButton_3.setStyleSheet("background-color: #5555ff")
        self.ui.widget_2.setStyleSheet("background-color: rgba(0,0,0,0.1)")


        Date = self.ui.dateEdit.date()
        self.ColorCount(Date.year(), Date.month(), Date.day(), 0)

        t = Thread(target=self.PaintPie)
        t.start()

        self.ui.dateEdit.setDate(QDate.currentDate())
        self.dateinit()
        self.ComboBoxInit()
        self.ScrollBarInit()
        self.ui.action.triggered.connect(self.about)
        # self.ui.widget_3.setStyleSheet("border-image: url(./Source/pie.png);")


    def Radio3(self):
        Date = self.ui.dateEdit.date()
        self.ColorCount(Date.year(), Date.month(), Date.day(), 0)
        t = Thread(target=self.PaintPie)
        t.start()
    def Radio2(self):
        Date = self.ui.dateEdit.date()
        self.ColorCount(Date.year(), Date.month(), Date.day(), 1)
        t = Thread(target=self.PaintPie)
        t.start()
    def Radio1(self):
        Date = self.ui.dateEdit.date()
        self.ColorCount(Date.year(), Date.month(), Date.day(), 2)
        t = Thread(target=self.PaintPie)
        t.start()
    def PaintPie(self):

        fig, ax = plt.subplots()
        c = [1]
        rcParams.update({'font.size': 18, 'font.family': 'serif'})
        ax.pie(self.c2, radius=1.5, colors=self.colors2, shadow=False, startangle=90)
        TempCValue=[]
        TempC=[]
        for i in range(0,len(self.c1)):
            if self.c1[i]!=0:
                TempCValue.append(self.c1[i])
                TempC.append(self.colors1[i])
        if TempCValue:
            ax.pie(TempCValue, radius=1.2,autopct='%1.0f%%', shadow=False, colors=TempC, startangle=90,pctdistance=0.95)
        ax.pie(c, radius=0.9, shadow=False, colors='k', startangle=90)
        Date = self.ui.dateEdit.date()

        self.ColorCount(Date.year(), Date.month(), Date.day(), 3)
        TempCValue=[]
        TempC=[]
        for i in range(0,len(self.c2)):
            if self.c2[i]!=0:
                TempCValue.append(self.c2[i])
                TempC.append(self.colors2[i])
        if TempCValue:
            ax.pie(TempCValue, radius=0.7, autopct='%1.0f%%',shadow=False, colors=TempC, startangle=90)
        plt.savefig(os.getcwd()+'\\Source\\pie.png', format='png', bbox_inches='tight', transparent=True, dpi=100)
        plt.close()
        self.ui.widget_3.setStyleSheet("border-image: url(./Source/pie.png);")
        if self.ui.radioButton_3.isChecked():
            mode=0
        elif self.ui.radioButton_2.isChecked():
            mode=1
        else:
            mode=2
        self.ColorCount(Date.year(), Date.month(), Date.day(), mode)
        fig, ax = plt.subplots()
        plt.grid(True)
        plt.grid(color='w', linestyle='--', linewidth=2, alpha=0.7)
        ax.plot(self.C1,'*-',color="#22fe27",linewidth=3.0)
        ax.plot(self.C2,'*-',color="#ffff00",linewidth=3.0)
        ax.plot(self.C3,'*-',color="#00ffff",linewidth=3.0)
        ax.plot(self.C4,'*-',color="#ffaa00",linewidth=3.0)
        ax.plot(self.C5,'r*-',linewidth=3.0)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_color('w')
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_color('w')


        plt.savefig(os.getcwd() + '\\Source\\plot1.png', format='png', bbox_inches='tight', transparent=True, dpi=100)
        plt.close()
        self.ui.widget_4.setStyleSheet("border-image: url(./Source/plot1.png);")
    def ColorCount(self,year,month,day,mode):
        ColorAll = ReadSqliteEventColor(self.NameDB, year, month, day, mode)
        self.c1=[0]*5
        self.c2=[0]*8
        self.C1=[]
        self.C2 = []
        self.C3 = []
        self.C4 = []
        self.C5 = []
        for i in range(0, len(ColorAll)):
            id = ColorAll[i].Id
            DayColor = ColorAll[i].DayColor
            Num = ColorAll[i].Num
            EventColor = ColorAll[i].EventColor
            Row = ColorAll[i].Row
            C0 = [0]*5
            for j in range(0, Num):
                if j < Num - 1:
                    num = (int(Row[j + 1]) - int(Row[j]))*0.5
                    ColorNow = EventColor[j].lower()
                    if len(ColorNow) == 9:
                        ColorNow = '#' + ColorNow[3:9]
                    if ColorNow in self.Green:
                        C0[0]+=num
                        self.c1[0] += num
                        self.c2[0] += num
                    elif ColorNow in self.Yellow:
                        C0[1] += num
                        self.c1[1] += num
                        self.c2[1] += num
                    elif ColorNow in self.Blue:
                        C0[2] += num
                        self.c1[2] += num
                        self.c2[2] += num
                    elif ColorNow in self.Delight:
                        C0[2] += num
                        self.c1[2] += num
                        self.c2[3] += num
                    elif ColorNow in self.Pink:
                        C0[2] += num
                        self.c1[2] += num
                        self.c2[4] += num
                    elif ColorNow in self.Tired:
                        C0[3] += num
                        self.c1[3] += num
                        self.c2[5] += num
                    elif ColorNow in self.Red:
                        C0[4] += num
                        self.c1[4] += num
                        self.c2[6] += num
                    elif ColorNow in self.Fucked:
                        C0[4] += num
                        self.c1[4] += num
                        self.c2[7] += num
                else:
                    num = (35 - int(Row[j]))*0.5
                    ColorNow = EventColor[j].lower()
                    if len(ColorNow) == 9:
                        ColorNow = '#' + ColorNow[3:9]
                    if ColorNow in self.Green:
                        C0[0] += num
                        self.c1[0] += num
                        self.c2[0] += num
                    elif ColorNow in self.Yellow:
                        C0[1] += num
                        self.c1[1] += num
                        self.c2[1] += num
                    elif ColorNow in self.Blue:
                        C0[2] += num
                        self.c1[2] += num
                        self.c2[2] += num
                    elif ColorNow in self.Delight:
                        C0[2] += num
                        self.c1[2] += num
                        self.c2[3] += num
                    elif ColorNow in self.Pink:
                        C0[2] += num
                        self.c1[2] += num
                        self.c2[4] += num
                    elif ColorNow in self.Tired:
                        C0[3] += num
                        self.c1[3] += num
                        self.c2[5] += num
                    elif ColorNow in self.Red:
                        C0[4] += num
                        self.c1[4] += num
                        self.c2[6] += num
                    elif ColorNow in self.Fucked:
                        C0[4] += num
                        self.c1[4] += num
                        self.c2[7] += num
            self.C1.append(C0[0])
            self.C2.append(C0[1])
            self.C3.append(C0[2])
            self.C4.append(C0[3])
            self.C5.append(C0[4])
    def about(self):
        Box1=QMessageBox()
        Box1.information(self, "版本1.2", "快捷键说明：\nCtrl+S ：  保存\nAlt+1~5：涂色1~5")
    def AllHide(self):
        self.ui.verticalScrollBar.hide()
        self.ui.dateEdit.hide()
        self.ui.widget_2.hide()
        self.ui.tableWidget.hide()
        self.ui.tableWidget_2.hide()

        self.ui.textEdit.hide()
        self.ui.pushButton_10.hide()

        self.ui.pushButton_9.hide()
        self.ui.pushButton.hide()
        self.ui.pushButton_4.hide()
        self.ui.pushButton_3.hide()
        self.ui.pushButton_2.hide()
        self.ui.pushButton_5.hide()
        self.ui.pushButton_6.hide()
        self.ui.pushButton_7.hide()
        self.ui.pushButton_8.hide()

        self.ui.comboBox.hide()
        self.ui.comboBox_2.hide()
        self.ui.comboBox_3.hide()
        self.ui.comboBox_4.hide()
        self.ui.comboBox_5.hide()
        self.ui.toolButton.hide()

        self.ui.widget_3.hide()
        self.ui.widget_4.hide()
        self.ui.radioButton.hide()
        self.ui.radioButton_2.hide()
        self.ui.radioButton_3.hide()

        self.ui.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.setMinimumSize(self.width(),self.height())
        self.setMaximumSize(self.width(),self.height())
    def login(self):

        str1=self.ui.lineEdit_2.text()
        if str1=='123456':
            self.AllShow()
        else:
            self.ui.statusbar.showMessage('Get out of here!(╯‵□′)╯︵┴─┴', 2000)
    def AllShow(self):
        self.ui.lineEdit_2.hide()
        self.setMaximumSize(111111111,111111111)
        self.showMaximized()

        self.ui.verticalScrollBar.show()
        self.ui.dateEdit.show()
        self.ui.widget_2.show()
        self.ui.tableWidget.show()
        self.ui.tableWidget_2.show()

        self.ui.textEdit.show()
        self.ui.pushButton_10.show()

        self.ui.pushButton_9.show()
        self.ui.pushButton.show()
        self.ui.pushButton_4.show()
        self.ui.pushButton_3.show()
        self.ui.pushButton_2.show()
        self.ui.pushButton_5.show()
        self.ui.pushButton_6.show()
        self.ui.pushButton_7.show()
        self.ui.pushButton_8.show()

        self.ui.comboBox.show()
        self.ui.comboBox_2.show()
        self.ui.comboBox_3.show()
        self.ui.comboBox_4.show()
        self.ui.comboBox_5.show()
        self.ui.toolButton.show()

        self.ui.widget_3.show()
        self.ui.widget_4.show()
        self.ui.radioButton.show()
        self.ui.radioButton_2.show()
        self.ui.radioButton_3.show()
    def ScrollBarSet(self):
        distance=self.ui.verticalScrollBar.value()
        pos=distance-self.SliderValue
        if pos>0:
            ValueNow=self.SliderValue+1
        elif pos<0:
            ValueNow = self.SliderValue - 1
        else:
            return
        self.ui.verticalScrollBar.setValue(ValueNow)
        self.SliderValue=ValueNow

        year = self.ui.dateEdit.date().year()
        # self.DateSet(year,ValueNow+1,1)
        self.ui.dateEdit.setDate(QDate(year,ValueNow+1, 1))

    def BackToToday(self):
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.dateinit()
    def ScrollBarInit(self):

        month = datetime.datetime.now().month
        self.ui.verticalScrollBar.setMaximum(11)
        self.ui.verticalScrollBar.setValue(month-1)
        self.SliderValue=month-1
    def KeyInit(self):
        self.key=self.key
    def keyPressEvent(self, event):
        keyEvent = QKeyEvent(event)
        if keyEvent.key() == Qt.Key_S:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.DataSave()
        elif keyEvent.key()== Qt.Key_1:
            if QApplication.keyboardModifiers() == Qt.AltModifier:
                self.Color1()
        elif keyEvent.key()== Qt.Key_2:
            if QApplication.keyboardModifiers() == Qt.AltModifier:
                self.Color2()
        elif keyEvent.key()== Qt.Key_3:
            if QApplication.keyboardModifiers() == Qt.AltModifier:
                self.Color3()
        elif keyEvent.key()== Qt.Key_4:
            if QApplication.keyboardModifiers() == Qt.AltModifier:
                self.Color4()
        elif keyEvent.key()== Qt.Key_5:
            if QApplication.keyboardModifiers() == Qt.AltModifier:
                self.Color5()
        elif keyEvent.key()== Qt.Key_Q:
            if QApplication.keyboardModifiers() == Qt.AltModifier:
                self.TableCombine()
        elif keyEvent.key()== Qt.Key_L:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.login()
    def DayColorAutoSelect(self,ColorAll):
        ColorSum=self.Green+self.Yellow+self.Blue+self.Delight+self.Pink+self.Tired+self.Red+self.Fucked
        C=[0]*len(ColorSum)
        for i in range(0, 1):
            Num = ColorAll.Num
            EventColor = ColorAll.EventColor
            Row = ColorAll.Row
            for j in range(1, Num+1):
                if j < Num:
                    num = int(Row[j + 1]) - int(Row[j])
                    ColorNow = EventColor[j].lower()
                    if len(ColorNow) == 9:
                        ColorNow = '#' + ColorNow[3:9]
                    if ColorNow in ColorSum:
                        C[ColorSum.index(ColorNow)]+=num
                else:
                    num = 35 - int(Row[j])
                    ColorNow = EventColor[j].lower()
                    if len(ColorNow) == 9:
                        ColorNow = '#' + ColorNow[3:9]
                    if ColorNow in ColorSum:
                        C[ColorSum.index(ColorNow)]+=num
        Level=[9,8,7,15,14,13,6,5,2,0,10]
        for pos in Level:
            if C[pos]!=0:
                return ColorSum[pos]
        if sum(C)==0:
            return self.ColorDateDefault
        else:
            return ColorSum[C.index(max(C))]
    def DataSave(self):
        TodayData=self.TableDataGet()
        ColorSingle = ColorDay(TodayData.Id, TodayData.DayColor, TodayData.Num, TodayData.EventColor, TodayData.Row)
        TodayData.DayColor=self.DayColorAutoSelect(ColorSingle)

        if TodayData.Id not in self.IdAll:
            self.ui.statusbar.showMessage('正在写入新数据...')
            WriteSqlite(self.NameDB,TodayData)
            self.ui.statusbar.showMessage('数据已写入!(′～`）',5000)
            self.IdAll.append(TodayData.Id)
        else:
            DeleteSqlite(self.NameDB,TodayData.Id)
            self.ui.statusbar.showMessage('已删除今日数据!')
            WriteSqlite(self.NameDB, TodayData)
            self.ui.statusbar.showMessage('已更新今日数据!－(>口＜-)', 5000)
        # else:
        #     self.ui.statusbar.showMessage('今日数据为空！', 5000)
    def TableDataGet(self):
        DateNow=self.ui.dateEdit.date()
        year=DateNow.year()
        month=DateNow.month()
        day=DateNow.day()
        d1 = datetime.date(2013, 11, 4)
        d2 = datetime.date(year, month,day)
        Id = (d2 - d1).days
        DayYear=year
        DayDate=str(month)+'.'+str(day)
        DayComment=self.ui.textEdit.toPlainText()
        if not DayComment:
            DayComment='12'
        DayComment=encrypt_oracle(self.key,DayComment)
        CalenderData = calendar.monthcalendar(year, month)
        for i in range(0,len(CalenderData)):
            if day in CalenderData[i]:
                table2_i=i
                table2_j=CalenderData[i].index(day)
                table1_j=table2_j
        table2_item=self.ui.tableWidget_2.item(table2_i,table2_j)
        DayColor=table2_item.background().color().name()
        if DayColor=='#000000':
            DayColor=self.ColorDateDefault
        DayValue=[Id]
        EventColor=[Id]
        DayRow=[Id]
        DayNum=0
        for i in range(0,34):
            item=self.ui.tableWidget.item(i,table1_j)
            if item.text():
                DayValue.append(encrypt_oracle(self.key,item.text()))
                EventColor.append(item.background().color().name())
                DayRow.append(i)
                DayNum+=1
        for i in range(0,34-len(DayRow)+1):
            DayValue.append(' ')
            EventColor.append(' ')
            DayRow.append(' ')
        return WeekDay(Id,DayYear, DayDate, DayComment, DayColor, DayNum, DayValue, EventColor, DayRow)
    def TableShowText(self,DYear,DMonth,DDay):
        self.IdAll.clear()
        for i in range(0,7):
            self.TableClear2(i)
        WeekDate=ReadSqlite(self.NameDB,DYear,DMonth,DDay)
        self.ui.textEdit.clear()
        if WeekDate:
            Id=WeekDate[0].Id
            d1 = datetime.date(2013, 11, 4)
            d2 = d1 + datetime.timedelta(days=Id-(Id%7))
            HorizontalHeader = []
            DayNow=(datetime.date(DYear,DMonth,DDay)-d1).days
            for i in range(0, 7):
                t_time = str(d2.month)+'.'+str(d2.day)
                d2=d2+datetime.timedelta(days=1)
                HorizontalHeader.append(t_time)
            self.ui.tableWidget.setHorizontalHeaderLabels(HorizontalHeader)
            PosAll=[]
            for j in range(0, len(WeekDate)):
                Pos=WeekDate[j].Id%7
                PosAll.append(Pos)
                Year=WeekDate[j].Year
                Date=WeekDate[j].Date
                Comment=WeekDate[j].Comment
                DayColor=WeekDate[j].DayColor
                Num=WeekDate[j].Num
                Value=WeekDate[j].Value
                EventColor=WeekDate[j].EventColor
                Row=WeekDate[j].Row
                self.IdAll.append(WeekDate[j].Id)
                for i in range(0,Num):
                    if i<Num-1:
                        self.ui.tableWidget.setSpan(int(Row[i]),Pos,int(Row[i+1])-int(Row[i]),1)  # 要改变单元格的   1行数  2列数     要合并的  3行数  4列
                        newItem = QTableWidgetItem(decrypt_oralce(self.key,Value[i]))
                        newItem.setForeground(QColor(0, 0, 0))  # 设置字体颜色
                        newItem.setFont(QFont("宋体"))
                        newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                        newItem.setBackground(QColor(EventColor[i]))
                        self.ui.tableWidget.setItem(int(Row[i]), Pos, newItem)
                    else:
                        self.ui.tableWidget.setSpan(int(Row[i]),Pos,35-int(Row[i]),1)  # 要改变单元格的   1行数  2列数     要合并的  3行数  4列
                        newItem = QTableWidgetItem(decrypt_oralce(self.key,Value[i]))
                        newItem.setForeground(QColor(0, 0, 0))  # 设置字体颜色
                        newItem.setFont(QFont("宋体"))
                        newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                        newItem.setBackground(QColor(EventColor[i]))
                        self.ui.tableWidget.setItem(int(Row[i]), Pos, newItem)
            if DayNow%7 in PosAll:
                CommentIndex=PosAll.index(DayNow%7)
                Comment = WeekDate[CommentIndex].Comment
                self.ui.textEdit.append(decrypt_oralce(self.key,Comment))
        else:
            d1 = datetime.date(2013, 11, 4)
            d2 = datetime.date(DYear, DMonth, DDay)
            Id=(d2-d1).days
            d2 = d1 + datetime.timedelta(days=Id - (Id % 7))
            HorizontalHeader=[]
            for i in range(0, 7):
                t_time = str(d2.month)+'.'+str(d2.day)
                d2=d2+datetime.timedelta(days=1)
                HorizontalHeader.append(t_time)
            self.ui.tableWidget.setHorizontalHeaderLabels(HorizontalHeader)
    def TableFill(self,ColumnNum,RowNum):
        for i in range(0,RowNum):
            for j in range(0,ColumnNum):
                newItem = QTableWidgetItem(str(i*5+j+1)+' '+self.ColorList[i*5+j])
                newItem.setForeground(QColor(0, 0, 0))#设置字体颜色
                newItem.setFont(QFont("宋体"))
                newItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                self.ui.tableWidget.setItem(i, j, newItem)
                newItem.setBackground(QColor(self.ColorList[i*5+j]))
    def ComboBoxInit(self):
        self.ComboBoxInit1()
        self.ComboBoxInit2()
        self.ComboBoxInit3()
        self.ComboBoxInit4()
        self.ComboBoxInit5()
        self.ui.comboBox.setCurrentIndex(1)
        self.ui.comboBox_4.setCurrentIndex(1)
    def ButtonColorChange1(self):
        index=self.ui.comboBox.currentIndex()
        self.ColorPaint1=self.ColorList1[index]
        self.ui.pushButton_4.setStyleSheet("background-color: " + self.ColorList1[index])
    def ButtonColorChange2(self):
        index=self.ui.comboBox_2.currentIndex()
        self.ColorPaint2 = self.ColorList2[index]
        self.ui.pushButton_5.setStyleSheet("background-color: " + self.ColorList2[index])
    def ButtonColorChange3(self):
        index=self.ui.comboBox_3.currentIndex()
        self.ColorPaint3 = self.ColorList3[index]
        self.ui.pushButton_6.setStyleSheet("background-color: " + self.ColorList3[index])
    def ButtonColorChange4(self):
        index=self.ui.comboBox_4.currentIndex()
        self.ColorPaint4 = self.ColorList4[index]
        self.ui.pushButton_7.setStyleSheet("background-color: " + self.ColorList4[index])
    def ButtonColorChange5(self):
        index=self.ui.comboBox_5.currentIndex()
        self.ColorPaint5 = self.ColorList5[index]
        self.ui.pushButton_8.setStyleSheet("background-color: " + self.ColorList5[index])
    def ComboBoxInit1(self):
        for color in self.ColorList1:
            pix_color = QPixmap(60, 20)
            pix_color.fill(QColor(color))
            self.ui.comboBox.addItem(QIcon(pix_color), ' ')
        self.ui.comboBox.setIconSize(QSize(60, 20))
    def ComboBoxInit2(self):
        for color in self.ColorList2:
            pix_color = QPixmap(60, 20)
            pix_color.fill(QColor(color))
            self.ui.comboBox_2.addItem(QIcon(pix_color), ' ')
        self.ui.comboBox_2.setIconSize(QSize(60, 20))
    def ComboBoxInit3(self):
        for color in self.ColorList3:
            pix_color = QPixmap(60, 20)
            pix_color.fill(QColor(color))
            self.ui.comboBox_3.addItem(QIcon(pix_color), ' ')
        self.ui.comboBox_3.setIconSize(QSize(60, 20))
    def ComboBoxInit4(self):
        for color in self.ColorList4:
            pix_color = QPixmap(60, 20)
            pix_color.fill(QColor(color))
            self.ui.comboBox_4.addItem(QIcon(pix_color), ' ')
        self.ui.comboBox_4.setIconSize(QSize(60, 20))
    def ComboBoxInit5(self):
        for color in self.ColorList5:
            pix_color = QPixmap(60, 20)
            pix_color.fill(QColor(color))
            self.ui.comboBox_5.addItem(QIcon(pix_color), ' ')
        self.ui.comboBox_5.setIconSize(QSize(60, 20))
    def resizeEvent(self, event):#重写窗口变换事件
        t_WinSize=self.size()
        self.ui.widget.setMinimumHeight(t_WinSize.height())
        self.ui.widget.setMinimumWidth(t_WinSize.width())
        self.ui.widget.setMaximumHeight(t_WinSize.height())
        self.ui.widget.setMaximumWidth(t_WinSize.width())

        H_table1=(t_WinSize.height()-50)*0.95
        H_table2=(t_WinSize.height()-50)*0.95-206-50
        H_widget=(t_WinSize.height()-50)*0.95-510
        self.ui.tableWidget.setMinimumHeight(H_table1)
        self.ui.tableWidget.setMaximumHeight(H_table1)
        self.ui.textEdit.setMinimumHeight(H_table2)
        self.ui.textEdit.setMaximumHeight(H_table2)

        self.ui.widget_2.setMaximumHeight(H_table1)
        self.ui.widget_2.setMinimumHeight(H_table1)

        self.ui.widget_5.setMaximumHeight(H_widget)
        self.ui.widget_5.setMinimumHeight(H_widget)

    def ResetDate(self):
        DateNow=self.ui.dateEdit.date()
        year=DateNow.year()
        month=DateNow.month()
        day=DateNow.day()
        self.DateSet(year,month,day)
        self.TableShowText(year, month, day)
        self.SliderValue=month-1
        self.ui.verticalScrollBar.setValue(month-1)
        if self.ui.radioButton_3.isChecked():
            mode=0
        elif self.ui.radioButton_2.isChecked():
            mode=1
        else:
            mode=2
        self.ColorCount(year, month, day, mode)
        # self.PaintPie()
    def SelectClear1(self):
        self.ui.tableWidget_2.clearSelection()
    def SelectClear2(self):
        self.ui.tableWidget.clearSelection()
        DateOld = self.ui.dateEdit.date()
        YearOld = DateOld.year()
        MonthOld = DateOld.month()
        item = self.ui.tableWidget_2.selectedIndexes()
        for it in item:
            DayNew=self.ui.tableWidget_2.item(it.row(),it.column()).text()
            if it.row()==0 and int(DayNew)>7:
                if MonthOld==1:
                    YearNew=YearOld-1
                    MonthNew=12
                else:
                    YearNew=YearOld
                    MonthNew=MonthOld-1
            elif it.row()>3 and int(DayNew)<=14:
                if MonthOld==12:
                    YearNew=YearOld+1
                    MonthNew=1
                else:
                    YearNew=YearOld
                    MonthNew=MonthOld+1
            else:
                YearNew = YearOld
                MonthNew = MonthOld
        self.DateSet(YearNew, MonthNew, int(DayNew))
        self.ui.dateEdit.setDate(QDate(YearNew, MonthNew, int(DayNew)))
        t = Thread(target=self.PaintPie)
        t.start()


    def DateSet(self,year,month,day):#日历设置
        FillCount = 0
        CalenderData = calendar.monthcalendar(year, month)
        DayColorAll=ReadSqliteDayColor(self.NameDB,year,month,day)
        d2 = datetime.date(year,month, 1)
        d1 = datetime.date(2013, 11, 4)
        DayPos = int((d2 - d1).days)
        DayList=[]
        for i in range(0,len(DayColorAll)):
            DayList.append(DayColorAll[i][0]-DayPos+1)
        for i in range(0,len(CalenderData)):
            for j in range(0,7):
                if CalenderData[i][j]!=0:
                    newItem = QTableWidgetItem(str(CalenderData[i][j]))

                    font = QFont("Times New Roman")
                    font.setPointSize(10)
                    font.setBold(True)
                    if CalenderData[i][j] in DayList:
                        ColorIndex=DayList.index(CalenderData[i][j])
                        newItem.setBackground(QColor(DayColorAll[ColorIndex][1]))
                    if CalenderData[i][j] == day:
                        newItem.setForeground(QColor(255, 0, 0))
                    else:
                        newItem.setForeground(QColor(0, 0, 0))  # 设置字体颜色
                    newItem.setFont(font)
                    newItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                    self.ui.tableWidget_2.setItem(i, j, newItem)
                    FillCount = FillCount + 1
        ###计算前一月数据
        if CalenderData[0][0] == 0:
            if month != 1:
                CalenderData0 = calendar.monthcalendar(year, month - 1)
            else:
                CalenderData0 = calendar.monthcalendar(year - 1, 12)
            for j in range(0, 7):
                data0 = CalenderData0[len(CalenderData0) - 1][j]
                if data0 == 0:
                    break
                newItem = QTableWidgetItem(str(data0))
                font = QFont("Times New Roman")
                font.setPointSize(10)
                newItem.setForeground(QColor(self.ColorFontDefault))
                font.setBold(True)
                newItem.setFont(font)
                newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.ui.tableWidget_2.setItem(0, j, newItem)
                FillCount = FillCount + 1
        ###计算后一月数据
        if FillCount<42:
            if month!=12:
                CalenderData1 = calendar.monthcalendar(year, month + 1)
            else:
                CalenderData1 = calendar.monthcalendar(year+1, 1)
            pos = FillCount % 7
            if FillCount<35:
                for j in range(pos, 7):
                    data0 = CalenderData1[0][j]
                    newItem = QTableWidgetItem(str(data0))
                    font = QFont("Times New Roman")
                    font.setPointSize(10)
                    newItem.setForeground(QColor(self.ColorFontDefault))
                    font.setBold(True)
                    newItem.setFont(font)
                    newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.ui.tableWidget_2.setItem(4, j, newItem)
                for j in range(0, 7):
                    data0 = CalenderData1[1][j]
                    newItem = QTableWidgetItem(str(data0))
                    font = QFont("Times New Roman")
                    font.setPointSize(10)
                    newItem.setForeground(QColor(self.ColorFontDefault))
                    font.setBold(True)
                    newItem.setFont(font)
                    newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.ui.tableWidget_2.setItem(5, j, newItem)
            else:
                for j in range(pos, 7):
                    data0 = CalenderData1[0][j]
                    newItem = QTableWidgetItem(str(data0))
                    font = QFont("Times New Roman")
                    font.setPointSize(10)
                    newItem.setForeground(QColor(self.ColorFontDefault))
                    font.setBold(True)
                    newItem.setFont(font)
                    newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.ui.tableWidget_2.setItem(5, j, newItem)
    def dateinit(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day

        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)#表格内容禁用修改
        self.ui.tableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)  #仅能单选
        self.ui.tableWidget_2.verticalHeader().setVisible(False)
        self.ui.tableWidget_2.setFrameShape(QFrame.NoFrame)#无边框显示
        self.ui.tableWidget_2.setShowGrid(False) #设置不显示格子线
        self.DateSet(year,month,day)

    def TableItemInit(self,ColumnNum,RowNum):
        for i in range(0,RowNum):
            for j in range(0,ColumnNum):
                newItem = QTableWidgetItem('23')
                newItem.setForeground(QColor(0, 0, 0))#设置字体颜色
                newItem.setFont(QFont("宋体"))
                newItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                self.ui.tableWidget.setItem(i, j, newItem)

    def TableInit(self,ColumnNum,RowNum):#表格大小设置
        self.ui.tableWidget.setColumnCount(ColumnNum)
        self.ui.tableWidget.setRowCount(RowNum)
        VerticalHeader=[]
        for i in range(0,RowNum):
            self.ui.tableWidget.setRowHeight(i, 20)
        for i in range(7,24):
            t_time=str(i)+':00-'+str(i)+':30'
            VerticalHeader.append(t_time)
            if i!=23:
                t_time = str(i) + ':30-' + str(i+1) + ':00'
                VerticalHeader.append(t_time)
            else:
                t_time = '23:30-00:00'
                VerticalHeader.append(t_time)
        self.ui.tableWidget.setVerticalHeaderLabels(VerticalHeader)
        self.ui.tableWidget.setStyleSheet("selection-background-color:lightblue;")#选中背景设置
        self.ui.tableWidget_2.setStyleSheet("selection-background-color:lightblue;")#选中背景设置
    def TableCombine(self):#合并单元格
        # self.ui.tableWidget.setColumnCount(15)
        item=self.ui.tableWidget.selectedIndexes()
        RowIndex=[]
        ColumnIndex=[]
        SpanIndex=[]
        for it in item:
            RowIndex.append(it.row())
            ColumnIndex.append(it.column())
        if len(RowIndex)<2:
            return
        if ColumnIndex[0] * len(RowIndex) != sum(ColumnIndex): #仅对列进行合并，判断均为一列
            return
        SpanIndex.append(RowIndex[0])
        SpanIndex.append(ColumnIndex[0])
        SpanIndex.append(RowIndex[len(RowIndex)-1]-RowIndex[0]+1)
        SpanIndex.append(1)
        self.ui.tableWidget.setSpan(SpanIndex[0],SpanIndex[1],SpanIndex[2],SpanIndex[3])#要改变单元格的   1行数  2列数     要合并的  3行数  4列
    def TableClear2(self,Column):
        t_ColumnHeadItem=self.ui.tableWidget.horizontalHeaderItem(Column)
        t_ColumnHead=t_ColumnHeadItem.text()#获取当前列表头

        self.ui.tableWidget.removeColumn(Column)#移除当前列
        self.ui.tableWidget.insertColumn(Column)#插入当前列
        item1 = QTableWidgetItem(t_ColumnHead)#重写表头信息
        self.ui.tableWidget.setHorizontalHeaderItem(Column, item1)
        for k in range(0,34):
            newItem = QTableWidgetItem()
            self.ui.tableWidget.setItem(k,Column,newItem)
    def TableClear(self):#还原单元格
        item = self.ui.tableWidget.selectedIndexes()
        RowIndex = []
        ColumnIndex = []
        for it in item:
            RowIndex.append(it.row())
            ColumnIndex.append(it.column())
        if not RowIndex:
            return
        t_ColumnHeadItem=self.ui.tableWidget.horizontalHeaderItem(ColumnIndex[0])
        t_ColumnHead=t_ColumnHeadItem.text()#获取当前列表头

        self.ui.tableWidget.removeColumn(ColumnIndex[0])#移除当前列
        self.ui.tableWidget.insertColumn(ColumnIndex[0])#插入当前列
        item1 = QTableWidgetItem(t_ColumnHead)#重写表头信息
        self.ui.tableWidget.setHorizontalHeaderItem(ColumnIndex[0], item1)
        for k in range(0,34):
            newItem = QTableWidgetItem()
            self.ui.tableWidget.setItem(k,ColumnIndex[0],newItem)
        # horizontalHeader = ["工号", "姓名", "性别", "年龄", "职称"]
        # self.ui.tableWidget.setHorizontalHeaderLabels(horizontalHeader)
    def ColorSelect(self):#颜色选取
        col = QColorDialog.getColor()
        self.ui.pushButton_3.setStyleSheet("background-color: "+col.name())
        self.ColorCanChange=col.name()
    def Color0(self):
        sbit=self.ColorFill1(self.ColorCanChange)
        if sbit:
            return True
        self.ColorFill2(self.ColorCanChange)
    def Color1(self):
        sbit=self.ColorFill1(self.ColorPaint1)
        if sbit:
            return True
        self.ColorFill2(self.ColorPaint1)
    def Color2(self):
        sbit=self.ColorFill1(self.ColorPaint2)
        if sbit:
            return True
        self.ColorFill2(self.ColorPaint2)
    def Color3(self):
        sbit=self.ColorFill1(self.ColorPaint3)
        if sbit:
            return True
        self.ColorFill2(self.ColorPaint3)
    def Color4(self):
        sbit=self.ColorFill1(self.ColorPaint4)
        if sbit:
            return True
        self.ColorFill2(self.ColorPaint4)
    def Color5(self):
        sbit=self.ColorFill1(self.ColorPaint5)
        if sbit:
            return True
        self.ColorFill2(self.ColorPaint5)
    def ColorFill1(self,Colorstr):#颜色填充
        item = self.ui.tableWidget.selectedIndexes()
        RowIndex = []
        ColumnIndex = []
        if not item:
            return False#防止同时给两个表格上色
        for it in item:
            RowIndex.append(it.row())
            ColumnIndex.append(it.column())
        for i in RowIndex:
            for j in ColumnIndex:
                newItem = self.ui.tableWidget.item(i, j)
                newItem.setBackground(QColor(Colorstr))
        return True
    def ColorFill2(self,Colorstr):#颜色填充
        item = self.ui.tableWidget_2.selectedIndexes()
        RowIndex = []
        ColumnIndex = []
        for it in item:
            RowIndex.append(it.row())
            ColumnIndex.append(it.column())
        for i in RowIndex:
            for j in ColumnIndex:
                t_item=self.ui.tableWidget_2.item(i, j)
                t_item.setBackground(QColor(Colorstr))