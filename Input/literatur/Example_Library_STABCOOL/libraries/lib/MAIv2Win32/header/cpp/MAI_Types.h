#ifndef _MAI_TYPES_H_
#define _MAI_TYPES_H_



typedef unsigned long	ulong;

typedef unsigned char	uchar;
typedef unsigned short	ushort;
typedef unsigned int	uint;
typedef unsigned long long u64;



#ifndef __GCC_BUILD_

#include <windows.h>

typedef VOID (NTAPI * MAI_DEVICELISTCHANGED_CALLBACK) (  unsigned int /*  number of new found devices */, 
                                                         int*		  /*  instance Numbers of the new found devices */ ,
                                                         unsigned int /*  number of missing devices */, 
                                                         int*		  /*  instance Numbers of the missing devices */ ); 

#else

typedef long long int __int64;
#define NULL 0

typedef void (*MAI_DEVICELISTCHANGED_CALLBACK) ( unsigned int /*  number of new found devices */, 
                                                         int*		  /*  instance Numbers of the new found devices */ ,
                                                         unsigned int /*  number of missing devices */, 
                                                         int*		  /*  instance Numbers of the missing devices */ )  __attribute__((stdcall)); 


#endif

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	  </summary>
/// <summaryE>	device info descriptor.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
typedef struct maidevinfo {
	uint		di_class;
	uint		di_instance;
	const char* di_name;
	struct maidevinfo *next;
} maidevinfo_t, *p_maidevinfo_t;

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Moegliche Werte für die Geraeteklasse.  </summary>
/// <summaryE>	possible values for the device class.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eDeviceClass { DEVICECLASS_BOTH, DEVICECLASS_PCI, DEVICECLASS_USB, DEVICECLASS_USBBASIC, DEVICECLASS_ETH };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Oversampling Modus eines AD Messkanals.  </summary>
/// <summaryE>	possible values for the oversampling mode of an  AD measurement channel.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eOversampling	{ oversamplingDISABLED, oversampling2x, oversampling4x, oversampling8x, oversampling16x };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Gainfaktor eines AD Messkanals.  </summary>
/// <summaryE>	possible values for the gain factor of an AD measurement channel.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eGain			{ gainDisabled, gain2x, gain4x, gain8x };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für die Polarität eines AD Messkanals.  </summary>
/// <summaryE>	possible values for an AD measurement channel's polarity.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eBipolar		{ polUNIPOLAR, polBIPOLAR };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Parameter PartBlock.  </summary>
/// <summaryE>	possible values for the PartBlock parameter.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum ePartBlock		{ partONLYFULLBLOCKS, partPARTBLOCK };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Parameter SkipData.  </summary>
/// <summaryE>	possible values for the SkipData parameter.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eSkipData		{ skipGETCAPTUREDVALUES, skipSKIPCAPTUREDVALUES };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Streaming Modus.  </summary>
/// <summaryE>	possible values for the streaming mode.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eStreamingMode { smOFF, smON };
////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Universalzähler Modi.  </summary>
/// <summaryE>	modes of an universal counter.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////

enum eCounterMode	{       cmIMPULSECOUNTER      = 0,
                            cmFREQUENCYCOUNTER    = 1,
                            cmPERIODCOUNTER       = 2, 
                            cmPULSWIDTHCOUNTER    = 3, 
                            cmINCREMENTALCOUNTER  = 4,
                            cmUPDOWNCOUNTER       = 5,
                            cmINCREMENTALEXTTIME  = 6,
                            cmINCREMENTALEXTFLOW  = 7,
                            cmAUDIOCARD_TTL	      = 8

					};

