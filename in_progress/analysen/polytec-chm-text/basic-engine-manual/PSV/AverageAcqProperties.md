# PSV – AverageAcqProperties

## AverageAcqProperties Object

*Quelle: `PSV~AverageAcqProperties.html` · Polytec PSV Type Library*

### Description

Average acquisition properties. Item of the AcquisitionProperties Collection.


---

## AverageAcqProperties Object Members

*Quelle: `PSV~AverageAcqProperties_members.html` · Polytec PSV Type Library*

### Public Properties

| Count | The average count. |
|---|---|
| Type | The averaging type. |


---

## Count Property

*Quelle: `PSV~AverageAcqProperties~Count.html` · Polytec PSV Type Library · AverageAcqProperties Object : Count Property*

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

*Quelle: `PSV~AverageAcqProperties~Type.html` · Polytec PSV Type Library · AverageAcqProperties Object : Type Property*

### Description

The averaging type.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCAverageType
```
