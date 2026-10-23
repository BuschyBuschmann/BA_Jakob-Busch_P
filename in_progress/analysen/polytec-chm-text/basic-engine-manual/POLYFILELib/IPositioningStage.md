# POLYFILELib – IPositioningStage

## IPositioningStage Interface

*Quelle: `POLYFILELib~IPositioningStage.html` · Polytec PolyFile Type Library*

### Description

The positioning stage object allows to control the x/y positioning stage that is optionally connected to MSA systems.

### Remarks

It is recommended to cast to the PositioningStage Object.


---

## IPositioningStage Interface Members

*Quelle: `POLYFILELib~IPositioningStage_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Name | The name of the positioning stage. |
|---|---|
| Type | Returns ptcInfoPositioningStage. Can be used as index to the InfosAcq collection . |


---

## Name Property

*Quelle: `POLYFILELib~IPositioningStage~Name.html` · Polytec PolyFile Type Library · IPositioningStage Interface : Name Property*

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

*Quelle: `POLYFILELib~IPositioningStage~Type.html` · Polytec PolyFile Type Library · IPositioningStage Interface : Type Property*

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
