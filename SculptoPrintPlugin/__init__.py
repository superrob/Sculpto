# Copyright (c) 2015 Ultimaker B.V.
# Cura is released under the terms of the AGPLv3 or higher.
from . import SculptoPrintOutputDevicePlugin
from . import DiscoverOctoPrintAction
from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

def getMetaData():
    return {
        "type": "extension",
        "plugin": {
            "name": "Sculpto connection",
            "author": "RobseRob",
            "version": "1.0",
            "description": catalog.i18nc("@info:whatsthis", "Allows sending prints to Sculpto and monitoring the progress"),
            "api": 3
        }
    }

def register(app):
    return {
        "output_device": SculptoPrintOutputDevicePlugin.SculptoPrintOutputDevicePlugin(),        
        "machine_action": DiscoverOctoPrintAction.DiscoverOctoPrintAction()
    }