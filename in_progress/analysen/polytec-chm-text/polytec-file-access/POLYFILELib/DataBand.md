# POLYFILELib – DataBand

## DataBand Object

*Quelle: `POLYFILELib~DataBand.html` · Polytec PolyFile Type Library*

### Description

Item of the DataBands collection.

### Object Model


---

## DataBand Object Members

*Quelle: `POLYFILELib~DataBand_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Get3DData | Retrieves the 3D data of this band for a given Display . If the data source is 1D the method fills the missing directions with zeros. |
|---|---|
| Get3DDataSection | Get3DDataSection extends Get3DData: it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex. |
| GetData | Retrieves the data of this band for a given Display . |
| GetDataSection | GetDataSection extends GetData: it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex. |
| GetFrames | Retrieves the frame count for the given signal. |
| GetScanStatus | Gets an array containing the scan status for the given signal for all scan points of this band. |
| SetData | Sets the data for this band for a given user-defined signal. |
| SetScanStatus | Sets the scan status for the given signal for all scan points of this band. |

### Public Properties

| BandDefinition | Returns the definition of the band. |
|---|---|
| BandDomain | Returns the BandDomain. |
| EntireBandwidth | Returns whether the band is the entire bandwidth band. |
| Index | The index of the band in the DataBands collection . |
| Name | Returns the name of the band. Can be used as an index to the DataBands collection . |
| Peak | Returns the peak frequency of the band. |
| Start | Returns the start frequency of the band. |
| Stop | Returns the stop frequency of the band. |


---

## Get3DData Method

*Quelle: `POLYFILELib~DataBand~Get3DData.html` · Polytec PolyFile Type Library · DataBand Object : Get3DData Method*

### Description

Retrieves the 3D data of this band for a given Display. If the data source is 1D the method fills the missing directions with zeros.

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

To obtain a Display object navigate through the BandDomain / Channels / Signals / Displays objects.

lFrame

In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. For user-defined bands you can specify a frame number in the rage of 1, ..., (number of frames). The frame number should be 0 in all other cases. See the GetFrames Method on how to obtain the number of frames.

### Return Type

One dimensional 0-based array of float values. When you asked for a display with two types of data (Real & Imaginary, Magnitude & Phase), the data returned will be interleaved. E.g. in case of display Real & Imaginary, the real values are stored at even indices and imaginary values are stored at odd indices. The index into the array is based on the measurement point index  1.

The data for the x-direction is followed by the data of the y-direction and z-direction.


---

## Get3DDataSection Method

*Quelle: `POLYFILELib~DataBand~Get3DDataSection.html` · Polytec PolyFile Type Library · DataBand Object : Get3DDataSection Method*

### Description

Get3DDataSection extends Get3DData: it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex.

### Syntax

*Visual Basic:*
```
Public Function Get3DDataSection( _
   ByVal pIDisplay As IDisplay2, _
   ByVal lFrame As Long, _
   ByVal lFirstIndex As Long, _
   ByVal lLastIndex As Long _
) As Single()
```

### Parameters

pIDisplay

To obtain a Display object navigate through the BandDomain / Channels / Signals / Displays objects.

lFrame

In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. For user-defined bands you can specify a frame number in the range of 1, ..., (number of frames). The frame number should be 0 in all other cases. See the GetFrames Method on how to obtain the number of frames.

lFirstIndex

Index of first data value to retrieve.

lLastIndex

Index of last data value to retrieve.

### Return Type

One dimensional 0-based array of float values. The data returned in Single(0 : LastIndex  FirstIndex) by GetDataSection is identical to the data returned by GetData in Single(FirstIndex : LastIndex) for not-interleaved data. For interleaved data, the data returned in Single(0 : 2 * (LastIndex  FirstIndex) + 1) is identical to the data returned by GetData in Single(2 * FirstIndex : 2 * LastIndex + 1). Note that in any case both arrays are zero-based.

The data for the x-direction is followed by the data of the y-direction and z-direction.


---

## GetData Method

*Quelle: `POLYFILELib~DataBand~GetData.html` · Polytec PolyFile Type Library · DataBand Object : GetData Method*

### Description

Retrieves the data of this band for a given Display.

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

To obtain a Display object navigate through the BandDomain / Channels / Signals / Displays objects.

lFrame

In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. For user-defined bands you can specify a frame number in the rage of 1, ..., (number of frames). The frame number should be 0 in all other cases. See the GetFrames Method on how to obtain the number of frames.

### Return Type

One dimensional 0-based array of float values. When you asked for a display with two types of data (Real & Imaginary, Magnitude & Phase), the data returned will be interleaved. E.g. in case of display Real & Imaginary, the real values are stored at even indices and imaginary values are stored at odd indices. The index into the array is based on the measurement point index  1.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## GetDataSection Method

*Quelle: `POLYFILELib~DataBand~GetDataSection.html` · Polytec PolyFile Type Library · DataBand Object : GetDataSection Method*

### Description

GetDataSection extends GetData: it is possible to retrieve only a section of the data by specifying FirstIndex and LastIndex.

### Syntax

*Visual Basic:*
```
Public Function GetDataSection( _
   ByVal pIDisplay As IDisplay2, _
   ByVal lFrame As Long, _
   ByVal lFirstIndex As Long, _
   ByVal lLastIndex As Long _
) As Single()
```

### Parameters

pIDisplay

To obtain a Display object navigate through the BandDomain / Channels / Signals / Displays objects.

lFrame

In MultiFrame mode you can specify the frame number. 0 is the average frame 1, , (number of frames) are the other frames. For user-defined bands you can specify a frame number in the range of 1, ..., (number of frames). The frame number should be 0 in all other cases. See the GetFrames Method on how to obtain the number of frames.

lFirstIndex

Index of first data value to retrieve.

lLastIndex

Index of last data value to retrieve.

### Return Type

One dimensional 0-based array of float values. The data returned in Single(0 : LastIndex  FirstIndex) by GetDataSection is identical to the data returned by GetData in Single(FirstIndex : LastIndex) for not-interleaved data. For interleaved data, the data returned in Single(0 : 2 * (LastIndex  FirstIndex) + 1) is identical to the data returned by GetData in Single(2 * FirstIndex : 2 * LastIndex + 1). Note that in any case both arrays are zero-based.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## GetFrames Method

*Quelle: `POLYFILELib~DataBand~GetFrames.html` · Polytec PolyFile Type Library · DataBand Object : GetFrames Method*

### Description

Retrieves the frame count for the given signal.

### Syntax

*Visual Basic:*
```
Public Function GetFrames( _
   ByVal pISignal As ISignal5 _
) As Long
```

### Parameters

pISignal

Specifies the type of data to receive. To obtain a Signal object navigate through the BandDomain / Channels / Signals.

### Return Type

In MultiFrame mode and for user signals you can get a frame count greater than 1. The frame count for MultiFrame data is without the average frame.


---

## GetScanStatus Method

*Quelle: `POLYFILELib~DataBand~GetScanStatus.html` · Polytec PolyFile Type Library · DataBand Object : GetScanStatus Method*

### Description

Gets an array containing the scan status for the given signal for all scan points of this band.

### Syntax

*Visual Basic:*
```
Public Function GetScanStatus( _
   ByVal pISignal As ISignal5 _
) As Long()
```

### Parameters

pISignal

The signal to get the scan status for.

### Return Type

One dimensional 0-based array of integer values containing the scan status (PTCScanStatus Enumeration) for all scan points of this band. The index into the array is the measurement point index  1.


---

## SetData Method

*Quelle: `POLYFILELib~DataBand~SetData.html` · Polytec PolyFile Type Library · DataBand Object : SetData Method*

### Description

Sets the data for this band for a given user-defined signal.

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

Specifies the type of data to set. To obtain a user-defined band, navigate through the BandDomain / Channels / Signals objects. Channel Caps must be ptcChannelCapsUser.

lFrame

Frame number - starting from 1. You have to specify a frame number starting from 1. Remember, data must be put with the sequential increasing number of Frame. Once data have been set for each frame you can change data for any frame directly with this method.

psaData

One dimensional array of float values. When the band is complex, the length of data array must be double; the real values are stored at even indices and imaginary values are stored at odd indices.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.


---

## SetScanStatus Method

*Quelle: `POLYFILELib~DataBand~SetScanStatus.html` · Polytec PolyFile Type Library · DataBand Object : SetScanStatus Method*

### Description

Sets the scan status for the given signal for all scan points of this band.

### Syntax

*Visual Basic:*
```
Public Sub SetScanStatus( _
   ByVal pISignal As ISignal5, _
   ByVal psaScanStatus() As Long _
)
```

### Parameters

pISignal

The signal to set the scan status for.

psaScanStatus

One dimensional 0-based array of integer values containing the scan status (PTCScanStatus Enumeration) for all scan points of this band. The index into the array is the measurement point index  1.

### Remarks

You can only set the scan status for user-defined data bands. You can use this method to invalidate user-defined data at this scan point by adding the status ptcScanStatusInvalidated to the status you retrieved from the GetScanStatus Method. The MPV/PSV software then will ignore the data of the band of this point and interpolate it by using neighbor scan points, when interpolate invalid points is active in the presentation.


---

## BandDefinition Property

*Quelle: `POLYFILELib~DataBand~BandDefinition.html` · Polytec PolyFile Type Library · DataBand Object : BandDefinition Property*

### Description

Returns the definition of the band.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BandDefinition As IBandDef3
```

