# Pythonモジュール
import csv, io, base64

# データベースクラス
import sys
sys.path.append("../")
from Top.models import UserSettings

from .UserData import UserData
'''
カラム設定csvファイル用のpythonファイル
'''

def handle_uploaded_file(file):
    # ファイルをバイナリデータに変換
    byte_data = base64.b64encode(file.read())
    '''
    何かしらの暗号処理
    '''
    # データベースモデルに保存
    obj = UserSettings(content=byte_data)
    obj.save()


def csv_to_userdata():
    '''
    バイナリデータのcsvファイルをデータベースから受け取って、ユーザークラスに格納.
    '''
    # データベースから取り出す
    q = UserSettings.objects.first()
    # バイナリデータをUTF−８でデコード
    csv_file = base64.b64decode(q.content)
    csv_file = csv_file.decode('utf-8')

    # csvの読み込み
    csvreader = csv.reader(io.StringIO(csv_file))

    # カラムヘッダーのリスト
    header = next(csvreader)

    # ユーザー情報を辞書型（キーはヘッダー）にしてリストに格納
    data_list = [dict(zip(header, row) )for row in csvreader]
    # ユーザークラスにユーザー情報を登録して、リストに格納
    user_lst = []
    for data in data_list:
        user = UserData(id=data.pop('ID'),
                        name=data.pop('表示名'),
                        time=data.pop('登録(フォロー)日時'),
                        data=data)
        user_lst.append(user)

    return header, user_lst

'''
# データベースに登録
q.all_columns = ', '.join(header)
q.save()
'''