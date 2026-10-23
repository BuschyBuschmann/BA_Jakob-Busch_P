# Polytec_IO_VibInterfaces – ISensorHeadCollection

## ISensorHeadCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the sensor heads of the controller.

### Object Model


---

## ISensorHeadCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ByKey | Returns the item of the collection with the given sensor head identifier. |
|---|---|
| Contains | Returns true, if the collection contains the item with the given sensor head identifier or name. |
| IndexOf | Returns the 0-based index of the given item. |
| IsEqual | Returns true if the given quantity collection is equal to this collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index or name. |


---

## ByKey Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection~ByKey.html` · Polytec IO VibInterfaces Type Library · ISensorHeadCollection Collection : ByKey Method*

### Description

Returns the item of the collection with the given sensor head identifier.

### Syntax

*Visual Basic:*
```
Public Function ByKey( _
   ByVal SensorHeadIdentifier As SensorHeadIdentifier _
) As ISensorHead
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

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection~Contains.html` · Polytec IO VibInterfaces Type Library · ISensorHeadCollection Collection : Contains Method*

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

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · ISensorHeadCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal sensorHead As ISensorHead _
) As Long
```

### Parameters

sensorHead

The sensor head to get the index for.

### Remarks

Returns -1 if the item is not contained in the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · ISensorHeadCollection Collection : IsEqual Method*

### Description

Returns true if the given quantity collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal sensorHeadCongeries As ISensorHeadCollection _
) As Boolean
```

### Parameters

sensorHeadCongeries

The other quantities collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection~Count.html` · Polytec IO VibInterfaces Type Library · ISensorHeadCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~ISensorHeadCollection~Item.html` · Polytec IO VibInterfaces Type Library · ISensorHeadCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As ISensorHead
```

### Parameters

index

The 0-based index or name of the item.
