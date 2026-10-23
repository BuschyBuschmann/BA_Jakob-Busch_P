# PSV – DigitalPort

## DigitalPort Object

*Quelle: `PSV~DigitalPort.html` · Polytec PSV Type Library*

### Description

Represents a digital i/o port of the PSV or VibSoft junction box (Aux In/Aux Out).


---

## DigitalPort Object Members

*Quelle: `PSV~DigitalPort_members.html` · Polytec PSV Type Library*

### Public Methods

| Pulse | Sends a pulse to the digital output port. |
|---|---|

### Public Properties

| Type | The type of the digital i/o port. |
|---|---|
| Value | The current value of the digital i/o port. |


---

## Pulse Method

*Quelle: `PSV~DigitalPort~Pulse.html` · Polytec PSV Type Library · DigitalPort Object : Pulse Method*

### Description

Sends a pulse to the digital output port.

### Syntax

*Visual Basic:*
```
Public Sub Pulse( _
   ByVal Value As Boolean, _
   Optional ByVal Length As Long = 50 _
)
```

### Parameters

Value

If True, sends a high level pulse, if False, sends a low level pulse.

Length

The duration of the pulse in µs. If not specified, the pulse has a duration of 50 µs.


---

## Type Property

*Quelle: `PSV~DigitalPort~Type.html` · Polytec PSV Type Library · DigitalPort Object : Type Property*

### Description

The type of the digital i/o port.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDigitalPortType
```


---

## Value Property

*Quelle: `PSV~DigitalPort~Value.html` · Polytec PSV Type Library · DigitalPort Object : Value Property*

### Description

The current value of the digital i/o port.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Value As Boolean
```

### Return Type

True represents the high level, False the low level.
