unit PWM_Functions;

interface


function PWM_StartOutput(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_StartOutput';
function PWM_StopOutput(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_StopOutput';
function PWM_PreparePWMOutput(nInstance: Cardinal; nChannel: Cardinal; StartFrequency: Cardinal; nStartRatio: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_PreparePWMOutput';
function PWM_PrepareFMOutput(nInstance: Cardinal; nChannel: Cardinal; StartFrequency: Cardinal; nPulsWidthRatio: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_PrepareFMOutput';
function PWM_WriteNewPWMRatio(nInstance: Cardinal; nChannel: Cardinal; nRatio: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_WriteNewPWMRatio';
function PWM_WriteNewFMFrequency(nInstance: Cardinal; nChannel: Cardinal; Frequency: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_WriteNewFMFrequency';
function PWM_GetPWMRatio(nInstance: Cardinal; nChannel: Cardinal; var nRatio: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_GetPWMRatio';
function PWM_GetFMFrequency(nInstance: Cardinal; nChannel: Cardinal; var Frequency: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PWM_GetFMFrequency';

implementation

end.
