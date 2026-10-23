unit MAI_Types;

interface

uses
	windows;

type
	TDeviceClass = (DEVICECLASS_BOTH, DEVICECLASS_PCI, DEVICECLASS_USB, DEVICECLASS_USBBASIC, DEVICECLASS_ETH); 
	TOversampling = (oversamplingDISABLED, oversampling2x, oversampling4x, oversampling8x, oversampling16x); 
	TGain = (gainDisabled, gain2x, gain4x, gain8x); 
	TBipolar = (polUNIPOLAR, polBIPOLAR); 
	TPartBlock = (partONLYFULLBLOCKS, partPARTBLOCK); 
	TSkipData = (skipGETCAPTUREDVALUES, skipSKIPCAPTUREDVALUES); 
	TStreamingMode = (smOFF, smON); 
	TCounterMode = (cmIMPULSECOUNTER = 0, cmFREQUENCYCOUNTER = 1, cmPERIODCOUNTER = 2, cmPULSWIDTHCOUNTER = 3, cmINCREMENTALCOUNTER = 4, cmUPDOWNCOUNTER = 5, cmINCREMENTALEXTTIME = 6, cmINCREMENTALEXTFLOW = 7, cmAUDIOCARD_TTL = 8); 
	TCounterModesList = (cmlIMPULSECOUNTER = (1 SHL Integer(cmIMPULSECOUNTER)), cmlPERIODCOUNTER = (1 SHL Integer(cmPERIODCOUNTER)), cmlPULSWIDTHCOUNTER = (1 SHL Integer(cmPULSWIDTHCOUNTER)), cmlFREQUENCYCOUNTER = (1 SHL Integer(cmFREQUENCYCOUNTER)), cmlUPDOWNCOUNTER = (1 SHL Integer(cmUPDOWNCOUNTER)), cmlINCREMENTALCOUNTER = (1 SHL Integer(cmINCREMENTALCOUNTER)), cmlINCREMENTALEXTTIME = (1 SHL Integer(cmINCREMENTALEXTTIME)), cmlINCREMENTALEXTFLOW = (1 SHL Integer(cmINCREMENTALEXTFLOW))); 
	TCounterParam = (ctparamRESOLUTION = 0, ctparamCOMPAREBITWIDTH = 1, ctparamPRESETVALUE = 2, ctparamIMPULSEDIRECTION = 3, ctparamSIGNALEDGE = 4, ctparamEACHPERIOD = 5, ctparamSOFTWARERESET = 6, ctparamHARDWARERESETMODE = 7, ctparamHARDWARERESETEDGE = 8, ctparamINCREMENTINTERPOLATION = 9, ctparamRESOLUTIONFREQUENCY = 10, ctparamRESOLUTIONINCTIMESTAMP = 11); 
	TCounterParamsList = (ctplPRESETVALUE = (1 SHL Integer(ctparamPRESETVALUE)), ctplIMPULSEDIRECTION = (1 SHL Integer(ctparamIMPULSEDIRECTION)), ctplSIGNALEDGE = (1 SHL Integer(ctparamSIGNALEDGE)), ctplRESOLUTIONFREQUENCY = (1 SHL Integer(ctparamRESOLUTIONFREQUENCY)), ctplSOFTWARERESET = (1 SHL Integer(ctparamSOFTWARERESET)), ctplHARDWARERESETMODE = (1 SHL Integer(ctparamHARDWARERESETMODE)), ctplHARDWARERESETEDGE = (1 SHL Integer(ctparamHARDWARERESETEDGE)), ctplINTERPOLATIONMODE = (1 SHL Integer(ctparamINCREMENTINTERPOLATION)), ctplINCREMENTALEXTTIMERESOLUTION = (1 SHL Integer(ctparamRESOLUTIONINCTIMESTAMP))); 
	TTrigger = (trigDISABLED, trigEXTERN_TRIGGER, trigEXTERN_CLOCK); 
	TExternEdge = (tedgeFALLING_EDGE, tedgeRISING_EDGE); 
	TFFT_Type = (fftAbsolute = 0, fftRMS = 1, fftPower = 2, fftPhase = 3); 
	TFFT_Size = (fft_s512 = 0, fft_s1024 = 1, fft_s2048 = 2, fft_s4096 = 3); 
	TTrigger_Type = (trigMax = 0, trigMin = 1, trigUnterSchwelle = 2, trigUeberSchwelle = 3, trigFenster = 4, trigUnterGradientensteigung = 5, trigUeberGradientensteigung = 6, trigGradientenfenster = 7); 
	TPIDControllerType = (pidPID1 = 0, pidPID2 = 1, pidPID3 = 2); 
	TFilterType = (ftLOWPASS = 0, ftHIGHPASS = 1, ftBANDPASS = 2, ftBANDSTOP = 3); 
	TIIRFilterDesign = (iirBUTTERWORTH = 0, iirCHEBYSHEV_T1 = 1, iirCHEBYSHEV_T2 = 2, iirELLIPTIC = 3, iirBESSEL = 4); 
	TFIRWindowFunction = (firwinRectangular = 0, firwinHanning = 1, firwinHamming = 2, firwinBlackman = 3, firwinKaiser = 4, firwinBartlett = 5, firwinDolph_Tschebytschow = 6, firwinTriangular = 7, firwinBlackman_Harris = 8, firwinBlackman_Nuttall = 9, firwinFlat_Top = 10); 
	TSWExtensionsBitNumber = (swxOnline_FFT = 0, swxOnline_Filter = 1, swxOnline_PID = 2, swxOnline_Linearisierung = 3, swxOnboardFunktionsgenerator = 4, swxWabco_Projekt = 9, swxAirbag_Pruefstand = 14, swxUpDown_Card = 15, swxExtended_Stoptrigger = 16); 
	THWExtensionsBitNumber = (hwxZaehlerupgrade = 0, hwxUpDown_Counter = 1, hwxPWM_Ausgabe = 2, hwxPWM_Karte = 3, hwxDA_Wandler = 4, hwxMultiplexerUeberspannungsschutz = 5, hwxDualWandler = 8, hwxZeitstempel = 9, hwxTTL_Bitweise = 10, hwxCoprozessor_56307 = 11, hwxCoprozessor_56311 = 12, hwxInkrementalzaehler = 13, hwxRegeneratorAutomotiv = 14, hwxMH_Zaehlererweiterung = 15, hwxSSI_Schnittstelle = 16, hwxThermoelementanschluss_8Kanal = 17, hwx32Bit_Counter = 18, hwxICP_Einspeisung = 19); 
	TIEPEMode = (iepeDC_SE_IEPE_off = 0, iepeDC_Diff_IEPE_off = 1, iepeAC_SE_IEPE_off = 2, iepeAC_SE_IEPE_on = 3); 
	TMeasurementChannelType = (MEASUREMENTCHANNELTYPE_UNKNOWN = -1, MEASUREMENTCHANNELTYPE_AD, MEASUREMENTCHANNELTYPE_CT, MEASUREMENTCHANNELTYPE_TTL, MEASUREMENTCHANNELTYPE_FIRST = MEASUREMENTCHANNELTYPE_AD, MEASUREMENTCHANNELTYPE_LAST = MEASUREMENTCHANNELTYPE_TTL, MEASUREMENTCHANNELTYPE_DEFAULT = MEASUREMENTCHANNELTYPE_AD); 


implementation

end.
