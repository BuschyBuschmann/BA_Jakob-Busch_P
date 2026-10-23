#Class for functions related to the interface between computer and measurement / USB / serial devices.
#To use Prolific USB to serial adapter, first install the corresponding drivers from
#SLA:\09_LABOR\MESSTECHNIK - Unterlagen\GEITMANN_GOLDAMMER\SICONN USB_Basic\USB Seriell Adapter (blau)\PL2303_Prolific_DriverInstaller_v110.exe

import sys
import glob
import win32com.client
import serial
import chardet


def usb_devices():
    """
    lists all the USB devices attached to the computer
    :return:

    """
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(strComputer, "root\\CIMV2")
    colItems = objWMIService.ExecQuery("Select * from Win32_USBHub")
    list_descriptions = []
    for objItem in colItems:
        list_descriptions.append(objItem.Description)
    return list_descriptions

def serial_ports():
    """
    Lists serial port names
        :raises OSError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        all_ports = [f'COM{i+1}' for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        all_ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        all_ports = glob.glob('/dev/tty.*')
    else:
        raise OSError('Unsupported platform')

    com_ports = []
    for port in all_ports:
        try:
            s = serial.Serial(port)
            s.close()
            com_ports.append(port)
        except (OSError, serial.SerialException):
            pass
    return com_ports

def is_usb_device(device):
    devices = usb_devices()
    if device not in devices:
        return False
    else:
        return True

def is_serial(port):
    com_ports = serial_ports()
    if port not in com_ports:
        return False
    else:
        return True

def decode_bytes(bytestring):
    enc = chardet.detect(bytestring)['encoding']
    return bytestring.decode(enc)