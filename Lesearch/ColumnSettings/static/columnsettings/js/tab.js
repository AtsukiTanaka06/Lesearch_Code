TAB_NAME = 'setting-column-btn'
GROUP_NAME = 'group-name'
GROUP_NAME_INPUT = 'group-setting-input'

SUB_TAB_NAME = 'setting-column-sub-btn'
MAIN_TAG_NAME1 = 'tag-name-main-main-1'
MAIN_TAG_NAME2 = 'tag-name-main-main-2'
MAIN_TAG_NAME3 = 'tag-name-main-main-3'
MAIN_TAG_NAME4 = 'tag-name-main-main-4'
MAIN_TAG_NAME5 = 'tag-name-main-main-5'

SET_TAG_NAME1 = 'set-tag-name-main-1'
SET_TAG_NAME2 = 'set-tag-name-main-2'
SET_TAG_NAME3 = 'set-tag-name-main-3'
SET_TAG_NAME4 = 'set-tag-name-main-4'
SET_TAG_NAME5 = 'set-tag-name-main-5'

// 最初に表示するカラム設定タブ
const col_name = document.currentScript.dataset.colname;
click_btns(col_name)
changeMainTabText(col_name)
//input = document.getElementById(MAIN_TAG_NAME1)
//input.value = '流入経路'
//input.readOnly = true;

// 設定済みカラムの表示
setTagInit()
const set_tag = JSON.parse(document.getElementById(get_btn_num(col_name)+1).textContent);
for (var i=0; i<set_tag.length; i++){
    tag_list = set_tag[i].tag
    label_list = set_tag[i].label
    
    var tag_id = 'set-tag-name-main-' + (i+1)
    var disp_id = 'display-name-main-' + (i+1)
    
    var tag_inputs = document.getElementsByName(tag_id)
    var disp_inputs = document.getElementsByName(disp_id)

    for(var j=0; j<tag_list.length; j++){
        tag_inputs[j].placeholder = tag_list[j]
        tag_inputs[j].value = tag_list[j]
        disp_inputs[j].placeholder = label_list[j]
        disp_inputs[j].value = label_list[j]
    }
}

// クリックイベント追加
addClickEvent(TAB_NAME)
addClickSubTubEvent(SUB_TAB_NAME)


/*--------------------------------------------------------------------
タブの番号を返す関数
--------------------------------------------------------------------*/
function get_btn_num(btn_name){
    var num;
    switch(btn_name) {
        case "platform":
            num = 0;
            break;
        case "customer":
            num = 1;
            break;
        case "survey":
            num = 2;
            break;
        case "menu":
            num = 3;
            break;
        case "channel":
            num = 4;
            break;
        case "conversion":
            num = 5;
            break;
        default:
            num = 0;
    }
    return num
}

/*--------------------------------------------------------------------
タブのidを指定してそのタブをクリックする関数
--------------------------------------------------------------------*/
function click_btns(btn_name){
    const btn = document.getElementsByName(TAB_NAME)
    const btn_num = get_btn_num(btn_name)

    for (let i=0; i<btn.length; i++){
        if (i == btn_num){
            btn[i].checked = true;
        }
        else{
            btn[i].checked = false;
        }
    }
}

/*--------------------------------------------------------------------
クリックイベントを追加する関数
--------------------------------------------------------------------*/
function addClickEvent(btn_name){
    document.addEventListener('DOMContentLoaded', function(){
        const btn = document.getElementsByName(btn_name)
        for (let i=0; i<btn.length; i++){
            // クリックイベント追加をする
            btn[i].addEventListener('click', function(){
                group =  btn[i].id
                changeText(group)
                changeMainTabText(group)
                set_tag_name(group)
            
                // tab_id = TAB_ID + btn[i].id;
                // display_contents(tab_id);

            })
        }
    })
}

// テキスト内容を変更する関数
function changeText(new_text){
    console.log(new_text)

    var group;
    switch(new_text) {
        case "platform":
            group = "流入経路";
            break;
        case "customer":
            group = "顧客属性";
            break;
        case "survey":
            group = "アンケート回答";
            break;
        case "menu":
            group = "リッチメニュー";
            break;
        case "channel":
            group = "配信";
            break;
        case "conversion":
            group = "コンバージョン";
            break;
        default:
            group = "流入経路";
    }
    // 表示テキスト変更
    document.getElementById(GROUP_NAME).textContent = group + 'のカラム設定'
    // POST内容変更
    element = document.getElementById(GROUP_NAME_INPUT)
    element.setAttribute('value', new_text)
}

