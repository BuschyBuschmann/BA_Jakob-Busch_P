# POLYFILELib – PointDomain

## PointDomain Object

*Quelle: `POLYFILELib~PointDomain.html` · Polytec PolyFile Type Library*

### Description

Item of the PointDomains collection. One domain of the point data.

### Object Model

### Example


---

## PointDomain Object Members

*Quelle: `POLYFILELib~PointDomain_members.html` · Polytec PolyFile Type Library*

### Public Methods

| CreateDataPointReaderAsync | Creates a DataPointReader object asynchronously. |
|---|---|
| GetXAxis | Returns an XAxis object that describes the x-axis to display the data of this point domain. |
| GetYAxes | Returns the YAxes collection. |

### Public Properties

| Channels | Returns the Channels collection. |
|---|---|
| DataPoints | Returns the DataPoints collection. |
| Name | Returns the name of the PointDomain. Can be used as an index to the PointDomains collection . |
| RmsCorrectionFactor | Retrieves the RMS correction factor for the given signal. |
| Type | Returns the type of the PointDomain. Can be used as an index to the PointDomains collection . |


---

## CreateDataPointReaderAsync Method

*Quelle: `POLYFILELib~PointDomain~CreateDataPointReaderAsync.html` · Polytec PolyFile Type Library · PointDomain Object : CreateDataPointReaderAsync Method*

### Description

Creates a DataPointReader object asynchronously.

### Syntax

*Visual Basic:*
```
Public Function CreateDataPointReaderAsync( _
   ByVal displays() As Object, _
   ByVal scanStatusFilterForDelivery As PTCScanStatus, _
   ByVal comProgress As IComProgress _
) As IComTask
```

### Parameters

displays

One-dimensional zero-based array of displays the data point reader reads data for.

scanStatusFilterForDelivery

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
A mask for the scan status for the scan points the data point reader reads data for.

comProgress

An optional interface to report progress. You can pass nothing.

### Return Type

A task for creating the data point reader.

### Remarks

### Example


---

## GetXAxis Method

*Quelle: `POLYFILELib~PointDomain~GetXAxis.html` · Polytec PolyFile Type Library · PointDomain Object : GetXAxis Method*

### Description

Returns an XAxis object that describes the x-axis to display the data of this point domain.

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

*Quelle: `POLYFILELib~PointDomain~GetYAxes.html` · Polytec PolyFile Type Library · PointDomain Object : GetYAxes Method*

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

Display to retrieve the y-axis information for.


---

## Channels Property

*Quelle: `POLYFILELib~PointDomain~Channels.html` · Polytec PolyFile Type Library · PointDomain Object : Channels Property*

### Description

Returns the Channels collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Channels As IChannels2
```

### Return Type

Channels collection.


---

## DataPoints Property

*Quelle: `POLYFILELib~PointDomain~DataPoints.html` · Polytec PolyFile Type Library · PointDomain Object : DataPoints Property*

### Description

Returns the DataPoints collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DataPoints As DataPoints
```


---

## Name Property

*Quelle: `POLYFILELib~PointDomain~Name.html` · Polytec PolyFile Type Library · PointDomain Object : Name Property*

### Description

Returns the name of the PointDomain. Can be used as an index to the PointDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## RmsCorrectionFactor Property

*Quelle: `POLYFILELib~PointDomain~RmsCorrectionFactor.html` · Polytec PolyFile Type Library · PointDomain Object : RmsCorrectionFactor Property*

### Description

Retrieves the RMS correction factor for the given signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RmsCorrectionFactor( _
   ByVal pISignal As ISignal5 _
) As Double
```

### Parameters

pISignal

Signal to retrieve the RMS correction factor for.


---

## Type Property

*Quelle: `POLYFILELib~PointDomain~Type.html` · Polytec PolyFile Type Library · PointDomain Object : Type Property*

### Description

Returns the type of the PointDomain. Can be used as an index to the PointDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDomainType
```

### Return Type

PTCDomainType.
