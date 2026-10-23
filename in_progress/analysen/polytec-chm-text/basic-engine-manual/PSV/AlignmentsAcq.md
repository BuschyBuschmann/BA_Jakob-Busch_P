# PSV – AlignmentsAcq

## AlignmentsAcq Object

*Quelle: `PSV~AlignmentsAcq.html` · Polytec PSV Type Library*

### Description

Item of the InfosAcq collection. It contains the definition of 2D and 3D alignment objects.

### Object Model


---

## AlignmentsAcq Object Members

*Quelle: `PSV~AlignmentsAcq_members.html` · Polytec PSV Type Library*

### Public Methods

| GetVideoRect | Gets the video rectangle defining the video coordinate system. |
|---|---|

### Public Properties

| Alignments2D | Returns the 2D Alignments object. |
|---|---|
| Alignments3D | Returns the 3D Alignments object. |
| AlignmentsCamera | Returns the Camera Alignments object. |
| Name | Returns "Alignments". Can be used as an index into the InfosAcq collection . |
| Type | Returns ptcInfoAlignments. Can be used as an index into the InfosAcq collection . |


---

## GetVideoRect Method

*Quelle: `PSV~AlignmentsAcq~GetVideoRect.html` · Polytec PSV Type Library · AlignmentsAcq Object : GetVideoRect Method*

### Description

Gets the video rectangle defining the video coordinate system.

### Syntax

*Visual Basic:*
```
Public Sub GetVideoRect( _
   ByRef pfLeft As Single, _
   ByRef pfTop As Single, _
   ByRef pfRight As Single, _
   ByRef pfBottom As Single _
)
```

### Parameters

pfLeft

receives the left side of the video rectangle

pfTop

receives the top side of the video rectangle

pfRight

receives the right side of the video rectangle

pfBottom

receives the bottom side of the video rectangle

### Remarks

The rectangle contains the video coordinates of the corners of the video image. In this coordinate system the alignments were defined, i.e. the positions of the alignments points on the video image and the coordinates passed to VideoToScanner are defined in this system.


---

## Alignments2D Property

*Quelle: `PSV~AlignmentsAcq~Alignments2D.html` · Polytec PSV Type Library · AlignmentsAcq Object : Alignments2D Property*

### Description

Returns the 2D Alignments object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Alignments2D As IAlignments2D
```


---

## Alignments3D Property

*Quelle: `PSV~AlignmentsAcq~Alignments3D.html` · Polytec PSV Type Library · AlignmentsAcq Object : Alignments3D Property*

### Description

Returns the 3D Alignments object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Alignments3D As IAlignments3D
```


---

## AlignmentsCamera Property

*Quelle: `PSV~AlignmentsAcq~AlignmentsCamera.html` · Polytec PSV Type Library · AlignmentsAcq Object : AlignmentsCamera Property*

### Description

Returns the Camera Alignments object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AlignmentsCamera As IAlignmentsCamera
```


---

## Name Property

*Quelle: `PSV~AlignmentsAcq~Name.html` · Polytec PSV Type Library · AlignmentsAcq Object : Name Property*

### Description

Returns "Alignments". Can be used as an index into the InfosAcq collection.

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

*Quelle: `PSV~AlignmentsAcq~Type.html` · Polytec PSV Type Library · AlignmentsAcq Object : Type Property*

### Description

Returns ptcInfoAlignments. Can be used as an index into the InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoAlignments.
