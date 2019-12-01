import psutil
import os
from requests import get


def getEverything():
    """Find and return everything

    Returns:
        string -- Everything
    """
    return os.popen('inxi -F -c 0').read()


def getExternalIP():
    """Find and return External Ip Address

    Returns:
        string -- External IP Address
    """
    return get('https://api.ipify.org').text


def getOSVersion():
    """Find and return OS Version

    Returns:
        string -- OS Version
    """
    return os.uname().version


def getHostName():
    """Find and return Host Name

    Returns:
        string -- Host Name
    """
    return os.uname().nodename


def getOS():
    """Find and return OS

    Returns:
        string -- OS Name
    """
    return os.uname().sysname


def getCpuUsage():
    """Find and return CPU Usage

    Returns:
        int -- Cpu Usage
    """
    cpuUsage = psutil.cpu_percent()
    return int(cpuUsage)


def getMemUsage():
    """Find and return Mem Usage

    Returns:
        int -- Mem Usage
    """
    memUsage = psutil.virtual_memory().percent
    return int(memUsage)


def getCpuTemp():
    """Find and return CPU Temp

    Returns:
        int -- Cpu Temp
    """
    cpuTemp = psutil.sensors_temperatures()["coretemp"][0].current
    return int(cpuTemp)


def getGpuTemp():
    """Find and return GPU Temp

    Returns:
        int -- Gpu Temp
    """
    gpuTemp = psutil.sensors_temperatures()["coretemp"][2].current
    return int(gpuTemp)
