# POLYFILELib – IVibrometerGroups

## IVibrometerGroups Collection

*Quelle: `POLYFILELib~IVibrometerGroups.html` · Polytec PolyFile Type Library*

### Description

The collection of vibrometer controller groups.

### Object Model


---

## IVibrometerGroups Collection Members

*Quelle: `POLYFILELib~IVibrometerGroups_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index. |
| Name | Returns "VibrometerGroups". |
| Type | Returns ptcInfoVibrometers. |


---

## Count Property

*Quelle: `POLYFILELib~IVibrometerGroups~Count.html` · Polytec PolyFile Type Library · IVibrometerGroups Collection : Count Property*

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

*Quelle: `POLYFILELib~IVibrometerGroups~Item.html` · Polytec PolyFile Type Library · IVibrometerGroups Collection : Item Property*

### Description

Returns the item of the collection with the given index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal nIndex As Long _
) As IControllerGroup
```

### Parameters

nIndex

The index of the item.


---

## Name Property

*Quelle: `POLYFILELib~IVibrometerGroups~Name.html` · Polytec PolyFile Type Library · IVibrometerGroups Collection : Name Property*

### Description

Returns "VibrometerGroups".

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "VibrometerGroups".


---

## Type Property

*Quelle: `POLYFILELib~IVibrometerGroups~Type.html` · Polytec PolyFile Type Library · IVibrometerGroups Collection : Type Property*

### Description

Returns ptcInfoVibrometers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoVibrometers.
