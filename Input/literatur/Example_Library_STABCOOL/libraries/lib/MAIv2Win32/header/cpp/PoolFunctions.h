

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	Device Pool Funktionen. </category>
/// <categoryE>	device pool functions. </categoryE>
///
///
/// <filesummary>	zur Geräteübergreifenden Steuerung stehen diese Funktionen zur Verfügung: </filesummary>
/// <filesummaryE>	Functions that apply to all devices are: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////


//MAIV2DLL_EXPORT UnloadDevicePool();
MAIV2DLL_EXPORT GetFirstDevice();
MAIV2DLL_EXPORT GetNumberOfDevices();

MAIV2DLL_EXPORT GetDeviceHandles					(uint Handles[], uint* iHandleCount);
MAIV2DLL_EXPORT GetDeviceHandlesMultichoiceETH		(uint Handles[], uint* iHandleCount);
MAIV2DLL_EXPORT GetDeviceHandlesMultichoicePCI		(uint Handles[], uint* iHandleCount);
MAIV2DLL_EXPORT GetDeviceHandlesMultichoiceUSB		(uint Handles[], uint* iHandleCount);
MAIV2DLL_EXPORT GetDeviceHandlesMultichoiceUSBBasic	(uint Handles[], uint* iHandleCount);
																		 
MAIV2DLL_EXPORT GetFirstDeviceByType(uint DeviceType);					 
MAIV2DLL_EXPORT OpenDevice(uint nInstance);								 
MAIV2DLL_EXPORT CloseDevice(uint nInstance);							 
MAIV2DLL_EXPORT IsDeviceOpen(uint nInstance);
MAIV2DLL_EXPORT GetErrorDescription(uint nInstance, long ErrorNumber, char ErrorDescription[]);
MAIV2DLL_EXPORT SetGPCIFile(const char AIFilePath[], uint nLength);
MAIV2DLL_EXPORT_CHAR GetGPCIFilePath();

MAIV2DLL_EXPORT SetMAIDevicelistChangedHandler(MAI_DEVICELISTCHANGED_CALLBACK AIMAIDevicelistChangedFunction);

MAIV2DLL_EXPORT ReCreateDeviceListOmittingDeviceTypes(bool AICreatePCI,bool AICreateUSBMC4, bool CreateUSBBasic);
MAIV2DLL_EXPORT ShowMessageBoxOnDeviceCreationError(bool AIShowMsgBox);
MAIV2DLL_EXPORT GetNumberOfUninitializedDevices();
MAIV2DLL_EXPORT GetDeviceCreationErrorMessage(uint nNumber, const char AOText[], uint nTextBufferLength);

MAIV2DLL_EXPORT DeviceInfoGet(enum eDeviceClass type, struct maidevinfo** info);
MAIV2DLL_EXPORT DeviceInfoFree(struct maidevinfo* info);