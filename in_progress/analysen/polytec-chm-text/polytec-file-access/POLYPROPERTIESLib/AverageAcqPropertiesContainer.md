# POLYPROPERTIESLib – AverageAcqPropertiesContainer

## AverageAcqPropertiesContainer Object

*Quelle: `POLYPROPERTIESLib~AverageAcqPropertiesContainer.html` · Polytec PolyProperties Type Library*

### Description

Average acquisition properties. Item of the AcquisitionProperties Collection.


---

## AverageAcqPropertiesContainer Object Members

*Quelle: `POLYPROPERTIESLib~AverageAcqPropertiesContainer_members.html` · Polytec PolyProperties Type Library*

### Public Properties

| Count | The average count. |
|---|---|
| Type | The averaging type. |


---

## Count Property

*Quelle: `POLYPROPERTIESLib~AverageAcqPropertiesContainer~Count.html` · Polytec PolyProperties Type Library · AverageAcqPropertiesContainer Object : Count Property*

### Description

The average count.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```

### Remarks

Allowed values are in the range of 3 and 10000. In FastScan mode the number of averages is limited to 100. In time mode the number of averages is limited when using signal enhancement.


---

## Type Property

*Quelle: `POLYPROPERTIESLib~AverageAcqPropertiesContainer~Type.html` · Polytec PolyProperties Type Library · AverageAcqPropertiesContainer Object : Type Property*

### Description

The averaging type.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCAverageType
```
