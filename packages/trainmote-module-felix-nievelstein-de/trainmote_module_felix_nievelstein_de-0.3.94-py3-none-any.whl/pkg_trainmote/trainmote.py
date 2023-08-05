from .models.ConfigModel import ConfigModel
from pkg_trainmote.stateControllerModule import StateController
from . import gpioservice
from flask import Flask
from flask import request
from flask import abort
from flask import Response
from .powerControllerModule import PowerThread
from .configControllerModule import ConfigController
from . import stateControllerModule
from .libInstaller import LibInstaller
from .databaseControllerModule import DatabaseController
from .stopPointAPI import stopPointApi
from .validator import Validator
from . import baseAPI
from typing import Optional
import sys
import os
import json
import signal

stateController: Optional[StateController]
dataBaseController: Optional[DatabaseController]
powerThread: Optional[PowerThread]
config: Optional[ConfigController]
app = Flask(__name__)
app.register_blueprint(stopPointApi)

version: str = '0.3.94'


def loadPersistentData():
    if config.loadPreferences():
        if not config.isSQLiteInstalled():
            libInstaller = LibInstaller()
            libInstaller.installSQLite()
            if config.setSQLiteInstalled():
                restart()
            else:
                shutDown()


def main():
    gpioservice.setup()    
    global dataBaseController
    dataBaseController = DatabaseController()
    dataBaseController.checkUpdate(version)

    global powerThread
    powerThread = None

    global stateController
    stateController = None

    conf = DatabaseController().getConfig()
    if conf is not None:
        if conf.powerRelais is not None:
            setupPowerGPIO(conf.powerRelais)
        if conf.stateRelais is not None:
            stateController = stateControllerModule.StateController(conf.stateRelais)
            stateController.setState(stateControllerModule.STATE_NOT_CONNECTED)

    global config
    config = ConfigController()
    print("Start webserver")
    app.run(host="0.0.0.0")
    signal.signal(signal.SIGINT, handler)

##
# Setup PowerThread to track user event to shut down.
##
def setupPowerGPIO(pin: int):
    powerThread = PowerThread(pin)
    powerThread.start()

@app.route('/trainmote/api/v1')
def hello_world():
    stateController.setState(stateControllerModule.STATE_CONNECTED)
    return json.dumps({"trainmote": "trainmote.module.felix-nievelstein.de", "version": version})

##
# Endpoint Switch
##

@app.route('/trainmote/api/v1/switch/<switch_id>', methods=["GET"])
def switch(switch_id: str):
    if switch_id is None:
        abort(400)
    return gpioservice.getSwitch(switch_id), 200, baseAPI.defaultHeader()


@app.route('/trainmote/api/v1/switch/<switch_id>', methods=["PATCH"])
def setSwitch(switch_id: str):
    if switch_id is None:
        abort(400)
    try:
        return gpioservice.setSwitch(switch_id), 200, baseAPI.defaultHeader()
    except ValueError as e:
        return json.dumps({"error": str(e)}), 400, baseAPI.defaultHeader()


@app.route('/trainmote/api/v1/switch/<switch_id>', methods=["DELETE"])
def deleteSwitch(switch_id: str):
    if switch_id is None:
        abort(400)
    dataBaseController.deleteSwitchModel(int(switch_id)), 205, baseAPI.defaultHeader()
    return 'ok'


@app.route('/trainmote/api/v1/switch', methods=["POST"])
def addSwitch():
    mJson = request.get_json()
    if mJson is not None:
        if Validator().validateDict(mJson, "switch_scheme") is False:
            abort(400)
        config = dataBaseController.getConfig()
        if config is not None and config.containsPin(mJson["id"]):
            return json.dumps({"error": "Pin is already in use as power relais"}), 409, baseAPI.defaultHeader()

        try:
            return gpioservice.createSwitch(mJson), 201, baseAPI.defaultHeader()
        except ValueError as e:
            return json.dumps({"error": str(e)}), 400, baseAPI.defaultHeader()
    else:
        abort(400)


@app.route('/trainmote/api/v1/switch/all')
def getAllSwitches():
    return Response(gpioservice.getAllSwitches(), mimetype="application/json"), 200, baseAPI.defaultHeader()

##
# Endpoint StopPoint
##

