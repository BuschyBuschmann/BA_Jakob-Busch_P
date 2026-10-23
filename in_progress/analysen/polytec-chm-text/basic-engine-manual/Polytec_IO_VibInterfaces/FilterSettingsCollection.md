# Polytec_IO_VibInterfaces – FilterSettingsCollection

## FilterSettingsCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~FilterSettingsCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the filter settings.

### Object Model


---

## FilterSettingsCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~FilterSettingsCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ByKey | Returns the item of the collection with the given type of the filter. |
|---|---|
| Contains | Returns true, if the item with the given name or filter type is contained in the collection. |
| IndexOf | Returns the 0-based index of the given item of the collection. |

### Public Properties

| Count | The number of items of the collection. |
|---|---|
| Item | Returns the item of the collection with the given index or name. |


---

## ByKey Method

*Quelle: `Polytec_IO_VibInterfaces~FilterSettingsCollection~ByKey.html` · Polytec IO VibInterfaces Type Library · FilterSettingsCollection Collection : ByKey Method*

### Description

Returns the item of the collection with the given type of the filter.

### Syntax

*Visual Basic:*
```
Public Function ByKey( _
   ByVal FilterType As FilterType _
) As FilterSettings
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

*Quelle: `Polytec_IO_VibInterfaces~FilterSettingsCollection~Contains.html` · Polytec IO VibInterfaces Type Library · FilterSettingsCollection Collection : Contains Method*

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

*Quelle: `Polytec_IO_VibInterfaces~FilterSettingsCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · FilterSettingsCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item of the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal FilterSettings As FilterSettings _
) As Long
```

### Parameters

FilterSettings

The item of the collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~FilterSettingsCollection~Count.html` · Polytec IO VibInterfaces Type Library · FilterSettingsCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~FilterSettingsCollection~Item.html` · Polytec IO VibInterfaces Type Library · FilterSettingsCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As FilterSettings
```

### Parameters

index

The 0-based index or name of the item.
