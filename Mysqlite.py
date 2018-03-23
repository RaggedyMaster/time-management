# -*- coding: utf-8 -*-
import sqlite3
import datetime
from MyDataClass import WeekDay,ColorDay
import calendar

def ReadSqliteDayColor(NameDB,DYear,DMonth,DDay):
    MonthNow = calendar.monthrange(DYear, DMonth)
    DayNum = MonthNow[1]

    d2 = datetime.date(DYear, DMonth, 1)
    d1 = datetime.date(2013, 11, 4)

    DayBetween = int((d2 - d1).days)
    SheetName = ['DayBasicInformation', 'DaySize', 'DayValue', 'DayColor']
    DayB = str(DayBetween)
    DayE = str(DayBetween + DayNum - 1)

    conn = sqlite3.connect(NameDB)
    c = conn.cursor()

    c.execute('SELECT id,DayColor FROM ' + SheetName[0] + ' WHERE id BETWEEN ' + DayB + ' and ' + DayE)
    DayColorAll = c.fetchall()
    conn.close()
    return DayColorAll
def ReadSqlite(NameDB,DYear,DMonth,DDay):
    d2=datetime.date(DYear, DMonth, DDay)
    d1 = datetime.date(2013, 11, 4)
    DayBetween = int((d2 - d1).days-(d2 - d1).days%7)
    SheetName=['DayBasicInformation','DaySize','DayValue','DayColor']
    DayB=str(DayBetween)
    DayE=str(DayBetween+6)

    conn = sqlite3.connect(NameDB)
    c = conn.cursor()

    c.execute('SELECT * FROM ' + SheetName[0] +' WHERE id BETWEEN '+DayB+' and '+DayE)
    WeekSelectedDay=c.fetchall()
    c.execute('SELECT * FROM ' + SheetName[1] +' WHERE id BETWEEN '+DayB+' and '+DayE)
    WeekSelectedSize=c.fetchall()
    c.execute('SELECT * FROM ' + SheetName[2] +' WHERE id BETWEEN '+DayB+' and '+DayE)
    WeekSelectedValue=c.fetchall()
    c.execute('SELECT * FROM ' + SheetName[3] +' WHERE id BETWEEN '+DayB+' and '+DayE)
    WeekSelectedColor=c.fetchall()
    Week=[]
    if WeekSelectedDay:
        for i in range(0,len(WeekSelectedDay)):
            Id=WeekSelectedDay[i][0]
            Year=WeekSelectedDay[i][1]
            Date = WeekSelectedDay[i][2]
            Num=WeekSelectedDay[i][3]
            DayColor=WeekSelectedDay[i][4]
            Comment=WeekSelectedDay[i][5]

            Value=WeekSelectedValue[i][1:Num+1]
            EventColor = WeekSelectedColor[i][1:Num + 1]
            Row = WeekSelectedSize[i][1:Num + 1]
            WeekSingle=WeekDay(Id, Year, Date, Comment, DayColor, Num, Value, EventColor, Row)
            Week.append(WeekSingle)
    conn.close()
    return Week
def WriteSqlite(NameDB,SingleDate):
    conn = sqlite3.connect(NameDB)
    Mydb = conn.cursor()

    t_DayBasicInformation=[SingleDate.Id,SingleDate.Year,SingleDate.Date,SingleDate.Num,SingleDate.DayColor,SingleDate.Comment]

    Mydb.execute("INSERT INTO DayBasicInformation VALUES (?, ?, ?,?,?,?)", t_DayBasicInformation)
    Mydb.execute("INSERT INTO DaySize VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",SingleDate.Row)
    Mydb.execute("INSERT INTO DayValue VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",SingleDate.Value)
    Mydb.execute("INSERT INTO DayColor VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",SingleDate.EventColor)

    conn.commit()
    conn.close()
def DeleteSqlite(NameDB,id):
    conn = sqlite3.connect(NameDB)
    Mydb = conn.cursor()
    Id=str(id)
    Mydb.execute('DELETE FROM DayBasicInformation WHERE id='+Id)
    Mydb.execute('DELETE FROM DaySize WHERE id=' + Id)
    Mydb.execute('DELETE FROM DayValue WHERE id=' + Id)
    Mydb.execute('DELETE FROM DayColor WHERE id=' + Id)

    conn.commit()
    conn.close()
