var net = require('net');
var server = net.createServer(function(connection) {
   server.close();
   console.log('client connected');
   connection.on('end', function() {
      console.log('客户端关闭连接');
   });
   connection.on('close',function(){
	   console.log('服务器关闭');
   });
   connection.on('data',function(data){
	   console.log(data.toString());
   })
   //connection.write("hello world");
});
server.listen(8000, function() { 
  console.log('server is listening');
});