sv = net.createServer(net.TCP, 30)

function receiver(sck, data)
  print(data)
end
print("server is listening,port is 8080 ...")
if sv then
  sv:listen(8080, function(conn)
    conn:on("connection",function(sck,c)
        sv:close()
        print("connected")
        sck:send("message from server")
    end)
    conn:on("receive", receiver)
    conn:on("disconnection",function(sck,c)
        print("server closed")
    end)
  end)
end