enum eCounterModesList  {   cmlIMPULSECOUNTER     = 1 << cmIMPULSECOUNTER,
                            cmlPERIODCOUNTER      = 1 << cmPERIODCOUNTER, 
                            cmlPULSWIDTHCOUNTER   = 1 << cmPULSWIDTHCOUNTER, 
                            cmlFREQUENCYCOUNTER   = 1 << cmFREQUENCYCOUNTER,
                            cmlUPDOWNCOUNTER      = 1 << cmUPDOWNCOUNTER,
                            cmlINCREMENTALCOUNTER = 1 << cmINCREMENTALCOUNTER,
                            cmlINCREMENTALEXTTIME = 1 << cmINCREMENTALEXTTIME,
                            cmlINCREMENTALEXTFLOW = 1 << cmINCREMENTALEXTFLOW };

enum eCounterParam	{  	ctparamRESOLUTION		  = 0,	
						ctparamCOMPAREBITWIDTH    = 1,
						ctparamPRESETVALUE        = 2,
						ctparamIMPULSEDIRECTION   = 3,
						ctparamSIGNALEDGE         = 4,
						ctparamEACHPERIOD         = 5,
						ctparamSOFTWARERESET          = 6,
						ctparamHARDWARERESETMODE      = 7,
						ctparamHARDWARERESETEDGE      = 8,
						ctparamINCREMENTINTERPOLATION = 9,
						ctparamRESOLUTIONFREQUENCY    = 10, 
						ctparamRESOLUTIONINCTIMESTAMP = 11 };




enum eCounterParamsList	{   ctplPRESETVALUE                   = 1 << ctparamPRESETVALUE,
                            ctplIMPULSEDIRECTION              = 1 << ctparamIMPULSEDIRECTION, 
                            ctplSIGNALEDGE                    = 1 << ctparamSIGNALEDGE, 
                            ctplRESOLUTIONFREQUENCY           = 1 << ctparamRESOLUTIONFREQUENCY,
                            ctplSOFTWARERESET                 = 1 << ctparamSOFTWARERESET,
                            ctplHARDWARERESETMODE             = 1 << ctparamHARDWARERESETMODE,
                            ctplHARDWARERESETEDGE             = 1 << ctparamHARDWARERESETEDGE,
                            ctplINTERPOLATIONMODE             = 1 << ctparamINCREMENTINTERPOLATION,
                            ctplINCREMENTALEXTTIMERESOLUTION  = 1 << ctparamRESOLUTIONINCTIMESTAMP };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den externen Trigger Modus.  </summary>
/// <summaryE>	possible values for external trigger mode.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eTrigger		{ trigDISABLED, trigEXTERN_TRIGGER, trigEXTERN_CLOCK };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für die externe Trigger Signalflanke.  </summary>
/// <summaryE>	possible values for external trigger's signal edge.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eExternEdge	{ tedgeFALLING_EDGE, tedgeRISING_EDGE };


////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Typ der FFT Analyse.  </summary>
/// <summaryE>	possible values for the FFT spectrum's type.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eFFT_Type {	fftAbsolute	=0, 
                    /// Root Mean Square (Effektivwert).  
                    fftRMS 	    =1,
                    ///  Quadrat der Effektivwerte. 
                    fftPower 	=2,
                    /// Phasenspektrum.  
                    fftPhase 	=3};

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für die Anzahl von Stützstellen bei der Onlie FFT Analyse.  </summary>
/// <summaryE>	possible values for the number of FFT points.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eFFT_Size {
                    /// <summary> 512 Stützstellen.  </summary>
                    /// <summaryE> 512 points.  </summaryE>
                    fft_s512  =  0,
                    /// <summary> 1024 Stützstellen.  </summary>
                    /// <summaryE> 1024 points.  </summaryE>
                    fft_s1024 =  1,
                    /// <summary> 2048 Stützstellen.  </summary>
                    /// <summaryE> 2048 points.  </summaryE>
                    fft_s2048 =  2,
                    /// <summary> 4096 Stützstellen.  </summary>
                    /// <summaryE> 4096 points.  </summaryE>
                    fft_s4096 =  3
            };
