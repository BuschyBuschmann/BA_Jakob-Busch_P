# POLYFILELib – Alignments

## Alignments Object

*Quelle: `POLYFILELib~Alignments.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. It contains 2D, 3D, and camera alignment objects.

### Object Model

### Remarks

Available in MPV/PSV files only.


---

## Alignments Object Members

*Quelle: `POLYFILELib~Alignments_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetVideoRect | Gets the video rectangle defining the video coordinate system. |
|---|---|

### Public Properties

| Alignments2D | Returns the 2D Alignments object for the file. |
|---|---|
| Alignments3D | Returns the 3D Alignments object for the file. |
| AlignmentsCamera | Returns the Camera Alignments object for the file. |
| Name | Returns "Alignments". Can be used as an index into the Infos collection . |
| Type | Returns ptcInfoAlignments. Can be used as an index into the Infos collection . |


---

## GetVideoRect Method

*Quelle: `POLYFILELib~Alignments~GetVideoRect.html` · Polytec PolyFile Type Library · Alignments Object : GetVideoRect Method*

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

*Quelle: `POLYFILELib~Alignments~Alignments2D.html` · Polytec PolyFile Type Library · Alignments Object : Alignments2D Property*

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

*Quelle: `POLYFILELib~Alignments~Alignments3D.html` · Polytec PolyFile Type Library · Alignments Object : Alignments3D Property*

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

## AlignmentsCamera Property

*Quelle: `POLYFILELib~Alignments~AlignmentsCamera.html` · Polytec PolyFile Type Library · Alignments Object : AlignmentsCamera Property*

### Description

Returns the Camera Alignments object for the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AlignmentsCamera As IAlignmentsCamera
```


---

## Name Property

*Quelle: `POLYFILELib~Alignments~Name.html` · Polytec PolyFile Type Library · Alignments Object : Name Property*

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

*Quelle: `POLYFILELib~Alignments~Type.html` · Polytec PolyFile Type Library · Alignments Object : Type Property*

### Description

Returns ptcInfoAlignments. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```
