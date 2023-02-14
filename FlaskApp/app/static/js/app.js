$(document).ready(function () {
    console.log('conected');
    const MAX_DATA_COUNT = 10;
    //connect to the socket server.
    //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  
    //receive details from server
    

    
});
$('#results').on('load', function() {
    console.log('page finded')
    var socket = io.connect();
    socket.on("updateSensorData", function (msg) {
        console.log("Received sensorData :: " + msg);
        const ctx = document.getElementById("message");
        ctx.append(msg)
        
      });
  });

  $('#buts').on('click', function(e){
   console.log('clicked')
    //alert("termino el proceso se paginara el siguiente:"+id_d);
    //document.getElementById(id_d).click();
});

$('#send').on('click', function() {
   console.log('data')
  })