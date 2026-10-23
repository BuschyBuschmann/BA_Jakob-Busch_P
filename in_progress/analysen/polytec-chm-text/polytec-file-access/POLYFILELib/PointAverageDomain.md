# POLYFILELib – PointAverageDomain

## PointAverageDomain Object

*Quelle: `POLYFILELib~PointAverageDomain.html` · Polytec PolyFile Type Library*

### Description

Item of the PointAverageDomains collection. A domain of the point average data.

### Object Model


---

## PointAverageDomain Object Members

*Quelle: `POLYFILELib~PointAverageDomain_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetData | Retrieves the data of this point average for a given Display. |
|---|---|
| GetDataSection | GetDataSection extends GetData in two ways: first it is possible to specify the average number to retrieve. Moreover it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex. |
| GetFrames | Returns the number of frames for the given display . |
| GetXAxis | Returns an XAxis object that describes the x-axis to display the data of this point average domain. |
| GetYAxes | Returns the YAxes collection. |
| SetData | Sets the data of this measurement point for a given User-defined signal. |

### Public Properties

| AverageCount | Returns the number of available time traces that contributed to an averaged FFT spectrum. |
|---|---|
| Channels | Returns the Channels collection . |
| Name | Returns the name of the PointAverageDomain. Can be used as an index to the PointAverageDomains collection . |
| Type | Returns the type of the PointAverageDomain. Can be used as an index to the PointAverageDomains collection . |


---

## GetData Method

*Quelle: `POLYFILELib~PointAverageDomain~GetData.html` · Polytec PolyFile Type Library · PointAverageDomain Object : GetData Method*

### Description

Retrieves the data of this point average for a given Display.

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

Specifies the type of data to receive. To obtain a Display object navigate through the Channels / Signals / Displays objects.

lFrame

Frame number. In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. The frame numbers of user-defined signals start at 1. The signals principal inputs and virtual coherences have frames from 1 to the number of reference channels. The frame number should be 0 in all other cases.

### Return Type

When you asked for a display with two types of data (Real & Imaginary, Magnitude & Phase), the data returned will be interleaved. E.g. in case of display Real & Imaginary, the real values are stored at even indices and imaginary values are stored at odd indices.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## GetDataSection Method

*Quelle: `POLYFILELib~PointAverageDomain~GetDataSection.html` · Polytec PolyFile Type Library · PointAverageDomain Object : GetDataSection Method*

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

Specifies the type of data to receive. To obtain a Display object navigate through the Channels / Signals / Displays objects.

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

## GetFrames Method

*Quelle: `POLYFILELib~PointAverageDomain~GetFrames.html` · Polytec PolyFile Type Library · PointAverageDomain Object : GetFrames Method*

### Description

Returns the number of frames for the given display.

### Syntax

*Visual Basic:*
```
Public Function GetFrames( _
   ByVal pIDisplay As IDisplay2 _
) As Long
```

### Parameters

pIDisplay

The display to get the number of frames for.

### Return Type

In MultiFrame mode, for virtual coherences, for principal inputs and for user signals you can get a frame count greater than 1. The frame count for MultiFrame data is without the average frame.


---

## GetXAxis Method

*Quelle: `POLYFILELib~PointAverageDomain~GetXAxis.html` · Polytec PolyFile Type Library · PointAverageDomain Object : GetXAxis Method*

### Description

Returns an XAxis object that describes the x-axis to display the data of this point average domain.

### Syntax

*Visual Basic:*
```
Public Function GetXAxis( _
   ByVal pIDisplay As IDisplay2 _
) As XAxis
```

### Parameters

pIDisplay

Display to retrieve the x-axis information for.


---

## GetYAxes Method

*Quelle: `POLYFILELib~PointAverageDomain~GetYAxes.html` · Polytec PolyFile Type Library · PointAverageDomain Object : GetYAxes Method*

### Description

Returns the YAxes collection.

### Syntax

*Visual Basic:*
```
Public Function GetYAxes( _
   ByVal pIDisplay As IDisplay2 _
) As YAxes
```

### Parameters

pIDisplay

Display to retrieve the y-axis information for


---

## SetData Method

*Quelle: `POLYFILELib~PointAverageDomain~SetData.html` · Polytec PolyFile Type Library · PointAverageDomain Object : SetData Method*

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

Specifies the type of data to set. To obtain a user-defined average spectrum, navigate through the Channels / Signals objects. Channel Caps must be ptcChannelCapsUser.

lFrame

Frame number  starting from 1. You have to specify a frame number starting from 1. Remember, data must be put with the sequential increasing number of frame. You cant set data for frame 2 without setting data for frame 1 first. Once data have been set for each frame you can change data for any frame directly with this method.

psaData

One dimensional 0-based array of float values. When the signal is complex, the length of data array must be even; the real values are stored at even indices and imaginary values are stored at odd indices.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## AverageCount Property

*Quelle: `POLYFILELib~PointAverageDomain~AverageCount.html` · Polytec PolyFile Type Library · PointAverageDomain Object : AverageCount Property*

### Description

Returns the number of available time traces that contributed to an averaged FFT spectrum.

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

## Channels Property

*Quelle: `POLYFILELib~PointAverageDomain~Channels.html` · Polytec PolyFile Type Library · PointAverageDomain Object : Channels Property*

### Description

Returns the Channels collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Channels As IChannels2
```


---

## Name Property

*Quelle: `POLYFILELib~PointAverageDomain~Name.html` · Polytec PolyFile Type Library · PointAverageDomain Object : Name Property*

### Description

Returns the name of the PointAverageDomain. Can be used as an index to the PointAverageDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYFILELib~PointAverageDomain~Type.html` · Polytec PolyFile Type Library · PointAverageDomain Object : Type Property*

### Description

Returns the type of the PointAverageDomain. Can be used as an index to the PointAverageDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDomainType
```
