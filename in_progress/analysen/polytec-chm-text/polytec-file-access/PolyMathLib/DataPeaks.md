# PolyMathLib – DataPeaks

## DataPeaks Collection

*Quelle: `PolyMathLib~DataPeaks.html` · Polytec PolyMath Type Library*

### Description

The data peaks found by the peak finder.

### Object Model


---

## DataPeaks Collection Members

*Quelle: `PolyMathLib~DataPeaks_members.html` · Polytec PolyMath Type Library*

### Public Properties

| Count | The number of data peaks in the collection. |
|---|---|
| Item | Returns the data peak with the specified index in the data peaks collection. |


---

## Count Property

*Quelle: `PolyMathLib~DataPeaks~Count.html` · Polytec PolyMath Type Library · DataPeaks Collection : Count Property*

### Description

The number of data peaks in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `PolyMathLib~DataPeaks~Item.html` · Polytec PolyMath Type Library · DataPeaks Collection : Item Property*

### Description

Returns the data peak with the specified index in the data peaks collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Long _
) As DataPeak
```

### Parameters

index

The one-based index of the data peak in the data peaks collection.

### Return Type

The data peak.
