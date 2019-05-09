var Service, Characteristic;
var request = require("superagent");

// Require and instantiate a cache module
var cacheModule = require("cache-service-cache-module");
var cache = new cacheModule({storage: "session", defaultExpiration: 60});

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
    this.url             = config["url"];
    this.httpMethod      = config["httpMethod"] || "GET";
    this.name            = config["name"];
    this.manufacturer    = config["manufacturer"] || "Arduino";
    this.model           = config["model"] || "HTTP(S)";
    this.serial          = config["serial"] || "";
    //this.humidity        = config["humidity"];
    this.lastUpdateAt    = config["lastUpdateAt"] || null;
    this.cacheExpiration = config["cacheExpiration"] || 60;
}