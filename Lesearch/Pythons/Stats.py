class StatMixin:
    '''定型分析で使う関数をまとめたクラス.'''

    def yeardata(self, group, year, percent=False, calendar=False):
        '''通年のデータ配列を返す.'''
        # タグリスト
        tag_list = self.tag_dict[group].keys()

        data = self.yeardata_array(year, calendar=calendar, tag_list=tag_list)

        col = calendar * 2
        sum = self.get_sum(year)
        if percent and sum != 0:
            return data[:, col:] / sum * 100
        return data

    def monthdata(self, group, year, month, percent=False, calendar=False, weekdays=False):
        '''月毎のデータ配列を返す.'''
        # タグリスト
        tag_list = self.tag_dict[group].keys()

        data = self.monthdata_array(year, month, tag_list=tag_list, 
                                    calendar=calendar, weekdays=weekdays)
        if calendar:
            col = 3 + weekdays
        else:
            col = 0

        sum = self.get_sum(year, month)
        if percent and sum != 0:
            return data[:, col:] / sum * 100
        return data

    def weeklydata(self, group, year, month, firstweekday='sunday', percent=False):
        '''月毎のデータ配列を返す.'''
        # タグリスト
        tag_list = self.tag_dict[group].keys()

        data = self.weeklydata_array(year, month, tag_list=tag_list, firstweekday=firstweekday)

        sum = self.get_sum(year, month)
        if percent and sum != 0:
            return data / sum * 100
        return data

    def sum(self, group, year, month=None):
        '''通年、月毎の合計を返す.'''
        if month:
            data = self.monthdata(group, year, month)
        else:
            data = self.yeardata(group, year)

        lst = []
        for i in range(data.shape[1]):
            lst.append(data[:, i].sum())
        return np.array(lst)
        
    def max(self, group, year, month=None):
        '''通年、月毎の最大を返す.'''
        if month:
            data = self.monthdata(group, year, month)
        else:
            data = self.yeardata(group, year)

        lst = []
        for i in range(data.shape[1]):
            lst.append(data[:, i].max())
        return np.array(lst)

    def min(self, group, year, month=None):
        '''通年、月毎の最小を返す.'''
        if month:
            data = self.monthdata(group,year, month)
        else:
            data = self.yeardata(group, year)

        lst = []
        for i in range(data.shape[1]):
            lst.append(data[:, i].min())
        return np.array(lst)

    def mean(self, group, year, month=None):
        '''通年、月毎の平均を返す.'''
        if month:
            data = self.monthdata(group, year, month)
        else:
            data = self.yeardata(group, year)

        lst = []
        for i in range(data.shape[1]):
            lst.append(data[:, i].mean())
        return np.array(lst)

    def datasets(self, group, year, month=None, week=False, firstweekday='sunday', percent=False):
        '''グラフ表示用のデータセット'''
        # 週毎
        if week and month:
            data = self.weeklydata(group, year, month, firstweekday=firstweekday, percent=percent).T.tolist()
            x_labels = self.weeklydays(year, month, firstweekday=firstweekday, string=True)
        # 月毎
        elif month:
            data = self.monthdata(group, year, month, percent).T.tolist()
            x_labels = self.days(year, month, labels=True)
        # 年毎
        else:
            data = self.yeardata(group, year, percent).T.tolist()
            x_labels = [str(i+1)+'月' for i in range(12)]

        # attrs = self.labels[group]
        labels = list(self.tag_dict[group].values())
        if len(labels) != len(data):
            labels.append('不明')
        
        datasets = [0, 0]
        datasets[0] = {'labels': x_labels}
        datasets[1] = {'datasets': [{'label': labels[i], 'data': data[i]} for i in range(len(data))]}

        return datasets