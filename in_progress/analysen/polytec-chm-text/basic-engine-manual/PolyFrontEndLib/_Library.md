# PolyFrontEndLib – _Library

## Project Overview

*Quelle: `PolyFrontEndLib_P.html` · Polytec PolyFrontEnd Type Library*

### Description

The Polytec PolyFrontEnd type library contains enumerations for the front-end type, acquisition board type and program identifiers of the MPV/PSV/VibSoft system that was used for acquiring the data.

Moreover, in MPV/PSV/VibSoft you can access the front-end attached to the system and control it. E.g. with certain front-ends you can switch the lasers on or off.

### Object Model

### Classes

| Class Module | Description |
|---|---|
| FrontEnd | Item of the FrontEnds collection . The front-end describes a combination of a junction box and a data acquisition hardware. The FrontEnd object allows to control the front-end and to query for its capabilities and properties. |
| FrontEndControl | The FrontEndControl object controls the hardware of the front-end. |
| FrontEndControlDioDac | Controls the digital analog converters and the digital i/o lines of the junction box. |
| FrontEnds | The typed and named collection of available front-end types. |
| LogicalChannel | Item of the LogicalChannels collection . |
| LogicalChannels | Named collection of the available logical channels of the front-end. |
| PhysicalChannel | Item of the PhysicalChannels collection describing a physical channel of the front-end. |
| PhysicalChannels | Named collection of the available physical channels of the front-end. |

### Interfaces

| Class Module | Description |
|---|---|
| IFrontEnd | Item of the FrontEnds collection . The front-end describes a combination of a junction box and a data acquisition hardware. The FrontEnd object allows to control the front-end and to query for its capabilities and properties. |
| IFrontEnd2 | Item of the FrontEnds collection . The front-end describes a combination of a junction box and a data acquisition hardware. The FrontEnd object allows to control the front-end and to query for its capabilities and properties. |
| IFrontEndControl | The FrontEndControl object controls the hardware of the front-end. |
| IFrontEnds | The typed and named collection of available front-end types. |

### Public Enumerations

| Enumeration | Description |
|---|---|
| PTCAcqBoardType | The acquisition board type. |
| PTCFrontEndAuxOutModeType | The Aux Out mode. |
| PTCFrontEndAuxStateType | The state of the Aux digital i/o lines. |
| PTCFrontEndCapsType | The front-end capabilities. |
| PTCFrontEndChannelCapsType | The capabilities of a channel. |
| PTCFrontEndConnectStateType | The connected state of the front-end. |
| PTCFrontEndControlCapsType | The front-end control capabilities. |
| PTCFrontEndDacMovingType | The moving type for the front-end digital to analog converters. |
| PTCFrontEndDeviceType | The front-end device type. |
| PTCFrontEndDIODeviceType | The digital i/o device type for the front-end. |
| PTCFrontEndDIOMaskType | The digital i/o mask type of the front-end. |
| PTCFrontEndIlluminationStateType | The illumination state. |
| PTCFrontEndLaserType | The laser type. |
| PTCFrontEndOperatingStateType | The operating state of the junction box. |
| PTCFrontEndPortType | The front-end port type. |
| PTCFrontEndType | The front-end type. |
| PTCProgramID | The program identifier of the application. |


---

## References

*Quelle: `PolyFrontEndLib_references.html` · Polytec PolyFrontEnd Type Library*


