# POLYFILELib – IDataBand

## IDataBand Interface

*Quelle: `POLYFILELib~IDataBand.html` · Polytec PolyFile Type Library*

### Description

Item of the DataBands collection.

### Object Model

### Remarks

It is recommended to cast to the DataBand object.


---

## IDataBand Interface Members

*Quelle: `POLYFILELib~IDataBand_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetData | Retrieves the data of this band for a given Display . |
|---|---|

### Public Properties

| BandDomain | Returns the BandDomain. |
|---|---|
| Name | Returns the name of the band. Can be used as an index to the DataBands collection . |
| Peak | Returns the peak frequency of the band. |
| Start | Returns the start frequency of the band. |
| Stop | Returns the stop frequency of the band. |


---

## GetData Method

*Quelle: `POLYFILELib~IDataBand~GetData.html` · Polytec PolyFile Type Library · IDataBand Interface : GetData Method*

### Description

Retrieves the data of this band for a given Display.

### Syntax

*Visual Basic:*
```
Public Function GetData( _
   ByVal pIDisplay As IDisplay, _
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

## BandDomain Property

*Quelle: `POLYFILELib~IDataBand~BandDomain.html` · Polytec PolyFile Type Library · IDataBand Interface : BandDomain Property*

### Description

Returns the BandDomain.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BandDomain As IBandDomain
```


---

## Name Property

*Quelle: `POLYFILELib~IDataBand~Name.html` · Polytec PolyFile Type Library · IDataBand Interface : Name Property*

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

*Quelle: `POLYFILELib~IDataBand~Peak.html` · Polytec PolyFile Type Library · IDataBand Interface : Peak Property*

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

*Quelle: `POLYFILELib~IDataBand~Start.html` · Polytec PolyFile Type Library · IDataBand Interface : Start Property*

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

*Quelle: `POLYFILELib~IDataBand~Stop.html` · Polytec PolyFile Type Library · IDataBand Interface : Stop Property*

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