### Return Type

The definition of the band.


---

## BandDomain Property

*Quelle: `POLYFILELib~DataBand~BandDomain.html` · Polytec PolyFile Type Library · DataBand Object : BandDomain Property*

### Description

Returns the BandDomain.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BandDomain As BandDomain
```


---

## EntireBandwidth Property

*Quelle: `POLYFILELib~DataBand~EntireBandwidth.html` · Polytec PolyFile Type Library · DataBand Object : EntireBandwidth Property*

### Description

Returns whether the band is the entire bandwidth band.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property EntireBandwidth As Boolean
```

### Return Type

True if the band is the entire bandwidth band.


---

## Index Property

*Quelle: `POLYFILELib~DataBand~Index.html` · Polytec PolyFile Type Library · DataBand Object : Index Property*

### Description

The index of the band in the DataBands collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Index As Long
```

### Return Type

The 1-based index of the band in the DataBands collection.

### Remarks

The returned index can be used as an index into the DataBands collection.


---

## Name Property

*Quelle: `POLYFILELib~DataBand~Name.html` · Polytec PolyFile Type Library · DataBand Object : Name Property*

### Description

Returns the name of the band. Can be used as an index to the DataBands collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

In RMS domain the last band of the data bands collection has the name "Entire Bandwidth. It holds RMS data over the whole frequency range of the measurement.


---

## Peak Property

*Quelle: `POLYFILELib~DataBand~Peak.html` · Polytec PolyFile Type Library · DataBand Object : Peak Property*

### Description

Returns the peak frequency of the band.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Peak As Single
```

### Remarks

Available in FFT domain only.


---

## Start Property

*Quelle: `POLYFILELib~DataBand~Start.html` · Polytec PolyFile Type Library · DataBand Object : Start Property*

### Description

Returns the start frequency of the band.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Start As Single
```

### Remarks

Available in RMS domain only.


---

## Stop Property

*Quelle: `POLYFILELib~DataBand~Stop.html` · Polytec PolyFile Type Library · DataBand Object : Stop Property*

### Description

Returns the stop frequency of the band.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Stop As Single
```

### Remarks

Available in RMS domain only.