////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Typ eines Online Triggers.  </summary>
/// <summaryE>	possible values for the type of an online trigger.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eTrigger_Type {
                    /// <summary> Maximum.  </summary>
                    /// <summaryE> maximum.  </summaryE>
                    trigMax						=0,  
                    /// <summary> Minumum.  </summary>
                    /// <summaryE> minumum.  </summaryE>
                    trigMin						=1, 
                    /// <summary> unterhalb einer Schwelle.  </summary>
                    /// <summaryE> on threshold underrun.  </summaryE>
                    trigUnterSchwelle 			=2, 
                    /// <summary> oberhalb einer Schwelle.  </summary>
                    /// <summaryE>  on threshold overrun.  </summaryE>
                    trigUeberSchwelle 			=3, 
                    /// <summary> in einem Fenster.  </summary>
                    /// <summaryE> inside a window.  </summaryE>
                    trigFenster					=4, 
                    /// <summary> unterhalb einer Gradientensteigung.  </summary>
                    /// <summaryE> on gradient slope underrun.  </summaryE>
                    trigUnterGradientensteigung	=5, 
                    /// <summary> oberhalb einer Gradientensteigung.  </summary>
                    /// <summaryE> on gradient slope overrun.  </summaryE>
                    trigUeberGradientensteigung =6, 
                    /// <summary> in einem Gradientenfenster.  </summary>
                    /// <summaryE> inside a gradient window.  </summaryE>
                    trigGradientenfenster		=7			
            };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	 Entwurfsmethoden des PID Controller-Algorithmus  </summary>
/// <summaryE>	 design method of the PID controller algorithm  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////

enum  ePIDControllerType  {
        /// <summary> Integralalgorithmus linke Intervallgrenze.  </summary>
        /// <summaryE> lower limit of the integral integal.  </summaryE>
        pidPID1			= 0,		
        /// <summary> Integralalgorithmus rechte Intervallgrenze.  </summary>
        /// <summaryE> upper limit of the integral.  </summaryE>
        pidPID2		    = 1,	 
        /// <summary> Integralalgorithmus Trapetznäherung.  </summary>
        /// <summaryE> trapezoid.  </summaryE>
        pidPID3		    = 2,	 
         
    };
////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Legt die Charakteristik eines digitalen Filters fast.  </summary>
/// <summaryE>	digital filters characteristics.  </summaryE>
///
////////////////////////////////////////////////////////////////////////////////////////////////////

enum  eFilterType  {
           /// <summary> Tiefpass.  </summary>
           /// <summaryE> low pass.  </summaryE>
           ftLOWPASS  = 0,
           /// <summary> Hochpass.  </summary>
           /// <summaryE> high pass.  </summaryE>
           ftHIGHPASS = 1,
           /// <summary> Bandpass.  </summary>
           /// <summaryE> band pass.  </summaryE>
           ftBANDPASS = 2,
           /// <summary> Bandstop.  </summary>
           /// <summaryE> band stop.  </summaryE>
           ftBANDSTOP = 3,
    };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	IIR Filter Designmethode  </summary>
/// <summaryE>	IIR filter design method  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum  eIIRFilterDesign  {
        /// <summary> Butterworth.  </summary>
        /// <summaryE> Butterworth.  </summaryE>
        iirBUTTERWORTH                = 0,
        /// <summary> Tschebytschow 1.  </summary>
        /// <summaryE> Tschebytschow 1.  </summaryE>
        iirCHEBYSHEV_T1               = 1,
        /// <summary> Tschebytschow 2.  </summary>
        /// <summaryE> Tschebytschow 2.  </summaryE>
        iirCHEBYSHEV_T2               = 2,
        /// <summary> Elliptisch (Cauer).  </summary>
        /// <summaryE> Elliptisch (Cauer).  </summaryE>
        iirELLIPTIC                   = 3,
        /// <summary> Bessel.  </summary>
        /// <summaryE> Bessel.  </summaryE>
        iirBESSEL                     = 4,
    };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Mögliche Werte für den Typ der FIR Fensterfunktion.  </summary>
