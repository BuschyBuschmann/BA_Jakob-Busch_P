# POLYFILELib – VideoBitmap

## VideoBitmap Object

*Quelle: `POLYFILELib~VideoBitmap.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. The VideoBitmap object allows to retrieve and set the video image used for MPV/PSV measurement files.

### Remarks

The object is only available for MPV/PSV measurement files.


---

## VideoBitmap Object Members

*Quelle: `POLYFILELib~VideoBitmap_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Get3DVideoOffset | Gets the offset of the video position in 3d coordinates. |
|---|---|
| GetImageRect | Gets the rectangle of the image in video coordinates. |
| GetVideoOffset | Gets the offset of the video position in video coordinates. |
| LoadImageFile | Loads an image from the given file. |
| Save | Commits the changes to the VideoBitmap object to the file. |
| SetImage | Sets the image to image given in the array of bytes. |

### Public Properties

| Image | Returns an array of bytes containing the image in the format specified by the PTCGraphicFormatType enumerator. Saving this array to a binary file with a corresponding extension allows to open the image in a suitable image processing application. |
|---|---|
| Name | Returns "VideoBitmap. Can be used as an index to the Infos collection . |
| TextureColumns | The number of columns in the stitched video image of a combined file. |
| TextureCoordinates | Returns the texture coordinates for the scan points. |
| TextureCount | Returns the number of video bitmaps of contained files that were stitched. |
| TextureRows | The number of rows in the stitched video image of a combined file. |
| Type | Returns ptcInfoVideoBitmap. Can be used as an index to the Infos collection . |


---

## Get3DVideoOffset Method

*Quelle: `POLYFILELib~VideoBitmap~Get3DVideoOffset.html` · Polytec PolyFile Type Library · VideoBitmap Object : Get3DVideoOffset Method*

### Description

Gets the offset of the video position in 3d coordinates.

### Syntax

*Visual Basic:*
```
Public Sub Get3DVideoOffset( _
   ByRef pfXVal As Single, _
   ByRef pfYVal As Single, _
   ByRef pfZVal As Single _
)
```

### Parameters

pfXVal

The x component of the video offset.

pfYVal

The y component of the video offset.

pfZVal

The z component of the video offset.

### Remarks

The offset is used for PSV-UHF systems to adjust the position of the video plane for the 3D display to the position of the xy-positioning stage.

### Example


---

## GetImageRect Method

*Quelle: `POLYFILELib~VideoBitmap~GetImageRect.html` · Polytec PolyFile Type Library · VideoBitmap Object : GetImageRect Method*

### Description

Gets the rectangle of the image in video coordinates.

### Syntax

*Visual Basic:*
```
Public Sub GetImageRect( _
   ByRef pfLeft As Single, _
   ByRef pfTop As Single, _
   ByRef pfRight As Single, _
   ByRef pfBottom As Single _
)
```

### Parameters

pfLeft

receives the left side of the image rectangle

pfTop

receives the top side of the image rectangle

pfRight

receives the right side of the image rectangle

pfBottom

receives the bottom side of the image rectangle

### Remarks

The rectangle is calculated from the aspect ratio of the image assuming square pixels. This is used for default cases, where the rectangle of the video image in video coordinates is not available, like VibSoft files with video image and old files. For all other cases (in any case you have a MeasPoints collection) use GetVideoRect.


---

## GetVideoOffset Method

*Quelle: `POLYFILELib~VideoBitmap~GetVideoOffset.html` · Polytec PolyFile Type Library · VideoBitmap Object : GetVideoOffset Method*

### Description

Gets the offset of the video position in video coordinates.

### Syntax

*Visual Basic:*
```
Public Sub GetVideoOffset( _
   ByRef pfXVal As Single, _
   ByRef pfYVal As Single _
)
```

### Parameters

pfXVal

The x component of the video position.

pfYVal

The y component of the video position.

### Remarks

The offset is used for PSV-UHF systems to adjust the video image to the position of the xy-positioning stage.

### Example


---

## LoadImageFile Method

*Quelle: `POLYFILELib~VideoBitmap~LoadImageFile.html` · Polytec PolyFile Type Library · VideoBitmap Object : LoadImageFile Method*

### Description

Loads an image from the given file.

### Syntax

*Visual Basic:*
```
Public Sub LoadImageFile( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

Name and path of the image file.

### Remarks

The supported image file formats are Bitmap (.bmp), Jpeg (.jpg), Tiff (.tif), PNG (.png) and GIF (.gif)

### Example


---

## Save Method

*Quelle: `POLYFILELib~VideoBitmap~Save.html` · Polytec PolyFile Type Library · VideoBitmap Object : Save Method*

### Description

Commits the changes to the VideoBitmap object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## SetImage Method

*Quelle: `POLYFILELib~VideoBitmap~SetImage.html` · Polytec PolyFile Type Library · VideoBitmap Object : SetImage Method*

### Description

Sets the image to image given in the array of bytes.

### Syntax

*Visual Basic:*
```
Public Sub SetImage( _
   ByVal psaImage() As Byte _
)
```

### Parameters

psaImage

0-based, one dimensional array of bytes containing the binary representation of the image corresponding to an image file in the formats Bitmap (.bmp), Jpeg (.jpg), Tiff (.tif), PNG (.png) or GIF (.gif).


---

## Image Property

*Quelle: `POLYFILELib~VideoBitmap~Image.html` · Polytec PolyFile Type Library · VideoBitmap Object : Image Property*

### Description

Returns an array of bytes containing the image in the format specified by the PTCGraphicFormatType enumerator. Saving this array to a binary file with a corresponding extension allows to open the image in a suitable image processing application.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Image( _
   ByVal PTCGraphicFormatType As PTCGraphicFormatType, _
   ByRef plWidth As Long, _
   ByRef plHeight As Long _
) As Byte()
```

