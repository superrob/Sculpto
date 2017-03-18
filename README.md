# Sculpto
A collection of my current knowledge about the printers internal workings.

The printer is split between two processors, one accepting and executing G-Code. The other running Linux and serving as the interface to the outside world.
## Printer MCU
- LPC1768 microcontroller
- Firmware: Smoothieware (Modified?)
- Accepts commands through Serial

## Operating system board
- Implemented on an Linkit smart 7688 development board, plugged into a socket on the MCU board.
- Running OpenWRT
- Stripped down version of Busybox.
- Running the Dropbear SSH server.
- Lists itself as a Zeroconf device as *_SCULPTO-PRINTER* with the name *Sculpto3D-SERIALNUMBER*
- Communicating with the MCU through Serial 1

## Sculpto services
Two different versions of the Sculpto services exists. Version 1 ran directly on internal flash in the /root/ directory is superseeded by Version 2.

Version 2 runs on the external 1GB SD Card which is encrypted (Sigh..)
MD5 sums are saved of each file on the SD Card and compared at boot time. A backup will be restored should any file show any modification, accidental or intended.

### PrintServer
Python program which talks with the MCU through Serial 1.
Opens a web server on port 8080 as it's interface. Is available to the entire network.
Generally returns a JSON object in return.
Provides the following HTTP methods:
- **GET** /progress

Returns the percentage (0.0 to 1.0) of Gcode lines executed to indicate the current progress.
0 if not printing.

- **GET** /temperature

Returns the current hot end temperature. 

- **POST** /gcode_single

Looks for the field *gcode_line* and sends it directly to the MCU. Could be used to implement direct tethered printing.
Returns the response from the MCU or an error indicating no "OK" response from the MCU.

- **POST** /gcode_file

Looks for the field *gcode_file_path* and opens the file through *open*. Should be possible to trigger printing on network paths! Though not possible without editing the config for the **PrinterAPI** as it contains a sanitycheck. The check prevents the hotend staying hot, stopping any prints not started through the Sculpto web app.

- **POST** /stop_print

Has two behaviors. If currently printing it stops the print and returns "Stopped the print". This is done by simply deleting the current queue of Gcode. **Warning** This leaves the hotend hot! 
If not currently printing it will look for the field *cool*. If this field is found, a request to cool the hot end is sent.

- **GET** /ping

Returns "pong"
