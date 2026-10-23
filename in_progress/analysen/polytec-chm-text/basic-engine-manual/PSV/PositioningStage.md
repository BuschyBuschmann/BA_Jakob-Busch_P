# PSV – PositioningStage

## PositioningStage Object

*Quelle: `PSV~PositioningStage.html` · Polytec PSV Type Library*

### Description

Item of the InfosAcq collection. The positioning stage object allows to control the x/y positioning stage that is optionally connected to MSA systems.

### Remarks

Using PositioningStage is deprecated. Please use PositionDevice instead.


---

## PositioningStage Object Members

*Quelle: `PSV~PositioningStage_members.html` · Polytec PSV Type Library*

### Public Properties

| Name | The name of the positioning stage. |
|---|---|
| Type | Returns ptcInfoPositioningStage. Can be used as index to the InfosAcq collection . |


---

## Name Property

*Quelle: `PSV~PositioningStage~Name.html` · Polytec PSV Type Library · PositioningStage Object : Name Property*

### Description

The name of the positioning stage.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `PSV~PositioningStage~Type.html` · Polytec PSV Type Library · PositioningStage Object : Type Property*

### Description

Returns ptcInfoPositioningStage. Can be used as index to the InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoPositioningStage.
