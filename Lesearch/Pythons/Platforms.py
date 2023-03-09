from .Calendar import MyCalendar
from .Stats import StatMixin

class MyPlatform(MyCalendar, StatMixin):
    '''流入経路ページ用のクラス'''
    def __init__(self, users, tag):
        super().__init__(users=users)

        self.tag_dict = tag # タグの辞書