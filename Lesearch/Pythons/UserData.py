from datetime import datetime as dtime

class UserData:
    '''LINE登録者データ保存用のクラス.'''
    def __init__(self, id, name, time, data):
        self.id = id        # ID
        self.name = name    # 表示名
        # timeは"2021/12/29 10:18"のフォーマットのstrなので、datetimeに変換する
        self.time = dtime.strptime(time, '%Y/%m/%d %H:%M')  # 登録(フォロー)日時
        self.data = data    # その他のユーザーデータ(辞書型)

        self.year = self.time.year      # 登録(フォロー)年
        self.month = self.time.month    # 登録(フォロー)月
        self.day = self.time.day        # 登録(フォロー)日

    def add_data(self, key, value):
        '''データを追加する.'''
        self.data[key] = value