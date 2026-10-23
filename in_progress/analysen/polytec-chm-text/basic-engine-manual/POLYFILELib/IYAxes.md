# POLYFILELib – IYAxes

## IYAxes Collection

*Quelle: `POLYFILELib~IYAxes.html` · Polytec PolyFile Type Library*

### Description

Collection that contains information about the y-axes used to display the data returned by GetData. For combined displays as e.g. ptcDisplayMagPhase or ptcDisplayRealImag YAxes contains two items of type YAxis one for each part of the data.

### Object Model

### Remarks

It is recommended to cast to the YAxes object.


---

## IYAxes Collection Members

*Quelle: `POLYFILELib~IYAxes_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Count | Returns the number of items in the YAxes collection. |
|---|---|
| Item | Returns an item of the YAxes collection. |


---

## Count Property

*Quelle: `POLYFILELib~IYAxes~Count.html` · Polytec PolyFile Type Library · IYAxes Collection : Count Property*

### Description

Returns the number of items in the YAxes collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYFILELib~IYAxes~Item.html` · Polytec PolyFile Type Library · IYAxes Collection : Item Property*

### Description

Returns an item of the YAxes collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As YAxis
```

### Parameters

Index

Index of the YAxis object.
