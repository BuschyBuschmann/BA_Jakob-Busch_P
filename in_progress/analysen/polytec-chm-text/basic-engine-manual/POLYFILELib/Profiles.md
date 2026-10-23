# POLYFILELib – Profiles

## Profiles Collection

*Quelle: `POLYFILELib~Profiles.html` · Polytec PolyFile Type Library*

### Description

Collection of Profile objects to hold all the profiles in a file. Member of the Infos collection.

### Object Model


---

## Profiles Collection Members

*Quelle: `POLYFILELib~Profiles_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new Profile to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Remove | Removes an item from the collection. |
| Save | Saves all modified Profiles in the underlying file. |

### Public Properties

| Count | Returns the number of items in this collection. |
|---|---|
| Item | Returns an item of the collection. |
| Name | Returns "Profiles". This can be used as an index to the Infos collection . |
| Type | Returns ptcInfoProfiles and can be used as an index to the Infos collection . |


---

## Add Method

*Quelle: `POLYFILELib~Profiles~Add.html` · Polytec PolyFile Type Library · Profiles Collection : Add Method*

### Description

Adds a new Profile to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As IProfile
```

### Return Type

Newly added Profile object.


---

## Clear Method

*Quelle: `POLYFILELib~Profiles~Clear.html` · Polytec PolyFile Type Library · Profiles Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Remove Method

*Quelle: `POLYFILELib~Profiles~Remove.html` · Polytec PolyFile Type Library · Profiles Collection : Remove Method*

### Description

Removes an item from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal lIndex As Long _
)
```

### Parameters

lIndex

Index of the item


---

## Save Method

*Quelle: `POLYFILELib~Profiles~Save.html` · Polytec PolyFile Type Library · Profiles Collection : Save Method*

### Description

Saves all modified Profiles in the underlying file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## Count Property

*Quelle: `POLYFILELib~Profiles~Count.html` · Polytec PolyFile Type Library · Profiles Collection : Count Property*

### Description

Returns the number of items in this collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYFILELib~Profiles~Item.html` · Polytec PolyFile Type Library · Profiles Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As IProfile
```

### Parameters

lIndex

Index of the item


---

## Name Property

*Quelle: `POLYFILELib~Profiles~Name.html` · Polytec PolyFile Type Library · Profiles Collection : Name Property*

### Description

Returns "Profiles". This can be used as an index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYFILELib~Profiles~Type.html` · Polytec PolyFile Type Library · Profiles Collection : Type Property*

### Description

Returns ptcInfoProfiles and can be used as an index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

PTCInfoType
