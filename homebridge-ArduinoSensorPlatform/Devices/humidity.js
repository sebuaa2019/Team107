require('./Base');

var request = require("superagent");

// Require and instantiate a cache module
var cacheModule = require("cache-service-cache-module");
var cache = new cacheModule({ storage: "session", defaultExpiration: 60 });

var superagentCache = require("superagent-cache-plugin")(cache);

const inherits = require('util').inherits;

var Accessory, PlatformAccessory, Service, Characteristic, UUIDGen;

Humidity = function (log, platform, config) {
    this.init(platform, config);
    Accessory = platform.Accessory;
    PlatformAccessory = platform.PlatformAccessory;
    Service = platform.Service;
    Characteristic = platform.Characteristic;
    UUIDGen = platform.UUIDGen;

    this.accessories = {};
    if (this.config['Name'] && this.config['Name'] != "") {
        this.accessories['SensorAccessory'] = new HumidityService(log, this);
    }
    var accessoriesArr = this.obj2array(this.accessories);

    return accessoriesArr;
}

inherits(Humidity, Base);

HumidityService = function (log, dThis) {
    this.log = log
    this.device = dThis.device;
    this.name = dThis.config['Name'];
    //this.token = dThis.config['token'];
    this.platform = dThis.platform;
    this.updatetimere = dThis.config["updatetimer"] || true;
    this.interval = dThis.config["interval"] || 3;
    this.httpMethod = dThis.config["httpMethod"] || "GET";
    this.cacheExpiration = dThis.config["cacheExpiration"] || 10;
    this.url = dThis.config["url"]
    this.Senservice = false;
    this.timer;
    if(this.updatetimere === true){
        this.updateTimer();
    }
}

HumidityService.prototype.getHumidityState = function (callback) {
    request(this.httpMethod, this.url)
        .set("Accept", "application/json")
        .use(superagentCache)
        .expiration(this.cacheExpiration)
        .end(function (err, res, key) {
            if (err) {
                this.log(`HTTP failure (${this.url})`);
                callback(err);
            } else {
                this.log(`HTTP success (${key})`);
                
                this.HumidityServices.setCharacteristic(
                    Characteristic.CurrentRelativeHumidity,
                    res.body.humidity
                );
                this.platform.log.debug("[ArdSenPlatform][" + this.name + "][DEBUG]Humidity - getCurrentRelativeHumidity: " + res.body.humidity);
                callback(null, res.body.humidity);
            }
        }.bind(this));
}

HumidityService.prototype.getServices = function () {
    var that = this;
    var services = [];
    var infoService = new Service.AccessoryInformation();
    infoService
        .setCharacteristic(Characteristic.Manufacturer, "Arduino")
        .setCharacteristic(Characteristic.Model, "Humidity")
    services.push(infoService);

    this.HumidityServices = this.Senservice = new Service.HumiditySensor(this.name, "Humidity");

    this.HumidityServices
        .getCharacteristic(Characteristic.CurrentRelativeHumidity)
        .setProps({ minValue: -273, maxValue: 200 })
        .on('get', this.getHumidityState.bind(this));
    services.push(this.HumidityServices);
    return services;
}


HumidityService.prototype.updateTimer = function () {
    if (this.updatetimere) {
        clearTimeout(this.timer);
        this.timer = setTimeout(function () {
            if (this.Senservice !== false) {
                this.runTimer();
            }
            this.updateTimer();
        }.bind(this), this.interval * 1000);
    }
}

HumidityService.prototype.runTimer = function () {
    var that = this
    this.getHumidityState(function(err, value){
        //this.Senservice.setCharacteristic(Characteristic.CurrentRelativeHumidity).updateValue(value);
    });

    
}