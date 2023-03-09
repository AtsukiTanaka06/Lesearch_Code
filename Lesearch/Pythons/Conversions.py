from .Calendar import MyCalendar
from .Stats import StatMixin

class MyConversion(MyCalendar, StatMixin):
    '''コンバージョン用のクラス'''
    def __init__(self, users, tag):
        super().__init__(users)

        self.tag_dict = tag # タグの辞書