# POLYPROPERTIESLib – ITriggerAcqProperties3

## ITriggerAcqProperties3 Interface

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3.html` · Polytec PolyProperties Type Library*

### Description

The trigger acquisition properties.

### Remarks

It is recommended to cast to the TriggerAcqPropertiesContainer Object.


---

## ITriggerAcqProperties3 Interface Members

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3_members.html` · Polytec PolyProperties Type Library*

### Public Properties

| AnalogSourceChannel | Specifies the source channel for the analog trigger. |
|---|---|
| Edge | Specifies the trigger edge. |
| Level | Specifies the trigger level in percent. |
| PhaseFromRef | Specifies whether the phase for the response channels is determined from the phase of the frequency response function to the first reference channel when triggering is active. |
| PreTrigger | Specifies the pre-trigger value, in percent. Allowed values are in the range of PreTriggerMin and PreTriggerMax . |
| PreTriggerMax | The maximum pre-trigger value, in percent. |
| PreTriggerMin | The minimum pre-trigger value, in percent. |
| PreTriggerPossible | Returns whether pre-trigger is possible with the current data acquisition settings. |
| Source | Specifies the trigger source. |


---

## AnalogSourceChannel Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~AnalogSourceChannel.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : AnalogSourceChannel Property*

### Description

Specifies the source channel for the analog trigger.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AnalogSourceChannel As Long
```


---

## Edge Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~Edge.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : Edge Property*

### Description

Specifies the trigger edge.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Edge As PTCTriggerEdge
```


---

## Level Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~Level.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : Level Property*

### Description

Specifies the trigger level in percent.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Level As Long
```

### Remarks

Allowed values are in the range of -99% and 99%.


---

## PhaseFromRef Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~PhaseFromRef.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : PhaseFromRef Property*

### Description

Specifies whether the phase for the response channels is determined from the phase of the frequency response function to the first reference channel when triggering is active.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PhaseFromRef As Boolean
```


---

## PreTrigger Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~PreTrigger.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : PreTrigger Property*

### Description

Specifies the pre-trigger value, in percent. Allowed values are in the range of PreTriggerMin and PreTriggerMax.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PreTrigger As Long
```


---

## PreTriggerMax Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~PreTriggerMax.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : PreTriggerMax Property*

### Description

The maximum pre-trigger value, in percent.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PreTriggerMax As Long
```


---

## PreTriggerMin Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~PreTriggerMin.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : PreTriggerMin Property*

### Description

The minimum pre-trigger value, in percent.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PreTriggerMin As Long
```


---

## PreTriggerPossible Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~PreTriggerPossible.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : PreTriggerPossible Property*

### Description

Returns whether pre-trigger is possible with the current data acquisition settings.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PreTriggerPossible As Boolean
```


---

## Source Property

*Quelle: `POLYPROPERTIESLib~ITriggerAcqProperties3~Source.html` · Polytec PolyProperties Type Library · ITriggerAcqProperties3 Interface : Source Property*

### Description

Specifies the trigger source.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Source As PTCTriggerSource
```
