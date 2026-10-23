# POLYFILELib – ContainedFile

## ContainedFile Object

*Quelle: `POLYFILELib~ContainedFile.html` · Polytec PolyFile Type Library*

### Description

Item of the ContainedFiles collection. It refers to one of the single files building a combined file.

### Object Model


---

## ContainedFile Object Members

*Quelle: `POLYFILELib~ContainedFile_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Save | Save File information into the combined storage. |
|---|---|

### Public Properties

| Caps | Type of relation with the combined file. |
|---|---|
| File | Returns the PolyFile object for this contained file. |
| Name | Name of the Contained file. |


---

## Save Method

*Quelle: `POLYFILELib~ContainedFile~Save.html` · Polytec PolyFile Type Library · ContainedFile Object : Save Method*

### Description

Save File information into the combined storage.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```

### Remarks

If Caps is ptcContainedLink to make a link to the combined file, it must be in the same drive with the combined file and if the combined file to be saved in the network folder, it must be in the same folder.


---

## Caps Property

*Quelle: `POLYFILELib~ContainedFile~Caps.html` · Polytec PolyFile Type Library · ContainedFile Object : Caps Property*

### Description

Type of relation with the combined file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCContainedCaps
```


---

## File Property

*Quelle: `POLYFILELib~ContainedFile~File.html` · Polytec PolyFile Type Library · ContainedFile Object : File Property*

### Description

Returns the PolyFile object for this contained file.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property File As IPolyFile8
```


---

## Name Property

*Quelle: `POLYFILELib~ContainedFile~Name.html` · Polytec PolyFile Type Library · ContainedFile Object : Name Property*

### Description

Name of the Contained file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```
