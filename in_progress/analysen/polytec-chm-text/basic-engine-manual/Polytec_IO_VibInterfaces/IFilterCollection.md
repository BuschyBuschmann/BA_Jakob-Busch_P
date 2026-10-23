# Polytec_IO_VibInterfaces – IFilterCollection

## IFilterCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the filters of the vibrometer controller.

### Object Model


---

## IFilterCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ByKey | Returns the item of the collection with the given type of the filter. |
|---|---|
| Contains | Returns true, if the item with the given name or filter type is contained in the collection. |
| IndexOf | Returns the 0-based index of the given item of the collection. |
| IsEqual | Returns true, if the given filters collection is equal to this collection. |

### Public Properties

| Count | The number of items of the collection. |
|---|---|
| Item | Returns the item of the collection with the given index or name. |


---

## ByKey Method

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection~ByKey.html` · Polytec IO VibInterfaces Type Library · IFilterCollection Collection : ByKey Method*

### Description

Returns the item of the collection with the given type of the filter.

### Syntax

*Visual Basic:*
```
Public Function ByKey( _
   ByVal FilterType As FilterType _
) As IFilter
```

### Parameters

FilterType

| Value | Description |
|---|---|
| FilterType_AccelerationAse | The ASE filter for acceleration. |
| FilterType_AccelerationHighPass | The acceleration high pass filter. |
| FilterType_AccelerationLowPass | The acceleration low pass filter. |
| FilterType_Adaptive | The adaptive filter. |
| FilterType_Ase | The ASE filter, e.g. for a IVS-500 system. |
| FilterType_DCResponse | The DC response filter. |
| FilterType_DisplacementAse | The ASE filter for displacement. |
| FilterType_DisplacementHighPass | The displacement high pass filter. |
| FilterType_DisplacementLowPass | The displacement low pass filter. |
| FilterType_HighPass | The high pass filter. |
| FilterType_LowPass | The low pass filter. |
| FilterType_Rotation | The rotation filter. |
| FilterType_RpmResponse | The RPM response filter. |
| FilterType_Tracking | The tracking filter. |
| FilterType_Translation | The translation filter. |
The filter type of the item.


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection~Contains.html` · Polytec IO VibInterfaces Type Library · IFilterCollection Collection : Contains Method*

### Description

Returns true, if the item with the given name or filter type is contained in the collection.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The name or filter type of the item.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · IFilterCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item of the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal filter As IFilter _
) As Long
```

### Parameters

filter

The filter to get the index for.

### Remarks

Returns -1 if the item is not contained in the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · IFilterCollection Collection : IsEqual Method*

### Description

Returns true, if the given filters collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal filterCongeries As IFilterCollection _
) As Boolean
```

### Parameters

filterCongeries

The other filters collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection~Count.html` · Polytec IO VibInterfaces Type Library · IFilterCollection Collection : Count Property*

### Description

The number of items of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `Polytec_IO_VibInterfaces~IFilterCollection~Item.html` · Polytec IO VibInterfaces Type Library · IFilterCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As IFilter
```

### Parameters

index

The 0-based index or name of the item.
