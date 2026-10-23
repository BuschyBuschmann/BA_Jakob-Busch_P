# POLYFILELib – ITextures

## ITextures Collection

*Quelle: `POLYFILELib~ITextures.html` · Polytec PolyFile Type Library*

### Description

ITextures Interface

### Object Model

### Remarks

It is recommended to cast to the Textures Collection.


---

## ITextures Collection Members

*Quelle: `POLYFILELib~ITextures_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new texture to the collection and returns it. |
|---|---|
| Clear | Clears the collection by removing all textures from it. |
| Load | Loads the collection of the textures from the specified storage. |
| Remove | Removes the texture with the specified index. |
| Save | Saves the collection of the textures to the specified storage. |

### Public Properties

| Count | The count of the textures in the collection. |
|---|---|
| Item | Returns the item of the Texture collection with the specified index. |
| Name | Returns "Textures. Can be used as an index into the Infos collection . |
| Type | Returns ptcInfoTextures . Can be used as an index into the Infos collection . |


---

## Add Method

*Quelle: `POLYFILELib~ITextures~Add.html` · Polytec PolyFile Type Library · ITextures Collection : Add Method*

### Description

Adds a new texture to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As Texture
```

### Return Type

The new texture.


---

## Clear Method

*Quelle: `POLYFILELib~ITextures~Clear.html` · Polytec PolyFile Type Library · ITextures Collection : Clear Method*

### Description

Clears the collection by removing all textures from it.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Load Method

*Quelle: `POLYFILELib~ITextures~Load.html` · Polytec PolyFile Type Library · ITextures Collection : Load Method*

### Description

Loads the collection of the textures from the specified storage.

### Syntax

*Visual Basic:*
```
Public Sub Load( _
   ByVal storage As IStorage _
)
```

### Parameters

storage

The storage.


---

## Remove Method

*Quelle: `POLYFILELib~ITextures~Remove.html` · Polytec PolyFile Type Library · ITextures Collection : Remove Method*

### Description

Removes the texture with the specified index.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal Index As Long _
)
```

### Parameters

Index

The one-based index of the texture to remove.


---

## Save Method

*Quelle: `POLYFILELib~ITextures~Save.html` · Polytec PolyFile Type Library · ITextures Collection : Save Method*

### Description

Saves the collection of the textures to the specified storage.

### Syntax

*Visual Basic:*
```
Public Sub Save( _
   ByVal storage As IStorage, _
   ByVal clearDirty As Boolean _
)
```

### Parameters

storage

The storage.

clearDirty

If true, the dirty flag of the storage is cleared.


---

## Count Property

*Quelle: `POLYFILELib~ITextures~Count.html` · Polytec PolyFile Type Library · ITextures Collection : Count Property*

### Description

The count of the textures in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYFILELib~ITextures~Item.html` · Polytec PolyFile Type Library · ITextures Collection : Item Property*

### Description

Returns the item of the Texture collection with the specified index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As Texture
```

### Parameters

Index

The one-based index of the texture.

### Return Type

The texture.


---

## Name Property

*Quelle: `POLYFILELib~ITextures~Name.html` · Polytec PolyFile Type Library · ITextures Collection : Name Property*

### Description

Returns "Textures. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYFILELib~ITextures~Type.html` · Polytec PolyFile Type Library · ITextures Collection : Type Property*

### Description

Returns ptcInfoTextures. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```
