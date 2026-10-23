##Wrapper for the maiv2dll shared library

__docformat__ =  'restructuredtext'

import os
import inspect
import chardet

#%% Enums

class enumOversampling :
    DISABLED = 0 
    x2  = 1
    x4  = 2
    x8  = 3
    x16 = 4
    
class enumGain :
    Disabled = 0 
    x2 = 1
    x4 = 2
    x8 = 3
    
class enumBipolar :
    UNIPOLAR = 0 
    BIPOLAR = 1
    
class enumPartBlock :
    ONLYFULLBLOCKS = 0 
    PARTBLOCK = 1
    
class enumSkipData :
    GETCAPTUREDVALUES = 0 
    SKIPCAPTUREDVALUES = 1

class enumStreamingMode :
    OFF = 0
    ON = 1

class enumCounterMode :
    FREQUENCYCOUNTER = 0
    PERIODCOUNTER = 1
    PULSWIDTHCOUNTER = 2
    INCREMENTALCOUNTER = 3
    IMPULSECOUNTER = 4

class enumTrigger :
    DISABLED = 0
    EXTERN_TRIGGER = 1
    EXTERN_CLOCK = 2

class enumExternEdge :
    FALLING_EDGE = 0
    RISING_EDGE =  1

class enumFFT_Type :
    Absolute = 0
    RMS = 1
    Power = 2
    Phase = 3

class enumFFT_Size :
    s512 = 0
    s1024 = 1
    s2048 = 2
    s4096 = 3

class enumTrigger_Type :
    Max = 0
    Min = 1
    UnterSchwelle = 2
    UeberSchwelle = 3
    Fenster = 4
    UnterGradientensteigung = 5
    UeberGradientensteigung = 6
    Gradientenfenster = 7

class enumPIDControllerType :
    PID1 = 0
    PID2 = 1
    PID3 = 2

class enumFilterType :
    LOWPASS = 0
    HIGHPASS = 1
    BANDPASS = 2
    BANDSTOP = 3

class enumIIRFilterDesign :
    BUTTERWORTH = 0
    CHEBYSHEV_T1 = 1
    CHEBYSHEV_T2 = 2
    ELLIPTIC = 3
    BESSEL = 4

class enumFIRWindowFunction :
    Rectangular = 0
    Hanning = 1
    Hamming = 2
    Blackman = 3
    Kaiser = 4
    Bartlett = 5
    Dolph_Tschebytschow = 6
    Triangular = 7
    Blackman_Harris = 8
    Blackman_Nuttall = 9
    Flat_Top = 10

class enumSWExtensionsBitNumber :
    Online_FFT = 0
    Online_Filter = 1
    Online_PID = 2
    Online_Linearisierung = 3
    OnboardFunktionsgenerator = 4
    Wabco_Projekt = 9
    Airbag_Pruefstand = 14
    UpDown_Card = 15
    Extended_Stoptrigger = 16

class enumHWExtensionsBitNumber :
    Zaehlerupgrade = 0
    UpDown_Counter = 1
    PWM_Ausgabe = 2
    PWM_Karte = 3
    DA_Wandler = 4
    MultiplexerUeberspannungsschutz = 5
    DualWandler = 8
    Zeitstempel = 9
    TTL_Bitweise = 10
    Coprozessor_56307 = 11
    Coprozessor_56311 = 12
    Inkrementalzaehler = 13
    RegeneratorAutomotiv = 14
    MH_Zaehlererweiterung = 15
    SSI_Schnittstelle = 16
    Thermoelementanschluss_8Kanal = 17
    i32Bit_Counter = 18
    ICP_Einspeisung = 19

class enumIEPEMode :
    DC_SE_IEPE_off = 0
    DC_Diff_IEPE_off = 1
    AC_SE_IEPE_off = 2
    AC_SE_IEPE_on = 3


#%% Preamble

import ctypes, sys, platform
import ctypes.util
import numpy as np

_internalLObj = None

#%% AD Functions

def AD_ReadSingleValue(cardID,
                       channelID,
                       oversamplingMode=enumOversampling.DISABLED,
                       gainFactor=enumGain.Disabled,
                       polarity=enumBipolar.BIPOLAR ):
    retval = ctypes.c_int(0)
    _internalLObj.AD_ReadSingleValue(cardID,
                                     channelID,
                                     oversamplingMode,
                                     gainFactor,polarity,
                                     ctypes.byref(retval))
    return retval.value
    
def AD_ReadSingleVoltage( cardID, channelID, oversamplingMode = enumOversampling.DISABLED, gainFactor = enumGain.Disabled, polarity = enumBipolar.BIPOLAR ):
    retval = ctypes.c_double(0)
    _internalLObj.AD_ReadSingleVoltage(cardID, channelID, oversamplingMode,gainFactor,polarity,ctypes.byref(retval))
    return retval.value

def AD_GetChannelListSize( cardID ):
    retval = ctypes.c_uint(0)
    _internalLObj.AD_GetChannelListSize(cardID,ctypes.byref(retval))
    return retval.value

def AD_SetFrequency ( cardID, smaplerate ): 
    _internalLObj.AD_SetFrequency ( cardID, smaplerate )
    
def AD_ClearChannelList( cardID ):
    _internalLObj.AD_ClearChannelList( cardID )
   
def AD_AddChannelToList(  cardID, channelID, oversamplingMode = enumOversampling.DISABLED, gainFactor = enumGain.Disabled, polarity = enumBipolar.BIPOLAR ):
    _internalLObj.AD_AddChannelToList( cardID, channelID, oversamplingMode,gainFactor,polarity )


def AD_ReadData(cardID, channelListID, numberOfValues):
    nValuesPerChannel = ctypes.c_uint(numberOfValues)
    arr = (ctypes.c_double * numberOfValues)()
    _internalLObj.AD_ReadData(cardID, channelListID, None, arr, ctypes.byref(nValuesPerChannel), 0, 0)
    nparr = np.fromiter(arr, dtype=np.double, count=nValuesPerChannel.value)
    return nparr

def AD_ReadDataRAW(cardID, channelListID, numberOfValues):
    nValuesPerChannel = ctypes.c_uint(numberOfValues)
    arr = (ctypes.c_int * numberOfValues)()
    _internalLObj.AD_ReadData(cardID, channelListID, arr, None, ctypes.byref(nValuesPerChannel), 0, 0)
    nparr = np.fromiter(arr, dtype=np.int, count=nValuesPerChannel.value)
    return nparr

def AD_ReadBinaryData(cardID, nLength):
    lenbytes = ctypes.c_uint(nLength)
    arr = (ctypes.c_ubyte * nLength)()
    _internalLObj.AD_ReadBinaryData(cardID, arr, ctypes.byref(lenbytes))
    nparr = np.fromiter(arr, dtype=np.ubyte, count=lenbytes.value)
    return nparr

def AD_GetStreamPipeLevel(cardID):
    retval = ctypes.c_double(0)
    _internalLObj.AD_GetStreamPipeLevel(cardID, ctypes.byref(retval))
    return retval.value

def AD_GetNumberOfValues(cardID, * nNumberOfValues):
    retval = ctypes.c_uint(0)
    _internalLObj.AD_GetNumberOfValues(cardID, ctypes.byref(retval))
    return retval.value

def AD_GetFrequency(cardID):
    retval = ctypes.c_double(0)
    _internalLObj.AD_GetFrequency(cardID, ctypes.byref(retval))
    return retval.value

def AD_GetCorrectionValue(cardID, nChannel):
    return _internalLObj.AD_GetCorrectionValue(cardID, nChannel)

def AD_SetCorrectionValue(cardID, nChannel):
    return _internalLObj.AD_SetCorrectionValue(cardID, nChannel)

def AD_StartMeasure(cardID):
    _internalLObj.AD_StartMeasure(cardID)

def AD_StopMeasure(cardID):
    _internalLObj.AD_StopMeasure(cardID)

def AD_SetIEPE(cardID, channelID, nIEPEMode, bGain):
    _internalLObj.AD_SetIEPE(cardID, channelID, nIEPEMode, bGain)

def AD_SetIEPEOnAudioModul(cardID, channelID, bIEPEOn, bDCOn, bCurrentSourceOn, bGainOn):
    _internalLObj.AD_SetIEPE(cardID, channelID, bIEPEOn, bDCOn, bCurrentSourceOn, bGainOn)


def AD_Audio_SetHPFilter(cardID, channelID, bFilterOn):
    _internalLObj.AD_Audio_SetHPFilter(cardID, channelID, bFilterOn)

def AD_Audio_SetHPFilterResponse(cardID,  nADCNr, bLowGroupDelayResponseOn):
    _internalLObj.AD_Audio_SetHPFilterResponse(cardID,  nADCNr, bLowGroupDelayResponseOn)

def AD_ResetIEPE(cardID):
    _internalLObj.AD_ResetIEPE(cardID)

def AD_GetIEPEType(cardID):
    return _internalLObj.AD_GetIEPEType(cardID)

#%% CT Functions

def CT_ClearChannelList(cardID):
    _internalLObj.CT_ClearChannelList(cardID)

def CT_AddChannelToList(cardID, channelID, bToADChannellist):
    _internalLObj.CT_AddChannelToList(cardID, channelID, bToADChannellist)

