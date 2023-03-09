//------------------ グローバル変数 ------------------//
// タブボタンname
const YEAR_BTN = 'year-btn'                 // 通年
const MONTH_BTN = 'month-btn'               // 月毎
const DISP_UNIT_BTN = 'disp-unit-btn'       // 表示単位
const DAY_SELECT_BTN = 'select-day-btn'     // 基準曜日選択
const DENOM_BTN = 'denominator-btn'         // 分母
const DISP_FORM_BTN = 'disp-format-btn'     // 表示形式
const ATTR_BTN = 'group-btn'                // 属性種類
const BTN_LIST = [YEAR_BTN, MONTH_BTN, DISP_UNIT_BTN, DAY_SELECT_BTN, DENOM_BTN, DISP_FORM_BTN, ATTR_BTN]
// チャートID
const CHART_ID = 'myChart1'
// 基本情報
const BASIC_TABLE = 'basic-table'
//-------------------------------------------------//

// 最初の通年グラフを表示する
const year = document.getElementsByName(YEAR_BTN)[0].value
const attr_btn = document.getElementsByName(ATTR_BTN)[0].value
console.log(attr_btn)
const json_id = year + '_' + attr_btn
console.log(json_id)
plotChart(CHART_ID, 'line', json_id)
// 最初の基本情報を表示する

// クリックイベント追加
BTN_LIST.forEach(addClickEvent)

/*--------------------------------------------------------------------
クリックイベントを追加する関数
--------------------------------------------------------------------*/
function addClickEvent(btn_name){
    document.addEventListener('DOMContentLoaded', function(){
        const btn = document.getElementsByName(btn_name)
        for (let i=0; i<btn.length; i++){
            // 最初のボタンをクリックされた状態にする
            if (i == 0){
                btn[i].checked = true;
                console.log(btn[i].id + ' clicked')
            }
            else{
                btn[i].checked = false;
            }
            // クリックイベント追加をする
            btn[i].addEventListener('click', function(){
                // チェックされているボタンのidを取得する
                const year_btn = getCheckedBtn(YEAR_BTN)
                const month_btn = getCheckedBtn(MONTH_BTN)
                const disp_unit_btn = getCheckedBtn(DISP_UNIT_BTN)
                const select_day_btn = getCheckedBtn(DAY_SELECT_BTN)
                const denom_btn = getCheckedBtn(DENOM_BTN)
                const disp_form_btn = getCheckedBtn(DISP_FORM_BTN)
                const attr_btn = getCheckedBtn(ATTR_BTN)

                console.log('年 [id, value]: ' + year_btn)
                console.log('月 [id, value]: ' + month_btn)
                console.log('単位 [id, value]: ' + disp_unit_btn)
                console.log('曜日 [id, value]: ' + select_day_btn)
                console.log('分母 [id, value]: ' + denom_btn)
                console.log('フォーマット [id, value]: ' + disp_form_btn)
                console.log('属性: [id, value]: ' + attr_btn)

                // json id 作成
                // 通年
                if (month_btn[1]=='0'){
                    var json_id = year_btn[1] + '_' + attr_btn[1]
                }
                // 月毎
                else{
                    var json_id = year_btn[1] + '_' + month_btn[1]
                    // 週毎
                    if (disp_unit_btn[1]=='weekly'){
                        json_id += '_' + select_day_btn[1]
                    }
                    json_id += '_' + attr_btn[1]
                }
                
                // %表示
                if (disp_form_btn[1]=='ratio'){
                    json_id += '_ratio'
                }
                console.log('chart id: ' + json_id)

                // グラフ関数を呼ぶ
                /*
                今のところ分母のボタンを押してもグラフ表示なし
                */
                if (btn_name==DENOM_BTN){
                    console.log(btn_name, ' not yet buit.')
                }
                else{
                    plotChart(CHART_ID, 'line', json_id)
                    
                }
                console.log('\n')
            })
        }
    })
}


/*--------------------------------------------------------------------
どのタブが選択されているかを確認する関数
引数：ボタンタグname
戻り値：ボタンタグid, ボタンタグvalue, 
--------------------------------------------------------------------*/
function getCheckedBtn(btn_name){
    var btn_array = []  // [id, value]
    const btn = document.getElementsByName(btn_name)
    for (let i=0; i<btn.length; i++){
        if (btn[i].checked==true){
            btn_array[0] = btn[i].id
            btn_array[1] = btn[i].value
        }
    }
    return btn_array
}

/*--------------------------------------------------------------------
グラフをプロットする関数
--------------------------------------------------------------------*/
function plotChart(chart_id, chart_type, json_id){
    // pythonから送られるjsonデータをjson_idによって取得する
    const data_from_python = JSON.parse(document.getElementById(json_id).textContent);
    const labels = data_from_python[0].labels       // ラベル
    const datasets = data_from_python[1].datasets   // データセット

    console.log(datasets)

    var ctx = document.getElementById(chart_id);    // canvas contex
    // チャートが存在するなら削除する
    if (window.myChart != undefined) {
        window.myChart.destroy();
    }
    // チャート作成
    window.myChart = new Chart(ctx, {
        type: chart_type,
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: {
            scales: {
            y: {
                beginAtZero: true
            }
            }
        }
    });
}