@app.route('/trainmote/api/v1/stoppoint/<stop_id>', methods=["PATCH"])
def setStop(stop_id: str):
    if stop_id is None:
        abort(400)
    try:
        return gpioservice.setStop(stop_id), 200, baseAPI.defaultHeader()
    except ValueError as e:
        return json.dumps({"error": str(e)}), 400, baseAPI.defaultHeader()


@app.route('/trainmote/api/v1/stoppoint/<stop_id>', methods=["DELETE"])
def deleteStop(stop_id: str):
    if stop_id is None:
        abort(400)
    dataBaseController.deleteStopModel(int(stop_id)), 205, baseAPI.defaultHeader()
    return 'ok'


@app.route('/trainmote/api/v1/stoppoint', methods=["POST"])
def addStop():
    mJson = request.get_json()
    if mJson is not None:
        if Validator().validateDict(mJson, "stop_scheme") is False:
            abort(400)

        config = dataBaseController.getConfig()
        if config is not None and config.containsPin(mJson["id"]):
            return json.dumps({"error": "Pin is already in use as power relais"}), 409, baseAPI.defaultHeader()

        try:
            return gpioservice.createStop(mJson), 201, baseAPI.defaultHeader()
        except ValueError as e:
            return json.dumps({"error": str(e)}), 400, baseAPI.defaultHeader()
    else:
        abort(400)


@app.route('/trainmote/api/v1/stoppoint/all')
def getAllStops():
    return Response(gpioservice.getAllStopPoints(), mimetype="application/json"), 200, baseAPI.defaultHeader()

##
# Endpoints Config
##

@app.route('/trainmote/api/v1/config', methods=["GET"])
def getConfig():
    config = dataBaseController.getConfig()
    if config is not None:
        return json.dumps(config.to_dict()), 200, baseAPI.defaultHeader()
    else:
        abort(404)

@app.route('/trainmote/api/v1/config', methods=["POST"])
def setConfig():
    mJson = request.get_json()
    if mJson is not None:
        validator = Validator()
        if validator.validateDict(mJson, "config_scheme") is False:
            abort(400)

        stops = dataBaseController.getAllStopModels()
        switchs = dataBaseController.getAllSwichtModels()
        switchPowerRelaisIsStop = validator.containsPin(int(mJson["switchPowerRelais"]), stops)
        switchPowerRelaisIsSwitch = validator.containsPin(int(mJson["switchPowerRelais"]), switchs)
        if switchPowerRelaisIsStop or switchPowerRelaisIsSwitch:
            return json.dumps({"error": "Switch power relais pin is already in use"}), 409, baseAPI.defaultHeader()

        powerRelaisIsStop = validator.containsPin(int(mJson["powerRelais"]), stops)
        powerRelaisIsSwitch = validator.containsPin(int(mJson["powerRelais"]), switchs)
        if powerRelaisIsStop or powerRelaisIsSwitch:
            return json.dumps({"error": "Power relais pin is already in use"}), 409, baseAPI.defaultHeader()

        stateRelaisIsStop = validator.containsPin(int(mJson["stateRelais"]), stops)
        stateRelaisIsSwitch = validator.containsPin(int(mJson["stateRelais"]), switchs)
        if stateRelaisIsStop or stateRelaisIsSwitch:
            return json.dumps({"error": "State relais pin is already in use"}), 409, baseAPI.defaultHeader()

        dataBaseController.insertConfig(
            int(mJson["switchPowerRelais"]),
            int(mJson["powerRelais"]),
            int(mJson["stateRelais"])
        )

        if powerThread is not None:
            powerThread.stop()

        config = dataBaseController.getConfig()
        if config.powerRelais is not None:
            setupPowerGPIO(config.powerRelais)
        if config is not None:
            return json.dumps(config.to_dict()), 201, baseAPI.defaultHeader()
        else:
            abort(500)
    else:
        abort(400)

def restart():
    shutDown()
    os.execv(sys.executable, ['python'] + sys.argv)


def shutDown():
    print("Server going down")
    gpioservice.clean()
    if powerThread.is_alive():
        powerThread.kill.set()
        powerThread.isTurningOff = True
        powerThread.join()
    stateController.setState(stateControllerModule.STATE_SHUTDOWN)
    stateController.stop()


def closeClientConnection():
    print("Closing client socket")


if __name__ == '__main__':
    main()


def handler(signal, frame):
    shutDown()
    sys.exit(0)