def CT_GetChannelListSize(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.CT_GetChannelListSize(cardID,ctypes.byref(retval))
    return retval.value

def CT_SetFrequency(cardID, samplerate):
    _internalLObj.CT_SetFrequency(cardID, samplerate)

def CT_GetFrequency(cardID):
    retval = ctypes.c_double(0)
    _internalLObj.CT_GetFrequency(cardID,ctypes.byref(retval))
    return retval.value

def CT_SetResolution(cardID, channelID,  nResolution):
    _internalLObj.CT_SetResolution(cardID, channelID,  nResolution)

def CT_ImpulseCounter(cardID, channelID, nPresetValue, nUpDown, nEdge):
    _internalLObj.CT_ImpulseCounter(cardID, channelID, nPresetValue, nUpDown, nEdge)

def CT_FrequencyCounter(cardID, channelID, nResolution, nEdge, nEachPeriod):
    _internalLObj.CT_FrequencyCounter(cardID, channelID, nResolution, nEdge, nEachPeriod)

def CT_PeriodCounter(cardID, channelID, nResolution, nEdge, nEachPeriod):
    _internalLObj.CT_PeriodCounter(cardID, channelID, nResolution, nEdge, nEachPeriod)

def CT_PulswidthCounter(cardID, channelID, nResolution, nEdge, nEachPeriod):
    _internalLObj.CT_PulswidthCounter(cardID, channelID, nResolution, nEdge, nEachPeriod)

def CT_IncrementalCounter(cardID, channelID, nResolution, nEdge, nSoftwareReset, nHardwareReset, nHWResetEdge, nInterpolation):
    _internalLObj.CT_IncrementalCounter(cardID, channelID, nResolution, nEdge, nSoftwareReset, nHardwareReset, nHWResetEdge, nInterpolation)

def CT_IncrementalCounterExtensionTime(cardID, channelID, nResolution):
    _internalLObj.CT_IncrementalCounterExtensionTime(cardID, channelID, nResolution)

def CT_IncrementalCounterExtensionFlow(cardID, channelID):
    _internalLObj.CT_IncrementalCounterExtensionFlow(cardID, channelID)

def CT_UpDownCounter(cardID, channelID, nPresetValue, nUpDown, nEdge, nSoftwareReset):
    _internalLObj.CT_UpDownCounter(cardID, channelID, nPresetValue, nUpDown, nEdge, nSoftwareReset)

# def CT_ScaleData(cardID, channelListID, int pInBuffer[], double pOutBuffer[], nNumberOfValues, int& ARFirstLastValue):


def CT_ReadData(cardID, channelListID, numberOfValues):
    nValuesPerChannel = ctypes.c_uint(numberOfValues)
    arr = (ctypes.c_uint * numberOfValues)()
    _internalLObj.CT_ReadData(cardID, channelListID, arr, ctypes.byref(nValuesPerChannel), 0, 0)
    nparr = np.fromiter(arr, dtype=np.uint, count=nValuesPerChannel.value)
    return nparr

def CT_ReadSingleValue(cardID, channelID):
    retval = ctypes.c_uint(0)
    _internalLObj.CT_ReadSingleValue(cardID, channelID, ctypes.byref(retval))
    return retval.value

def CT_GetStreamPipeLevel(cardID):
    retval = ctypes.c_double(0)
    _internalLObj.CT_GetStreamPipeLevel(cardID,ctypes.byref(retval))
    return retval.value

def CT_GetNumberOfValues(cardID):
    retval = ctypes.c_long(0)
    _internalLObj.CT_GetNumberOfValues(cardID,ctypes.byref(retval))
    return retval.value

def CT_StartMeasure(cardID):
    _internalLObj.CT_StartMeasure(cardID)

def CT_StopMeasure(cardID):
    _internalLObj.CT_StopMeasure(cardID)

#%% DA Functions

def DA_SetRange(cardID, RangeID):
    _internalLObj.DA_SetRange(cardID, RangeID)

def DA_ClearChannelList(cardID):
    _internalLObj.DA_ClearChannelList(cardID)

def DA_AddChannelToList(cardID, channelID):
    _internalLObj.DA_AddChannelToList(cardID, channelID)

def DA_GetChannelListSize(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.CT_GetChannelListSize(cardID,ctypes.byref(retval))
    return retval.value

def DA_SetFrequency(cardID, samplerate):
    _internalLObj.DA_SetFrequency(cardID, samplerate)

def DA_StartOutput(cardID):
    _internalLObj.DA_StartOutput(cardID)

def DA_StopOutput(cardID):
    _internalLObj.DA_StopOutput(cardID)

def	DA_WriteChannelRaw(cardID, channelID, RawValue):
    _internalLObj.DA_WriteChannelRaw(cardID, channelID, RawValue)

def	DA_WriteChannelVoltage(cardID, channelID,  VoltageValue):
    _internalLObj.DA_WriteChannelVoltage(cardID, channelID, VoltageValue)

def DA_WriteRawData(cardID, channelListID, numpyIntArray, numberOfValues):
    nValuesPerChannel = ctypes.c_uint(numberOfValues)
    _internalLObj.DA_WriteRawData(cardID, channelListID, ctypes.byref(numpyIntArray.ctypes.data), ctypes.byref(nValuesPerChannel), 0)
    return nValuesPerChannel

def DA_WriteScaledData(cardID, channelListID, numpyDoubleArray, numberOfValues):
    nValuesPerChannel = ctypes.c_uint(numberOfValues)
    _internalLObj.DA_WriteScaledData(cardID, channelListID, ctypes.byref(numpyDoubleArray.ctypes.data) ,  ctypes.byref(nValuesPerChannel), 0)
    return nValuesPerChannel

def DA_GetFifoState(cardID, channelID, * nNumberOfValues):
    retval = ctypes.c_long(0)
    _internalLObj.DA_GetFifoState(cardID, channelID, ctypes.byref(retval))
    return retval.value


def DA_Audio_SetMonauralMode(cardID, bLoopbackModeOn):
    _internalLObj.DA_Audio_SetMonauralMode(cardID, bLoopbackModeOn)


def DA_Audio_SetADLoopbackMode(cardID, bLoopbackModeOn):
    _internalLObj.DA_Audio_SetADLoopbackMode(cardID, bLoopbackModeOn)

#%% General Functions

def ClearAllChannelLists(cardID):
    _internalLObj.ClearAllChannelLists(cardID)


def ResetDevice(cardID):
    _internalLObj.ResetDevice(cardID)


def LoadFirmware(cardID):
    _internalLObj.LoadFirmware(cardID)


def StartMeasure(cardID):
    _internalLObj.StartMeasure(cardID)


def StopMeasure(cardID):
    _internalLObj.StopMeasure(cardID)


def SetStreamingMode(cardID, nStreamingMode):
    _internalLObj.SetStreamingMode(cardID, nStreamingMode)


def SetRunningMode(cardID, MasterSlave):
    _internalLObj.SetRunningMode(cardID, MasterSlave)


def SetRunningModeEx(cardID, MasterSlave, MultipleMastersAllowed):
    _internalLObj.SetRunningModeEx(cardID, MasterSlave, MultipleMastersAllowed)


def EnableSoftwareClock(cardID, FetchADDataInUserMode):
    _internalLObj.EnableSoftwareClock(cardID, FetchADDataInUserMode)


def ConfigCard(cardID, TriggerExtern, ExternEdge, DifferenzMode, p4):
    _internalLObj.ConfigCard(cardID, TriggerExtern, ExternEdge, DifferenzMode, p4)


def SetGlobalTriggerValues(cardID, nPreTrigger, nPostTrigger, nWaitForStartTrigger):
    _internalLObj.SetGlobalTriggerValues(cardID, nPreTrigger, nPostTrigger, nWaitForStartTrigger)


def ConfigMeasure(cardID):
    _internalLObj.ConfigMeasure(cardID)


def IsUSBHighSpeed(cardID):
    retval = ctypes.c_long(0)
    _internalLObj.IsUSBHighSpeed(cardID, ctypes.byref(retval))
    return retval.value == 1


def DisconnectRemoteDevice(cardID):
    _internalLObj.DisconnectRemoteDevice(cardID)

#%% Card Properties

def GetCardName(cardID):
    return _internalLObj.GetCardName(cardID)

def GetCardProducer(cardID):
    return _internalLObj.GetCardProducer(cardID)


def GetCardSeller(cardID):
    return _internalLObj.GetCardSeller(cardID)


def GetManufacture_Name(cardID):
    return _internalLObj.GetManufacture_Name(cardID)


def GetSerialNumber(cardID):
    return _internalLObj.GetSerialNumber(cardID)


def GetCustomer_Name(cardID):
    return _internalLObj.GetCustomer_Name(cardID)


def GetCustomer_Number(cardID):
    return _internalLObj.GetCustomer_Number(cardID)


def GetCustomer_DateOfPurchase(cardID):
    return _internalLObj.GetCustomer_DateOfPurchase(cardID)


def GetADChannels(cardID):
    return _internalLObj.GetADChannels(cardID)


def GetADSampleWidth(cardID):
    return _internalLObj.GetADSampleWidth(cardID)


def GetADSampleRate(cardID):
    return _internalLObj.GetADSampleRate(cardID)


def GetDAChannels(cardID):
    return _internalLObj.GetDAChannels(cardID)


def GetDASampleWidth(cardID):
    return _internalLObj.GetDASampleWidth(cardID)


def GetDASampleRate(cardID):
    return _internalLObj.GetDASampleRate(cardID)


def GetTTLChannels(cardID):
    return _internalLObj.GetTTLChannels(cardID)


def GetTTLSampleWidth(cardID):
    return _internalLObj.GetTTLSampleWidth(cardID)


def GetTTLSampleRate(cardID):
    return _internalLObj.GetTTLSampleRate(cardID)


def GetCTChannels(cardID):
    return _internalLObj.GetCTChannels(cardID)


def GetCTSampleWidth(cardID):
    return _internalLObj.GetCTSampleWidth(cardID)


def GetCTSampleRate(cardID):
    return _internalLObj.GetCTSampleRate(cardID)


def GetPWMChannels(cardID):
    return _internalLObj.GetPWMChannels(cardID)


def GetPWMSampleWidth(cardID):
    return _internalLObj.GetPWMSampleWidth(cardID)


def GetPWMSampleRate(cardID):
    return _internalLObj.GetPWMSampleRate(cardID)

def GetSoftwareExtension(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.GetSoftwareExtension(cardID, ctypes.pointer(retval))
    return retval.value


def GetHardwareExtension(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.GetHardwareExtension(cardID, ctypes.pointer(retval))

    return retval.value


def GetMeasurementProcessorVersion(cardID):
    return _internalLObj.GetMeasurementProcessorVersion(cardID)


def GetControllerFirmwareVersion(cardID):
    return _internalLObj.GetControllerFirmwareVersion(cardID)

def GetSystemDriverVersion(cardID):
    s = ctypes.create_string_buffer(b'000', 200)
    _internalLObj.GetSystemDriverVersion(cardID,s)
    return s.value


#%% Device Interaction

def PrivateFlashDataRead(cardID,  length):
    s = ctypes.create_string_buffer(b'000',length)
    _internalLObj.PrivateFlashDataRead(cardID, s, length)
    return s.value

def PrivateFlashDataWrite(cardID, stringToWrite , length):
    pin = ctypes.c_char_p(stringToWrite)
    _internalLObj.PrivateFlashDataWrite(cardID, pin , length)

def PrivateFlashDataClear(cardID):
    return _internalLObj.PrivateFlashDataClear(cardID)
                
def	SetLEDs(cardID,RedOrFirstLEDOn,GreenOrSecondLEDOn,ThirdLEDOn):
    _internalLObj.SetLEDs(cardID,RedOrFirstLEDOn,GreenOrSecondLEDOn,ThirdLEDOn)

def GetDLLVersion():
    return _internalLObj.GetDLLVersion()

def GetLIBVersion():
    return _internalLObj.GetLIBVersion()

def GetCardIDBySerial(serialstring):
    pin = ctypes.c_char_p(serialstring)
    retval = ctypes.c_uint(0)
    _internalLObj.GetCardIDBySerial(pin,ctypes.byref(retval))
    return retval.value

def GetDeviceInfo(CardID):
    s = ctypes.create_string_buffer(b'000', 200)
    retval = ctypes.c_long(0)
    _internalLObj.GetDeviceInfo(CardID, ctypes.byref(retval), s)
    retDict = {"Serial" : s.value, "TypeID": retval.value}
    return retDict

def GetNumberOfBurstsOnADController(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.GetNumberOfBurstsOnADController(cardID, ctypes.byref(retval))
    return retval.value
    
def GetNumberOfBurstsOnCTController(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.GetNumberOfBurstsOnCTController(cardID, ctypes.byref(retval))
    return retval.value


def GetFirstDevice():
    try:
        return _internalLObj.GetFirstDevice()
    except Exception:
        return None


def GetNumberOfDevices():
    return _internalLObj.GetNumberOfDevices()

def GetDeviceHandles(numberOfDevices):
    pNOD = ctypes.c_uint(numberOfDevices)
    arr = (ctypes.c_uint * numberOfDevices)()
    _internalLObj.GetDeviceHandles(arr, ctypes.byref(pNOD))
    nparr = np.fromiter(arr, dtype=np.uint, count=pNOD.value)
    return nparr
    
def GetFirstDeviceByType(DeviceTypeID):
    return _internalLObj.GetFirstDeviceByType(DeviceTypeID)

def OpenDevice(cardID):
    _internalLObj.OpenDevice(cardID)

def CloseDevice(cardID):
    _internalLObj.CloseDevice(cardID)

def IsDeviceOpen(cardID):
    return _internalLObj.IsDeviceOpen()

def SetGPCIFile(pathString):
    pin = ctypes.c_char_p(pathString)
    _internalLObj.SetGPCIFile(pin, len(pathString))


#%% PWM Output


def PWM_StartOutput(cardID):
    _internalLObj.PWM_StartOutput(cardID)
def PWM_StopOutput(cardID):
    _internalLObj.PWM_StartOutput(cardID)
def PWM_PreparePWMOutput(cardID, channelID, StartFrequency, nStartRatio):
    _internalLObj.PWM_PreparePWMOutput(cardID, channelID, StartFrequency, nStartRatio)
def PWM_PrepareFMOutput(cardID, channelID, StartFrequency, nPulsWidthRatio):
    _internalLObj.PWM_PrepareFMOutput(cardID, channelID, StartFrequency, nPulsWidthRatio)
def PWM_WriteNewPWMRatio(cardID, channelID, nRatio):
    _internalLObj.PWM_WriteNewPWMRatio(cardID, channelID, nRatio)
def PWM_WriteNewFMFrequency(cardID, channelID, Frequency):
    _internalLObj.PWM_WriteNewFMFrequency(cardID, channelID, Frequency)
def PWM_GetPWMRatio(cardID, channelID):
    retval = ctypes.c_uint(0)
    _internalLObj.PWM_GetPWMRatio(cardID, channelID,ctypes.byref(retval))
    return retval.value
def PWM_GetFMFrequency(cardID, channelID):
    retval = ctypes.c_uint(0)
    _internalLObj.PWM_GetFMFrequency(cardID, channelID,ctypes.byref(retval))
    return retval.value
    
#%% Realtime Functions
    
def Realtime_DesignIIRFilter( SampleRate, FilterType, CutoffFreqency, CutoffFreqency2,  FrequenciesAreNormalized,
                      Passabsorbtion, Stopbandattenuation, DesignMethod, Order):
    # Ausgabe: int* AOFilterMode, double AOCoefficientsList[], double* AOGain = NULL):
    retFilterMode =  ctypes.c_uint(0)
    retGain =  ctypes.c_double(0)   
      
    numberOfCoefficientValues = (Order+1) * 3
    arrCoefficientsList = (ctypes.c_double * numberOfCoefficientValues)()

    _internalLObj.Realtime_DesignIIRFilter(SampleRate, FilterType, CutoffFreqency, CutoffFreqency2,  FrequenciesAreNormalized, Passabsorbtion, Stopbandattenuation,DesignMethod, Order,ctypes.byref(retFilterMode),arrCoefficientsList,ctypes.byref(retGain))
    retCoefficientsList = np.fromiter(arrCoefficientsList, dtype=np.double, count=numberOfCoefficientValues)
    print(numberOfCoefficientValues)
    return retFilterMode, retCoefficientsList, retGain 											


def Realtime_DesignFIRFilter(  SampleRate, FilterType, CutoffFreqLow, CutoffFreqHigh,  FrequenciesAreNormalized,
                                           Order, FilterWindow, AIWindowParameter, ScalePassband):

    # Ausgabe: uint* AOFilterMode, double AOCoefficientsList[]);	
    retFilterMode =  ctypes.c_uint(0)
    numberOfCoefficientValues = Order+1
    arrCoefficientsList = (ctypes.c_double * numberOfCoefficientValues)() 
    _internalLObj.Realtime_DesignFIRFilter(  SampleRate, FilterType, CutoffFreqLow, CutoffFreqHigh,  FrequenciesAreNormalized, Order, FilterWindow, AIWindowParameter, ScalePassband,ctypes.byref(retFilterMode),arrCoefficientsList)    
    retCoefficientsList = np.fromiter(arrCoefficientsList, dtype=np.double, count=numberOfCoefficientValues) 
    return retFilterMode, retCoefficientsList 											

def Realtime_AddFilterEntry(cardID, ChannelListEntry, FilterMode, FilterOrder, numpyDoubleArrayWithCoefficients, OutputGainFactor):
    retval = ctypes.c_uint(0) # IndexInChannelsRTList
    _internalLObj.Realtime_AddFilterEntry(cardID, ChannelListEntry, FilterMode, FilterOrder, ctypes.c_double(numpyDoubleArrayWithCoefficients.ctypes.data) , OutputGainFactor,ctypes.byref(retval))
    return retval.value    


def Realtime_AddTriggerEntry(cardID, channelListID, nStartTriggerAktiv,  dStartSchwellwert1,  dStartSchwellwert2,  nStartTriggerTyp, 
                             nStartEnableAtStart, nStartTriggerMessung, nStartTriggerSetTTL, nStartTriggerTTLKlemme, nStartTriggerTTLZustand, nStartTriggerTTLFlanke, 
                             nStopTriggerAktiv,  dStopSchwellwert1,  dStopSchwellwert2,  nStopTriggerTyp, nStopEnableAtStart, nStopTriggerMessung, nStopTriggerSetTTL, nStopTriggerTTLKlemme, nStopTriggerTTLZustand, nStopTriggerTTLFlanke, nRetriggerbar):
    retval = ctypes.c_uint(0) # IndexInChannelsRTList
    _internalLObj.Realtime_AddTriggerEntry(cardID, channelListID, nStartTriggerAktiv,  dStartSchwellwert1,  dStartSchwellwert2, nStartTriggerTyp, nStartEnableAtStart, nStartTriggerMessung, nStartTriggerSetTTL, nStartTriggerTTLKlemme, nStartTriggerTTLZustand, nStartTriggerTTLFlanke, nStopTriggerAktiv,  dStopSchwellwert1,  dStopSchwellwert2, nStopTriggerTyp, nStopEnableAtStart, nStopTriggerMessung, nStopTriggerSetTTL, nStopTriggerTTLKlemme, nStopTriggerTTLZustand, nStopTriggerTTLFlanke, nRetriggerbar,ctypes.byref(retval))
    return retval.value 												

def Realtime_AddPIDEntry(cardID, channelListID, P, I, D, PIDType,  Gain, NominalValue, MinValue, MaxValue, DAChannelID, SampleFreq):
    retval = ctypes.c_uint(0) # IndexInChannelsRTList
    _internalLObj.Realtime_AddPIDEntry(cardID, channelListID, P, I, D, PIDType,  Gain, NominalValue, MinValue, MaxValue, DAChannelID, SampleFreq,ctypes.byref(retval))
    return retval.value 
def Realtime_ChangePID_Params(cardID, channelListID, RTListID , newP, newI, newD):
    _internalLObj.Realtime_ChangePID_Params(cardID, channelListID, RTListID , newP, newI, newD)
    
def Realtime_ChangePID_NominalValue(cardID, channelListID, RTListID , newNominalValue):
    _internalLObj.Realtime_ChangePID_NominalValue(cardID, channelListID, RTListID , newNominalValue)
    
def Realtime_AddFFTEntry(cardID, channelListID, nAnzahlPunkte, Spektrum, Gain, FensterFunktion, extraParameter):
    retval = ctypes.c_uint(0) # IndexInChannelsRTList
    _internalLObj.Realtime_AddFFTEntry(cardID, channelListID, nAnzahlPunkte, Spektrum, Gain, FensterFunktion, extraParameter,ctypes.byref(retval))
    return retval.value 

def Realtime_FFT_ReadData(cardID, channelListID, numberOfValues):
    nValues = ctypes.c_uint(numberOfValues)
    arr = (ctypes.c_double * numberOfValues)()
    _internalLObj.Realtime_FFT_ReadData(cardID, channelListID, arr, ctypes.byref(nValues),)
    nparr = np.fromiter(arr, dtype=np.double, count=nValues.value)
    return nparr

#%% SSI Functions

def SSI_SetBitWidth(cardID, nBitWidth):
    _internalLObj.SSI_SetBitWidth(cardID, nBitWidth)

def SSI_ConfigSSI(cardID, nReset, nResetEdge, nActivePassiveMode, nClockFrequency, nEdge):
    _internalLObj.SSI_ConfigSSI(cardID, nReset, nResetEdge, nActivePassiveMode, nClockFrequency, nEdge)

#%% TTL Functions

def TTL_ClearChannelList(cardID):
    _internalLObj.TTL_ClearChannelList(cardID)

def TTL_AddChannelToList(cardID, channelID, bToADList, DigitalTypeID):
    _internalLObj.TTL_AddChannelToList(cardID, channelID, bToADList, DigitalTypeID)

def TTL_GetChannelListSize(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.TTL_GetChannelListSize(cardID,ctypes.byref(retval))
    return retval.value

def TTL_SetFrequency(cardID, fFrequency):
    _internalLObj.TTL_SetFrequency(cardID, fFrequency)

def TTL_SetChannelDirection(cardID, channelID, DirectionID):
    _internalLObj.TTL_SetChannelDirection(cardID, channelID, DirectionID)

def TTL_GetChannelDirection(cardID, channelID):
    retval = ctypes.c_uint(0)
    _internalLObj.TTL_GetChannelDirection(cardID, channelID,ctypes.byref(retval))
    return retval.value

def TTL_GetBurstSizeInBytes(cardID, numberOfValues, burstSize):
    retval = ctypes.c_uint(0)
    _internalLObj.TTL_GetBurstSize(cardID,ctypes.byref(retval))
    return retval.value

def TTL_ReadData(cardID, numberOfValues, burstSize):
    nValuesPerChannel = ctypes.c_uint(numberOfValues)
    nbytesinburst = ctypes.c_uint(burstSize)
    arr = (ctypes.c_char * numberOfValues* burstSize)()
    _internalLObj.TTL_ReadDataExt(cardID,  arr, ctypes.byref(nValuesPerChannel), nbytesinburst, None, None)
    nparr = np.fromiter(arr, dtype=np.uint8, count=burstSize*nValuesPerChannel.value)
    return nparr


def TTL_ReadPort(cardID, PortID):
    retval = ctypes.c_uint(0)
    _internalLObj.TTL_ReadPort(cardID, PortID,ctypes.byref(retval))
    return retval.value

def TTL_WritePort(cardID, PortID, nPortValue):
    _internalLObj.TTL_WritePort(cardID, PortID, nPortValue)

def TTL_ReadBit(cardID, channelID):
    retval = ctypes.c_uint(0)
    _internalLObj.TTL_ReadBit(cardID, channelID,ctypes.byref(retval))
    return retval.value

def TTL_WriteBit(cardID, channelID, nBit):
    _internalLObj.TTL_WriteBit(cardID, channelID, nBit)
 
def TTL_GetStreamPipeLevel(cardID):
    retval = ctypes.c_double(0)
    _internalLObj.TTL_GetStreamPipeLevel(cardID,ctypes.byref(retval))
    return retval.value
def TTL_GetNumberOfValues(cardID):
    retval = ctypes.c_uint(0)
    _internalLObj.TTL_GetNumberOfValues(cardID,ctypes.byref(retval))
    return retval.value
def TTL_InitializeTargetSettings(cardID):
    _internalLObj.TTL_InitializeTargetSettings(cardID)
def TTL_StartMeasure(cardID):
    _internalLObj.TTL_StartMeasure(cardID)
def TTL_StopMeasure(cardID):
    _internalLObj.TTL_StopMeasure(cardID)
def TTL_GetPortInfos(cardID, NumberOfPorts, PortWidth, NumberOfDigIn, NumberOfDigOut):
    r1 = ctypes.c_uint(0)
    r2 = ctypes.c_uint(0)
    r3 = ctypes.c_uint(0)
    r4 = ctypes.c_uint(0)
    _internalLObj.TTL_GetPortInfos(cardID,ctypes.byref(r1), ctypes.byref(r2),ctypes.byref(r3),ctypes.byref(r4))
    retDict = {"NumberOfPorts" : r1.value, "PortWidth": r2.value,"NumberOfDigIn" : r3.value, "NumberOfDigOut": r4.value}
    return retDict

#%% private Functions

def _getMAILibObject():
    folder = os.path.dirname( os.path.abspath( inspect.getfile(_getMAILibObject)))
    if sys.platform == 'darwin':
        return ctypes.CDLL('/usr/lib/libmaiv2dll.dylib')
    if sys.platform == 'win32':
        print('recognized win', platform.architecture())
        path = os.path.join(folder, r"x64/maiv2dll.dll")
        if platform.architecture()[0] == '32bit':
            return ctypes.PyDLL(path, use_errno=True)
        else:
            print('dll read')
            return ctypes.PyDLL(path, use_errno=True)
    # linux pfade :
    if platform.architecture()[0] == '32bit':
         return ctypes.PyDLL(os.path.join(folder, 'libmaiv2dll.so'))
    else:
         return ctypes.PyDLL(os.path.join(folder, 'x64/libmaiv2dll.so'))


def _maierrhandleNoResult(result, func, arguments):
    global _internalLObj
    devnum = 0
    if len(arguments) > 0 : 
        devnum = arguments[0]
    if result < 0 :
        s = ctypes.create_string_buffer(0, 200)
        _internalLObj.GetErrorDescription(devnum,result,s)
        print(result)
        raise Exception('MAI ERROR !', func.__name__ + ': '+ str(s.value))
        
    return result

def _maierrhandle(result, func, arguments):
    _maierrhandleNoResult(result, func, arguments)
    return result

def _getFunctionPointers(maiv2libobject):
    global _internalLObj
    
    _internalLObj = maiv2libobject

    _internalLObj.AD_ClearChannelList.argtypes = [ctypes.c_uint]
    _internalLObj.AD_ClearChannelList.restype = ctypes.c_int 
    _internalLObj.AD_ClearChannelList.errcheck = _maierrhandleNoResult
  

    _internalLObj.AD_AddChannelToList.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.AD_AddChannelToList.restype = ctypes.c_int 
    _internalLObj.AD_AddChannelToList.errcheck = _maierrhandleNoResult
 
   
    _internalLObj.AD_GetChannelListSize.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.AD_GetChannelListSize.restype = ctypes.c_int 
    _internalLObj.AD_GetChannelListSize.errcheck = _maierrhandle

    
    _internalLObj.AD_ReadSingleValue.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]
    _internalLObj.AD_ReadSingleValue.restype = ctypes.c_int 
    _internalLObj.AD_ReadSingleValue.errcheck = _maierrhandle
    
    
    _internalLObj.AD_ReadSingleVoltage.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    _internalLObj.AD_ReadSingleVoltage.restype = ctypes.c_int 
    _internalLObj.AD_ReadSingleVoltage.errcheck = _maierrhandle
    
    _internalLObj.AD_SetFrequency.argtypes = [ctypes.c_uint, ctypes.c_double]
    _internalLObj.AD_SetFrequency.restype = ctypes.c_int 
    _internalLObj.AD_SetFrequency.errcheck = _maierrhandle
  
    
    _internalLObj.AD_GetFrequency.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    _internalLObj.AD_GetFrequency.restype = ctypes.c_int 
    _internalLObj.AD_GetFrequency.errcheck = _maierrhandle
      
    _internalLObj.AD_ReadData.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.c_uint]
    _internalLObj.AD_ReadData.restype = ctypes.c_int 
    _internalLObj.AD_ReadData.errcheck = _maierrhandle
    
    _internalLObj.AD_ReadBinaryData.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.AD_ReadBinaryData.restype = ctypes.c_int 
    _internalLObj.AD_ReadBinaryData.errcheck = _maierrhandle
    
    _internalLObj.AD_GetStreamPipeLevel.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    _internalLObj.AD_GetStreamPipeLevel.restype = ctypes.c_int 
    _internalLObj.AD_GetStreamPipeLevel.errcheck = _maierrhandle
    
    
    _internalLObj.AD_GetNumberOfValues.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.AD_GetNumberOfValues.restype = ctypes.c_int 
    _internalLObj.AD_GetNumberOfValues.errcheck = _maierrhandle
    
    _internalLObj.AD_StartMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.AD_StartMeasure.restype = ctypes.c_int 
    _internalLObj.AD_StartMeasure.errcheck = _maierrhandle
    
    _internalLObj.AD_StopMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.AD_StopMeasure.restype = ctypes.c_int 
    _internalLObj.AD_StopMeasure.errcheck = _maierrhandle
    
    _internalLObj.AD_SetIEPE.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.AD_SetIEPE.restype = ctypes.c_int 
    _internalLObj.AD_SetIEPE.errcheck = _maierrhandle
    
    _internalLObj.AD_SetIEPEOnAudioModul.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.AD_SetIEPEOnAudioModul.restype = ctypes.c_int 
    _internalLObj.AD_SetIEPEOnAudioModul.errcheck = _maierrhandle
    
    
    _internalLObj.AD_SetEventToBeRaisedWhenNumberOfBurstsAvailable.argtypes = [ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
    _internalLObj.AD_SetIEPEOnAudioModul.restype = ctypes.c_int 
    _internalLObj.AD_SetIEPEOnAudioModul.errcheck = _maierrhandle
    
    _internalLObj.AD_Audio_SetHPFilter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.AD_Audio_SetHPFilter.restype = ctypes.c_int 
    _internalLObj.AD_Audio_SetHPFilter.errcheck = _maierrhandle
    
    _internalLObj.AD_Audio_SetHPFilterResponse.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.AD_Audio_SetHPFilterResponse.restype = ctypes.c_int 
    _internalLObj.AD_Audio_SetHPFilterResponse.errcheck = _maierrhandle
    
    _internalLObj.AD_ResetIEPE.argtypes = [ctypes.c_uint]
    _internalLObj.AD_ResetIEPE.restype = ctypes.c_int 
    _internalLObj.AD_ResetIEPE.errcheck = _maierrhandle
    
    _internalLObj.AD_GetIEPEType.argtypes = [ctypes.c_uint]
    _internalLObj.AD_GetIEPEType.restype = ctypes.c_int 
    _internalLObj.AD_GetIEPEType.errcheck = _maierrhandle

    _internalLObj.CT_ClearChannelList.argtypes = [ctypes.c_uint]
    _internalLObj.CT_ClearChannelList.restype = ctypes.c_int 
    _internalLObj.CT_ClearChannelList.errcheck = _maierrhandle
    
    _internalLObj.CT_GetChannelListSize.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetChannelListSize.restype = ctypes.c_int 
    _internalLObj.CT_GetChannelListSize.errcheck = _maierrhandle
    
    _internalLObj.CT_SetFrequency.argtypes = [ctypes.c_uint, ctypes.c_double]
    _internalLObj.CT_SetFrequency.restype = ctypes.c_int 
    _internalLObj.CT_SetFrequency.errcheck = _maierrhandle
    
    _internalLObj.CT_GetFrequency.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    _internalLObj.CT_GetFrequency.restype = ctypes.c_int 
    _internalLObj.CT_GetFrequency.errcheck = _maierrhandle
    
    _internalLObj.CT_SetCounterParameter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_SetCounterParameter.restype = ctypes.c_int 
    _internalLObj.CT_SetCounterParameter.errcheck = _maierrhandle
    
    _internalLObj.CT_GetCounterParameter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint,  ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetCounterParameter.restype = ctypes.c_int 
    _internalLObj.CT_GetCounterParameter.errcheck = _maierrhandle
    
    _internalLObj.CT_GetCounterParametersForMode.argtypes = [ctypes.c_uint, ctypes.c_uint,  ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetCounterParametersForMode.restype = ctypes.c_int 
    _internalLObj.CT_GetCounterParametersForMode.errcheck = _maierrhandle
    
    _internalLObj.CT_GetCounterParameterBoundaries.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetCounterParameterBoundaries.restype = ctypes.c_int 
    _internalLObj.CT_GetCounterParameterBoundaries.errcheck = _maierrhandle
    

    _internalLObj.CT_GetAvailableCounterModes.argtypes = [ctypes.c_uint, ctypes.c_uint,  ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetAvailableCounterModes.restype = ctypes.c_int 
    _internalLObj.CT_GetAvailableCounterModes.errcheck = _maierrhandle
    

    _internalLObj.CT_SetCounterMode.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_SetCounterMode.restype = ctypes.c_int 
    _internalLObj.CT_SetCounterMode.errcheck = _maierrhandle
    
    _internalLObj.CT_GetCounterMode.argtypes = [ctypes.c_uint, ctypes.c_uint,  ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetCounterMode.restype = ctypes.c_int 
    _internalLObj.CT_GetCounterMode.errcheck = _maierrhandle
     
    _internalLObj.CT_ImpulseCounter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_ImpulseCounter.restype = ctypes.c_int 
    _internalLObj.CT_ImpulseCounter.errcheck = _maierrhandle
    
    _internalLObj.CT_FrequencyCounter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_FrequencyCounter.restype = ctypes.c_int 
    _internalLObj.CT_FrequencyCounter.errcheck = _maierrhandle
    
    _internalLObj.CT_PeriodCounter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_PeriodCounter.restype = ctypes.c_int 
    _internalLObj.CT_PeriodCounter.errcheck = _maierrhandle
    
    _internalLObj.CT_PulswidthCounter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_PulswidthCounter.restype = ctypes.c_int 
    _internalLObj.CT_PulswidthCounter.errcheck = _maierrhandle
    
    _internalLObj.CT_IncrementalCounter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_IncrementalCounter.restype = ctypes.c_int 
    _internalLObj.CT_IncrementalCounter.errcheck = _maierrhandle
    
    _internalLObj.CT_IncrementalCounterExtensionTime.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_IncrementalCounterExtensionTime.restype = ctypes.c_int 
    _internalLObj.CT_IncrementalCounterExtensionTime.errcheck = _maierrhandle
    
    
    _internalLObj.CT_IncrementalCounterExtensionFlow.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_IncrementalCounterExtensionFlow.restype = ctypes.c_int 
    _internalLObj.CT_IncrementalCounterExtensionFlow.errcheck = _maierrhandle
    
    
    _internalLObj.CT_UpDownCounter.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_UpDownCounter.restype = ctypes.c_int 
    _internalLObj.CT_UpDownCounter.errcheck = _maierrhandle
    
    
    _internalLObj.CT_ScaleData.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]
    _internalLObj.CT_ScaleData.restype = ctypes.c_int 
    _internalLObj.CT_ScaleData.errcheck = _maierrhandle
    
    
    _internalLObj.CT_ReadData.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.c_uint]
    _internalLObj.CT_ReadData.restype = ctypes.c_int 
    _internalLObj.CT_ReadData.errcheck = _maierrhandle
    

    _internalLObj.CT_ReadSingleValue.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_ReadSingleValue.restype = ctypes.c_int 
    _internalLObj.CT_ReadSingleValue.errcheck = _maierrhandle
    
    
    _internalLObj.CT_GetStreamPipeLevel.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    _internalLObj.CT_GetStreamPipeLevel.restype = ctypes.c_int 
    _internalLObj.CT_GetStreamPipeLevel.errcheck = _maierrhandle
    
    
    _internalLObj.CT_GetNumberOfValues.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetNumberOfValues.restype = ctypes.c_int 
    _internalLObj.CT_GetNumberOfValues.errcheck = _maierrhandle
    
    
    _internalLObj.CT_StartMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.CT_StartMeasure.restype = ctypes.c_int 
    _internalLObj.CT_StartMeasure.errcheck = _maierrhandle
    
    
    _internalLObj.CT_StopMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.CT_StopMeasure.restype = ctypes.c_int 
    _internalLObj.CT_StopMeasure.errcheck = _maierrhandle
    
    
    _internalLObj.CT_GetIncrementalCounterDirections.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.CT_GetIncrementalCounterDirections.restype = ctypes.c_int 
    _internalLObj.CT_GetIncrementalCounterDirections.errcheck = _maierrhandle
    
    _internalLObj.DA_SetRange.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.DA_SetRange.restype = ctypes.c_int 
    _internalLObj.DA_SetRange.errcheck = _maierrhandle
    
    _internalLObj.DA_ClearChannelList.argtypes = [ctypes.c_uint]
    _internalLObj.DA_ClearChannelList.restype = ctypes.c_int 
    _internalLObj.DA_ClearChannelList.errcheck = _maierrhandle
    
    _internalLObj.DA_AddChannelToList.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.DA_AddChannelToList.restype = ctypes.c_int 
    _internalLObj.DA_AddChannelToList.errcheck = _maierrhandle
    
    _internalLObj.DA_GetChannelListSize.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.DA_GetChannelListSize.restype = ctypes.c_int 
    _internalLObj.DA_GetChannelListSize.errcheck = _maierrhandle
    
    _internalLObj.DA_SetFrequency.argtypes = [ctypes.c_uint, ctypes.c_double]
    _internalLObj.DA_SetFrequency.restype = ctypes.c_int 
    _internalLObj.DA_SetFrequency.errcheck = _maierrhandle
    
    _internalLObj.DA_StartOutput.argtypes = [ctypes.c_uint]
    _internalLObj.DA_StartOutput.restype = ctypes.c_int 
    _internalLObj.DA_StartOutput.errcheck = _maierrhandle
    
    _internalLObj.DA_StopOutput.argtypes = [ctypes.c_uint]
    _internalLObj.DA_StopOutput.restype = ctypes.c_int 
    _internalLObj.DA_StopOutput.errcheck = _maierrhandle
    
    _internalLObj.DA_WriteChannelRaw.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int]
    _internalLObj.DA_WriteChannelRaw.restype = ctypes.c_int 
    _internalLObj.DA_WriteChannelRaw.errcheck = _maierrhandle
    
    
    _internalLObj.DA_WriteChannelVoltage.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_double]
    _internalLObj.DA_WriteChannelVoltage.restype = ctypes.c_int 
    _internalLObj.DA_WriteChannelVoltage.errcheck = _maierrhandle
    
    
    _internalLObj.DA_WriteRawData.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]
    _internalLObj.DA_WriteRawData.restype = ctypes.c_int 
    _internalLObj.DA_WriteRawData.errcheck = _maierrhandle
    
    
    _internalLObj.DA_WriteScaledData.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]
    _internalLObj.DA_WriteScaledData.restype = ctypes.c_int 
    _internalLObj.DA_WriteScaledData.errcheck = _maierrhandle
    
    
    _internalLObj.DA_GetFifoState.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.DA_GetFifoState.restype = ctypes.c_int 
    _internalLObj.DA_GetFifoState.errcheck = _maierrhandle
    
    _internalLObj.DA_Audio_SetMonauralMode.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.DA_Audio_SetMonauralMode.restype = ctypes.c_int 
    _internalLObj.DA_Audio_SetMonauralMode.errcheck = _maierrhandle
    
    
    _internalLObj.DA_Audio_SetADLoopbackMode.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.DA_Audio_SetADLoopbackMode.restype = ctypes.c_int 
    _internalLObj.DA_Audio_SetADLoopbackMode.errcheck = _maierrhandle
    
    
    _internalLObj.ClearAllChannelLists.argtypes = [ctypes.c_uint]
    _internalLObj.ClearAllChannelLists.restype = ctypes.c_int 
    _internalLObj.ClearAllChannelLists.errcheck = _maierrhandle
    
    _internalLObj.ResetDevice.argtypes = [ctypes.c_uint]
    _internalLObj.ResetDevice.restype = ctypes.c_int 
    _internalLObj.ResetDevice.errcheck = _maierrhandle
    
    _internalLObj.LoadFirmware.argtypes = [ctypes.c_uint]
    _internalLObj.LoadFirmware.restype = ctypes.c_int 
    _internalLObj.LoadFirmware.errcheck = _maierrhandle

    _internalLObj.StartMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.StartMeasure.restype = ctypes.c_int 
    _internalLObj.StartMeasure.errcheck = _maierrhandle
    
    
    _internalLObj.StopMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.StopMeasure.restype = ctypes.c_int 
    _internalLObj.StopMeasure.errcheck = _maierrhandle
    
    _internalLObj.SetStreamingMode.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.SetStreamingMode.restype = ctypes.c_int 
    _internalLObj.SetStreamingMode.errcheck = _maierrhandle
    
    _internalLObj.SetRunningMode.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.SetRunningMode.restype = ctypes.c_int 
    _internalLObj.SetRunningMode.errcheck = _maierrhandle
    
    _internalLObj.EnableSoftwareClock.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.EnableSoftwareClock.restype = ctypes.c_int 
    _internalLObj.EnableSoftwareClock.errcheck = _maierrhandle
    
    _internalLObj.ConfigCard.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.ConfigCard.restype = ctypes.c_int 
    _internalLObj.ConfigCard.errcheck = _maierrhandle
    
    
    _internalLObj.SetGlobalTriggerValues.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.SetGlobalTriggerValues.restype = ctypes.c_int 
    _internalLObj.SetGlobalTriggerValues.errcheck = _maierrhandle
    
    
    _internalLObj.ConfigMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.ConfigMeasure.restype = ctypes.c_int 
    _internalLObj.ConfigMeasure.errcheck = _maierrhandle
    
    
    _internalLObj.IdentifierDevice.argtypes = [ctypes.c_uint]
    _internalLObj.IdentifierDevice.restype = ctypes.c_int 
    _internalLObj.IdentifierDevice.errcheck = _maierrhandle
    
    _internalLObj.IsUSBHighSpeed.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.IsUSBHighSpeed.restype = ctypes.c_int 
    _internalLObj.IsUSBHighSpeed.errcheck = _maierrhandle
    
    
    
    _internalLObj.RemoteDeviceConnect.argtypes = [ctypes.c_uint, ctypes.c_char_p , ctypes.c_int, ctypes.c_bool, ctypes.POINTER(ctypes.c_bool)] 
    _internalLObj.RemoteDeviceConnect.restype = ctypes.c_int 
    _internalLObj.RemoteDeviceConnect.errcheck = _maierrhandle    
    
    _internalLObj.RemoteDeviceDisconnect.argtypes = [ctypes.c_uint]
    _internalLObj.RemoteDeviceDisconnect.restype = ctypes.c_int 
    _internalLObj.RemoteDeviceDisconnect.errcheck = _maierrhandle   

    _internalLObj.RemoteDevicesSearch.argtypes = []
    _internalLObj.RemoteDevicesSearch.restype = ctypes.c_int 
    _internalLObj.RemoteDevicesSearch.errcheck = _maierrhandle   
    
    _internalLObj.RemoteDevicesSearchAndConnectAll.argtypes = []
    _internalLObj.RemoteDevicesSearchAndConnectAll.restype = ctypes.c_int 
    _internalLObj.RemoteDevicesSearchAndConnectAll.errcheck = _maierrhandle   
    
    _internalLObj.RemoteDevicesGetIPFromSearchResult.argtypes = [ctypes.c_uint, ctypes.c_char_p , ctypes.c_int ] 
    _internalLObj.RemoteDevicesGetIPFromSearchResult.restype = ctypes.c_int 
    _internalLObj.RemoteDevicesGetIPFromSearchResult.errcheck = _maierrhandle   
    
    _internalLObj.RemoteDeviceGetIPFromPoolHandle.argtypes  = [ctypes.c_uint, ctypes.c_char_p , ctypes.c_int, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_int)]
    _internalLObj.RemoteDeviceGetIPFromPoolHandle.restype = ctypes.c_int 
    _internalLObj.RemoteDeviceGetIPFromPoolHandle.errcheck = _maierrhandle   
    

    _internalLObj.GetCardName.argtypes = [ctypes.c_uint]
    _internalLObj.GetCardName.restype = ctypes.c_char_p
    
    _internalLObj.GetCardProducer.argtypes = [ctypes.c_uint]
    _internalLObj.GetCardProducer.restype = ctypes.c_char_p

    _internalLObj.GetCardSeller.argtypes = [ctypes.c_uint]
    _internalLObj.GetCardSeller.restype = ctypes.c_char_p
    
    _internalLObj.GetManufacture_Name.argtypes = [ctypes.c_uint]
    _internalLObj.GetManufacture_Name.restype = ctypes.c_char_p
    
    _internalLObj.GetSerialNumber.argtypes = [ctypes.c_uint]
    _internalLObj.GetSerialNumber.restype = ctypes.c_char_p

    _internalLObj.GetCustomer_Name.argtypes = [ctypes.c_uint]
    _internalLObj.GetCustomer_Name.restype = ctypes.c_char_p
    
    _internalLObj.GetCustomer_Number.argtypes = [ctypes.c_uint]
    _internalLObj.GetCustomer_Number.restype = ctypes.c_char_p
    
    _internalLObj.GetCustomer_DateOfPurchase.argtypes = [ctypes.c_uint]
    _internalLObj.GetCustomer_DateOfPurchase.restype = ctypes.c_char_p
    
    _internalLObj.GetADChannels.argtypes = [ctypes.c_uint]
    _internalLObj.GetADChannels.restype = ctypes.c_int 
    _internalLObj.GetADChannels.errcheck = _maierrhandle
    
    _internalLObj.GetADChannelsNumberOfOversamplingModes.argtypes = [ctypes.c_uint]
    _internalLObj.GetADChannelsNumberOfOversamplingModes.restype = ctypes.c_int 
    _internalLObj.GetADChannelsNumberOfOversamplingModes.errcheck = _maierrhandle
    
    _internalLObj.GetADChannelsNumberOfGainModes.argtypes = [ctypes.c_uint]
    _internalLObj.GetADChannelsNumberOfGainModes.restype = ctypes.c_int 
    _internalLObj.GetADChannelsNumberOfGainModes.errcheck = _maierrhandle
    
    _internalLObj.GetADSampleWidth.argtypes = [ctypes.c_uint]
    _internalLObj.GetADSampleWidth.restype = ctypes.c_int 
    _internalLObj.GetADSampleWidth.errcheck = _maierrhandle
    
    _internalLObj.GetADSampleRate.argtypes = [ctypes.c_uint]
    _internalLObj.GetADSampleRate.restype = ctypes.c_int 
    _internalLObj.GetADSampleRate.errcheck = _maierrhandle
    
    _internalLObj.GetDAChannels.argtypes = [ctypes.c_uint]
    _internalLObj.GetDAChannels.restype = ctypes.c_int 
    _internalLObj.GetDAChannels.errcheck = _maierrhandle
    
    _internalLObj.GetDASampleWidth.argtypes = [ctypes.c_uint]
    _internalLObj.GetDASampleWidth.restype = ctypes.c_int 
    _internalLObj.GetDASampleWidth.errcheck = _maierrhandle
    
    _internalLObj.GetDASampleRate.argtypes = [ctypes.c_uint]
    _internalLObj.GetDASampleRate.restype = ctypes.c_int 
    _internalLObj.GetDASampleRate.errcheck = _maierrhandle
    
    _internalLObj.GetTTLChannels.argtypes = [ctypes.c_uint]
    _internalLObj.GetTTLChannels.restype = ctypes.c_int 
    _internalLObj.GetTTLChannels.errcheck = _maierrhandle
    
    _internalLObj.GetTTLSampleWidth.argtypes = [ctypes.c_uint]
    _internalLObj.GetTTLSampleWidth.restype = ctypes.c_int 
    _internalLObj.GetTTLSampleWidth.errcheck = _maierrhandle
    
    _internalLObj.GetTTLSampleRate.argtypes = [ctypes.c_uint]
    _internalLObj.GetTTLSampleRate.restype = ctypes.c_int 
    _internalLObj.GetTTLSampleRate.errcheck = _maierrhandle
    
    _internalLObj.GetCTChannels.argtypes = [ctypes.c_uint]
    _internalLObj.GetCTChannels.restype = ctypes.c_int 
    _internalLObj.GetCTChannels.errcheck = _maierrhandle
    
    _internalLObj.GetCTSampleWidth.argtypes = [ctypes.c_uint]
    _internalLObj.GetCTSampleWidth.restype = ctypes.c_int 
    _internalLObj.GetCTSampleWidth.errcheck = _maierrhandle
    
    _internalLObj.GetCTSampleRate.argtypes = [ctypes.c_uint]
    _internalLObj.GetCTSampleRate.restype = ctypes.c_int 
    _internalLObj.GetCTSampleRate.errcheck = _maierrhandle
    
    _internalLObj.GetPWMChannels.argtypes = [ctypes.c_uint]
    _internalLObj.GetPWMChannels.restype = ctypes.c_int 
    _internalLObj.GetPWMChannels.errcheck = _maierrhandle
    
    _internalLObj.GetPWMSampleWidth.argtypes = [ctypes.c_uint]
    _internalLObj.GetPWMSampleWidth.restype = ctypes.c_int 
    _internalLObj.GetPWMSampleWidth.errcheck = _maierrhandle
    
    _internalLObj.GetPWMSampleRate.argtypes = [ctypes.c_uint]
    _internalLObj.GetPWMSampleRate.restype = ctypes.c_int 
    _internalLObj.GetPWMSampleRate.errcheck = _maierrhandle
    
    _internalLObj.GetSoftwareExtension.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.GetSoftwareExtension.restype = ctypes.c_int
    _internalLObj.GetSoftwareExtension.errcheck = _maierrhandle
    
    _internalLObj.GetHardwareExtension.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.GetHardwareExtension.restype = ctypes.c_int
    _internalLObj.GetHardwareExtension.errcheck = _maierrhandle
    
    _internalLObj.GetMeasurementProcessorVersion.argtypes = [ctypes.c_uint]
    _internalLObj.GetMeasurementProcessorVersion.restype = ctypes.c_int 
    _internalLObj.GetMeasurementProcessorVersion.errcheck = _maierrhandle
    
    _internalLObj.GetControllerFirmwareVersion.argtypes = [ctypes.c_uint]
    _internalLObj.GetControllerFirmwareVersion.restype = ctypes.c_int 
    _internalLObj.GetControllerFirmwareVersion.errcheck = _maierrhandle
    
    _internalLObj.GetSystemDriverVersion.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_char)]
    _internalLObj.GetSystemDriverVersion.restype = ctypes.c_int 
    _internalLObj.GetSystemDriverVersion.errcheck = _maierrhandle
    
    _internalLObj.PrivateFlashDataRead.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint]
    _internalLObj.PrivateFlashDataRead.restype = ctypes.c_int 
    _internalLObj.PrivateFlashDataRead.errcheck = _maierrhandle
    
    _internalLObj.PrivateFlashDataWrite.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint]
    _internalLObj.PrivateFlashDataWrite.restype = ctypes.c_int 
    _internalLObj.PrivateFlashDataWrite.errcheck = _maierrhandle
    
    _internalLObj.PrivateFlashDataClear.argtypes = [ctypes.c_uint]
    _internalLObj.PrivateFlashDataClear.restype = ctypes.c_int 
    _internalLObj.PrivateFlashDataClear.errcheck = _maierrhandle
    
    _internalLObj.GetDLLVersion.argtypes = []
    _internalLObj.GetDLLVersion.restype = ctypes.c_char_p
    
    _internalLObj.GetLIBVersion.argtypes = []
    _internalLObj.GetLIBVersion.restype = ctypes.c_char_p
    
    _internalLObj.GetCardIDBySerial.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.GetCardIDBySerial.restype = ctypes.c_int 
    _internalLObj.GetCardIDBySerial.errcheck = _maierrhandle
    
    _internalLObj.GetDeviceInfo.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_char)]
    _internalLObj.GetDeviceInfo.restype = ctypes.c_int 
    _internalLObj.GetDeviceInfo.errcheck = _maierrhandle
    
    _internalLObj.GetNumberOfBurstsOnADController.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.GetNumberOfBurstsOnADController.restype = ctypes.c_int 
    _internalLObj.GetNumberOfBurstsOnADController.errcheck = _maierrhandle
    
    _internalLObj.GetNumberOfBurstsOnCTController.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.GetNumberOfBurstsOnCTController.restype = ctypes.c_int 
    _internalLObj.GetNumberOfBurstsOnCTController.errcheck = _maierrhandle
    
    _internalLObj.AlteraRegisterRead.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.AlteraRegisterRead.restype = ctypes.c_int 
    _internalLObj.AlteraRegisterRead.errcheck = _maierrhandle
    
    _internalLObj.AlteraRegisterWrite.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
    _internalLObj.AlteraRegisterWrite.restype = ctypes.c_int 
    _internalLObj.AlteraRegisterWrite.errcheck = _maierrhandle
    
    
    _internalLObj.GetFirstDevice.argtypes = []
    _internalLObj.GetFirstDevice.restype = ctypes.c_int 
    _internalLObj.GetFirstDevice.errcheck = _maierrhandle
    
    _internalLObj.GetNumberOfDevices.argtypes = []
    _internalLObj.GetNumberOfDevices.restype = ctypes.c_int 
    _internalLObj.GetNumberOfDevices.errcheck = _maierrhandle
    
    _internalLObj.GetDeviceHandles.argtypes = [ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.GetDeviceHandles.restype = ctypes.c_int 
    _internalLObj.GetDeviceHandles.errcheck = _maierrhandle
    
    
    _internalLObj.GetFirstDeviceByType.argtypes = [ctypes.c_uint]
    _internalLObj.GetFirstDeviceByType.restype = ctypes.c_int 
    _internalLObj.GetFirstDeviceByType.errcheck = _maierrhandle
    
    
    _internalLObj.IsDeviceOpen = maiv2libobject.IsDeviceOpen
    _internalLObj.IsDeviceOpen.argtypes = [ctypes.c_uint]
    _internalLObj.IsDeviceOpen.restype = ctypes.c_int 
    _internalLObj.IsDeviceOpen.errcheck = _maierrhandle
    
    _internalLObj.GetErrorDescription.argtypes = [ctypes.c_uint, ctypes.c_long, ctypes.POINTER(ctypes.c_char)]
    _internalLObj.GetErrorDescription.restype = ctypes.c_int 
    _internalLObj.GetErrorDescription.errcheck = _maierrhandle
    
    _internalLObj.SetGPCIFile.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.c_uint]
    _internalLObj.SetGPCIFile.restype = ctypes.c_int 
    _internalLObj.SetGPCIFile.errcheck = _maierrhandle
    
    _internalLObj.GetGPCIFilePath.argtypes = []
    _internalLObj.GetGPCIFilePath.restype = ctypes.c_char_p
    
    
    _internalLObj.PWM_StartOutput.argtypes = [ctypes.c_uint]
    _internalLObj.PWM_StartOutput.restype = ctypes.c_int 
    _internalLObj.PWM_StartOutput.errcheck = _maierrhandle
    
    _internalLObj.PWM_StopOutput.argtypes = [ctypes.c_uint]
    _internalLObj.PWM_StopOutput.restype = ctypes.c_int 
    _internalLObj.PWM_StopOutput.errcheck = _maierrhandle
    
    _internalLObj.PWM_PreparePWMOutput.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.PWM_PreparePWMOutput.restype = ctypes.c_int 
    _internalLObj.PWM_PreparePWMOutput.errcheck = _maierrhandle
    
    _internalLObj.PWM_PrepareFMOutput.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.PWM_PrepareFMOutput.restype = ctypes.c_int 
    _internalLObj.PWM_PrepareFMOutput.errcheck = _maierrhandle
    
    _internalLObj.PWM_WriteNewPWMRatio.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.PWM_WriteNewPWMRatio.restype = ctypes.c_int 
    _internalLObj.PWM_WriteNewPWMRatio.errcheck = _maierrhandle
    
    _internalLObj.PWM_WriteNewFMFrequency.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.PWM_WriteNewFMFrequency.restype = ctypes.c_int 
    _internalLObj.PWM_WriteNewFMFrequency.errcheck = _maierrhandle
    
    _internalLObj.PWM_GetPWMRatio.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.PWM_GetPWMRatio.restype = ctypes.c_int 
    _internalLObj.PWM_GetPWMRatio.errcheck = _maierrhandle
    
    _internalLObj.PWM_GetFMFrequency.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.PWM_GetFMFrequency.restype = ctypes.c_int 
    _internalLObj.PWM_GetFMFrequency.errcheck = _maierrhandle
    
    _internalLObj.Realtime_AddTriggerEntry.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.Realtime_AddTriggerEntry.restype = ctypes.c_int 
    _internalLObj.Realtime_AddTriggerEntry.errcheck = _maierrhandle
    
    _internalLObj.Realtime_AddFilterEntry.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.Realtime_AddFilterEntry.restype = ctypes.c_int 
    _internalLObj.Realtime_AddFilterEntry.errcheck = _maierrhandle
    
    _internalLObj.Realtime_DesignFIRFilter.argtypes =  [ctypes.c_double, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_bool ,ctypes.c_uint, ctypes.c_uint, ctypes.c_double, ctypes.c_bool ,  ctypes.POINTER(ctypes.c_uint),ctypes.POINTER(ctypes.c_double)]
    _internalLObj.Realtime_DesignFIRFilter.restype = ctypes.c_int 
    _internalLObj.Realtime_DesignFIRFilter.errcheck = _maierrhandle    
 
    _internalLObj.Realtime_DesignIIRFilter.argtypes = [ctypes.c_double, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_bool ,ctypes.c_double,ctypes.c_double, ctypes.c_uint,ctypes.c_uint,  ctypes.POINTER(ctypes.c_uint),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double) ]
    _internalLObj.Realtime_DesignIIRFilter.restype = ctypes.c_int 
    _internalLObj.Realtime_DesignIIRFilter.errcheck = _maierrhandle       
    
    _internalLObj.Realtime_AddPIDEntry.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_double, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.Realtime_AddPIDEntry.restype = ctypes.c_int 
    _internalLObj.Realtime_AddPIDEntry.errcheck = _maierrhandle
    
    _internalLObj.Realtime_ChangePID_Params.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    _internalLObj.Realtime_ChangePID_Params.restype = ctypes.c_int 
    _internalLObj.Realtime_ChangePID_Params.errcheck = _maierrhandle
    
    _internalLObj.Realtime_ChangePID_NominalValue.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double]
    _internalLObj.Realtime_ChangePID_NominalValue.restype = ctypes.c_int 
    _internalLObj.Realtime_ChangePID_NominalValue.errcheck = _maierrhandle
    
    _internalLObj.Realtime_AddFFTEntry.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_double, ctypes.c_uint, ctypes.c_double, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.Realtime_AddFFTEntry.restype = ctypes.c_int 
    _internalLObj.Realtime_AddFFTEntry.errcheck = _maierrhandle
    
    _internalLObj.Realtime_FFT_ReadData.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.Realtime_FFT_ReadData.restype = ctypes.c_int 
    _internalLObj.Realtime_FFT_ReadData.errcheck = _maierrhandle
    
    _internalLObj.SSI_SetBitWidth.argtypes = [ctypes.c_uint, ctypes.c_uint]
    _internalLObj.SSI_SetBitWidth.restype = ctypes.c_int 
    _internalLObj.SSI_SetBitWidth.errcheck = _maierrhandle
    
    _internalLObj.SSI_ConfigSSI = maiv2libobject.SSI_ConfigSSI
    _internalLObj.SSI_ConfigSSI.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.SSI_ConfigSSI.restype = ctypes.c_int 
    _internalLObj.SSI_ConfigSSI.errcheck = _maierrhandle
    
    _internalLObj.TTL_ClearChannelList.argtypes = [ctypes.c_uint]
    _internalLObj.TTL_ClearChannelList.restype = ctypes.c_int 
    _internalLObj.TTL_ClearChannelList.errcheck = _maierrhandle
    
    _internalLObj.TTL_GetChannelListSize.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.TTL_GetChannelListSize.restype = ctypes.c_int 
    _internalLObj.TTL_GetChannelListSize.errcheck = _maierrhandle
    
    _internalLObj.TTL_SetFrequency.argtypes = [ctypes.c_uint, ctypes.c_double]
    _internalLObj.TTL_SetFrequency.restype = ctypes.c_int 
    _internalLObj.TTL_SetFrequency.errcheck = _maierrhandle
    
    _internalLObj.TTL_SetChannelDirection.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.TTL_SetChannelDirection.restype = ctypes.c_int 
    _internalLObj.TTL_SetChannelDirection.errcheck = _maierrhandle
    


    _internalLObj.TTL_ReadData.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.c_uint]
    _internalLObj.TTL_ReadData.restype = ctypes.c_int 
    _internalLObj.TTL_ReadData.errcheck = _maierrhandle
  
    _internalLObj.TTL_ReadDataExt.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(ctypes.c_double) ]
    _internalLObj.TTL_ReadDataExt.restype = ctypes.c_int 
    _internalLObj.TTL_ReadDataExt.errcheck = _maierrhandle

    _internalLObj.TTL_GetBurstSize.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint) ]
    _internalLObj.TTL_GetBurstSize.restype = ctypes.c_int 
    _internalLObj.TTL_GetBurstSize.errcheck = _maierrhandle
  
  
    _internalLObj.TTL_ReadPort.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.TTL_ReadPort.restype = ctypes.c_int 
    _internalLObj.TTL_ReadPort.errcheck = _maierrhandle
    
    _internalLObj.TTL_WritePort.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.TTL_WritePort.restype = ctypes.c_int 
    _internalLObj.TTL_WritePort.errcheck = _maierrhandle
    
    _internalLObj.TTL_ReadBit.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.TTL_ReadBit.restype = ctypes.c_int 
    _internalLObj.TTL_ReadBit.errcheck = _maierrhandle
    
    _internalLObj.TTL_WriteBit.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    _internalLObj.TTL_WriteBit.restype = ctypes.c_int 
    _internalLObj.TTL_WriteBit.errcheck = _maierrhandle
    
    _internalLObj.TTL_GetStreamPipeLevel.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    _internalLObj.TTL_GetStreamPipeLevel.restype = ctypes.c_int 
    _internalLObj.TTL_GetStreamPipeLevel.errcheck = _maierrhandle
    
    _internalLObj.TTL_GetNumberOfValues.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.TTL_GetNumberOfValues.restype = ctypes.c_int 
    _internalLObj.TTL_GetNumberOfValues.errcheck = _maierrhandle
    
    _internalLObj.TTL_InitializeTargetSettings.argtypes = [ctypes.c_uint]
    _internalLObj.TTL_InitializeTargetSettings.restype = ctypes.c_int 
    _internalLObj.TTL_InitializeTargetSettings.errcheck = _maierrhandle

    _internalLObj.TTL_StartMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.TTL_StartMeasure.restype = ctypes.c_int 
    _internalLObj.TTL_StartMeasure.errcheck = _maierrhandle

    _internalLObj.TTL_StopMeasure.argtypes = [ctypes.c_uint]
    _internalLObj.TTL_StopMeasure.restype = ctypes.c_int 
    _internalLObj.TTL_StopMeasure.errcheck = _maierrhandle

    _internalLObj.TTL_GetPortInfos.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
    _internalLObj.TTL_GetPortInfos.restype = ctypes.c_int 
    _internalLObj.TTL_GetPortInfos.errcheck = _maierrhandle

    print('imported MAIv2 function pointers')

