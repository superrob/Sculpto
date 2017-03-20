# Sculpto
A collection of my current knowledge about the printers internal workings.
Collaboration is highly anpreciated! Remember to keep this repo free of any copyrighted code from the printer itself. Please post any modifications as instructions or patches.

The printer is a combination of two processors, one running the printer firmware, accepting and executing G-Code. The other running  OpenWRT Linux and serving as the interface to the outside world.
## Printer MCU board
- LPC1768 microcontroller
- Firmware: Smoothieware (Modified?)
- Accepts commands through Serial

## Operating system board
- Implemented on an Linkit smart 7688 development board, plugged into a socket on the MCU board.
- Running OpenWRT
- Stripped down version of Busybox.
- Running the Dropbear SSH server.
- Lists itself as a Zeroconf device as *_SCULPTO-PRINTER* with the hostname *Sculpto3D-SERIALNUMBER*
- Communicating with the MCU through /dev/ttyS0 with a baud rate of 57600

## Sculpto services
Two different versions of the Sculpto services exists. Version 1 ran directly on internal flash in the /root/ directory and is superseeded by Version 2.

Version 2 runs on an external 1GB SD Card attached to the Linkit Smart board.

The SDcard is encrypted (Sigh..) using AES with a 256 bit randomly generated key stored in flash memory. Making each SD Card uniquely encrypted. 

MD5 sums are saved of each file on the SD Card and compared at boot time. A backup will be restored should any file show any modification, accidental or intended.

### PrinterAPI
Python program which works as the interface between the **Sculpto App** and the **PrintServer**. 

Talks throught the Django powered API through HTTP.
Attemps to associate with the API servers to get returned an session ID which is used as authentication.
Starts polling the API for tasks.

If association is not successfull the service opens a HTTP server and opens an accesspoint for the user to connect to which is then used for the initial setup. This association can fail either due to lack of connectivity or rejection by the Sculpto API.

Periodically queries the **PrinterAPI** service through the 8080 web interface to get current progress and temperature. Also uses this interface to start prints.

The PrinterAPI thus offers no direct user accessible interfaces.

### PrintServer
Python program which talks with the MCU through Serial. Is started by the **PrinterAPI** service.
Opens a *Bottle* web server on port 8080 as it's interface. Is available to the entire network.
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

Looks for the field *gcode_file_path* and opens the file through *open*. Should be possible to trigger printing on network paths! Though not possible without editing the config for the **PrinterAPI** as it contains a sanitycheck. The check prevents the hotend staying hot, stopping any prints not started through the Sculpto App.

- **POST** /stop_print

Has two behaviors. If currently printing it stops the print and returns "Stopped the print". This is done by simply deleting the current queue of Gcode. **Warning** This leaves the hotend hot! 
If not currently printing it will look for the field *cool*. If this field is found, a request to cool the hot end is sent.

- **GET** /ping

Returns "pong"

# Accessing the printer
**WARNING: Only proceed to connect to the printer through SSH if you know what you're doing! You are able to do considerable harm to the operating system if handled wrongly!**

The printer is accessible through SSH on port 22. 

**UNCONFIRMED** the password of the *root* user should according to the install script be set to the printer serial number with zeroes prepended to achieve six characters in total. Meaning a serial of *175* would give a root password of *000175*
