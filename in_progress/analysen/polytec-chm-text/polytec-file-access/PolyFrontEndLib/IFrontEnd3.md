# PolyFrontEndLib – IFrontEnd3

## IFrontEnd3 Interface

*Quelle: `PolyFrontEndLib~IFrontEnd3.html` · Polytec PolyFrontEnd Type Library*

### Description

Item of the FrontEnds collection. The front-end describes a combination of a junction box and a data acquisition hardware. The FrontEnd object allows to control the front-end and to query for its capabilities and properties.

### Object Model

### Remarks

It is recommended to cast to the FrontEnd object.


---

## IFrontEnd3 Interface Members

*Quelle: `PolyFrontEndLib~IFrontEnd3_members.html` · Polytec PolyFrontEnd Type Library*

### Public Methods

| GetCommPort | Retrieves the COM/RS232 port number for a given port type. |
|---|---|
| GetDIOMask | Retrieves the digital i/o mask for the given mask type. |

### Public Properties

| Caps | The front-end capabilities. |
|---|---|
| Control | The front-end control object. |
| FirmwareVersion | The firmware version of the front-end. |
| FrontEndIDs | This property is not implemented yet. It will provide an array containing the ID strings of all connected front-ends. |
| FrontEnds | The parent FrontEnds object. |
| HostIpAddress | The IP address of the host network adapter where this front-end is connected to. |
| LogicalChannels | The collection of logical channels of the front-end. |
| MacAddress | The MAC address of the front-end. |
| Name | The name of the front-end. |
| PhysicalChannels | The collection of physical channels of the front-end. |
| Type | The front-end type. |


---

## GetCommPort Method

*Quelle: `PolyFrontEndLib~IFrontEnd3~GetCommPort.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : GetCommPort Method*

### Description

Retrieves the COM/RS232 port number for a given port type.

### Syntax

*Visual Basic:*
```
Public Function GetCommPort( _
   ByVal ptcPortType As PTCFrontEndPortType, _
   ByRef plMUXChannel As Long _
) As Long
```

### Parameters

ptcPortType

| Value | Description |
|---|---|
| ptcFrontEndPortCamera | The port for the camera. |
| ptcFrontEndPortCameraCenter | The port for the center camera. |
| ptcFrontEndPortCameraLeft | The port for the camera of the scanning head left. |
| ptcFrontEndPortCameraTop | The port for the camera of the scanning head top. |
| ptcFrontEndPortControl | The port for the micro-controller of the front-end. |
| ptcFrontEndPortRangeFinder | The port for the distance sensor. |
| ptcFrontEndPortUnknown | Unknown port. |
| ptcFrontEndPortVibController | The vibrometer controller port. |
| ptcFrontEndPortVibControllerLeft | The port for the vibrometer controller left. |
| ptcFrontEndPortVibControllerRight | The port for the vibrometer controller right. |
| ptcFrontEndPortVibControllerTop | The port for the vibrometer controller top. |
| ptcFrontEndPortZStage | The port for the controller of the z-stage. |
The port type.

plMUXChannel

The multiplexer channel number.

### Remarks

Some front-ends have an internal USB to RS232 converter with multiple RS232 ports. To find out which hardware is connected to which port, you can pass the type of the port to this function and retrieve the number of the RS232 port of the adapter that is connected to the corresponding hardware.

### Example


---

## GetDIOMask Method

*Quelle: `PolyFrontEndLib~IFrontEnd3~GetDIOMask.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : GetDIOMask Method*

### Description

Retrieves the digital i/o mask for the given mask type.

### Syntax

*Visual Basic:*
```
Public Function GetDIOMask( _
   ByVal ptcDIOMaskType As PTCFrontEndDIOMaskType, _
   ByRef pptcDIODeviceType As PTCFrontEndDIODeviceType _
) As Long
```

### Parameters

ptcDIOMaskType

