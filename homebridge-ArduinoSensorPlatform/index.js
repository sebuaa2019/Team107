require('./Devices/temperature');
require('./Devices/humidity');
require('./Devices/smoke');
require('./Devices/occupancy');

var fs = require('fs');
var packageFile = require("./package.json");
var PlatformAccessory, Accessory, Service, Characteristic, UUIDGen;

module.exports = function (homebridge) {
	if (!isConfig(homebridge.user.configPath(), "platforms", "ArdSenPlatform")) {
		return;
	}

	PlatformAccessory = homebridge.platformAccessory;
	Accessory = homebridge.hap.Accessory;
	Service = homebridge.hap.Service;
	Characteristic = homebridge.hap.Characteristic;
	UUIDGen = homebridge.hap.uuid;

	homebridge.registerPlatform('homebridge-ArduinoSensorPlatform', 'ArdSenPlatform', ArdSenPlatform, true);
}

function isConfig(configFile, type, name) {
	var config = JSON.parse(fs.readFileSync(configFile));
	if ("accessories" === type) {
		var accessories = config.accessories;
		for (var i in accessories) {
			if (accessories[i]['accessory'] === name) {
				return true;
			}
		}
	} else if ("platforms" === type) {
		var platforms = config.platforms;
		for (var i in platforms) {
			if (platforms[i]['platform'] === name) {
				return true;
			}
		}
	} else {
	}

	return false;
}

function ArdSenPlatform(log, config, api) {
	if (null == config) {
		return;
	}

	this.Accessory = Accessory;
	this.PlatformAccessory = PlatformAccessory;
	this.Service = Service;
	this.Characteristic = Characteristic;
	this.UUIDGen = UUIDGen;

	this.log = log;
	this.config = config;

	if (api) {
		this.api = api;
	}


	this.log.info("[ReYeelight][INFO]*********************************************************************");
	this.log.info("[ReYeelight][INFO]*                         ArdSenPlatform v%s                      *", packageFile.version);
	this.log.info("[ReYeelight][INFO]*                                                                   *");
	this.log.info("[ReYeelight][INFO]*********************************************************************");
	this.log.info("[ReYeelight][INFO]start success...");

}

ArdSenPlatform.prototype = {
	accessories: function (callback) {
		var myAccessories = [];

		var deviceCfgs = this.config['deviceCfgs'];

		if (deviceCfgs instanceof Array) {
			for (var i = 0; i < deviceCfgs.length; i++) {
				var deviceCfg = deviceCfgs[i];
				if (null == deviceCfg['type'] || "" == deviceCfg['type'] ||  null == deviceCfg['url'] || "" == deviceCfg['url']) {
					continue;
				}

				if (deviceCfg['type'] == "temperature") {
					new Temperature(this.log, this, deviceCfg).forEach(function (accessory, index, arr) {
						myAccessories.push(accessory);
					});
				}else if(deviceCfg['type'] == "humidity") {
                    new Humidity(this.log, this, deviceCfg).forEach(function(accessory, index, arr){
                        myAccessories.push(accessory);
                    });
				}else if(deviceCfg['type'] == "smoke") {
                    new Smoke(this.log, this, deviceCfg).forEach(function(accessory, index, arr){
                        myAccessories.push(accessory);
                    });
                }else if(deviceCfg['type'] == "occupancy") {
                    new Occupancy(this.log, this, deviceCfg).forEach(function(accessory, index, arr){
                        myAccessories.push(accessory);
                    });
                }
			}
			this.log.info("[ArdSenPlatform][INFO]device size: " + deviceCfgs.length + ", accessories size: " + myAccessories.length);
		}

		callback(myAccessories);
	}
}