/// <summaryE>	possible values for the FIR window function.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eFIRWindowFunction {
 
        /// <summary> Rechteck.  </summary>
        firwinRectangular         = 0,
        /// <summary> Hanning (eg. Hann, ...).  </summary>
        firwinHanning             = 1,
        /// <summary> Hamming (eg. Hamm, ...).  </summary>
        firwinHamming             = 2,
        /// <summary> Blackman.  </summary>
        firwinBlackman            = 3,
        /// <summary> Kaiser.  </summary>
        firwinKaiser              = 4,
        /// <summary> Bartlett.  </summary>
        firwinBartlett            = 5,
        /// <summary> Dolph-Tschebytschow (eg. Dolph-Tschebytescheff,  Dolph-Chebycheff...).  </summary>
        firwinDolph_Tschebytschow = 6,
        /// <summary> Dreieck.  </summary>
        firwinTriangular          = 7,
        /// <summary> Blackman-Harris.  </summary>
        firwinBlackman_Harris		= 8,
        /// <summary> Blackman-Nuttall.  </summary>
        firwinBlackman_Nuttall    = 9,
        /// <summary> Flat Top (Flache Spitze).  </summary>
        firwinFlat_Top			= 10,
    };

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Bitnummern der verscheidenen Software Erweiterungen.  </summary>
/// <summaryE>	bit numbers of the existing software extensions.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eSWExtensionsBitNumber {
        /// <summary> Online_FFT  </summary>
        swxOnline_FFT					= 0,
        /// <summary> Online_Filter.  </summary>
        swxOnline_Filter				= 1,
        /// <summary> Online_PID.  </summary>
        swxOnline_PID					= 2,
        /// <summary> Online_Linearisierung.  </summary>
        swxOnline_Linearisierung		= 3,
        /// <summary> OnboardFunktionsgenerator.  </summary>
        swxOnboardFunktionsgenerator	= 4, 
        /// <summary> Wabco_Projekt.  </summary>
        swxWabco_Projekt				= 9,
        /// <summary> Airbag_Pruefstand.  </summary>
        swxAirbag_Pruefstand			= 14,
        /// <summary> UpDown_Card.  </summary>
        swxUpDown_Card					= 15,
        /// <summary> Extended_Stoptrigger.  </summary>
        swxExtended_Stoptrigger		= 16
};

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Bitnummern der verscheidenen Hardware Erweiterungen.  </summary>
/// <summaryE>	bit numbers of the existing hardware extensions.  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eHWExtensionsBitNumber {
        /// <summary> Zaehlerupgrade.  </summary>
        hwxZaehlerupgrade						= 0,
        /// <summary> UpDown_Counter.  </summary>
        hwxUpDown_Counter						= 1,
        /// <summary> PWM_Ausgabe.  </summary>
        hwxPWM_Ausgabe							= 2,
        /// <summary> PWM_Karte.  </summary>
        hwxPWM_Karte							= 3,
        /// <summary> DA_Wandler.  </summary>
        hwxDA_Wandler							= 4,
        /// <summary> MultiplexerUeberspannungsschutz.  </summary>
        hwxMultiplexerUeberspannungsschutz		= 5,
        /// <summary> DualWandler.  </summary>
        hwxDualWandler							= 8,
        /// <summary> Zeitstempel.  </summary>
        hwxZeitstempel							= 9,
        /// <summary> TTL_Bitweise.  </summary>
        hwxTTL_Bitweise						= 10,
        /// <summary> Coprozessor_56307.  </summary>
        hwxCoprozessor_56307					= 11,
        /// <summary> Coprozessor_56311.  </summary>
        hwxCoprozessor_56311					= 12,
        /// <summary> Inkrementalzaehler. .  </summary>
        hwxInkrementalzaehler  			    = 13,
        /// <summary> RegeneratorAutomotiv.  </summary>
        hwxRegeneratorAutomotiv				= 14,
        /// <summary> MH_Zaehlererweiterung.  </summary>
        hwxMH_Zaehlererweiterung				= 15,
        /// <summary> SSI_Schnittstelle.  </summary>
        hwxSSI_Schnittstelle					= 16,
        /// <summary> Thermoelementanschluss_8Kanal.  </summary>
        hwxThermoelementanschluss_8Kanal		= 17,
        /// <summary> 32Bit_Zaehler.  </summary>
        hwx32Bit_Counter						= 18,
        /// <summary> ICP_Einspeisung.  </summary>
        hwxICP_Einspeisung						= 19
};

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Modus der IEPE Ausgabe  </summary>
/// <summaryE>	IEPE powering mode  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////

