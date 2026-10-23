# POLYSIGNALLib – ISignal

## ISignal Interface

*Quelle: `POLYSIGNALLib~ISignal.html` · Polytec PolySignal Type Library*

### Description

Item of the Signals collection. A signal represents e.g. a velocity, displacement, or acceleration signal of a vibrometer channel, or a FRF, H1, or H2 signal of a combined channel (e.g. Vib & Ref1).

### Object Model

### Remarks

It is recommended to cast to the Signal object.


---

## ISignal Interface Members

*Quelle: `POLYSIGNALLib~ISignal_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Channel | The channel of the signal. |
|---|---|
| Displays | The collection of the available displays for the signal. |
| Name | The name of the signal. |


---

## Channel Property

*Quelle: `POLYSIGNALLib~ISignal~Channel.html` · Polytec PolySignal Type Library · ISignal Interface : Channel Property*

### Description

The channel of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Channel As IChannel
```


---

## Displays Property

*Quelle: `POLYSIGNALLib~ISignal~Displays.html` · Polytec PolySignal Type Library · ISignal Interface : Displays Property*

### Description

The collection of the available displays for the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Displays As IDisplays
```


---

## Name Property

*Quelle: `POLYSIGNALLib~ISignal~Name.html` · Polytec PolySignal Type Library · ISignal Interface : Name Property*

### Description

The name of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```