| Value | Description |
|---|---|
| ptcFrontEndDIOMaskAuxIn | The mask for AuxIn. |
| ptcFrontEndDIOMaskAuxOut | The mask for AuxOut. |
| ptcFrontEndDIOMaskDifferentialInput | The mask for differential input. |
| ptcFrontEndDIOMaskGate | The mask for the gate. |
| ptcFrontEndDIOMaskHandset | The mask for the handset. |
| ptcFrontEndDIOMaskICP | The mask for ICP. |
| ptcFrontEndDIOMaskPanTilt | The mask for the pan tilt head. |
| ptcFrontEndDIOMaskUnknown | Unknown mask type. |
The type of the digital i/o mask.

pptcDIODeviceType

| Value | Description |
|---|---|
| ptcFrontEndDIODeviceAcqBoard | The acquisition board. |
| ptcFrontEndDIODeviceDIOBoard | The digital i/o board. |
| ptcFrontEndDIODeviceFrontEnd | The front-end. |
| ptcFrontEndDIODeviceUnknown | Unknown hardware. |
The type of the digital i/o hardware.

### Remarks

Different front-ends have different means to read and write the digital i/o lines. With this function you can find out which device to use for which digital i/o line and which mask to use. The mask returned is a binary mask with a bit set at the position corresponding to the requested digital i/o line.


---

## Caps Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~Caps.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : Caps Property*

### Description

The front-end capabilities.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCFrontEndCapsType
```


---

## Control Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~Control.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : Control Property*

### Description

The front-end control object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Control As IFrontEndControl
```

### Remarks

This object is only available for controllable front-ends. See the Caps property to find out, if a front-end is controllable.


---

## FirmwareVersion Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~FirmwareVersion.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : FirmwareVersion Property*

### Description

The firmware version of the front-end.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FirmwareVersion As String
```


---

## FrontEndIDs Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~FrontEndIDs.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : FrontEndIDs Property*

### Description

This property is not implemented yet. It will provide an array containing the ID strings of all connected front-ends.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrontEndIDs As String()
```

### Remarks

For the PSV-500 system, the ID string is the MAC address of the front-end. For the MPV system, the strings represent the unique IDs of the connected optic units.


---

## FrontEnds Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~FrontEnds.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : FrontEnds Property*

### Description

The parent FrontEnds object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrontEnds As IFrontEnds
```


---

## HostIpAddress Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~HostIpAddress.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : HostIpAddress Property*

### Description

The IP address of the host network adapter where this front-end is connected to.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HostIpAddress As String
```


---

## LogicalChannels Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~LogicalChannels.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : LogicalChannels Property*

### Description

The collection of logical channels of the front-end.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LogicalChannels As LogicalChannels
```

### Remarks

For certain front-ends, the number of logical channels differs from the number of physical channels. E.g. for VDD front-ends the I and Q physical channels appear only as a single logical channel. For PSV-3D front-ends the physical channels Vib Left, Vib Right and Vib Top appear as a single logical Vib 3D channel.


---

## MacAddress Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~MacAddress.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : MacAddress Property*

### Description

The MAC address of the front-end.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MacAddress As String
```


---

## Name Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~Name.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : Name Property*

### Description

The name of the front-end.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

The name can be used as an index into the FrontEnds collection.


---

## PhysicalChannels Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~PhysicalChannels.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : PhysicalChannels Property*

### Description

The collection of physical channels of the front-end.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PhysicalChannels As PhysicalChannels
```

### Remarks

For certain front-ends, the number of logical channels differs from the number of physical channels. E.g. for VDD front-ends the I and Q physical channels appear only as a single logical channel. For PSV-3D front-ends the physical channels Vib Left, Vib Right and Vib Top appear as a single logical Vib 3D channel.


---

## Type Property

*Quelle: `PolyFrontEndLib~IFrontEnd3~Type.html` · Polytec PolyFrontEnd Type Library · IFrontEnd3 Interface : Type Property*

### Description

The front-end type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCFrontEndType
```

### Remarks

The type can be used as an index into the FrontEnds collection.
