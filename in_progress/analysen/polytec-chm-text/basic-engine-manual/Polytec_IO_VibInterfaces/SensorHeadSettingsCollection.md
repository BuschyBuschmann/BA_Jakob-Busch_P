# Polytec_IO_VibInterfaces – SensorHeadSettingsCollection

## SensorHeadSettingsCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettingsCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the sensor head settings.

### Object Model


---

## SensorHeadSettingsCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettingsCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ByKey | Returns the item of the collection with the given sensor head identifier. |
|---|---|
| Contains | Returns true, if the collection contains the item with the given sensor head identifier or name. |
| IndexOf | Returns the 0-based index of the given item. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index or name. |


---

## ByKey Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettingsCollection~ByKey.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettingsCollection Collection : ByKey Method*

### Description

Returns the item of the collection with the given sensor head identifier.

### Syntax

*Visual Basic:*
```
Public Function ByKey( _
   ByVal SensorHeadIdentifier As SensorHeadIdentifier _
) As SensorHeadSettings
```

### Parameters

SensorHeadIdentifier

| Value | Description |
|---|---|
| SensorHeadIdentifier_SensorHeadA | The sensor head is sensor head A. |
| SensorHeadIdentifier_SensorHeadB | The sensor head is sensor head B. |
The sensor head identifier.


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettingsCollection~Contains.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettingsCollection Collection : Contains Method*

### Description

Returns true, if the collection contains the item with the given sensor head identifier or name.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The sensor head identifier or the name of the item.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettingsCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettingsCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal SensorHeadSettings As SensorHeadSettings _
) As Long
```

### Parameters

SensorHeadSettings

The item of the collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettingsCollection~Count.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettingsCollection Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettingsCollection~Item.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettingsCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As SensorHeadSettings
```

### Parameters

index

The 0-based index or name of the item.
