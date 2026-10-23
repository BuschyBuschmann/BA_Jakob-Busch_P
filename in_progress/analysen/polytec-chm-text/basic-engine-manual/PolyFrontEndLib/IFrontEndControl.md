# PolyFrontEndLib – IFrontEndControl

## IFrontEndControl Interface

*Quelle: `PolyFrontEndLib~IFrontEndControl.html` · Polytec PolyFrontEnd Type Library*

### Description

The FrontEndControl object controls the hardware of the front-end.

### Object Model

### Remarks

It is recommended to cast to the FrontEndControl object.


---

## IFrontEndControl Interface Members

*Quelle: `PolyFrontEndLib~IFrontEndControl_members.html` · Polytec PolyFrontEnd Type Library*

### Public Properties

| Caps | The front-end control capabilities. |
|---|---|
| DifferentialInputEnabled | Specifies whether differential input is enabled. |
| FrontEnd | The parent front-end object. |
| GeneratorOutEnabled | Specifies whether the generator output is enabled. |
| ICPEnabled | Specifies whether ICP is active for the channels. |
| ICPMask | Returns which channels support ICP. |
| LaserMask | The laser mask. |
| LaserOn | Specifies whether the lasers are on or off. |
| RangeFinderEnabled | Specifies whether the distance sensor is enabled. |
| RangeFinderInProgress | Returns while the mirror for the distance sensor is moving. |
| VideoMUXChannel | Specifies the active channel of the video multiplexer. |


---

## Caps Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~Caps.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : Caps Property*

### Description

The front-end control capabilities.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCFrontEndControlCapsType
```

### Remarks

Not all front-end control objects have the same capabilities. Use this property to find out which capabilities are available.


---

## DifferentialInputEnabled Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~DifferentialInputEnabled.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : DifferentialInputEnabled Property*

### Description

Specifies whether differential input is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DifferentialInputEnabled As Boolean
```


---

## FrontEnd Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~FrontEnd.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : FrontEnd Property*

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

## GeneratorOutEnabled Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~GeneratorOutEnabled.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : GeneratorOutEnabled Property*

### Description

Specifies whether the generator output is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GeneratorOutEnabled As Boolean
```


---

## ICPEnabled Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~ICPEnabled.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : ICPEnabled Property*

### Description

Specifies whether ICP is active for the channels.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ICPEnabled As Long
```

### Remarks

The bit 0 of the value corresponds to channel 1, bit 1 to channel 2 etc. See the ICPMask property to find out, which channels support ICP.


---

## ICPMask Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~ICPMask.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : ICPMask Property*

### Description

Returns which channels support ICP.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ICPMask As Long
```

### Remarks

The bit 0 of the value corresponds to channel 1, bit 1 to channel 2 etc.


---

## LaserMask Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~LaserMask.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : LaserMask Property*

### Description

The laser mask.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserMask As PTCFrontEndLaserType
```

### Remarks

Values set in this mask can be set to the LaserOn property.


---

## LaserOn Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~LaserOn.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : LaserOn Property*

### Description

Specifies whether the lasers are on or off.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LaserOn As PTCFrontEndLaserType
```

### Remarks

See the LaserMask property for allowed values for this property.


---

## RangeFinderEnabled Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~RangeFinderEnabled.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : RangeFinderEnabled Property*

### Description

Specifies whether the distance sensor is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RangeFinderEnabled As Boolean
```

### Remarks

Changing this property causes a mirror to move in the scanning head. This takes some time. See the RangeFinderInProgress property to find out, if the mirror is still moving.


---

## RangeFinderInProgress Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~RangeFinderInProgress.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : RangeFinderInProgress Property*

### Description

Returns while the mirror for the distance sensor is moving.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RangeFinderInProgress As Boolean
```

### Remarks

Changing RangeFinderEnabled Property causes a mirror to move in the scanning head. This takes some time. While the mirror is moving, this property returns true.


---

## VideoMUXChannel Property

*Quelle: `PolyFrontEndLib~IFrontEndControl~VideoMUXChannel.html` · Polytec PolyFrontEnd Type Library · IFrontEndControl Interface : VideoMUXChannel Property*

### Description

Specifies the active channel of the video multiplexer.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoMUXChannel As Long
```
