# POLYFILELib – IAlignments2

## IAlignments2 Interface

*Quelle: `POLYFILELib~IAlignments2.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. It contains 2D and 3D alignment objects.

### Object Model

### Remarks

It is recommended to cast to the Alignments object.


---

## IAlignments2 Interface Members

*Quelle: `POLYFILELib~IAlignments2_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Alignments2D | Returns the 2D Alignments object for the file. |
|---|---|
| Alignments3D | Returns the 3D Alignments object for the file. |
| Name | Returns "Alignments". Can be used as an index into the Infos collection . |
| Type | Returns ptcInfoAlignments. Can be used as an index into the Infos collection . |


---

## Alignments2D Property

*Quelle: `POLYFILELib~IAlignments2~Alignments2D.html` · Polytec PolyFile Type Library · IAlignments2 Interface : Alignments2D Property*

### Description

Returns the 2D Alignments object for the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Alignments2D As IAlignments2D
```


---

## Alignments3D Property

*Quelle: `POLYFILELib~IAlignments2~Alignments3D.html` · Polytec PolyFile Type Library · IAlignments2 Interface : Alignments3D Property*

### Description

Returns the 3D Alignments object for the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Alignments3D As IAlignments3D
```


---

## Name Property

*Quelle: `POLYFILELib~IAlignments2~Name.html` · Polytec PolyFile Type Library · IAlignments2 Interface : Name Property*

### Description

Returns "Alignments". Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "Alignments".


---

## Type Property

*Quelle: `POLYFILELib~IAlignments2~Type.html` · Polytec PolyFile Type Library · IAlignments2 Interface : Type Property*

### Description

Returns ptcInfoAlignments. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```
