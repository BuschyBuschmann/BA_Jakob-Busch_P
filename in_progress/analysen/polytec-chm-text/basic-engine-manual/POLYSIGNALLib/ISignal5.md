# POLYSIGNALLib – ISignal5

## ISignal5 Interface

*Quelle: `POLYSIGNALLib~ISignal5.html` · Polytec PolySignal Type Library*

### Description

Item of the Signals collection. A signal represents e.g. a velocity, displacement or acceleration signal of a vibrometer channel or a FRF, H1 or H2 signal of a combined channel (e.g. Vib & Ref1).

### Object Model

### Remarks

It is recommended to cast to the Signal Object.


---

## ISignal5 Interface Members

*Quelle: `POLYSIGNALLib~ISignal5_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Channel | The channel of the signal. |
|---|---|
| Description | The description of the signal. |
| Displays | The collection of the available displays for the signal. |
| Name | The name of the signal. |


---

## Channel Property

*Quelle: `POLYSIGNALLib~ISignal5~Channel.html` · Polytec PolySignal Type Library · ISignal5 Interface : Channel Property*

### Description

The channel of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Channel As Channel
```


---

## Description Property

*Quelle: `POLYSIGNALLib~ISignal5~Description.html` · Polytec PolySignal Type Library · ISignal5 Interface : Description Property*

### Description

The description of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Description As SignalDescription
```


---

## Displays Property

*Quelle: `POLYSIGNALLib~ISignal5~Displays.html` · Polytec PolySignal Type Library · ISignal5 Interface : Displays Property*

### Description

The collection of the available displays for the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Displays As Displays
```


---

## Name Property

*Quelle: `POLYSIGNALLib~ISignal5~Name.html` · Polytec PolySignal Type Library · ISignal5 Interface : Name Property*

### Description

The name of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```
