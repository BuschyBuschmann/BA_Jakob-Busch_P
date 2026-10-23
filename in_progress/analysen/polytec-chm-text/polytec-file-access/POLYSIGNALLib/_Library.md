# POLYSIGNALLib – _Library

## Project Overview

*Quelle: `POLYSIGNALLib_P.html` · Polytec PolySignal Type Library*

### Description

The Polytec PolySignal type library contains objects that represent the domains, channels, signals and displays that are possible for the vibration data. The objects are organized in a hierarchy that corresponds to the domain, channel, signal and display menus in MPV/PSV/VibSoft. By navigating through the hierarchy you can select a display object that specifies the domain, channel, signal and display for vibration data as you would do it via the menus. Methods that get data or configure the display of data in windows accept this object. The collections in the hierarchy represent the selections that are possible at the given level. It is possible to fill menus or combo boxes with the contents of these collections to let a user choose the domain, channel, signal, or display respectively.

### Object Model

### Classes

| Class Module | Description |
|---|---|
| Attribute | Item of the Attributes Collection . |
| Attributes | Named collection of attribute items. |
| Channel | Item of the Channels collection . A channel represents a single acquisition channel (Vib, Ref1, Ref2, Ref3) or a combination of acquisition channels, e.g. Vib & Ref1. |
| Channels | Named collection of the available channels for a given domain. |
| DegreeOfFreedomID | Item of the DegreeOfFreedomIDs Collection describing a response or reference degree of freedom identifier. |
| DegreeOfFreedomIDs | The collection of the degree of freedom identifiers of responses or references. |
| Display | Item of the Displays collection . |
| DisplayInstVal | Item of the Displays collection . Derived from Display . Allows to specify / get the phase of the instantaneous value. If you use this display as an input for any of the GetData methods you get the magnitude of the data at the given phase. |
| Displays | Named and typed collection of the available displays of a Signal . |
| Domain | Base object of the PointDomain , PointAverageDomain and BandDomain objects. Not directly accessible. |
| Domains | The typed and named collection of the domains. |
| FunctionAtNodeDirections | The FunctionAtNodeDirections object provides a list of all PTCFunctionAtNodeDirection enumerator values and their string representations. You can use the object e.g. to create a user interface to let the user select a value. |
| FunctionTypes | The FunctionTypes object provides a list of all PTCFunctionType enumerator values and their string representations. You can use the object e.g. to create a user interface to let the user select a value. |
| Signal | Item of the Signals collection . A signal represents e.g. a velocity, displacement or acceleration signal of a vibrometer channel or a FRF, H1 or H2 signal of a combined channel (e.g. Vib & Ref1). |
| SignalDescription | The description of a signal. |
| Signals | Named collection of the available signals of a Channel . |
| SignalXAxis | The x-axis of the signal. |
| SignalYAxis | The y-axis of the signal. |

### Interfaces

| Class Module | Description |
|---|---|
| IChannel | Item of the Channels collection . A channel represents a single acquisition channel (Vib, Ref1, Ref2, Ref3) or a combination of acquisition channels, e.g. Vib & Ref1. |
| IChannels | Named collection of the available channels for a given domain. |
| IChannels2 | Named collection of the available channels for a given domain. |
| IDisplay | Item of the Displays collection . |
| IDisplay2 | Item of the Displays collection . |
| IDisplays | Named and typed collection of the available displays of a Signal . |
| IDomain | Base object of the PointDomain , PointAverageDomain and BandDomain objects. Not directly accessible. |
| IInfo | Info is the base object of all objects returned by the Infos collection . This object is not directly accessible. |
| IPref | The base object of all objects returned by the Preferences collection . This object is not directly accessible. |
| ISignal | Item of the Signals collection . A signal represents e.g. a velocity, displacement, or acceleration signal of a vibrometer channel, or a FRF, H1, or H2 signal of a combined channel (e.g. Vib & Ref1). |
| ISignal5 | Item of the Signals collection . A signal represents e.g. a velocity, displacement or acceleration signal of a vibrometer channel or a FRF, H1 or H2 signal of a combined channel (e.g. Vib & Ref1). |
| ISignalDescription | The description of a signal. |
| ISignals | Named collection of the available signals of a Channel . |

### Public Enumerations

| Enumeration | Description |
|---|---|
| PTCChannelCapsType | Capabilities of the channel. |
| PTCDataType | The type of the data. |
| PTCDisplayType | The type of the display. |
| PTCDomainType | The type of the domain. |
| PTCFunctionAtNodeDirection | The direction of the degree of freedom identifier. |
| PTCFunctionType | The function type of the signal. |
| PTCInfoType | PTCInfoType identifies the different items of the Infos collection . |
| PTCPhysicalQuantity | The type of the physical quantity. |
| PTCPrefType | Defines the types of objects that can be items of the Preferences collection . |
| PTCSignalBuildFlags | The build flags for the signal list. Specify these flags as parameters for the GetPointDomains Method , the GetPointAverageDomains Method or the GetBandDomains Method , respectively. |
| PTCSignalListBuildFlags | The build flags for the signal list. |


---

## References

*Quelle: `POLYSIGNALLib_references.html` · Polytec PolySignal Type Library*


