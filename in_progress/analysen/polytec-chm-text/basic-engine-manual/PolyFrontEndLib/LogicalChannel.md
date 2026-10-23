# PolyFrontEndLib – LogicalChannel

## LogicalChannel Object

*Quelle: `PolyFrontEndLib~LogicalChannel.html` · Polytec PolyFrontEnd Type Library*

### Description

Item of the LogicalChannels collection.

### Object Model


---

## LogicalChannel Object Members

*Quelle: `PolyFrontEndLib~LogicalChannel_members.html` · Polytec PolyFrontEnd Type Library*

### Public Methods

| GetDIOMask | Returns the digital i/o mask for the logical channel |
|---|---|

### Public Properties

| Caps | The capabilities of the logical channel. |
|---|---|
| Description | The description of the logical channel. |
| FrontEnd | The parent front-end object. |
| Name | The name of the logical channel. |
| Number | The number of the logical channel. |
| PhysicalChannels | The physical channels of this logical channel. |


---

## GetDIOMask Method

*Quelle: `PolyFrontEndLib~LogicalChannel~GetDIOMask.html` · Polytec PolyFrontEnd Type Library · LogicalChannel Object : GetDIOMask Method*

### Description

Returns the digital i/o mask for the logical channel

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
The device type used for the given digital i/o mask type.

### Remarks

Different front-ends have different means to read and write the digital i/o lines. With this function you can find out which device to use for which digital i/o line and which mask to use. The mask returned is a binary mask with a bit set at the position corresponding to the requested digital i/o line.


---

## Caps Property

*Quelle: `PolyFrontEndLib~LogicalChannel~Caps.html` · Polytec PolyFrontEnd Type Library · LogicalChannel Object : Caps Property*

### Description

The capabilities of the logical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCFrontEndChannelCapsType
```


---

## Description Property

*Quelle: `PolyFrontEndLib~LogicalChannel~Description.html` · Polytec PolyFrontEnd Type Library · LogicalChannel Object : Description Property*

### Description

The description of the logical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Description As String
```


---

## FrontEnd Property

*Quelle: `PolyFrontEndLib~LogicalChannel~FrontEnd.html` · Polytec PolyFrontEnd Type Library · LogicalChannel Object : FrontEnd Property*

### Description

The parent front-end object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrontEnd As IFrontEnd
```


---

## Name Property

*Quelle: `PolyFrontEndLib~LogicalChannel~Name.html` · Polytec PolyFrontEnd Type Library · LogicalChannel Object : Name Property*

### Description

The name of the logical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Number Property

*Quelle: `PolyFrontEndLib~LogicalChannel~Number.html` · Polytec PolyFrontEnd Type Library · LogicalChannel Object : Number Property*

### Description

The number of the logical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Number As Long
```


---

## PhysicalChannels Property

*Quelle: `PolyFrontEndLib~LogicalChannel~PhysicalChannels.html` · Polytec PolyFrontEnd Type Library · LogicalChannel Object : PhysicalChannels Property*

### Description

The physical channels of this logical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PhysicalChannels As PhysicalChannels
```

### Remarks

For certain front-ends, the number of logical channels differs from the number of physical channels. E.g. for VDD front-ends the I and Q physical channels appear only as a single logical channel. For PSV-3D front-ends the physical channels Vib Left, Vib Right and Vib Top appear as a single logical Vib 3D channel.