enum  eIEPEMode  {
    /// <summary> DC, Massebezogen, IEPE  inaktiv (default).  </summary>
    /// <summaryE>	DC, SE, IEPE_off (default) </summaryE>
    iepeDC_SE_IEPE_off		= 0,	
    /// <summary> DC, Differenz, IEPE  inaktiv.  </summary>
    /// <summaryE>	DC, Differencial, IEPE_off  </summaryE>
    iepeDC_Diff_IEPE_off	= 1,
    /// <summary> AC, Differenz, IEPE  inaktiv.  </summary>
    /// <summaryE>	AC, Differencial, IEPE_off  </summaryE>
    iepeAC_SE_IEPE_off		= 2,
    /// <summary> AC, Massebezogen IEPE  aktiv.  </summary>
    /// <summaryE>	AC, Differencial, IEPE_on  </summaryE>
    iepeAC_SE_IEPE_on	    = 3

};

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Typ der Messdatenkanals  </summary>
/// <summaryE>	Typ of measurement data channel  </summaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
enum eMeasurementChannelType {
	/// <summary> Unbekannter Messdatenkanal.  </summary>
	/// <summaryE>	Unknown measurement channel </summaryE>
	MEASUREMENTCHANNELTYPE_UNKNOWN = -1,
	/// <summary> Analog IN Messdatenkanal (default).  </summary>
	/// <summaryE>	Analog IN measurement channel (default) </summaryE>
	MEASUREMENTCHANNELTYPE_AD,
	/// <summary> Counter IN Messdatenkanal.  </summary>
	/// <summaryE>	Counter IN measurement channel </summaryE>
	MEASUREMENTCHANNELTYPE_CT,
	/// <summary> Digital IN Messdatenkanal.  </summary>
	/// <summaryE>	Digital IN measurement channel </summaryE>
	MEASUREMENTCHANNELTYPE_TTL,
	MEASUREMENTCHANNELTYPE_FIRST = MEASUREMENTCHANNELTYPE_AD,
	MEASUREMENTCHANNELTYPE_LAST = MEASUREMENTCHANNELTYPE_TTL,
	MEASUREMENTCHANNELTYPE_DEFAULT = MEASUREMENTCHANNELTYPE_AD
};

#if 1
// __stdcall
#define MAIV2DLL_EXPORT			extern "C" __declspec(dllexport) long __stdcall
#define MAIV2DLL_EXPORT_CHAR	extern "C" __declspec(dllexport) const char * __stdcall
#else
// __cdecl
#define MAIV2DLL_EXPORT			extern "C" __declspec(dllexport) long
#define MAIV2DLL_EXPORT_CHAR	extern "C" __declspec(dllexport) const char *
#endif

#ifdef __GCC_BUILD_
#undef MAIV2DLL_EXPORT
#undef MAIV2DLL_EXPORT_CHAR

#define MAIV2DLL_EXPORT	     __attribute__((visibility("default")))   int
#define MAIV2DLL_EXPORT_CHAR  __attribute__((visibility("default")))  const char*

#endif



#endif

