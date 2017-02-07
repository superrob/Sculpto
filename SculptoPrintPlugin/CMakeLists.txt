project(OctoPrintPlugin NONE)
cmake_minimum_required(VERSION 2.8.12)

install(FILES
    __init__.py
    SculptoPrintComponents.qml
    SculptoPrintOutputDevice.py
    SculptoPrintOutputDevicePlugin.py
    LICENSE
    README.md
    DESTINATION lib/cura/plugins/SculptoPlugin
)
