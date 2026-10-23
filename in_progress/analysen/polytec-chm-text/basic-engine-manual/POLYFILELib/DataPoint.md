# POLYFILELib – DataPoint

## DataPoint Object

*Quelle: `POLYFILELib~DataPoint.html` · Polytec PolyFile Type Library*

### Description

Item of the DataPoints collection.

### Object Model


---

## DataPoint Object Members

*Quelle: `POLYFILELib~DataPoint_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Get3DData | Retrieves the 3D data of this measurement point for a given Display. If the data source is 1D, the missing directions of the data are filled up with zeros. |
|---|---|
| Get3DDataSection | Get3DDataSection extends Get3DData in two ways: first it is possible to specify the average number to retrieve. Moreover it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex. |
| GetData | Retrieves the data of this measurement point for a given Display. |
| GetDataSection | GetDataSection extends GetData in two ways: first it is possible to specify the average number to retrieve. Moreover it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex. |
| GetFrameBoundaries | Retrieves the frame boundaries for a given time signal acquired in MultiFrame mode. |
| GetFrames | Retrieves the frame count for a given Display. |
| GetScanStatus | Retrieves the scan status of the scan point for the given signal. |
| SetData | Sets the data of this measurement point for a given User-defined signal. |
| SetScanStatus | Sets the scan status of the scan point for the given signal. |

### Public Properties

| AverageCount | Returns the number of available time traces that contributed to an averaged FFT or averaged time trace. |
|---|---|
| MeasPoint | Returns the measurement point corresponding to this data point. |
| PointDomain | Returns the PointDomain object. |


---

## Get3DData Method

*Quelle: `POLYFILELib~DataPoint~Get3DData.html` · Polytec PolyFile Type Library · DataPoint Object : Get3DData Method*

### Description

Retrieves the 3D data of this measurement point for a given Display. If the data source is 1D, the missing directions of the data are filled up with zeros.

### Syntax

*Visual Basic:*
```
Public Function Get3DData( _
   ByVal pIDisplay As IDisplay2, _
   ByVal lFrame As Long _
) As Single()
```

### Parameters

pIDisplay

Specifies the type of data to receive. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

lFrame

Frame number. In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. The frame numbers of user-defined signals start at 1. The signals principal inputs and virtual coherences have frames from 1 to the number of reference channels. The frame number should be 0 in all other cases.

### Return Type

One dimensional 0-based array of float values. When you ask for a display with two types of data (Real & Imaginary, Magnitude & Phase), the data returned will be interleaved. E.g. in case of display Real & Imaginary, the real values are stored at even indices and imaginary values are stored at odd indices.

The data for the x-direction is followed by the data of the y-direction and z-direction.


---

## Get3DDataSection Method

*Quelle: `POLYFILELib~DataPoint~Get3DDataSection.html` · Polytec PolyFile Type Library · DataPoint Object : Get3DDataSection Method*

### Description

Get3DDataSection extends Get3DData in two ways: first it is possible to specify the average number to retrieve. Moreover it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex.

### Syntax

*Visual Basic:*
```
Public Function Get3DDataSection( _
   ByVal pIDisplay As IDisplay2, _
   ByVal lFrame As Long, _
   ByVal lAverage As Long, _
   ByVal lFirstIndex As Long, _
   ByVal lLastIndex As Long _
) As Single()
```

### Parameters

pIDisplay

Specifies the type of data to receive. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

lFrame

Frame number. In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. The frame numbers of user-defined signals start at 1. The signals principal inputs and virtual coherences have frames from 1 to the number of reference channels. The frame number should be 0 in all other cases.

lAverage

FFT average number. An average number bigger than 1 is only valid for time traces taken in an acquisition mode with FFT averages. In this case you can retrieve the time traces that contributed to the averaged FFT spectrum. Valid values for Average are 1 to AverageCount.

lFirstIndex

Index of first data value to retrieve.

lLastIndex

Index of last data value to retrieve.

### Return Type

One dimensional 0-based array of float values. The data returned in Single(0 : LastIndex  FirstIndex) by Get3DDataSection is identical to the data returned by Get3DData in Single(FirstIndex : LastIndex) for not-interleaved data. For interleaved data, the data returned in Single(0 : 2 * (LastIndex  FirstIndex) + 1) is identical to the data returned by Get3DData in Single(2 * FirstIndex : 2 * LastIndex + 1). Note that in any case both arrays are zero-based.

The data for the x-direction is followed by the data of the y-direction and z-direction.


---

## GetData Method

*Quelle: `POLYFILELib~DataPoint~GetData.html` · Polytec PolyFile Type Library · DataPoint Object : GetData Method*

### Description

Retrieves the data of this measurement point for a given Display.

### Syntax

*Visual Basic:*
```
Public Function GetData( _
   ByVal pIDisplay As IDisplay2, _
   ByVal lFrame As Long _
) As Single()
```

### Parameters

pIDisplay

Specifies the type of data to receive. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

lFrame

Frame number. In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. The frame numbers of user-defined signals start at 1. The signals principal inputs and virtual coherences have frames from 1 to the number of reference channels. The frame number should be 0 in all other cases.

### Return Type

One dimensional 0-based array of float values. When you ask for a display with two types of data (Real & Imaginary, Magnitude & Phase), the data returned will be interleaved. E.g. in case of display Real & Imaginary, the real values are stored at even indices and imaginary values are stored at odd indices.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## GetDataSection Method

*Quelle: `POLYFILELib~DataPoint~GetDataSection.html` · Polytec PolyFile Type Library · DataPoint Object : GetDataSection Method*

### Description

GetDataSection extends GetData in two ways: first it is possible to specify the average number to retrieve. Moreover it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex.

### Syntax

*Visual Basic:*
```
Public Function GetDataSection( _
   ByVal pIDisplay As IDisplay2, _
   ByVal lFrame As Long, _
   ByVal lAverage As Long, _
   ByVal lFirstIndex As Long, _
   ByVal lLastIndex As Long _
) As Single()
```

### Parameters

pIDisplay

Specifies the type of data to receive. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

lFrame

Frame number. In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. The frame numbers of user-defined signals start at 1. The signals principal inputs and virtual coherences have frames from 1 to the number of reference channels. The frame number should be 0 in all other cases.

lAverage

FFT average number. An average number bigger than 1 is only valid for time traces taken in an acquisition mode with FFT averages. In this case you can retrieve the time traces that contributed to the averaged FFT spectrum. Valid values for Average are 1 to AverageCount.

lFirstIndex

Index of first data value to retrieve.

lLastIndex

Index of last data value to retrieve.

### Return Type

One dimensional 0-based array of float values. The data returned in Single(0 : LastIndex  FirstIndex) by GetDataSection is identical to the data returned by GetData in Single(FirstIndex : LastIndex) for not-interleaved data. For interleaved data, the data returned in Single(0 : 2 * (LastIndex  FirstIndex) + 1) is identical to the data returned by GetData in Single(2 * FirstIndex : 2 * LastIndex + 1). Note that in any case both arrays are zero-based.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## GetFrameBoundaries Method

*Quelle: `POLYFILELib~DataPoint~GetFrameBoundaries.html` · Polytec PolyFile Type Library · DataPoint Object : GetFrameBoundaries Method*

### Description

Retrieves the frame boundaries for a given time signal acquired in MultiFrame mode.

### Syntax

*Visual Basic:*
```
Public Function GetFrameBoundaries( _
   ByVal pIDisplay As IDisplay2, _
   ByVal lAverage As Long _
) As Double()
```

### Parameters

pIDisplay

Specifies the type of data to receive. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

lAverage

FFT average number. An average number bigger than 1 is only valid for time traces taken in an acquisition mode with FFT averages. In this case you can retrieve the time traces that contributed to the averaged FFT spectrum. Valid values for Average are 1 to AverageCount.


---

## GetFrames Method

*Quelle: `POLYFILELib~DataPoint~GetFrames.html` · Polytec PolyFile Type Library · DataPoint Object : GetFrames Method*

### Description

Retrieves the frame count for a given Display.

### Syntax

*Visual Basic:*
```
Public Function GetFrames( _
   ByVal pIDisplay As IDisplay2 _
) As Long
```

### Parameters

pIDisplay

Specifies the type of data to receive. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

### Return Type

In MultiFrame mode, for virtual coherences, for principal inputs and for user signals you can get a frame count greater than 1. The frame count for MultiFrame data is without the average frame.


---

## GetScanStatus Method

*Quelle: `POLYFILELib~DataPoint~GetScanStatus.html` · Polytec PolyFile Type Library · DataPoint Object : GetScanStatus Method*

### Description

Retrieves the scan status of the scan point for the given signal.

### Syntax

*Visual Basic:*
```
Public Function GetScanStatus( _
   ByVal pIDisplay As IDisplay2 _
) As PTCScanStatus
```

### Parameters

pIDisplay

Specifies the type of data to receive. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

### Remarks

If you want to retrieve the scan status of many measurement points, it is more efficient to use the GetScanStatus Method.


---

## SetData Method

*Quelle: `POLYFILELib~DataPoint~SetData.html` · Polytec PolyFile Type Library · DataPoint Object : SetData Method*

### Description

Sets the data of this measurement point for a given User-defined signal.

### Syntax

*Visual Basic:*
```
Public Sub SetData( _
   ByVal pISignal As ISignal5, _
   ByVal lFrame As Long, _
   ByVal psaData() As Single _
)
```

### Parameters

pISignal

Specifies the type of data to set. To obtain a user-defined signal, navigate through the PointDomain / Channels / Signals objects. Channel Caps must be ptcChannelCapsUser.

lFrame

Frame number - starting from 1. You have to specify a frame number starting from 1. Remember, data must be put with the sequential increasing number of Frame. Once data have been set for each frame you can change data for any frame directly with this method.

psaData

One dimensional array of float values. When the signal is complex, the length of data array must be double; the real values are stored at even indices and imaginary values are stored at odd indices.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## SetScanStatus Method

*Quelle: `POLYFILELib~DataPoint~SetScanStatus.html` · Polytec PolyFile Type Library · DataPoint Object : SetScanStatus Method*

### Description

Sets the scan status of the scan point for the given signal.

### Syntax

*Visual Basic:*
```
Public Sub SetScanStatus( _
   ByVal pIDisplay As IDisplay2, _
   ByVal PTCScanStatus As PTCScanStatus _
)
```

### Parameters

pIDisplay

Specifies the signal to specify the scan status for. To obtain a Display object navigate through the PointDomain / Channels / Signals / Displays objects.

PTCScanStatus

| Value | Description |
|---|---|
| ptcScanStatusAssignedChannel1D | Point mapped to a 1D channel, usable only with MPV files. |
| ptcScanStatusAssignedChannel3D | Point mapped to a 3D channel, usable only with MPV files. |
| ptcScanStatusAssignedSensor | Point mapped to a sensor, usable only with MPV files. |
| ptcScanStatusDisabled | Point is disabled for scan. |
| ptcScanStatusHidden | Point is hidden by the 3D geometry. |
| ptcScanStatusInterpolate | The data at the point shall be interpolated from the data of its neighbors. |
| ptcScanStatusInterpolationFailed | The interpolation of the data of this point failed. |
| ptcScanStatusInvalidated | Point is invalidated. |
| ptcScanStatusInvalidFrames | Point has invalid frames (MultiFrame only). |
| ptcScanStatusNone | Point is not measured. |
| ptcScanStatusNotReachable | Point was not reachable by the scanner. |
| ptcScanStatusOptimal | Point is optimal (Signal Enhancement only). |
| ptcScanStatusOverrange | Point has overrange status. |
| ptcScanStatusValid | Point is valid. |
| ptcScanStatusVideoTriangulationFailed | The video-triangulation failed for this point. |
The scan status of the point.

### Remarks

You can only set the scan status for user-defined datasets. You can use this method to invalidate user-defined data at this scan point by adding the status ptcScanStatusInvalidated to the status you retrieved from GetScanStatus Method. The MPV/PSV software then will ignore the data of the signal of this point and interpolate it by using neighbor scan points, when interpolate invalid points is active in the presentation.

If you want to change the scan status of many measurement points it is more efficient to use the SetScanStatus Method.


---

## AverageCount Property

*Quelle: `POLYFILELib~DataPoint~AverageCount.html` · Polytec PolyFile Type Library · DataPoint Object : AverageCount Property*

### Description

Returns the number of available time traces that contributed to an averaged FFT or averaged time trace.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AverageCount( _
   ByVal pIDisplay As IDisplay2 _
) As Long
```

### Parameters

pIDisplay

Specifies the type of data to receive the average count for. The signal of the display is used to distinguish between FFT, time domain and user signals.

### Remarks

For user signals the average count is always 1. If signal enhancement is active, the number of averages depends on the signal quality and can differ from point to point and from the average count setting in the acquisition properties. For the number of averages that contributed to this signal see the AverageCount property of the MeasPoint object.


---

## MeasPoint Property

*Quelle: `POLYFILELib~DataPoint~MeasPoint.html` · Polytec PolyFile Type Library · DataPoint Object : MeasPoint Property*

### Description

Returns the measurement point corresponding to this data point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MeasPoint As IMeasPoint9
```


---

## PointDomain Property

*Quelle: `POLYFILELib~DataPoint~PointDomain.html` · Polytec PolyFile Type Library · DataPoint Object : PointDomain Property*

### Description

Returns the PointDomain object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PointDomain As PointDomain
```
