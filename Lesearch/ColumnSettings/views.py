# Djangoモジュール
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from ColumnSettings.models import ColumnSettings

import sys, json, base64
sys.path.append('../')
from Pythons.file import csv_to_userdata

# Create your views here.
def columns(request):
    template = loader.get_template('columns.html')

    context = {}
    context['first_col_name'] = 'platform'
    context['tag_names'] = {'platform': '流入経路', 
                            'customer': '顧客属性', 
                            'survey': 'アンケート回答', 
                            'menu': 'リッチメニュー', 
                            'channel': '配信', 
                            'conversion': 'コンバージョン'}
    # メインタグの数
    main_tag = {'main-1': 1, 'main-2': 2, 'main-3': 3, 'main-4': 4, 'main-5': 5}
    context['main_tags'] = main_tag

    # カラム名のリストを取得
    header, _ = csv_to_userdata()
    context['columns'] = sorted(header, reverse=True)

    # POST
    if request.method=='POST':
        col_name, tags = column_setting(request.POST, main_tag)
        context['first_col_name'] = col_name
        context['tag_setting'] = tags
        print(col_name)

        # Save in Database
        save_database(col_name, tags)


    # 設定済みカラム取得
    context['customer_tag'] = tag_list(get_column_tags('customer'))
    context['platform_tag'] = tag_list(get_column_tags('platform'))
    context['survey_tag'] = tag_list(get_column_tags('survey'))
    context['menu_tag'] = tag_list(get_column_tags('menu'))
    context['channel_tag'] = tag_list(get_column_tags('channel'))
    context['conversion_tag'] = tag_list(get_column_tags('conversion'))

    return HttpResponse(template.render(context, request))

def tag_list(tag_dict):
    tag_list = []
    if tag_dict:
        for key in tag_dict.keys():
            set_tag = {}
            set_tag['tag'] = list(tag_dict[key])
            set_tag['label'] = list(tag_dict[key].values())
            tag_list.append(set_tag)
    return tag_list

# POSTされたカラム設定の取得
def column_setting(post_data, main_tag):
    group_name = post_data['group-setting-input']
    tag_name_main = post_data.getlist('tag-name-main')
    tag_main_num = len(tag_name_main)
    print(tag_name_main)

    checkbox_list = []
    tag_name_list = []
    set_tag_name_list = []
    display_name_list = []

    for i in range(1, tag_main_num+1):
        checkbox_name = 'checkbox-main-' + str(i)
        tag_name = 'tag-name-main-' + str(i)
        set_tag_name = 'set-tag-name-main-' + str(i)
        display_name = 'display-name-main-' + str(i)

        checkbox_list.append(post_data.getlist(checkbox_name))
        tag_name_list.append(post_data.getlist(tag_name))
        set_tag_name_list.append(post_data.getlist(set_tag_name))
        display_name_list.append(post_data.getlist(display_name))
    '''
    print(checkbox_list)
    print(tag_name_list)
    print(set_tag_name_list)
    print(display_name_list)'''

    tags = {}
    for i, main in enumerate(tag_name_main):
        tag_names = tag_name_list[i]
        set_names = set_tag_name_list[i]
        dis_names = display_name_list[i]
        temp = {}
        for str_i in checkbox_list[i]:
            j = int(str_i) - 1

            if tag_names[j] != 'none':
                t_name = tag_names[j]
                if dis_names[j]:
                    label = dis_names[j]
                else:
                    label = 'ラベルなし'
                temp[t_name] = label
            elif set_names[j]:
                t_name = set_names[j]
                if dis_names[j]:
                    label = dis_names[j]
                else:
                    label = 'ラベルなし'
                temp[t_name] = label
        if main:
            tags[main] = temp
    print(tags)

    return group_name, tags

# 辞書をバイナリに変換
def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary_txt = ' '.join(format(ord(letter), 'b') for letter in str)
    binary = bytes(binary_txt, 'utf-8')
    return binary

# カラム設定のバイナリデータをデータベースに保存
def save_database(group, tag_name_dict):
    # カラム設定タグをテキストに変換、','で分ける
    bin_data = dict_to_binary(tag_name_dict)
    
    #--------------------------------------------------------------------------
    #　ユーザー紐付け処理 追記
    try :
        col = ColumnSettings.objects.all()[0]
    except:
        col = ColumnSettings(title='test')
    #--------------------------------------------------------------------------

    if group=='platform':
        col.platform = bin_data
    elif group=='customer':
        col.customer = bin_data
    elif group=='survey':
        col.survey = bin_data
    elif group=='menu':
        col.menu = bin_data
    elif group=='channel':
        col.channel = bin_data
    elif group=='conversion':
        col.conversion = bin_data
    else:
        pass

    col.save()

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
        tags = bin_data

    return tags