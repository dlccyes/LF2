function getCookie(cookieName, defaultVal){ // from github copilot
  cookie = document.cookie;
  idxStart = cookie.search(cookieName+'=');
  if(idxStart == -1){
    return defaultVal;
  }
  idxStart += cookieName.length + 1
  idxEnd = idxStart;
  while(idxEnd < cookie.length-1){
    if(cookie[idxEnd] == ';'){
      break;
    }
    idxEnd++;
  }
  return cookie.slice(idxStart, idxEnd);
}
function setCookie(cookieName, newValue){
  document.cookie = cookieName + "=" + newValue + '; domain=' + window.location.hostname + '; path=/';
}
function getData(url, objData, callback){ //to backend
  var type = "GET";
  if (objData != null) {
    type = "POST";
  }
  $.ajax({
    type: type,
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(objData),
    url: url,
    success: function(result){
      reply_html = '';
      if (!result['success']){ // error
        console.log(result['error'])
      } else {
        callback(result['data']);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log('error ' + textStatus);
      console.log(jqXHR);
    },
  });
};

function drawLine(dataArr, id, xName, yName, yAx=null){
  $('#'+id).empty();
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(function(){
    var data = new google.visualization.DataTable();
    data.addColumn('date','log time');
    data.addColumn('number','num of students');
    for(var date of dataArr){
        data.addRow([new Date(date[0]), date[1]]);
    }
    var mainColor;
    if(night){
      mainColor = '#fff';
      lineColor = '#ffd8d2';
    }else{
      mainColor = '#000';
      lineColor = '#5692f0';
    }
    var options = {
      width: 'auto', //1200
      height: '300', //500
      series:{0:{color:lineColor}}, // color of the line
      backgroundColor: {fill:'transparent',stroke:'transparent'},
      chartArea: {backgroundColor:{fill:'transparent',stroke:mainColor}},
      chart: {
        title: '# students vs. time',
      },
      lineWidth: 4,
      // curveType: 'function', // line smoothing
      // tooltip:{textStyle:{color:mainColor}},
      legend:{textStyle: {color:'transparent'}},

      hAxis: { //x-axis
        title: xName,
        titleTextStyle:{color:mainColor, fontName:"Montserrat", fontSize:18},
        textStyle:{color:mainColor},
        baselineColor:'transparent',
        gridlines:{color:'transparent'},
        minorGridlines:{color:'transparent'},

        // format: 'mm:ss',
      },
      vAxis: { //y-axis
        title: yName, 
        titleTextStyle:{color:mainColor, fontName:"Montserrat", fontSize:18},
        viewWindow: {min:0},
        textStyle:{color:mainColor},
        baselineColor:'transparent',
        gridlines:{color:mainColor,multiple:1},
        minorGridlines:{color:'transparent', multiple:0.5, minSpacing:0},
      }
    };
    if(yAx){
      console.log(Math.ceil((yAx[1]-yAx[0])/yAx[2]));
      options.vAxis.viewWindow = {min:yAx[0], max:yAx[1]};
      options.vAxis.gridlines.count = Math.ceil((yAx[1]-yAx[0])/yAx[2]);
    }

    var chart = new google.visualization.LineChart(document.getElementById(id));

    chart.draw(data, options);
  });
}
function drawCloud(data, id){
  $('#'+id).empty();
  anychart.onDocumentReady(function () {
    // night=0;
    console.log('now is' + night);
    if(night){
      anychart.theme(anychart.themes.darkGlamour);
    }else{
      anychart.theme(null);
    }
    // anychart.theme(anychart.themes.darkTurquoise);

    var chart = anychart.tagCloud(data);

    // set the chart title
    chart.title('')
    // set array of angles, by which words will be placed
    chart.angles([0])
    // enable color range
    // set color range length
    chart.colorRange().length('80%');
    chart.background().fill('transparent');
    chart.background().stroke("0 transparent");
    chart.background().corners(20);
    // chart.fontColor('transparent');
    // display chart
    chart.container(id);
    chart.draw();
    // $('.anychart-credits').html('<span class="anychart-credits-text">made with AnyChart</span>') 
    $('.anychart-credits').html('') 
  });
}