import numpy as np

from .Calendar import MyCalendar
from .Stats import StatMixin
from .helper_functions import get_attribute, get_labels

class MyFriend(MyCalendar):
    '''LINE友達登録数ページ用のクラス'''

    def __init__(self, users):
        super().__init__(users=users)
        self.groups = None
        self.labels = None
        self.other_label = None

    def yeardata(self, year, percent=False, calendar=False):
        '''通年の友達登録人数を返す.'''
        # 通年の配列-データ数１
        data = super().year_array(year, 1, calendar)

        # 月毎に人数をカウントする
        col = 2 * calendar
        for month in range(1, 13):
            num = super().get_monthdata(year, month).shape[0]
            data[month-1][col] = num

        if percent:
            return (data[:, col:] / self.get_sum(year) * 100).flatten().tolist()

        return data if calendar else data.flatten().tolist()

    def monthdata(self, year, month, percent=False, calendar=False, weekdays=False):
        '''月毎の友達登録人数を返す.'''
        # 月の配列-データ数１
        data = super().month_array(year, month, 1, calendar=calendar, weekdays=weekdays)

        # 日毎に人数をカウントする
        if calendar:
            col = 3 + weekdays
        else:
            col = 0
        for day in range(1, len(data)+1):
            num = super().get_daydata(year, month, day).shape[0]
            data[day-1][col] = num

        if percent:
            return (data[:, col:] / self.get_sum(year) * 100).flatten().tolist()
            
        return data if calendar else data.flatten().tolist()

    def weeklydata(self, year, month, firstweekday='sunday', persent=False):
        weeks = super().weeklydays(year, month, string=True, firstweekday=firstweekday)
        user_data = super().get_weekdata(year, month, firstweekday)
        data = []
        if len(user_data)==0:
            return [0] * len(weeks)

        for i in range(len(user_data)):
            data.append(len(user_data[i]))

        if persent:
            return [x / self.sum(year, month) * 100 for x in data]
        return data

    def sum(self, year, month=None):
        '''year, monthに対応した合計友達人数を返す.'''
        return super().get_sum(year, month)

    def mean(self, year, month=None):
        '''year, monthに対応した平均友達人数を返す.'''
        if month:
            return self.sum(year, month) / len(super().days(year, month))
        
        return self.sum(year=year) / 12

    def max(self, year, month=None):
        '''year, monthに対応した最大友達人数を返す.'''
        if month:
            return np.array(self.monthdata(year, month)).max()
        
        return np.array(self.yeardata(year)).max()

    def min(self, year, month=None):
        '''year, monthに対応した最小友達人数を返す.'''
        if month:
            return np.array(self.monthdata(year, month)).min()
        
        return np.array(self.yeardata(year)).min()

    def datasets(self, year, month=None, weekly=None, firstweekday='sunday', percent=False):
        ''''''
        if weekly:
            data = self.weeklydata(year, month, firstweekday, percent)
            labels = super().weeklydays(year, month, firstweekday, string=True)
        elif month:
            data = self.monthdata(year, month, percent)
            labels = self.days(year, month, labels=True)
        else:
            data = self.yeardata(year, percent)
            labels = [str(i+1) + '月' for i in range(12)]

        datasets = [0, 0]
        datasets[0] = {'labels': labels}
        datasets[1] = {'datasets': [{'label': '友達登録数', 'data': data}]}

        return datasets