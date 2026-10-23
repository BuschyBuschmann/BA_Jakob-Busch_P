# POLYFILELib – DataPointReader

## DataPointReader Object

*Quelle: `POLYFILELib~DataPointReader.html` · Polytec PolyFile Type Library*

### Description

The data point reader allows to read data in large chunks, e.g. for several displays, scan points or frames at once.

### Object Model

### Remarks

The use of the data point reader is advanced. Use it only when performance for reading data is critical.

### Example


---

## DataPointReader Object Members

*Quelle: `POLYFILELib~DataPointReader_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetDataScanPointCount | Returns the number of scan points and the maximum number of available frames for the data of the specified display. |
|---|---|
| Read | Reads a chunk of data. |
| Read3D | Reads a chunk of data in 3D vector format. If the data source is 1D, the method fills up the missing directions with zeros. |


---

## GetDataScanPointCount Method

*Quelle: `POLYFILELib~DataPointReader~GetDataScanPointCount.html` · Polytec PolyFile Type Library · DataPointReader Object : GetDataScanPointCount Method*

### Description

Returns the number of scan points and the maximum number of available frames for the data of the specified display.

### Syntax

*Visual Basic:*
```
Public Function GetDataScanPointCount( _
   ByVal display As IDisplay2, _
   ByRef maxFrameCount As Long _
) As Long
```

### Parameters

display

The display of the data.

maxFrameCount

The maximum number of frames of the data of the specified display.

### Return Type

The number of scan points with data for the specified display.

### Example


---

## Read Method

*Quelle: `POLYFILELib~DataPointReader~Read.html` · Polytec PolyFile Type Library · DataPointReader Object : Read Method*

### Description

Reads a chunk of data.

### Syntax

*Visual Basic:*
```
Public Function Read( _
   ByRef data() As Single, _
   ByRef readScanPointCount() As Long _
) As DataDescriptor()
```

### Parameters

data

One dimensional 0-based array of float values. When you ask for a display with two types of data (Real & Imaginary, Magnitude & Phase), the data returned will be interleaved. E.g. in case of display Real & Imaginary, the real values are stored at even indices and imaginary values are stored at odd indices.

For 3D signals (SignalDescription.ResponseDOFs.Direction is ptcVector) the data for the x-direction is followed by the data of the y-direction and z-direction.

readScanPointCount

One dimensional 0-based array of integer values containing the number of scan points read for every corresponding display passed to the CreateDataPointReaderAsync Method.

### Return Type

One dimensional 0-based array of data descriptors describing the contents of the returned data array.

### Remarks

The use of the data point reader is advanced. Use it only when performance for reading data is critical.

### Example


---

## Read3D Method

*Quelle: `POLYFILELib~DataPointReader~Read3D.html` · Polytec PolyFile Type Library · DataPointReader Object : Read3D Method*

### Description

Reads a chunk of data in 3D vector format. If the data source is 1D, the method fills up the missing directions with zeros.

### Syntax

*Visual Basic:*
```
Public Function Read3D( _
   ByRef data() As Single, _
   ByRef readScanPointCount() As Long _
) As DataDescriptor()
```

### Parameters

data

One dimensional 0-based array of float values. When you ask for a display with two types of data (Real & Imaginary, Magnitude & Phase), the data returned will be interleaved. E.g. in case of display Real & Imaginary, the real values are stored at even indices and imaginary values are stored at odd indices.

The data for the x-direction is followed by the data of the y-direction and z-direction.

readScanPointCount

One dimensional 0-based array of integer values containing the number of scan points read for every corresponding display passed to the CreateDataPointReaderAsync Method.

### Return Type

One dimensional 0-based array of data descriptors describing the contents of the returned data array.

### Remarks

The use of the data point reader is advanced. Use it only when performance for reading data is critical.
