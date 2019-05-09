var Service, Characteristic;
var request = require("superagent");

// Require and instantiate a cache module
var cacheModule = require("cache-service-cache-module");
var cache = new cacheModule({ storage: "session", defaultExpiration: 60 });

// Require superagent-cache-plugin and pass your cache module
var superagentCache = require("superagent-cache-plugin")(cache);

module.exports = function (homebridge) {
    Service = homebridge.hap.Service;
    Characteristic = homebridge.hap.Characteristic;
    homebridge.registerAccessory("homebridge-httpalarm", "HttpAlarm", HttpAlarm);
}
function HttpAlarm(log, config) {
    this.log = log;

    // Configuration in config.json
    this.url = config["url"];
    this.httpMethod = config["httpMethod"] || "GET";
    this.name = config["name"];
    this.manufacturer = config["manufacturer"] || "Arduino";
    this.model = config["model"] || "HTTP(S)";
    this.serial = config["serial"] || "";
    //this.humidity        = config["humidity"];
    this.lastUpdateAt = config["lastUpdateAt"] || null;
    this.cacheExpiration = config["cacheExpiration"] || 60;
}

HttpTemphum.prototype = {

    getRemoteState: function (service, callback) {
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

                    this.temperatureService.setCharacteristic(
                        Characteristic.CurrentTemperature,
                        res.body.temperature
                    );
                    this.temperature = res.body.temperature;

                    this.humidityService.setCharacteristic(
                        Characteristic.CurrentRelativeHumidity,
                        res.body.humidity
                    );
                    this.humidity = res.body.humidity;

                    this.OccupancyService.setCharacteristic(
                        Characteristic.OccupancyDetected,
                        res.body.occupancy
                    );
                    this.occupancy = res.body.occupancy;

                    this.smokeService.setCharacteristic(
                        Characteristic.SmokeDetected,
                        res.body.smoke
                    );
                    this.smoke = res.body.smoke;

                    this.lastUpdateAt = +Date.now();

                    switch (service) {
                        case "temperature":
                            callback(null, this.temperature);
                            break;
                        case "humidity":
                            callback(null, this.humidity);
                            break;
                        case "occupancy":
                            callback(null, this.occupancy);
                            break;
                        case "smoke":
                            callback(null, this.smoke);
                            break;
                        default:
                            var error = new Error("Unknown service: " + service);
                            callback(error);
                    }
                }
            }.bind(this));
    },

    getTemperatureState: function (callback) {
        this.getRemoteState("temperature", callback);
    },

    getHumidityState: function (callback) {
        this.getRemoteState("humidity", callback);
    },

    getOccupancyState: function (callback) {
        this.getRemoteState("occupancy", callback);
    },

    getSmokeState: function (callback) {
        this.getRemoteState("smoke", callback);
    },

    getServices: function () {
        var services = [],
            informationService = new Service.AccessoryInformation();

        informationService
            .setCharacteristic(Characteristic.Manufacturer, this.manufacturer)
            .setCharacteristic(Characteristic.Model, this.model)
            .setCharacteristic(Characteristic.SerialNumber, this.serial);
        services.push(informationService);

        this.temperatureService = new Service.TemperatureSensor(this.name);
        this.temperatureService
            .getCharacteristic(Characteristic.CurrentTemperature)
            .setProps({ minValue: -273, maxValue: 200 })
            .on("get", this.getTemperatureState.bind(this));
        services.push(this.temperatureService);

        this.humidityService = new Service.HumiditySensor(this.name);
        this.humidityService
            .getCharacteristic(Characteristic.CurrentRelativeHumidity)
            .setProps({ minValue: 0, maxValue: 100 })
            .on("get", this.getHumidityState.bind(this));
        services.push(this.humidityService);

        this.occupancyService = new Service.OccupancySensor(this.name);
        this.occupancyService
            .getCharacteristic(Characteristic.OccupancyDetected)
            .setProps({ minValue: 0, maxValue: 1 })
            .on("get", this.getOccupancyState.bind(this));
        services.push(this.occupancyService);

        this.smokeService = new Service.SmokeSensor(this.name);
        this.smokeService
            .getCharacteristic(Characteristic.SmokeDetected)
            .setProps({ minValue: 0, maxValue: 1 })
            .on("get", this.getSmokeState.bind(this));
        services.push(this.smokeService);

        return services;
    }
};