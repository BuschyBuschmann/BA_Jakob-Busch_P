# PolyAcquisitionLib – AcquisitionPointDataStream

## AcquisitionPointDataStream Object

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream.html` · Polytec PolyAcquisition Type Library*

### Description

The data stream of the point data.


---

## AcquisitionPointDataStream Object Members

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream_members.html` · Polytec PolyAcquisition Type Library*

### Public Methods

| Close | Closes the data stream. |
|---|---|
| Read | Reads data from the data stream. |

### Public Properties

| BlockIndex | The block index of the data in the stream. |
|---|---|
| FrameIndex | The frame index of the data in the stream. |
| Length | The current length of the data stream. |
| Position | The current position of the seek pointer of the data stream. |
| ScanPointIndex | The scan point index of the point data stream. |
| Stride | The stride of the values in the data stream. |


---

## Close Method

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~Close.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : Close Method*

### Description

Closes the data stream.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## Read Method

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~Read.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : Read Method*

### Description

Reads data from the data stream.

### Syntax

*Visual Basic:*
```
Public Function Read( _
   ByVal lOffset As Long, _
   ByVal lCount As Long, _
   ByRef ppData() As Single _
) As Long
```

### Parameters

lOffset

Zero-based index into the given data array where Read starts to store the data.

lCount

The number of samples or FFT lines to read. Pass -1 for the maximum number of samples possible.

ppData

Zero-based, one-dimensional array of Single to store the data in. If you pass an empty array, Read will allocate an array of suitable size. If you pass an array that is too small, Read will read less the lCount values.

### Return Type

The number of samples or FFT lines that were read.

### Remarks

The number of values stored in the array depends on the Stride of the data. If the stride is two, every sample or FFT line occupies two places in the data array.


---

## BlockIndex Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~BlockIndex.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : BlockIndex Property*

### Description

The block index of the data in the stream.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BlockIndex As Long
```

### Return Type

The 1-based block index.


---

## FrameIndex Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~FrameIndex.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : FrameIndex Property*

### Description

The frame index of the data in the stream.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrameIndex As Long
```


---

## Length Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~Length.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : Length Property*

### Description

The current length of the data stream.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Length As Long
```

### Remarks

For time domain the length corresponds to the number of samples in the stream. For FFT domain the length corresponds to the number of FFT lines.


---

## Position Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~Position.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : Position Property*

### Description

The current position of the seek pointer of the data stream.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Position As Long
```

### Remarks

The position is the 0-based index of the first time sample or FFT line that will be retrieved at the next call to the Read Method.


---

## ScanPointIndex Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~ScanPointIndex.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : ScanPointIndex Property*

### Description

The scan point index of the point data stream.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanPointIndex As Long
```

### Return Type

The one-based scan point index.


---

## Stride Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointDataStream~Stride.html` · Polytec PolyAcquisition Type Library · AcquisitionPointDataStream Object : Stride Property*

### Description

The stride of the values in the data stream.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Stride As Long
```

### Remarks

The stride is 1 or 2 depending on the signal and display. E.g. for the display type ptcDisplayTypeRealImag the stride is 2 and the stream contains interleaved real and imaginary parts for the complex FFT lines.
