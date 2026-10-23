# PSV – VibrometerGroups

## VibrometerGroups Collection

*Quelle: `PSV~VibrometerGroups.html` · Polytec PSV Type Library*

### Description

The collection of vibrometer controller groups. Item of the InfosAcq collection.

### Object Model


---

## VibrometerGroups Collection Members

*Quelle: `PSV~VibrometerGroups_members.html` · Polytec PSV Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index. |
| Name | Returns "VibrometerGroups". Can be used as an index into the InfosAcq Collection . |
| Type | Returns ptcInfoVibrometers. Can be used as an index into the InfosAcq collection . |


---

## Count Property

*Quelle: `PSV~VibrometerGroups~Count.html` · Polytec PSV Type Library · VibrometerGroups Collection : Count Property*

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

*Quelle: `PSV~VibrometerGroups~Item.html` · Polytec PSV Type Library · VibrometerGroups Collection : Item Property*

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

*Quelle: `PSV~VibrometerGroups~Name.html` · Polytec PSV Type Library · VibrometerGroups Collection : Name Property*

### Description

Returns "VibrometerGroups". Can be used as an index into the InfosAcq Collection.

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

*Quelle: `PSV~VibrometerGroups~Type.html` · Polytec PSV Type Library · VibrometerGroups Collection : Type Property*

### Description

Returns ptcInfoVibrometers. Can be used as an index into the InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoVibrometers.
