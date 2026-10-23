# PolyFrontEndLib – PhysicalChannel

## PhysicalChannel Object

*Quelle: `PolyFrontEndLib~PhysicalChannel.html` · Polytec PolyFrontEnd Type Library*

### Description

Item of the PhysicalChannels collection describing a physical channel of the front-end.

### Object Model


---

## PhysicalChannel Object Members

*Quelle: `PolyFrontEndLib~PhysicalChannel_members.html` · Polytec PolyFrontEnd Type Library*

### Public Methods

| GetDIOMask | Returns the digital i/o mask for the physical channel. |
|---|---|

### Public Properties

| Caps | The capabilities of the physical channel. |
|---|---|
| Description | The description of the physical channel. |
| FrontEnd | The parent front-end object. |
| LogicalChannel | The logical channel this physical channel belongs to. |
| Name | The name of the physical channel. |
| Number | The number of the physical channel. |


---

## GetDIOMask Method

*Quelle: `PolyFrontEndLib~PhysicalChannel~GetDIOMask.html` · Polytec PolyFrontEnd Type Library · PhysicalChannel Object : GetDIOMask Method*

### Description

Returns the digital i/o mask for the physical channel.

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

*Quelle: `PolyFrontEndLib~PhysicalChannel~Caps.html` · Polytec PolyFrontEnd Type Library · PhysicalChannel Object : Caps Property*

### Description

The capabilities of the physical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCFrontEndChannelCapsType
```


---

## Description Property

*Quelle: `PolyFrontEndLib~PhysicalChannel~Description.html` · Polytec PolyFrontEnd Type Library · PhysicalChannel Object : Description Property*

### Description

The description of the physical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Description As String
```


---

## FrontEnd Property

*Quelle: `PolyFrontEndLib~PhysicalChannel~FrontEnd.html` · Polytec PolyFrontEnd Type Library · PhysicalChannel Object : FrontEnd Property*

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

## LogicalChannel Property

*Quelle: `PolyFrontEndLib~PhysicalChannel~LogicalChannel.html` · Polytec PolyFrontEnd Type Library · PhysicalChannel Object : LogicalChannel Property*

### Description

The logical channel this physical channel belongs to.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LogicalChannel As LogicalChannel
```


---

## Name Property

*Quelle: `PolyFrontEndLib~PhysicalChannel~Name.html` · Polytec PolyFrontEnd Type Library · PhysicalChannel Object : Name Property*

### Description

The name of the physical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Number Property

*Quelle: `PolyFrontEndLib~PhysicalChannel~Number.html` · Polytec PolyFrontEnd Type Library · PhysicalChannel Object : Number Property*

### Description

The number of the physical channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Number As Long
```
