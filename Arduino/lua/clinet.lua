mytimer=tmr.create()
led=1
count=0
gpio.mode(led, gpio.OUTPUT)
srv = net.createConnection(net.TCP, 0)
mytimer:alarm(1000,tmr.ALARM_AUTO,function()
    srv:connect(8000,"192.168.50.157")
end)
srv:on("receive", function(sck, c) 
    on=string.sub(c,-1)
    if(on=='1') then 
        gpio.write(led,gpio.HIGH)
        print("led on");
        count=count+1
        if(count==5) then
            mytimer:stop()
        end
    end
    if(on=='0') then 
        gpio.write(led,gpio.LOW)
        print("led off");
        count=count+1
        if(count==5) then
            mytimer:stop()
        end
    end
end)
-- Wait for connection before sending.
srv:on("connection", function(sck, c)
    -- 'Connection: close' rather than 'Connection: keep-alive' to have server
    -- initiate a close of the connection after final response (frees memory
    -- earlier here), https://tools.ietf.org/html/rfc7230#section-6.6
    port,ip=srv:getaddr()
    print(port.."  "..ip)
    s="GET /nodemcu_led/ HTTP/1.1\r\n"..
    --"User-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3"
    "Host: 192.168.50.157\r\n"..
    --"Accept-Language: en, mi"
    "Connection: close\r\n\r\n"
    srv:send(s)
end)
srv:on("sent",function(sck)
    print("send ok")
end)
srv:on("disconnection",function(sck,c)
    print("disconnection");
end)    
