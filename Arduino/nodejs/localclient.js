var net = require('net');
var client = net.connect(8080,'192.168.50.106', function() {
   console.log('连接到服务器！');
	console.log('本地地址'+client.address());
	console.log('本地IP地址'+client.localAddress);
	console.log('本地端口'+client.localPort);
	console.log('远程IP地址'+client.remoteAddress);
	console.log('远程端口'+client.remotePort);
	//client.write("hello world");
});
client.on('data', function(data) {
   console.log(data.toString());
   client.end();
});
client.on('end', function() { 
   console.log('断开与服务器的连接');
});