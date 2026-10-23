# POLYFILELib – ContainedFiles

## ContainedFiles Collection

*Quelle: `POLYFILELib~ContainedFiles.html` · Polytec PolyFile Type Library*

### Description

Named collection of the ContainedFile objects.

### Object Model


---

## ContainedFiles Collection Members

*Quelle: `POLYFILELib~ContainedFiles_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Add a new ContainedFile to the collection. |
|---|---|
| Clear | Removes all Items from the collection. If a file is open, all contained files will be deleted from the storage. |
| Save | Saves all modified Contained File objects in the combined file. |

### Public Properties

| ActiveFile | Sets/Retrieves the Active File object of the combined File. Active Filess Infos will be used as the active infos for the combined file. By default, It is the first contained file. If its needed to be set to another contained file, set before getting the Infos object. |
|---|---|
| Count | Returns the number of items in the collection. |
| Item | Returns an item of this collection. |


---

## Add Method

*Quelle: `POLYFILELib~ContainedFiles~Add.html` · Polytec PolyFile Type Library · ContainedFiles Collection : Add Method*

### Description

Add a new ContainedFile to the collection.

### Syntax

*Visual Basic:*
```
Public Sub Add( _
   ByVal bstrFileName As String, _
   Optional ByVal PTCContainedCaps As PTCContainedCaps = ptcContainedCopy _
)
```

### Parameters

bstrFileName

The file name.

PTCContainedCaps

| Value | Description |
|---|---|
| ptcContainedCopy | Copied to the combined file. |
| ptcContainedLink | Linked to the combined file. |
| ptcContainedNone | Undefined. |
Link or copy the contained file.

### Remarks

If Caps is ptcContainedLink to make a link to the combined file, it must be in the same drive with the combined file and if the combined file to be saved in the network folder, it must be in the same folder.


---

## Clear Method

*Quelle: `POLYFILELib~ContainedFiles~Clear.html` · Polytec PolyFile Type Library · ContainedFiles Collection : Clear Method*

### Description

Removes all Items from the collection. If a file is open, all contained files will be deleted from the storage.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Save Method

*Quelle: `POLYFILELib~ContainedFiles~Save.html` · Polytec PolyFile Type Library · ContainedFiles Collection : Save Method*

### Description

Saves all modified Contained File objects in the combined file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## ActiveFile Property

*Quelle: `POLYFILELib~ContainedFiles~ActiveFile.html` · Polytec PolyFile Type Library · ContainedFiles Collection : ActiveFile Property*

### Description

Sets/Retrieves the Active File object of the combined File. Active Filess Infos will be used as the active infos for the combined file. By default, It is the first contained file. If its needed to be set to another contained file, set before getting the Infos object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ActiveFile As IPolyFile8
```

### Example


---

## Count Property

*Quelle: `POLYFILELib~ContainedFiles~Count.html` · Polytec PolyFile Type Library · ContainedFiles Collection : Count Property*

### Description

Returns the number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYFILELib~ContainedFiles~Item.html` · Polytec PolyFile Type Library · ContainedFiles Collection : Item Property*

### Description

Returns an item of this collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As ContainedFile
```

### Parameters

lIndex

Index of the item.