// メインタグ名を変更する関数
function changeMainTabText(group){
    var input1 = document.getElementById(MAIN_TAG_NAME1);
    var input2 = document.getElementById(MAIN_TAG_NAME2);
    var input3 = document.getElementById(MAIN_TAG_NAME3);
    var input4 = document.getElementById(MAIN_TAG_NAME4);
    var input5 = document.getElementById(MAIN_TAG_NAME5);

    input1.value = "";
    input2.value = "";
    input3.value = "";
    input4.value = "";
    input5.value = "";
    input1.placeholder = "メインのタグ名1を入力してください";
    input2.placeholder = "メインのタグ名2を入力してください";
    input3.placeholder = "メインのタグ名3を入力してください";
    input4.placeholder = "メインのタグ名4を入力してください";
    input5.placeholder = "メインのタグ名5を入力してください";
    input1.readOnly = false;
    input2.readOnly = false;
    input3.readOnly = false;
    input4.readOnly = false;
    input5.readOnly = false;
    
    switch(group) {
        case "platform":
            input1.value = "流入経路";
            input1.readOnly = true;
            break;
        case "customer":
            input1.value = "性別";
            input2.value = "年代";
            input3.value = "職業";
            input4.value = "都道府県";
            input1.readOnly = true;
            input2.readOnly = true;
            input3.readOnly = true;
            input4.readOnly = true;
            break;
        case "survey":
            input1.placeholder = "アンケート名１を入力してください";
            input2.placeholder = "アンケート名２を入力してください";
            input3.placeholder = "アンケート名３を入力してください";
            input4.placeholder = "アンケート名４を入力してください";
            input5.placeholder = "アンケート名５を入力してください";
            break;
        case "menu":
            break;
        case "channel":
            input1.placeholder = "配信シナリオ名１を入力してください";
            input2.placeholder = "配信シナリオ名２を入力してください";
            input3.placeholder = "配信シナリオ名３を入力してください";
            input4.placeholder = "配信シナリオ名４を入力してください";
            input5.placeholder = "配信シナリオ名５を入力してください";
            break;
        case "conversion":
            input1.placeholder = "コンバージョン名１を入力してください";
            input2.placeholder = "コンバージョン名２を入力してください";
            input3.placeholder = "コンバージョン名３を入力してください";
            input4.placeholder = "コンバージョン名４を入力してください";
            input5.placeholder = "コンバージョン名５を入力してください";
        default:
            input1.placeholder = "メインのタグ名1を入力してください";
            input2.placeholder = "メインのタグ名2を入力してください";
            input3.placeholder = "メインのタグ名3を入力してください";
            input4.placeholder = "メインのタグ名4を入力してください";
            input5.placeholder = "メインのタグ名5を入力してください";
    }
}

// 設定済みカラムを表示する関数
function set_tag_name(group){
    setTagInit()
    const set_tag_plat = JSON.parse(document.getElementById('1').textContent);
    const set_tag_cust = JSON.parse(document.getElementById('2').textContent);
    const set_tag_surv = JSON.parse(document.getElementById('3').textContent);
    const set_tag_menu = JSON.parse(document.getElementById('4').textContent);
    const set_tag_chan = JSON.parse(document.getElementById('5').textContent);
    const set_tag_conv = JSON.parse(document.getElementById('6').textContent);

    var tag
    switch(group) {
        case "platform":
            tag = set_tag_plat
            break;
        case "customer":
            tag = set_tag_cust
            break;
        case "survey":
            tag = set_tag_surv
            break;
        case "menu":
            tag = set_tag_menu
            break;
        case "channel":
            tag = set_tag_chan
            break;
        case "conversion":
            tag = set_tag_conv
            break;
        default:
            group = "流入経路";
    }

    for (var i=0; i<tag.length; i++){
        tag_list = tag[i].tag
        label_list = tag[i].label
        var tag_id = 'set-tag-name-main-' + (i+1)
        var disp_id = 'display-name-main-' + (i+1)
        var tag_inputs = document.getElementsByName(tag_id)
        var disp_inputs = document.getElementsByName(disp_id)
        for(var j=0; j<tag_list.length; j++){
            tag_inputs[j].placeholder = tag_list[j]
            tag_inputs[j].value = tag_list[j]
            disp_inputs[j].placeholder = label_list[j]
            disp_inputs[j].value = label_list[j]
        }
    }
}

