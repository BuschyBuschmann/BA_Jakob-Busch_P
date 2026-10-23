unit Misc_Functions;

interface

uses
	MAILIBAPI\iMAI_LIB;

function GetMAILIB(var hMAILIB: IMAILIB):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetMAILIB';

implementation

end.