### Parameters

PTCGraphicFormatType

| Value | Description |
|---|---|
| ptcGraphicFormatBitmap | Bitmap format |
| ptcGraphicFormatGIF | GIF format |
| ptcGraphicFormatJPEG | JPEG format |
| ptcGraphicFormatMacintoshPict | Not supported any more. |
| ptcGraphicFormatMetafile | Not supported any more. |
| ptcGraphicFormatPCX | Not supported any more. |
| ptcGraphicFormatPhotoshop30 | Not supported any more. |
| ptcGraphicFormatPNG | PNG format |
| ptcGraphicFormatPostscript | Not supported any more. |
| ptcGraphicFormatSUN | Not supported any more. |
| ptcGraphicFormatTARGA | Not supported any more. |
| ptcGraphicFormatTIFF | TIFF format |
| ptcGraphicFormatWordPerfect | Not supported any more. |
desired format of the image

plWidth

returned width of image

plHeight

returned height of image

### Return Type

one dimensional, 0-based array of byte values

### Remarks

For combined files, the video bitmaps of the contained files are stitched in a single bitmap that is organized in rows and columns. Use the index of the contained file returned by the ContainedFileIndex Property, the number of columns (TextureColumns Property) and the number of rows (TextureRows Property) to find the position of the corresponding bitmap of the contained file in the stitched bitmap. The images are stitched row by row.

### Example

This macro opens a PSV scan file and saves the contained bitmap to a file in the .bmp format.

- Save Bitmap to File (Visual Basic)

```
Dim oFile  As New PolyFile
oFile.Open("D:\Temp\FileWithBitmap.svd")

Dim oVideoBitmap As VideoBitmap
Set oVideoBitmap = oFile.Infos.Type(ptcInfoVideoBitmap)

Dim image() As Byte
Dim lWidth As Long
Dim lHeight As Long
image = oVideoBitmap.Image(ptcGraphicFormatBitmap, lWidth, lHeight)

oFile.Close()

Open strBmpFileName For Binary Access Write As #1
Put #1,,image
Close #1
```


---

## Name Property

*Quelle: `POLYFILELib~VideoBitmap~Name.html` · Polytec PolyFile Type Library · VideoBitmap Object : Name Property*

### Description

Returns "VideoBitmap. Can be used as an index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "VideoBitmap".


---

## TextureColumns Property

*Quelle: `POLYFILELib~VideoBitmap~TextureColumns.html` · Polytec PolyFile Type Library · VideoBitmap Object : TextureColumns Property*

### Description

The number of columns in the stitched video image of a combined file.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TextureColumns As Long
```

### Remarks

For combined files, the video bitmaps of the contained files are stitched in a single bitmap that is organized in rows and columns. Use the index of the contained file returned by the ContainedFileIndex Property, the number of columns and the number of rows to find the position of the corresponding bitmap of the contained file in the stitched bitmap. The images are stitched row by row.


---

## TextureCoordinates Property

*Quelle: `POLYFILELib~VideoBitmap~TextureCoordinates.html` · Polytec PolyFile Type Library · VideoBitmap Object : TextureCoordinates Property*

### Description

Returns the texture coordinates for the scan points.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TextureCoordinates As Single()
```

### Return Type

Zero-based array of texture coordinates for every scan point. The size of the array is twice the number of scan points. It contains the x- and y-coordinates in an alternating sequence (x0, y0, y1, y1, ..., ).

### Remarks

The texture coordinates are defined in a coordinate system, where the top left corner of the texture is x = 0.0, y = 1.0 and the bottom right corner is x = 1.0, y = 0.0.


---

## TextureCount Property

*Quelle: `POLYFILELib~VideoBitmap~TextureCount.html` · Polytec PolyFile Type Library · VideoBitmap Object : TextureCount Property*

### Description

Returns the number of video bitmaps of contained files that were stitched.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TextureCount As Long
```

### Remarks

For combined files, the video bitmaps of the contained files are stitched in a single bitmap that is organized in rows and columns. Use the index of the contained file returned by the ContainedFileIndex Property, the number of columns and the number of rows to find the position of the corresponding bitmap of the contained file in the stitched bitmap. The images are stitched row by row.


---

## TextureRows Property

*Quelle: `POLYFILELib~VideoBitmap~TextureRows.html` · Polytec PolyFile Type Library · VideoBitmap Object : TextureRows Property*

### Description

The number of rows in the stitched video image of a combined file.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TextureRows As Long
```

### Remarks

For combined files, the video bitmaps of the contained files are stitched in a single bitmap that is organized in rows and columns. Use the index of the contained file returned by the ContainedFileIndex Property, the number of columns and the number of rows to find the position of the corresponding bitmap of the contained file in the stitched bitmap. The images are stitched row by row.


---

## Type Property

*Quelle: `POLYFILELib~VideoBitmap~Type.html` · Polytec PolyFile Type Library · VideoBitmap Object : Type Property*

### Description

Returns ptcInfoVideoBitmap. Can be used as an index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoVideoBitmap.
