from .Calendar import MyCalendar
from .Stats import StatMixin

class MyChannel(MyCalendar, StatMixin):
    '''配信ページ用のクラス'''
    
    def __init__(self, users, tag):
        super().__init__(users=users)

        self.tag_dict = tag