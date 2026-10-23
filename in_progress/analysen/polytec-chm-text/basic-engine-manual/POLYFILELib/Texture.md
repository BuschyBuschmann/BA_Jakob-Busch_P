# POLYFILELib – Texture

## Texture Object

*Quelle: `POLYFILELib~Texture.html` · Polytec PolyFile Type Library*

### Description

Item of the Textures Collection. The Texture object represents a texture of an imported geometry.


---

## Texture Object Members

*Quelle: `POLYFILELib~Texture_members.html` · Polytec PolyFile Type Library*

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

*Quelle: `POLYFILELib~Texture~Load.html` · Polytec PolyFile Type Library · Texture Object : Load Method*

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

*Quelle: `POLYFILELib~Texture~LoadImageFile.html` · Polytec PolyFile Type Library · Texture Object : LoadImageFile Method*

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

*Quelle: `POLYFILELib~Texture~Save.html` · Polytec PolyFile Type Library · Texture Object : Save Method*

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

*Quelle: `POLYFILELib~Texture~SetImage.html` · Polytec PolyFile Type Library · Texture Object : SetImage Method*

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

*Quelle: `POLYFILELib~Texture~Height.html` · Polytec PolyFile Type Library · Texture Object : Height Property*

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

*Quelle: `POLYFILELib~Texture~Image.html` · Polytec PolyFile Type Library · Texture Object : Image Property*

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

*Quelle: `POLYFILELib~Texture~Width.html` · Polytec PolyFile Type Library · Texture Object : Width Property*

### Description

The width of the texture in pixels.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Width As Long
```
