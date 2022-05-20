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

function drawLine(dataArr, id, xName, yName){
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(function(){
  // function drawChart () {
      // dateVScountArr = [['a','f']].concat(dateVScountArr);
      var data = new google.visualization.DataTable();
      // var data = google.visualization.arrayToDataTable(dateVScountArr);
      data.addColumn('date','log time');
      data.addColumn('number','num of students');
      for(var date of dataArr){
          data.addRow([new Date(date[0]), date[1]]);
      }

      var options = {
          width: 'auto', //1200
          height: 'auto', //500
          series:{0:{color:'#ffd8d2'}},
          backgroundColor: {fill:'transparent',stroke:'transparent'},
          chartArea: {backgroundColor:{fill:'transparent',stroke:'#fff'}},
          chart: {
            title: '# students vs. time',
          },
          // curveType: 'function', // line smoothing
          // tooltip:{textStyle:{color:'#fff'}},
          legend:{textStyle: {color:'transparent'}},
          hAxis: { //x-axis
              title: xName,
              titleTextStyle:{color:"#fff", fontName:"verdana", fontSize:18},
              textStyle:{color:'#fff'},
              baselineColor:'transparent',
              gridlines:{color:'transparent'},
              minorGridlines:{color:'transparent'},
              // format: 'mm:ss',
          },
          vAxis: { //y-axis
              title: yName, 
              titleTextStyle:{color:"#fff", fontName:"verdana", fontSize:18},
              viewWindow: {min:0},
              textStyle:{color:'#fff'},
              baselineColor:'transparent',
              gridlines:{color:'transparent',multiple:1},
              // minorGridlines:{color:'transparent',minSpacing:0}
          }
      };

      var chart = new google.visualization.LineChart(document.getElementById(id));

      chart.draw(data, options);
  });
}