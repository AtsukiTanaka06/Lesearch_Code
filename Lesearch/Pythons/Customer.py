from .Calendar import MyCalendar
from .Stats import StatMixin

class MyCustomer(MyCalendar, StatMixin):
    '''顧客属性ページ用のクラス'''
    
    def __init__(self, users, tag):
        super().__init__(users=users)

        self.tag_dict = tag # タグの辞書

        # 都道府県のリスト
        if '都道府県' in tag.keys():
            prefec_list = []
            for user in users:
                prefec = user.data['都道府県']
                prefec_list.append(prefec)
            prefec_list = list(set(prefec_list))
            self.tag_dict['都道府県'] = dict(zip(prefec_list, prefec_list))


    def prefec_yeardata_array(self, year, tag_list, calendar=False):
        '''都道府県用のデータ配列'''
        n = len(tag_list)
        data_array = self.year_array(year, n, calendar=calendar)

        # ユーザデータなしならそのまま返す
        if not year in self.year_list:
            pass
            # return data_array

        # 通年のユーザデータ
        users = self.get_yeardata(year)

        col = calendar * 2
        for user in users:
            idx = tag_list.index(user.data['都道府県'])

            data_array[user.month-1, col:][idx] += 1

        return data_array

    def prefec_monthdata_array(self, year, month, tag_list, calendar=False, weekdays=True):
        '''月毎の都道府県用のデータ配列を返す.'''
        # 月毎データ格納配列
        n = len(tag_list)
        data_array = self.month_array(year, month, n, calendar=calendar, weekdays=weekdays)

        # ユーザデータなしならそのまま返す
        if not month in self.months_list(year):
            return data_array

        # 月毎のユーザデータ
        users = self.get_monthdata(year=year, month=month)

        if calendar:
            col = 3 + weekdays
        else:
            col = 0
        
        for user in users:
            idx = tag_list.index(user.data['都道府県'])

            data_array[user.day-1, col:][idx] += 1

        return data_array

    def prefec_weeklydata_array(self, year, month, tag_list, firstweekday='sunday'):
        '''週毎の都道府県用のデータ配列を返す.'''
        # 週の配列
        weeklydays = self.weeklydays(year, month)

        # 週毎のデータ格納配列
        n = len(tag_list)
        data_array = self.weekly_array(year, month, n, firstweekday=firstweekday)

        # 週毎のユーザデータ
        weekly_users = self.get_weekdata(year, month, firstweekday=firstweekday)

        week = 0
        for users in weekly_users:
            week += 1
            if users:
                for user in users:
                    idx = tag_list.index(user.data['都道府県'])
                    data_array[week-1, :][idx] += 1

        return data_array


    def prefec_yeardata(self, year, percent=False, calendar=False):
        '''通年のデータ配列を返す.'''
        # タグリスト
        tag_list = list(self.tag_dict['都道府県'].keys())

        data = self.prefec_yeardata_array(year, calendar=calendar, tag_list=tag_list)

        col = calendar * 2
        sum = self.get_sum(year)
        if percent and sum != 0:
            return data[:, col:] / sum * 100
        return data

    def prefec_monthdata(self, year, month, percent=False, calendar=False, weekdays=False):
        '''月毎のデータ配列を返す.'''
        # タグリスト
        tag_list = list(self.tag_dict['都道府県'].keys())

        data = self.prefec_monthdata_array(year, month, tag_list=tag_list, calendar=calendar, weekdays=weekdays)
        if calendar:
            col = 3 + weekdays
        else:
            col = 0

        sum = self.get_sum(year, month)
        if percent and sum != 0:
            return data[:, col:] / sum * 100
        return data

    def prefec_weeklydata(self, year, month, firstweekday='sunday', percent=False):
        '''月毎のデータ配列を返す.'''
        # タグリスト
        tag_list = list(self.tag_dict['都道府県'].keys()
)
        data = self.prefec_weeklydata_array(year, month, tag_list=tag_list, firstweekday=firstweekday)

        sum = self.get_sum(year, month)
        if percent and sum != 0:
            return data / sum * 100
        return data

    def prefec_datasets(self, year, month=None, week=False, firstweekday='sunday', percent=False):
        '''都道府県グラフ表示用のデータセット'''

        # 週毎
        if week and month:
            data = self.prefec_weeklydata(year, month, firstweekday=firstweekday, percent=percent).T.tolist()
            x_labels = self.weeklydays(year, month, firstweekday=firstweekday, string=True)
        # 月毎
        elif month:
            data = self.prefec_monthdata(year, month, percent).T.tolist()
            x_labels = self.days(year, month, labels=True)
        # 年毎
        else:
            data = self.prefec_yeardata(year, percent).T.tolist()
            x_labels = [str(i+1)+'月' for i in range(12)]

        # attrs = self.labels[group]
        labels = list(self.tag_dict['都道府県'].values())
        labels = ['不明' if x == '' else x for x in labels]
        
        datasets = [0, 0]
        datasets[0] = {'labels': x_labels}
        datasets[1] = {'datasets': [{'label': labels[i], 'data': data[i]} for i in range(len(data))]}

        return datasets