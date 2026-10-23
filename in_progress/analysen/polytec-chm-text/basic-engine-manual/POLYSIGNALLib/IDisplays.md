# POLYSIGNALLib – IDisplays

## IDisplays Collection

*Quelle: `POLYSIGNALLib~IDisplays.html` · Polytec PolySignal Type Library*

### Description

Named and typed collection of the available displays of a Signal.

### Object Model

### Remarks

It is recommended to cast to the Displays collection.


---

## IDisplays Collection Members

*Quelle: `POLYSIGNALLib~IDisplays_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true, if the item with the given index exists in the collection. |
| Item | Returns an item of the collection. |
| Type | Returns the item of the given type in the collection. |


---

## Count Property

*Quelle: `POLYSIGNALLib~IDisplays~Count.html` · Polytec PolySignal Type Library · IDisplays Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYSIGNALLib~IDisplays~Exists.html` · Polytec PolySignal Type Library · IDisplays Collection : Exists Property*

### Description

Returns true, if the item with the given index exists in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal Index As Variant _
) As Boolean
```

### Parameters

Index

Name or type of the item.


---

## Item Property

*Quelle: `POLYSIGNALLib~IDisplays~Item.html` · Polytec PolySignal Type Library · IDisplays Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As IDisplay
```

### Parameters

Index

The name or index of the item.


---

## Type Property

*Quelle: `POLYSIGNALLib~IDisplays~Type.html` · Polytec PolySignal Type Library · IDisplays Collection : Type Property*

### Description

Returns the item of the given type in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal eType As PTCDisplayType _
) As IDisplay
```

### Parameters

eType

| Value | Description |
|---|---|
| ptcDisplayImag | The imaginary part. |
| ptcDisplayInstVal | The instantaneous value for a given phase. |
| ptcDisplayIQFitted | The IQ display (digital demodulation, VDD only). |
| ptcDisplayMag | The magnitude. |
| ptcDisplayMagDb | The magnitude in dB. |
| ptcDisplayMagDbA | The magnitude in dBA. |
| ptcDisplayMagDbPhase | The magnitude in dB and the phase in degree. |
| ptcDisplayMagDbPhaseRad | The magnitude in dB and the phase in radian. |
| ptcDisplayMagPhase | The magnitude and the phase in degree. |
| ptcDisplayMagPhaseRad | The magnitude and the phase in radian. |
| ptcDisplayNotAvail | The display is not available. |
| ptcDisplayNyquist | Nyquist. |
| ptcDisplayPhase | The phase. |
| ptcDisplayReal | The real part. |
| ptcDisplayRealImag | The real and the imaginary part. |
| ptcDisplaySamples | The samples (for the time domain only). |
The type of the item.
