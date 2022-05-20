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