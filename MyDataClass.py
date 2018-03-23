class SingleDay(object):
    def __init__(self,Year,Date,Comment,DayColor,Num,Value,EventColor,Row):
        self.Year=Year
        self.Date=Date #日子
        self.Comment = Comment #批注
        self.DayColor = DayColor #当日颜色
        self.Num = Num #当天块数量
        self.Value = Value #块内数值
        self.EventColor = EventColor #事件块颜色
        self.Row = Row #块大小
class WeekDay(object):
    def __init__(self,Id,Year,Date,Comment,DayColor,Num,Value,EventColor,Row):
        self.Id=Id
        self.Year=Year
        self.Date=Date #日子
        self.Comment = Comment #批注
        self.DayColor = DayColor #当日颜色
        self.Num = Num #当天块数量
        self.Value = Value #块内数值
        self.EventColor = EventColor #事件块颜色
        self.Row = Row #块大小
class ColorDay(object):
    def __init__(self,Id,DayColor,Num,EventColor,Row):
        self.Id=Id
        self.DayColor = DayColor #当日颜色
        self.Num = Num #当天块数量
        self.EventColor = EventColor #事件块颜色
        self.Row = Row #块大小