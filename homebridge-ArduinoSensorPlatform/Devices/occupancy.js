require('./Base');

var request = require("superagent");

// Require and instantiate a cache module
var cacheModule = require("cache-service-cache-module");
var cache = new cacheModule({ storage: "session", defaultExpiration: 60 });

var superagentCache = require("superagent-cache-plugin")(cache);

const inherits = require('util').inherits;

var Accessory, PlatformAccessory, Service, Characteristic, UUIDGen;

Occupancy = function (log, platform, config) {
    this.init(platform, config);
    Accessory = platform.Accessory;
    PlatformAccessory = platform.PlatformAccessory;
    Service = platform.Service;
    Characteristic = platform.Characteristic;
    UUIDGen = platform.UUIDGen;

    this.accessories = {};
    if (this.config['Name'] && this.config['Name'] != "") {
        this.accessories['SensorAccessory'] = new OccupancyService(log, this);
    }
    var accessoriesArr = this.obj2array(this.accessories);

    return accessoriesArr;
}

inherits(Occupancy, Base);

OccupancyService = function (log, dThis) {
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

OccupancyService.prototype.getOccupancyState = function (callback) {
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
                
                this.OccupancyServices.setCharacteristic(
                    Characteristic.OccupancyDetected,
                    res.body.occupancy
                );
                this.platform.log.debug("[ArdSenPlatform][" + this.name + "][DEBUG]Occupancy - getOccupancyDetected: " + res.body.occupancy);
                callback(null, res.body.occupancy);
            }
        }.bind(this));
}

OccupancyService.prototype.getServices = function () {
    var that = this;
    var services = [];
    var infoService = new Service.AccessoryInformation();
    infoService
        .setCharacteristic(Characteristic.Manufacturer, "Arduino")
        .setCharacteristic(Characteristic.Model, "Occupancy")
    services.push(infoService);

    this.OccupancyServices = this.Senservice = new Service.OccupancySensor(this.name, "Occupancy");

    this.OccupancyServices
        .getCharacteristic(Characteristic.OccupancyDetected)
        .setProps({ minValue: -273, maxValue: 200 })
        .on('get', this.getOccupancyState.bind(this));
    services.push(this.OccupancyServices);
    return services;
}


OccupancyService.prototype.updateTimer = function () {
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

OccupancyService.prototype.runTimer = function () {
    var that = this
    this.getOccupancyState(function(err, value){
        //this.Senservice.setCharacteristic(Characteristic.OccupancyDetected).updateValue(value);
    });

    
}