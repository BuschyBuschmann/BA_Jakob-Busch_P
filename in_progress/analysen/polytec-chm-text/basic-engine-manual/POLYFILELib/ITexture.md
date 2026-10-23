# POLYFILELib – ITexture

## ITexture Object

*Quelle: `POLYFILELib~ITexture.html` · Polytec PolyFile Type Library*

### Description

ITexture Interface

### Remarks

It is recommended to cast to the Texture Object.


---

## ITexture Object Members

*Quelle: `POLYFILELib~ITexture_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Load | Loads a texture from the specified stream. |
|---|---|
| LoadImageFile | Loads a texture from an image file with the specified file name. |
| Save | Saves the texture to the specified stream. |
| SetImage | Sets the image of the texture from the specified array. |

### Public Properties

| Height | The height of the texture in pixels. |
|---|---|
| Image | Returns a byte array that corresponds to the contents of an image file in the graphics file format BMP. |
| Width | The width of the texture in pixels. |


---

## Load Method

*Quelle: `POLYFILELib~ITexture~Load.html` · Polytec PolyFile Type Library · ITexture Object : Load Method*

### Description

Loads a texture from the specified stream.

### Syntax

*Visual Basic:*
```
Public Sub Load( _
   ByVal textureStream As IStream _
)
```

### Parameters

textureStream

The stream to load the texture from.


---

## LoadImageFile Method

*Quelle: `POLYFILELib~ITexture~LoadImageFile.html` · Polytec PolyFile Type Library · ITexture Object : LoadImageFile Method*

### Description

Loads a texture from an image file with the specified file name.

### Syntax

*Visual Basic:*
```
Public Sub LoadImageFile( _
   ByVal FileName As String _
)
```

### Parameters

FileName

The name of the image file.

### Remarks

The graphics file formats supported are BMP, GIF, JPEG, PNG, and TIFF.


---

## Save Method

*Quelle: `POLYFILELib~ITexture~Save.html` · Polytec PolyFile Type Library · ITexture Object : Save Method*

### Description

Saves the texture to the specified stream.

### Syntax

*Visual Basic:*
```
Public Sub Save( _
   ByVal textureStream As IStream _
)
```

### Parameters

textureStream

The stream


---

## SetImage Method

*Quelle: `POLYFILELib~ITexture~SetImage.html` · Polytec PolyFile Type Library · ITexture Object : SetImage Method*

### Description

Sets the image of the texture from the specified array.

### Syntax

*Visual Basic:*
```
Public Sub SetImage( _
   ByVal imageArray() As Byte _
)
```

### Parameters

imageArray

### Remarks

The array must contain the contents of an image file in one of the supported fiile formats BMP, GIF, JPEG, PNG, and TIFF.


---

## Height Property

*Quelle: `POLYFILELib~ITexture~Height.html` · Polytec PolyFile Type Library · ITexture Object : Height Property*

### Description

The height of the texture in pixels.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Height As Long
```


---

## Image Property

*Quelle: `POLYFILELib~ITexture~Image.html` · Polytec PolyFile Type Library · ITexture Object : Image Property*

### Description

Returns a byte array that corresponds to the contents of an image file in the graphics file format BMP.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Image As Byte()
```


---

## Width Property

*Quelle: `POLYFILELib~ITexture~Width.html` · Polytec PolyFile Type Library · ITexture Object : Width Property*

### Description

The width of the texture in pixels.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Width As Long
```
