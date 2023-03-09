import calendar
from calendar import Calendar
import numpy as np

class MyCalendar(Calendar):
    '''時間（年、月、週、日）処理用のクラス. 定型分析クラスに継承させる.'''
    def __init__(self, users, start=None, end=None):
        super().__init__()
        self.users = users  # ユーザーオブジェクトのリスト
        self.start = start  # 期間選択用
        self.end = end      # 期間選択用

        # ユーザー登録年のリスト [2020, 2021, 2022]
        self.year_list = np.array(list(set([user.year for user in users])), dtype='int16')

        # ユーザー登録年、月（タプル）のリスト [(2020, 12), (2021, 1), (2021, 3), (2022, 8)]
        self.month_list = np.array(sorted(list(set([(user.year, user.month) for user in users]))), dtype='int16')
        
        # ユーザー登録年、月、日（タプル）のリスト [(2020, 12, 24), (2020, 12, 25), (2021, 3, 8), (2022, 8, 20)]
        self.day_list = np.array(sorted(list(set([(user.year, user.month, user.day) for user in users]))), dtype='int16')

        self.weekdays = {'MONDAY': 0, 'TUESDAY': 1, 'WEDNESDAY': 2, 'THURSDAY': 3, 'FRIDAY': 4, 'SATURDAY': 5, 'SUNDAY': 6}

    def years_list(self):
        '''ユーザー登録年のリストを返す.'''
        return self.year_list
    
    def months_list(self, year, calendar=False):
        '''ユーザー登録年、月のリストを返す.'''
        mask = self.month_list[:, 0] == year
        if calendar:
            return self.month_list[mask]
        return self.month_list[mask][:, 1]
        
    def days_list(self, year, month, calendar=False):
        '''ユーザー登録年、月、日のリストを返す.'''
        mask = (self.day_list[:,0]==year) * (self.day_list[:,1]==month)

        if calendar:
            return self.day_list[mask]
        return self.day_list[mask][:, 2]

    def days(self, year, month, weekdays=False, labels=False):
        '''日付を返す.'''
        if weekdays:
            days = np.array(self.monthdays2calendar(year, month))
            days = days.reshape(days.shape[0]*days.shape[1], 2)
            return days[days[:, 0] > 0]

        days = np.array(list(self.itermonthdays(year, month)))
        days = days[days>0]
        if labels:
            days = [str(i) for i in days]
            days[0] = f'{month}/1'
        return days

    def weeklydays(self, year, month, firstweekday='sunday', weekdays=False, string=False):
        '''週毎の日付を返す.'''
        self.setfirstweekday(self.weekdays[firstweekday.upper()])

        if weekdays:
            return np.array(self.monthdays2calendar(year, month))

        weeks = np.array(self.monthdayscalendar(year, month))
        if string:
            weeks_str = []
            for week in weeks:
                indices = np.nonzero(week)
                first = week[indices[0][0]]
                last = week[indices[0][-1]]
                weeks_str.append(f'{month}/{first} ~ {month}/{last}')
            return weeks_str

        return weeks

    def year_array(self, year, num=1, calendar=False):
        '''通年の配列を返す.'''
        n = 12
        data = np.zeros((n, num), dtype='int16')
        if calendar:
            y = np.array([year]*n, dtype='int16').reshape(n, 1)
            m = np.arange(1, n+1, dtype='int16').reshape(n, 1)
            return np.concatenate((y, m, data), axis=1)
        return data

    def month_array(self, year, month, num=1, calendar=False, weekdays=False):
        '''月毎の配列を返す.'''
        d = self.days(year=year, month=month, weekdays=weekdays)
        if not weekdays:
            d = d.reshape(len(d), 1)
        data = np.zeros((len(d), num), dtype='int16')
        if calendar:
            y = np.array([year]*len(d), dtype='int16').reshape(len(d), 1)
            m = np.array([month]*len(d), dtype='int16').reshape(len(d), 1)
            return np.concatenate((y, m, d, data), axis=1)
        return data

    def weekly_array(self, year, month, num=1, firstweekday='sunday'):
        '''週毎の配列を返す.'''
        week = self.weeklydays(year=year, month=month, firstweekday=firstweekday)
        data = np.zeros((len(week), num), dtype='int16')

        return data

    def set_datas(self, start, end):
        '''期間選択.'''
        self.start = start
        self.end = end

    def get_yeardata(self, year, calendar=False):
        '''年毎のユーザーデータを返す.'''
        if year in self.year_list:
            if calendar:
                return np.array([(year, user.month, user.day, user) for user in self.users if user.year==year])
            else:
                return np.array([user for user in self.users if user.year==year])
        else:    
            return np.array([])

    def get_monthdata(self, year, month, calendar=False):
        '''月毎のユーザーデータを返す.'''
        # yearに対応した月リスト
        months = self.months_list(year)
        if not month in months:
            return np.array([])

        # yearに対応したユーザーデータ
        users = self.get_yeardata(year)
        
        # monthに対応したユーザーデータ
        if calendar:
            return np.array([(year, month, user.day, user) for user in users if user.month==month])
        else:
            return np.array([user for user in users if user.month==month])

    def get_weekdata(self, year, month, firstweekday='sunday'):
        '''週毎のユーザーデータを返す.'''
        ###            ###
        #   期間選択追記   #
        ###            ###

        # year, monthに対応した日リスト
        days = self.days_list(year, month)
        if not days.any():
            return np.array([])

        # 週毎の配列
        weeks = self.weeklydays(year, month, firstweekday)

        # year, monthに対応したユーザーリスト
        users = self.get_monthdata(year, month)

        # 
        data = [[]]* len(weeks)
        for i, week in enumerate(weeks):
            temp = []
            for day in week:
                temp += [user for user in users if user.day==day]
            data[i] = temp
        return data

    def get_daydata(self, year, month, day, calendar=False):
        '''日毎のユーザーデータを返す.'''
        ###            ###
        #   期間選択追記   #
        ###            ###

        # year, monthに対応した日リスト
        days = self.days_list(year, month)
        if not days.any():
            return np.array([])

        # year, monthに対応したユーザーリスト
        users = self.get_monthdata(year, month)

        if calendar:
            return np.array([(year, month, day, user) for user in users if user.day==day])
        else:
            return np.array([user for user in users if user.day==day])


    def yeardata_array(self, year, tag_list, calendar=False):
        '''通年の配列データを返す.'''

        # 通年データ格納配列(”不明”用にattributesの数+１)
        n = len(tag_list)
        data_array = self.year_array(year, n, calendar=calendar)

        # その他用通年データ格納配列
        other_array = self.year_array(year, calendar=calendar)

        # ユーザデータなしならそのまま返す
        if not year in self.year_list:
            return data_array

        # 通年のユーザデータ
        users = self.get_yeardata(year)

        col = calendar * 2
        for user in self.get_yeardata(year):
            count = 0 # その他用に属性データカウント
            for i, attr in enumerate(tag_list):
                data_array[user.month-1, col:][i] += int(user.data[attr])
                count += int(user.data[attr])

            # カウント0ならその他データに+1
            if not count:
                other_array[user.month-1, col:][0] += 1

        # ”不明”用の通年データの合計が0なら削除, 0以外ならデータ配列に足す
        if other_array.sum() == 0:
            return data_array
        else:
            if calendar:
                return np.concatenate((data_array, other_array[:,-1].reshape(len(other_array), 1)), axis=1)
            else:
                return np.concatenate((data_array, other_array), axis=1)


    def monthdata_array(self, year, month, tag_list, calendar=False, weekdays=True):
        '''月毎の配列データを返す.'''
        # 通年データ格納配列
        n = len(tag_list)
        data_array = self.month_array(year, month, n, calendar=calendar, weekdays=weekdays)

        # ”不明”用の通年データ格納配列
        other_array = self.month_array(year, month, calendar=calendar, weekdays=weekdays)

        # ユーザデータなしならそのまま返す
        if not month in self.months_list(year):
            return data_array

        # 通年のユーザデータ
        users = self.get_monthdata(year=year, month=month)

        if calendar:
            col = 3 + weekdays
        else:
            col = 0
        
        for user in users:
            count = 0   # ”不明”用に属性データカウント-
            for i, attr in enumerate(tag_list):
                data_array[user.day-1, col:][i] += int(user.data[attr])
                count += int(user.data[attr])

            # カウント0ならその他データに+1
            if not count:
                other_array[user.day-1, col:][0] += 1

        # ”不明”用の通年データの合計が0なら削除, 0以外ならデータ配列に足す
        if other_array.sum() == 0:
            return data_array
        else:
            if calendar:
                return np.concatenate((data_array, other_array[:,-1].reshape(len(other_array), 1)), axis=1)
            else:
                return np.concatenate((data_array, other_array), axis=1)

    def weeklydata_array(self, year, month, tag_list, firstweekday='sunday'):
        '''週毎の配列データを返す.'''
        # 週の配列
        weeklydays = self.weeklydays(year, month)

        # 週毎のデータ格納配列
        n = len(tag_list)
        data_array = self.weekly_array(year, month, n, firstweekday=firstweekday)

        # ”不明”用の通年データ格納配列
        other_array = self.weekly_array(year, month, firstweekday=firstweekday)

        # 週毎のユーザデータ
        weekly_users = self.get_weekdata(year, month, firstweekday=firstweekday)

        week = 0
        for users in weekly_users:
            week += 1
            if users:
                for user in users:
                    count = 0   # ”不明”用に属性データカウント-
                    for i, attr in enumerate(tag_list):
                        data_array[week-1, :][i] += int(user.data[attr])
                        count += int(user.data[attr])

                    # カウント0ならその他データに+1
                    if not count:
                        other_array[week-1, :][0] += 1

        # ”不明”用の通年データの合計が0なら削除, 0以外ならデータ配列に足す
        if other_array.sum() == 0:
            return data_array

        else:
            return np.concatenate((data_array, other_array), axis=1)
        

    def get_sum(self, year, month=None):
        if month:
            return self.get_monthdata(year, month).shape[0]
        
        return self.get_yeardata(year).shape[0]