def ReadSqliteEventColor(NameDB,DYear,DMonth,DDay,Mode):
    SheetName = ['DayBasicInformation', 'DaySize','DayColor']
    d2=datetime.date(DYear, DMonth, DDay)
    d1 = datetime.date(2013, 11, 4)
    DayEnd=int((d2-d1).days)
    DayE = str(DayEnd)
    if Mode==0:
        if DayEnd -6>0:
            DayB = str(DayEnd -7)
        else:
            DayB='0'
    elif Mode==1:
        if DayEnd - 30 > 0:
            DayB = str(DayEnd - 30)
        else:
            DayB = '0'
    elif Mode==2:
        if DayEnd - 364 > 0:
            DayB = str(DayEnd - 365)
        else:
            DayB='0'
    elif Mode==3:
        DayB=str(DayEnd)
    conn = sqlite3.connect(NameDB)
    c = conn.cursor()

    c.execute('SELECT id,num,DayColor FROM ' + SheetName[0] +' WHERE id BETWEEN '+DayB+' and '+DayE)
    ColorNumSum = c.fetchall()
    c.execute('SELECT * FROM ' + SheetName[1] +' WHERE id BETWEEN '+DayB+' and '+DayE)
    DaySizeSum=c.fetchall()
    c.execute('SELECT * FROM ' + SheetName[2] +' WHERE id BETWEEN '+DayB+' and '+DayE)
    ColorSum=c.fetchall()

    ColorALL=[]
    for i in range(0,len(ColorNumSum)):
        Id=ColorNumSum[i][0]
        Num=ColorNumSum[i][1]
        DayColor = ColorNumSum[i][2]
        EventColor = ColorSum[i][1:Num + 1]
        Row = DaySizeSum[i][1:Num + 1]

        ColorSingle = ColorDay(Id,DayColor,Num,EventColor,Row)
        ColorALL.append(ColorSingle)
    conn.close()
    return ColorALL
if __name__ == '__main__':
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



    NameDB = '.\\Source\\test.db'
    ColorAll=ReadSqliteEventColor(NameDB,2013,12,1,3)
    c1 = [0] * 5
    c2 = [0] * 8
    print(ColorAll)
    for i in range(0,len(ColorAll)):
        id=ColorAll[i].Id
        DayColor=ColorAll[i].DayColor
        Num=ColorAll[i].Num
        EventColor=ColorAll[i].EventColor
        Row=ColorAll[i].Row
        for j in range(0,Num):
            if j < Num - 1:
                num=int(Row[j + 1]) - int(Row[j])
                ColorNow=EventColor[j].lower()
                if len(ColorNow)==9:
                    ColorNow='#'+ColorNow[3:9]
                    print(ColorNow)
                if ColorNow in Green:
                    c1[0]+=num
                    c2[0]+=num
                elif ColorNow in Yellow:
                    c1[1] += num
                    c2[1] += num
                elif ColorNow in Blue:
                    c1[2] += num
                    c2[2] += num
                elif ColorNow in Delight:
                    c1[2] += num
                    c2[3] += num
                elif ColorNow in Pink:
                    c1[2] += num
                    c2[4] += num
                elif ColorNow in Tired:
                    c1[3] += num
                    c2[5] += num
                elif ColorNow in Red:
                    c1[4] += num
                    c2[6] += num
                elif ColorNow in Fucked:
                    c1[4] += num
                    c2[7] += num
            else:
                num = 35-int(Row[j])
                ColorNow=EventColor[j].lower()
                if len(ColorNow)==9:
                    ColorNow='#'+ColorNow[3:9]
                if ColorNow in Green:
                    c1[0]+=num
                    c2[0]+=num
                elif ColorNow in Yellow:
                    c1[1] += num
                    c2[1] += num
                elif ColorNow in Blue:
                    c1[2] += num
                    c2[2] += num
                elif ColorNow in Delight:
                    c1[2] += num
                    c2[3] += num
                elif ColorNow in Pink:
                    c1[2] += num
                    c2[4] += num
                elif ColorNow in Tired:
                    c1[3] += num
                    c2[5] += num
                elif ColorNow in Red:
                    c1[4] += num
                    c2[6] += num
                elif ColorNow in Fucked:
                    c1[4] += num
                    c2[7] += num
    print(c1)
    print(c2)