#%% Added FSC

def get_device_info(id):
    try:
        name = GetCardName(id)
    except:
        ValueError('Device ID not found.')

    function_list = [
        GetCardName,
        GetCardProducer,
        GetCardSeller,
        GetManufacture_Name,
        GetSerialNumber,
        GetCustomer_Name,
        GetCustomer_Number,
        GetCustomer_DateOfPurchase,
        GetADChannels,
        GetADSampleWidth,
        GetADSampleRate,
        GetDAChannels,
        GetDASampleWidth,
        GetDASampleRate,
        GetTTLChannels,
        GetTTLSampleWidth,
        GetTTLSampleRate,
        GetCTChannels,
        GetCTSampleWidth,
        GetCTSampleRate,
        GetPWMChannels,
        GetPWMSampleWidth,
        GetPWMSampleRate,
        #GetSoftwareExtension,
        #GetHardwareExtension,
        GetMeasurementProcessorVersion,
        GetControllerFirmwareVersion,
        GetSystemDriverVersion,
        GetDeviceInfo,
        GetNumberOfBurstsOnADController,
        GetNumberOfBurstsOnCTController
    ]
    return_dict = {}
    for func in function_list:
        key = func.__name__[3:]
        try:
            value = func(id)
        except:
            value = 'function error occurred'
        return_dict[key] = value

    return return_dict

_getFunctionPointers(_getMAILibObject())

if __name__ == "__main__":
    dev_id = 0
    debug=False
    for key, value in get_device_info(dev_id).items():
        if debug:
            print(f"{key}: {value}, {type(value)}")
        else:
            print(f"{key}: {value}")