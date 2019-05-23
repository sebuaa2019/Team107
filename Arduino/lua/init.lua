-- init.lua
print('Setting up WIFI...')
wifi.setmode(wifi.STATIONAP)
station_cfg={}
station_cfg.ssid="ASUS"
station_cfg.pwd="xuyitaodashabi"
wifi.sta.config(station_cfg)
mytimer=tmr.create()
mytimer:alarm(1000,tmr.ALARM_AUTO, function()
    if wifi.sta.getip() == nil then
        print('Waiting for IP ...')
    else
        print('IP is ' .. wifi.sta.getip())
		mytimer:unregister()
        dofile('clinet.lua')
    end
end)
