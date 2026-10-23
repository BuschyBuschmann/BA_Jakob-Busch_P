# POLYSIGNALLib – DisplayInstVal

## DisplayInstVal Object

*Quelle: `POLYSIGNALLib~DisplayInstVal.html` · Polytec PolySignal Type Library*

### Description

Item of the Displays collection. Derived from Display. Allows to specify / get the phase of the instantaneous value. If you use this display as an input for any of the GetData methods you get the magnitude of the data at the given phase.

### Object Model


---

## DisplayInstVal Object Members

*Quelle: `POLYSIGNALLib~DisplayInstVal_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Name | Returns "Inst. Val.". |
|---|---|
| Phase | Phase of the instantaneous value in degree (± 180°) |
| Signal | Returns the signal. |
| Type | The type of the display. Can be used as an index to the Displays collection . |


---

## Name Property

*Quelle: `POLYSIGNALLib~DisplayInstVal~Name.html` · Polytec PolySignal Type Library · DisplayInstVal Object : Name Property*

### Description

Returns "Inst. Val.".

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Phase Property

*Quelle: `POLYSIGNALLib~DisplayInstVal~Phase.html` · Polytec PolySignal Type Library · DisplayInstVal Object : Phase Property*

### Description

Phase of the instantaneous value in degree (± 180°)

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Phase As Double
```


---

## Signal Property

*Quelle: `POLYSIGNALLib~DisplayInstVal~Signal.html` · Polytec PolySignal Type Library · DisplayInstVal Object : Signal Property*

### Description

Returns the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Signal As Signal
```


---

## Type Property

*Quelle: `POLYSIGNALLib~DisplayInstVal~Type.html` · Polytec PolySignal Type Library · DisplayInstVal Object : Type Property*

### Description

The type of the display. Can be used as an index to the Displays collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDisplayType
```
