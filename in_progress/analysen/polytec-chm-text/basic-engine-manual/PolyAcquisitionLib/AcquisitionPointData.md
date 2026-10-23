# PolyAcquisitionLib – AcquisitionPointData

## AcquisitionPointData Object

*Quelle: `PolyAcquisitionLib~AcquisitionPointData.html` · Polytec PolyAcquisition Type Library*

### Description

The point data.

### Object Model


---

## AcquisitionPointData Object Members

*Quelle: `PolyAcquisitionLib~AcquisitionPointData_members.html` · Polytec PolyAcquisition Type Library*

### Public Methods

| OpenDataStream | Opens a data stream to the point data with the given block and frame index. |
|---|---|

### Public Properties

| BlockCount | The number of blocks in the point data. |
|---|---|
| Display | The display of the point data. |
| FrameBoundaries | The frame boundaries of the point data acquired in MultiFrame mode. |
| FrameCount | The number of frames of the point data acquired in MultiFrame mode. |
| RmsCorrectionFactor | The RMS correction factor of the point data. |
| XAxis | The x-axis of the point data. |
| YAxes | The collection of y-axes of the point data. |


---

## OpenDataStream Method

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~OpenDataStream.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : OpenDataStream Method*

### Description

Opens a data stream to the point data with the given block and frame index.

### Syntax

*Visual Basic:*
```
Public Function OpenDataStream( _
   ByVal lBlockIndex As Long, _
   ByVal lFrameIndex As Long _
) As AcquisitionPointDataStream
```

### Parameters

lBlockIndex

The one-based block index (1 ... BlockCount) for the data stream.

lFrameIndex

The zero-based frame index for the data stream.

### Remarks

The frame index is zero for time signals and spectra.

For MultiFrame spectra 0 is the index of the average frames, and 1 ... FrameCount are the indices of the frames.

For the virtual coherences and principal inputs signals (MIMO) the frame index is 1 ... FrameCount.


---

## BlockCount Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~BlockCount.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : BlockCount Property*

### Description

The number of blocks in the point data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BlockCount As Long
```


---

## Display Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~Display.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : Display Property*

### Description

The display of the point data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Display As IDisplay
```


---

## FrameBoundaries Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~FrameBoundaries.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : FrameBoundaries Property*

### Description

The frame boundaries of the point data acquired in MultiFrame mode.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrameBoundaries As Double()
```

### Return Type

The one-dimensional, zero-based array of double with the time values in second for the frame boundaries in the MultiFrame time signal.


---

## FrameCount Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~FrameCount.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : FrameCount Property*

### Description

The number of frames of the point data acquired in MultiFrame mode.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrameCount As Long
```

### Remarks

The frame count is > 1 for MultiFrame acquisition mode and the virtual coherences or principal inputs signals (MIMO). For MultiFrame, the frame count does not include the average frame.

Otherwise, the frame count is 1.


---

## RmsCorrectionFactor Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~RmsCorrectionFactor.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : RmsCorrectionFactor Property*

### Description

The RMS correction factor of the point data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RmsCorrectionFactor As Double
```


---

## XAxis Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~XAxis.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : XAxis Property*

### Description

The x-axis of the point data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property XAxis As IXAxis
```


---

## YAxes Property

*Quelle: `PolyAcquisitionLib~AcquisitionPointData~YAxes.html` · Polytec PolyAcquisition Type Library · AcquisitionPointData Object : YAxes Property*

### Description

The collection of y-axes of the point data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property YAxes As IYAxes
```
