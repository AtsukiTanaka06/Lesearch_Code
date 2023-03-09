from .Calendar import MyCalendar
from .Stats import StatMixin
from .helper_functions import get_attribute, get_labels

class MySurvey(MyCalendar, StatMixin):
    '''アンケート回答ページ用のクラス'''
    
    def __init__(self, users, tag):
        super().__init__(users=users)

        self.tag_dict = tag # タグの辞書


class MySurvey1(MyCalendar, StatMixin):
    '''アンケート回答ページ用のクラス'''
    
    def __init__(self, users, header):
        super().__init__(users=users)

        self.groups = ['自己分析シート']  # カラム設定グループ名
        # カラム設定質問タグ
        questions = ['4.僕を知ったのはいつですか？', 
                     '6.今ダイエットがなかなかうまく行っていない原因はどんなことだと思いますか？',
                     '8.どういった環境があればダイエットで結果が出せそうですか？',
                     '9.今までどんなダイエットをしましたか？',
                     '10.リバウンドの経験はありますか？',
                     ]

        self.attrs = get_attribute(header, self.groups) # カラム設定属性
        answers = get_attribute(header, questions) # カラム設定属性
        self.attrs.update(answers)  # アップデート

        self.labels = get_labels(header, self.groups)    # グラフ用ラベル
        answer_labels = get_labels(header, questions)    # グラフ用ラベル
        self.labels.update(answer_labels)   # アップデート

        self.other_label = None # グラフ用ラベル（未回答の場合

    def yeardata_array(self, year, attributes, calendar=False):
        '''通年の配列データを返す.'''
        # 通年データ格納配列(その他用にattributesの数+１)
        n = len(attributes)
        data_array = self.year_array(year, n, calendar=calendar)

        # ユーザデータなしならそのまま返す
        if not year in self.year_list:
            return data_array

        # 通年のユーザデータ
        users = self.get_yeardata(year)

        col = calendar * 2
        for user in self.get_yeardata(year):
            for i, attr in enumerate(attributes):
                data_array[user.month-1, col:][i] += int(user.data[attr])

        return data_array

    def monthdata_array(self, year, month, attributes, calendar=False, weekdays=True):
        '''月毎の配列データを返す.'''
        
        n = len(attributes)
        # 通年データ格納配列(その他用にattributesの数+１)
        data_array = self.month_array(year, month, n, calendar=calendar, weekdays=weekdays)

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
            for i, attr in enumerate(attributes):
                data_array[user.day-1, col:][i] += int(user.data[attr])

        return data_array