// 設定済みタグ名を初期化する関数
function setTagInit(){
    var main_tag = document.getElementsByName('setting-column-sub-btn')
    for(var i=0; i<main_tag.length; i++){
        var tag_name = 'set-tag-name-main-' + (i+1)
        var disp_name = 'display-name-main-' + (i+1)
        var tag_inputs = document.getElementsByName(tag_name)
        var disp_inputs = document.getElementsByName(disp_name)

        for(var j=0; j<tag_inputs.length; j++){
            tag_inputs[j].placeholder = '設定済みのタグを表示します'
            tag_inputs[j].value = ''
            disp_inputs[j].placeholder = 'グラフでの表示名を入力してください'
            disp_inputs[j].value = ''
        }
    }
}

/*--------------------------------------------------------------------
クリックイベントを追加する関数
--------------------------------------------------------------------*/
function addClickSubTubEvent(btn_name){
    document.addEventListener('DOMContentLoaded', function(){
        const btn = document.getElementsByName(btn_name);
        for (let i=0; i<btn.length; i++){
            // クリックイベント追加をする
            btn[i].addEventListener('click', function(){
                group =  btn[i].id
            })
            if (i == 0){
                btn[0].checked = true;
            }
        }
    })

    //先頭のタブボタンをcheckedにする（初期値）
    // btn[0].checked = true;
}

/*--------------------------------------------------------------------
カラム追加用ボタン
目的：追加ボタンでカラム設定できる項目を追加するため
--------------------------------------------------------------------*/
function AddColumn(data_table_key){    

    var table = document.getElementById(data_table_key);
    //追加先のdataTableのうち、tbodyを取得する（カラム設定を追加する場所）
    var table_tbody = document.getElementById(data_table_key).children[1];
    console.log(table_tbody);

    var tr = document.createElement("tr");

    //セル1：表示非表示を制御するラジオボタンの追加
    //セル1の<td>タグ生成
    var cell_1 = document.createElement("td");
     //セル1の<td>タグ下の<labe
    var label_checkbox = document.createElement("label");

    if ($(".js-switch")[0]) {
        var elems = Array.prototype.slice.call(table.getElementsByClassName("js-switch"));
        var cloneElems = elems[0].cloneNode(true);
        var value = elems[elems.length - 1].getAttribute('value'); //既存で表示されている最後の要素
        var splitVale = String(value).split('-');

        cloneElems.setAttribute("id","checkbox" + "-" + splitVale[0] + "-" + splitVale[1] + "-" + (Number(splitVale[2]) + 1));
        cloneElems.setAttribute("value", splitVale[0] + "-" + splitVale[1] + "-" + (Number(splitVale[2]) + 1));
    }

    label_checkbox.appendChild(cloneElems);
    cell_1.appendChild(label_checkbox);
    tr.appendChild(cell_1);
    table_tbody.appendChild(tr);

    //CSSの当てなおし
    var elems = Array.prototype.slice.call(table.getElementsByClassName("js-switch"));
    console.log(elems);
    var switchery = new Switchery(elems[elems.length-1], {
        color: '#26B99A'
    });

    //セル2：タグの設定用プルダウンの項目追加
    var elems2 = Array.prototype.slice.call(table.getElementsByClassName("select_search"));
    var cloneElems2 = elems2[0].cloneNode(true);

    var cell_2 = document.createElement("td");
    cell_2.appendChild(cloneElems2);
    tr.appendChild(cell_2);
    table_tbody.appendChild(tr);

    $('.select_search').select2({
        language: "ja", //日本語化のためのオプション,
        width: 'auto',
     });

     //セル3：設定済みのタグ名表示用テキスト追加
    var elems3 = Array.prototype.slice.call(table.getElementsByClassName("set_tag"));
    var cloneElems3 = elems3[0].cloneNode(true);

    var cell_3 = document.createElement("td");
    cell_3.appendChild(cloneElems3);
    tr.appendChild(cell_3);
    table_tbody.appendChild(tr);

    //セル4：グラフ表示用のテキスト追加
    var elems4 = Array.prototype.slice.call(table.getElementsByClassName("dip_tag"));
    var cloneElems4 = elems4[0].cloneNode(true);

    var cell_4 = document.createElement("td");
    cell_4.appendChild(cloneElems4);
    tr.appendChild(cell_4);
    table_tbody.appendChild(tr);

    //testComment
}