# PSV – TriggerAcqProperties

## TriggerAcqProperties Object

*Quelle: `PSV~TriggerAcqProperties.html` · Polytec PSV Type Library*

### Description

The trigger acquisition properties. Item of the AcquisitionProperties collection.


---

## TriggerAcqProperties Object Members

*Quelle: `PSV~TriggerAcqProperties_members.html` · Polytec PSV Type Library*

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

*Quelle: `PSV~TriggerAcqProperties~AnalogSourceChannel.html` · Polytec PSV Type Library · TriggerAcqProperties Object : AnalogSourceChannel Property*

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

*Quelle: `PSV~TriggerAcqProperties~Edge.html` · Polytec PSV Type Library · TriggerAcqProperties Object : Edge Property*

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

*Quelle: `PSV~TriggerAcqProperties~Level.html` · Polytec PSV Type Library · TriggerAcqProperties Object : Level Property*

### Description

Specifies the trigger level in percent.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Level As Double
```

### Remarks

Allowed values are in the range of -99% and 99%.


---

## PhaseFromRef Property

*Quelle: `PSV~TriggerAcqProperties~PhaseFromRef.html` · Polytec PSV Type Library · TriggerAcqProperties Object : PhaseFromRef Property*

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

*Quelle: `PSV~TriggerAcqProperties~PreTrigger.html` · Polytec PSV Type Library · TriggerAcqProperties Object : PreTrigger Property*

### Description

Specifies the pre-trigger value, in percent. Allowed values are in the range of PreTriggerMin and PreTriggerMax.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PreTrigger As Double
```


---

## PreTriggerMax Property

*Quelle: `PSV~TriggerAcqProperties~PreTriggerMax.html` · Polytec PSV Type Library · TriggerAcqProperties Object : PreTriggerMax Property*

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

*Quelle: `PSV~TriggerAcqProperties~PreTriggerMin.html` · Polytec PSV Type Library · TriggerAcqProperties Object : PreTriggerMin Property*

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

*Quelle: `PSV~TriggerAcqProperties~PreTriggerPossible.html` · Polytec PSV Type Library · TriggerAcqProperties Object : PreTriggerPossible Property*

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

*Quelle: `PSV~TriggerAcqProperties~Source.html` · Polytec PSV Type Library · TriggerAcqProperties Object : Source Property*

### Description

Specifies the trigger source.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Source As PTCTriggerSource
```
