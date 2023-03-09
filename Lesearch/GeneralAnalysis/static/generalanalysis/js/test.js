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

/* Satrt Atsuki Add--*/
// 基本情報
var MyBasicDataTable = null; //描画済みか判断するフラグ
const BASIC_TABLE = 'basic-table';
const BASIC_TABLE_JQuery = $('#basic-table'); //Jquery用id指定

//データ一覧表示用テーブル
var MyDataTable = null; //描画済みか判断するフラグ
const DATA_TABLE = 'datatable'
const DATA_TABLE_JQuery = $('#datatable'); //Jquery用id指定
/* Satrt Atsuki End--*/
//-------------------------------------------------//


// 最初の通年グラフを表示する
const year = document.getElementsByName(YEAR_BTN)[0].value
const attr = document.getElementsByName(ATTR_BTN)[0].value
const json_id = year + '_' + attr
console.log(json_id)
plotChart(CHART_ID, 'line', json_id);
/* Satrt Atsuki Add--*/
// 最初のデータ一覧を表示する
diplayBasicData(json_id);
diplayData(json_id);
/* End Atsuki Add--*/


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

                plotChart(CHART_ID, 'line', json_id)
                /* Satrt Atsuki Add--*/
                diplayBasicData(json_id);  
                diplayData(json_id);   
                /* Satrt Atsuki End--*/
                    
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

/* Satrt Atsuki Add--*/
/*--------------------------------------------------------------------
基本情報を表示する関数
--------------------------------------------------------------------*/
function diplayBasicData(json_id){
    // pythonから送られるjsonデータをjson_idによって取得する
    const data_from_python = JSON.parse(document.getElementById(json_id).textContent);
    const labels = data_from_python[0].labels;       // ラベル
    const datasets = data_from_python[1].datasets;   // データセット

    console.log(datasets);

    //書くラベルごとに合計、平均、最大値、最小値を産出する
    var basicInfoArray = []
    for(var datasets_index = 0; datasets_index < datasets.length;datasets_index++){
       nums = datasets[datasets_index].data;
       const sum = nums.reduce((sum, num) => sum + num, 0);                                    //合計
       const average = Math.round((nums.reduce((a, b) => a + b) / nums.length) * 100) /100;    //平均

       const aryMax = function (a, b) {return Math.max(a, b);}
       const aryMin = function (a, b) {return Math.min(a, b);}
       let max = nums.reduce(aryMax);                                                          //最大値
       let min = nums.reduce(aryMin);                                                          //最小値

       var basicInfo = {label:datasets[datasets_index].label, sum:sum, average:average, max: max, min:min};

       basicInfoArray.push(basicInfo);
    }
    console.log(basicInfoArray);

   //以下表への描画処理
   //描画するデータテーブルID 
   var table = document.getElementById(BASIC_TABLE);

   if (MyBasicDataTable) {
       // 二回目以降の描画の場合、初期化が必要
       MyBasicDataTable.state.clear();
       MyBasicDataTable.destroy();
       BASIC_TABLE_JQuery.empty();
   }
       
   //データ一覧の項目を描画する
   const basicTable_Items = ["項目","合計","平均","最大値","最小値"];
   var table_thead = document.createElement("thead");
   table_thead.innerHTML = "";
   var table_thead_tr = document.createElement("tr");
   for(var basicTable_Items_Index= 0; basicTable_Items_Index < basicTable_Items.length;basicTable_Items_Index++){
       var table_thead_tr_td = document.createElement("td");
       table_thead_tr_td.textContent = basicTable_Items[basicTable_Items_Index];
       table_thead_tr.appendChild(table_thead_tr_td);
   }
   
   table_thead.appendChild(table_thead_tr);

   //データ一覧のデータ部分を描画する
   var table_tbody = document.createElement("tbody");
   table_tbody.innerHTML = "";

   for(var basicInfoArray_Index = 0; basicInfoArray_Index < basicInfoArray.length;basicInfoArray_Index++){
       var table_tbody_tr = document.createElement("tr");

       basicInfo_Keys = Object.keys(basicInfoArray[basicInfoArray_Index]);
       for(basicInfo_Key of basicInfo_Keys){
           var table_tbody_tr_td = document.createElement("td");
           table_tbody_tr_td.textContent = basicInfoArray[basicInfoArray_Index][basicInfo_Key];
           table_tbody_tr.appendChild(table_tbody_tr_td);
           console.log(basicInfoArray[basicInfoArray_Index][basicInfo_Key]);
       }
       table_tbody.appendChild(table_tbody_tr);
   }

   table.appendChild(table_thead);
   table.appendChild(table_tbody);

   console.log(table);

   MyBasicDataTable = BASIC_TABLE_JQuery.DataTable({searching: false,info: false,lengthChange: false});
}
/*--------------------------------------------------------------------
データ一覧を表示する関数
--------------------------------------------------------------------*/
function diplayData(json_id){

   var table = document.getElementById(DATA_TABLE);
   if (MyDataTable) {
       // 二回目以降の描画の場合、初期化が必要
       MyDataTable.state.clear();
       MyDataTable.destroy();
       DATA_TABLE_JQuery.empty();
   }


   // pythonから送られるjsonデータをjson_idによって取得する
   const data_from_python = JSON.parse(document.getElementById(json_id).textContent);
   const labels = data_from_python[0].labels;       // ラベル
   const datasets = data_from_python[1].datasets;   // データセット
   var datasetsLabel = [];
   datasetsLabel.push(" ");
   var datasetsDatas = [];
   
   //データ一覧の項目を抽出する
   for(var datasets_index = 0;datasets_index < datasets.length;datasets_index++){
       datasetsLabel.push(datasets[datasets_index].label);
   }

   //データ一覧のデータ部分を抽出する
   for(var dataIndex = 0; dataIndex < datasets[0].data.length; dataIndex++){
       var datasetsData = [];
       for(var datasets_index = 0;datasets_index < datasets.length;datasets_index++){
           datasetsData.push(datasets[datasets_index].data[dataIndex]);
       }

       datasetsDatas.push(datasetsData);
   }
  
   //データ一覧の項目を描画する
   var table_thead = document.createElement("thead");
   table_thead.innerHTML = "";
   var table_thead_tr = document.createElement("tr");
   for(var labels_index = 0; labels_index < datasetsLabel.length;labels_index++){
       var table_thead_tr_td = document.createElement("td");
       table_thead_tr_td.textContent = datasetsLabel[labels_index];
       table_thead_tr.appendChild(table_thead_tr_td);
   }
   
   table_thead.appendChild(table_thead_tr);
   
   //データ一覧のデータ部分を描画する
   var table_tbody = document.createElement("tbody");
   table_tbody.innerHTML = "";

   for(var datasIndex = 0; datasIndex < datasetsDatas.length;datasIndex++){
       var table_tbody_tr = document.createElement("tr");
       for(var dataNum = 0;dataNum < datasetsDatas[datasIndex].length;dataNum++){
           if(dataNum == 0){
               var table_tbody_tr_td = document.createElement("td");
               table_tbody_tr_td.textContent = labels[datasIndex];
               table_tbody_tr.appendChild(table_tbody_tr_td);
           }
           var table_tbody_tr_td = document.createElement("td");
           table_tbody_tr_td.textContent = datasetsDatas[datasIndex][dataNum];
           table_tbody_tr.appendChild(table_tbody_tr_td);

       }
       table_tbody.appendChild(table_tbody_tr);
   }

   table.appendChild(table_thead);
   table.appendChild(table_tbody);
   MyDataTable = DATA_TABLE_JQuery.DataTable();
}
/* End Atsuki Add--*/