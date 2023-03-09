from django.db import models
'''
csvファイルをデータベースに保存するモデル.
変更するたびに以下を実行.
>> python manage.py makemigrations
>> python manage.py migrate
'''
class UserSettings(models.Model):
    ''''''
    # 全カラム
    all_columns = models.TextField(max_length=500)
    # 流入経路カラム
    platform_columns = models.BinaryField(max_length=300)
    # 顧客属性カラム
    customer_columns = models.BinaryField(max_length=300)
    # リッチメニューカラム
    survey_columns = models.BinaryField(max_length=300)
    # 配信カラム
    menu_columns = models.BinaryField(max_length=300)
    # コンバージョンカラム
    conversion_columns = models.BinaryField(max_length=300)
    # csvファイル
    content = models.BinaryField()
