# Djangoモジュール
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from ColumnSettings.models import ColumnSettings

import sys, json
sys.path.append('../')
from Pythons.file import csv_to_userdata
from Pythons.Friend import MyFriend
from Pythons.Platforms import MyPlatform
from Pythons.Customer import MyCustomer
from Pythons.Survey import MySurvey
from Pythons.Conversions import MyConversion
from Pythons.Channels import MyChannel
from Pythons.Menus import MyMenus

global DAY_LIST 
DAY_LIST = [{'mon': '月', 'tue': '火', 'wed': '水', 'thu': '木'},
            {'fri': '金', 'sat': '土', 'sun': '日'}]

global WEEKS 
WEEKS = ['sunday','monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

#-----------------------------#
########## 友達登録数 ##########
#-----------------------------#
def friends(request):
    template = loader.get_template('friends.html')
    context = {'name': '友達登録数'}

    # カラム名のユーザデータリストを取得
    _, user_list = csv_to_userdata()
    friend = MyFriend(users=user_list)

    # 通年のリスト
    year_list = friend.years_list()
    context['year_list'] = year_list

    # 月
    context['day_list'] = DAY_LIST
 
    # Year data
    context['year_data'] = get_year_datasets(friend, year_list)
    # Month data
    context['month_data'] = get_month_datasets(friend, year_list)
    # Weekly data
    context['weekly_data'] = get_weekly_datasets(friend, year_list)

    return HttpResponse(template.render(context, request))

#-----------------------------#
#---------- 流通経路 ----------#
#-----------------------------#
def platforms(request):
    template = loader.get_template('platforms.html')
    context = {'name': '流入経路'}

    # タグを取得
    tag_names = get_column_tags('platform')
    print(tag_names)

    # タグのグループ名取得
    keys = tag_names.keys()
    groups = dict(zip(range(len(keys)), keys))
    context['groups'] = groups
    print(groups)

    # カラム名のユーザデータリストを取得
    _, user_list = csv_to_userdata()
    plat = MyPlatform(users=user_list, tag=tag_names)

    # 通年のリスト
    year_list = plat.years_list()
    context['year_list'] = year_list

    # 月
    context['day_list'] = DAY_LIST

    # Year data
    context['year_data'] = get_year_datasets(plat, year_list, groups=groups)
    # Month data
    context['month_data'] = get_month_datasets(plat, year_list, groups=groups)

    # Weekly data
    data = {}
    for year in year_list:
            for month in range(1, 13):
                for week in WEEKS:
                    for key, g in groups.items():
                        data[f'{year}_{month}_{week[:3]}_{key}'] = plat.datasets(group=g, year=year, month=month, week=True, firstweekday=week)
                        data[f'{year}_{month}_{week[:3]}_{key}_ratio'] = plat.datasets(group=g, year=year, month=month, week=True, firstweekday=week, percent=True)
    context['weekly_data'] = data

    return HttpResponse(template.render(context, request))

#-----------------------------#
#---------- 顧客属性 ----------#
#-----------------------------#
def customers(request):
    global DAY_LIST

    template = loader.get_template('customers.html')
    context = {'name': '顧客属性'}

    # タグを取得
    tag_names = get_column_tags('customer')
    print(tag_names)

    # タグのグループ名取得
    keys = tag_names.keys()
    groups = dict(zip(range(len(keys)), keys))
    context['groups'] = groups
    print(groups)

    # カラム名のユーザデータリストを取得
    header, user_list = csv_to_userdata()
    customer = MyCustomer(users=user_list, tag=tag_names)

    # 通年のリスト
    year_list = customer.years_list()
    context['year_list'] = year_list

    # 月
    context['day_list'] = DAY_LIST

    # Year data
    # context['year_data'] = get_year_datasets(customer, year_list, groups=groups)
    # Month data
    # context['month_data'] = get_month_datasets(customer, year_list, groups=groups)

    # 通年データ
    year_data = {}
    for year in year_list:
        for key, group in groups.items():
            if group=='都道府県':
                year_data[f'{year}_{key}'] = customer.prefec_datasets(year)
                year_data[f'{year}_{key}_ratio'] = customer.prefec_datasets(year)
            else:
                year_data[f'{year}_{key}'] = customer.datasets(group=group, year=year)
                year_data[f'{year}_{key}_ratio'] = customer.datasets(group=group, year=year, percent=True)
    context['year_data'] = year_data

    # 月毎のデータ
    month_data = {}
    for year in year_list:
        for month in range(1, 13):
            for key, group in groups.items():
                if group=='都道府県':
                    month_data[f'{year}_{month}_{key}'] = customer.prefec_datasets(year, month=month)
                    month_data[f'{year}_{month}_{key}_ratio'] = customer.prefec_datasets(year, month=month)
                else:
                    month_data[f'{year}_{month}_{key}'] = customer.datasets(group=group, year=year, month=month)
                    month_data[f'{year}_{month}_{key}_ratio'] = customer.datasets(group=group, year=year, month=month, percent=True)
    context['month_data'] = month_data

    # Weekly data
    data = {}
    for year in year_list:
            for month in range(1, 13):
                for week in WEEKS:
                    for key, group in groups.items():
                        if group=='都道府県':
                            data[f'{year}_{month}_{week[:3]}_{key}'] = customer.prefec_datasets(year, month=month, week=True, firstweekday=week)
                            data[f'{year}_{month}_{week[:3]}_{key}_ratio'] = customer.prefec_datasets(year, month=month, week=True, firstweekday=week, percent=True)
                        else:
                            data[f'{year}_{month}_{week[:3]}_{key}'] = customer.datasets(group=group, year=year, month=month, week=True, firstweekday=week)
                            data[f'{year}_{month}_{week[:3]}_{key}_ratio'] = customer.datasets(group=group, year=year, month=month, week=True, firstweekday=week, percent=True)
    context['weekly_data'] = data

    return HttpResponse(template.render(context, request))

#-----------------------------#
########## アンケート回答 ##########
#-----------------------------#
def surveys(request):
    global DAY_LIST

    template = loader.get_template('surveys.html')
    context = {'name': 'アンケート回答'}

    # タグを取得
    tag_names = get_column_tags('survey')
    print(tag_names)

    # タグのグループ名取得
    keys = tag_names.keys()
    groups = dict(zip(range(len(keys)), keys))
    context['groups'] = groups
    print(groups)

    # カラム名のユーザデータリストを取得
    header, user_list = csv_to_userdata()
    survey = MySurvey(users=user_list, tag=tag_names)

    # 通年のリスト
    year_list = survey.years_list()
    context['year_list'] = year_list

    # 月
    context['day_list'] = DAY_LIST

    # Year data
    # context['year_data'] = get_year_datasets(survey, year_list, groups=groups)
    # Month data
    # context['month_data'] = get_month_datasets(survey, year_list, groups=groups)

    # 通年データ
    year_data = {}
    for year in year_list:
        for key, group in groups.items():
            year_data[f'{year}_{key}'] = survey.datasets(group=group, year=year)
            year_data[f'{year}_{key}_ratio'] = survey.datasets(group=group, year=year, percent=True)
    context['year_data'] = year_data

    # 月毎のデータ
    month_data = {}
    for year in year_list:
        for month in range(1, 13):
            for key, group in groups.items():
                month_data[f'{year}_{month}_{key}'] = survey.datasets(group=group, year=year, month=month)
                month_data[f'{year}_{month}_{key}_ratio'] = survey.datasets(group=group, year=year, month=month, percent=True)
    context['month_data'] = month_data

    # Weekly data
    data = {}
    for year in year_list:
            for month in range(1, 13):
                for week in WEEKS:
                    for key, group in groups.items():
                        data[f'{year}_{month}_{week[:3]}_{key}'] = survey.datasets(group=group, year=year, month=month, week=True, firstweekday=week)
                        data[f'{year}_{month}_{week[:3]}_{key}_ratio'] = survey.datasets(group=group, year=year, month=month, week=True, firstweekday=week, percent=True)
    context['weekly_data'] = data

    return HttpResponse(template.render(context, request))

#-----------------------------#
########## リッチメニュー ##########
#-----------------------------#
def menus(request):
    global DAY_LIST

    template = loader.get_template('menus.html')
    context = {'name': 'リッチメニュー'}

    # タグを取得
    tag_names = get_column_tags('menu')
    print(tag_names)

    # タグのグループ名取得
    keys = tag_names.keys()
    groups = dict(zip(range(len(keys)), keys))
    context['groups'] = groups
    print(groups)

    # カラム名のユーザデータリストを取得
    header, user_list = csv_to_userdata()
    menu = MyMenus(users=user_list, tag=tag_names)

    # 通年のリスト
    year_list = menu.years_list()
    context['year_list'] = year_list

    # 月
    context['day_list'] = DAY_LIST

        # 通年データ
    year_data = {}
    for year in year_list:
        for key, group in groups.items():
            year_data[f'{year}_{key}'] = menu.datasets(group=group, year=year)
            year_data[f'{year}_{key}_ratio'] = menu.datasets(group=group, year=year, percent=True)
    context['year_data'] = year_data

    # 月毎のデータ
    month_data = {}
    for year in year_list:
        for month in range(1, 13):
            for key, group in groups.items():
                month_data[f'{year}_{month}_{key}'] = menu.datasets(group=group, year=year, month=month)
                month_data[f'{year}_{month}_{key}_ratio'] = menu.datasets(group=group, year=year, month=month, percent=True)
    context['month_data'] = month_data

    # Weekly data
    data = {}
    for year in year_list:
            for month in range(1, 13):
                for week in WEEKS:
                    for key, group in groups.items():
                        data[f'{year}_{month}_{week[:3]}_{key}'] = menu.datasets(group=group, year=year, month=month, week=True, firstweekday=week)
                        data[f'{year}_{month}_{week[:3]}_{key}_ratio'] = menu.datasets(group=group, year=year, month=month, week=True, firstweekday=week, percent=True)
    context['weekly_data'] = data

    return HttpResponse(template.render(context, request))

#-----------------------------#
########## 配信 ##########
#-----------------------------#
def channels(request):
    global DAY_LIST

    template = loader.get_template('channels.html')
    context = {'name': '配信'}

    # タグを取得
    tag_names = get_column_tags('menu')
    print(tag_names)

    # タグのグループ名取得
    keys = tag_names.keys()
    groups = dict(zip(range(len(keys)), keys))
    context['groups'] = groups
    print(groups)

    # カラム名のユーザデータリストを取得
    header, user_list = csv_to_userdata()
    chan = MyChannel(users=user_list, tag=tag_names)

    # 通年のリスト
    year_list = chan.years_list()
    context['year_list'] = year_list

    # 月
    context['day_list'] = DAY_LIST

    # 通年データ
    year_data = {}
    for year in year_list:
        for key, group in groups.items():
            year_data[f'{year}_{key}'] = chan.datasets(group=group, year=year)
            year_data[f'{year}_{key}_ratio'] = chan.datasets(group=group, year=year, percent=True)
    context['year_data'] = year_data

    # 月毎のデータ
    month_data = {}
    for year in year_list:
        for month in range(1, 13):
            for key, group in groups.items():
                month_data[f'{year}_{month}_{key}'] = chan.datasets(group=group, year=year, month=month)
                month_data[f'{year}_{month}_{key}_ratio'] = chan.datasets(group=group, year=year, month=month, percent=True)
    context['month_data'] = month_data

    # Weekly data
    data = {}
    for year in year_list:
            for month in range(1, 13):
                for week in WEEKS:
                    for key, group in groups.items():
                        data[f'{year}_{month}_{week[:3]}_{key}'] = chan.datasets(group=group, year=year, month=month, week=True, firstweekday=week)
                        data[f'{year}_{month}_{week[:3]}_{key}_ratio'] = chan.datasets(group=group, year=year, month=month, week=True, firstweekday=week, percent=True)
    context['weekly_data'] = data

    return HttpResponse(template.render(context, request))

#-----------------------------#
########## コンバージョン ##########
#-----------------------------#
def conversions(request):
    global DAY_LIST

    template = loader.get_template('conversions.html')
    context = {'name': 'コンバージョン'}

    # タグを取得
    tag_names = get_column_tags('conversion')
    print(tag_names)

    # タグのグループ名取得
    keys = tag_names.keys()
    groups = dict(zip(range(len(keys)), keys))
    context['groups'] = groups
    print(groups)

    # カラム名のユーザデータリストを取得
    header, user_list = csv_to_userdata()
    conv = MyConversion(users=user_list, tag=tag_names)

    # 通年のリスト
    year_list = conv.years_list()
    context['year_list'] = year_list

    # 月
    context['day_list'] = DAY_LIST

    # 通年データ
    year_data = {}
    for year in year_list:
        for key, group in groups.items():
            year_data[f'{year}_{key}'] = conv.datasets(group=group, year=year)
            year_data[f'{year}_{key}_ratio'] = conv.datasets(group=group, year=year, percent=True)
    context['year_data'] = year_data

    # 月毎のデータ
    month_data = {}
    for year in year_list:
        for month in range(1, 13):
            for key, group in groups.items():
                month_data[f'{year}_{month}_{key}'] = conv.datasets(group=group, year=year, month=month)
                month_data[f'{year}_{month}_{key}_ratio'] = conv.datasets(group=group, year=year, month=month, percent=True)
    context['month_data'] = month_data

    # Weekly data
    data = {}
    for year in year_list:
            for month in range(1, 13):
                for week in WEEKS:
                    for key, group in groups.items():
                        data[f'{year}_{month}_{week[:3]}_{key}'] = conv.datasets(group=group, year=year, month=month, week=True, firstweekday=week)
                        data[f'{year}_{month}_{week[:3]}_{key}_ratio'] = conv.datasets(group=group, year=year, month=month, week=True, firstweekday=week, percent=True)
    context['weekly_data'] = data

    return HttpResponse(template.render(context, request))



def test(request):
    global DAY_LIST

    template = loader.get_template('test.html')
    context = {'name': 'テスト'}


    # グループ
    groups = {'sex': '性別', 'age': '年代', 'work': '職業'}
    context['groups'] = groups

    
    return HttpResponse(template.render(context, request))

# バイナリデータを辞書に戻す
def binary_to_dict(the_binary):
    binary_txt = the_binary.decode()
    jsn = ''.join(chr(int(x, 2)) for x in binary_txt.split())
    d = json.loads(jsn)  
    return d

# データベースからカラム設定情報を取り出す
def get_column_tags(group):
    #--------------------------------------------------------------------------
    #　ユーザー紐付け処理 追記
    col = ColumnSettings.objects.all()[0]
    #--------------------------------------------------------------------------
    
    if group=='platform':
        bin_data = col.platform
    elif group=='customer':
        bin_data = col.customer
    elif group=='survey':
        bin_data = col.survey
    elif group=='menu':
        bin_data = col.menu
    elif group=='channel':
        bin_data = col.channel
    elif group=='conversion':
        bin_data = col.conversion
    else:
        bin_data = b'1010'

    if bin_data:
        tags = binary_to_dict(bin_data)
    else:
        tags = {}

    return tags

#
def get_year_datasets(obj, year_list, groups=None):
    year_data = {}
    if groups:
        for year in year_list:
            for key, group in groups.items():
                year_data[f'{year}_{key}'] = obj.datasets(group=group, year=year)
                year_data[f'{year}_{key}_ratio'] = obj.datasets(group=group, year=year, percent=True)
    else:
        for year in year_list:
            year_data[f'{year}'] = obj.datasets(year=year)
            year_data[f'{year}_ratio'] = obj.datasets(year=year, percent=True)

    return year_data
    

def get_month_datasets(obj, year_list, groups=None):
    month_data = {}

    if groups:
        for year in year_list:
            for month in range(1, 13):
                for key, group in groups.items():
                    month_data[f'{year}_{month}_{key}'] = obj.datasets(group=group, year=year, month=month)
                    month_data[f'{year}_{month}_{key}_ratio'] = obj.datasets(group=group, year=year, month=month, percent=True)
    else:
        for year in year_list:
            for month in range(1, 13):
                month_data[f'{year}_{month}'] = obj.datasets(year=year, month=month)
                month_data[f'{year}_{month}_ratio'] = obj.datasets(year=year, month=month, percent=True)
    
    return month_data
    

def get_weekly_datasets(obj, year_list, groups=None):
    global WEEKS

    data = {}
    if groups:
        for year in year_list:
            for month in range(1, 13):
                for key, group in groups.items():
                    data[f'{year}_{month}_{key}'] = obj.datasets(group=group, year=year, month=month)
                    data[f'{year}_{month}_{key}_ratio'] = obj.datasets(group=group, year=year, month=month, percent=True)
    else:
        for year in year_list:
            for month in range(1, 13):
                for week in WEEKS:
                    data[f'{year}_{month}_{week[:3]}'] = obj.datasets(year=year, month=month, weekly=True, firstweekday=week)
                    data[f'{year}_{month}_{week[:3]}_ratio'] = obj.datasets(year=year, month=month, weekly=True, firstweekday=week, percent=True)
    return data