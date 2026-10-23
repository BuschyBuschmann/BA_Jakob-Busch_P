# POLYFILELib – MeasurementLocation

## MeasurementLocation Object

*Quelle: `POLYFILELib~MeasurementLocation.html` · Polytec PolyFile Type Library*

### Description

Item of the MeasurementsLocations collection. The MeasurementLocation object contains the properties of the measurement location of a measurement point (scan point).


---

## MeasurementLocation Object Members

*Quelle: `POLYFILELib~MeasurementLocation_members.html` · Polytec PolyFile Type Library*

### Public Properties

| ChannelName | The channel name. |
|---|---|
| Direction | The measurement direction or measurement directions, depending on the value of the property Mode , in the coordinate system of the measurement object. |
| MeasPointIndex | The 1-based measurement point index in the MeasPoints collection . |
| Mode | Currently fixed to the value ptcMeasurementLocationModeFixed . |
| Normal | The normal vector or the normal vectors, depending on the value of the property Mode , of the measurement point(s) in the coordinate system of the measurement object. |
| Status | The measurement status of the referenced measurement point. |


---

## ChannelName Property

*Quelle: `POLYFILELib~MeasurementLocation~ChannelName.html` · Polytec PolyFile Type Library · MeasurementLocation Object : ChannelName Property*

### Description

The channel name.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ChannelName As String
```


---

## Direction Property

*Quelle: `POLYFILELib~MeasurementLocation~Direction.html` · Polytec PolyFile Type Library · MeasurementLocation Object : Direction Property*

### Description

The measurement direction or measurement directions, depending on the value of the property Mode, in the coordinate system of the measurement object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Direction As Single()
```

### Return Type

Please see Remarks.

### Remarks

If the measurement data is scalar-valued, then the returned array is empty. Otherwise:

If the property Mode is set to the value ptcMeasurementLocationModeFixed, then the returned array contains the three components of the measurement direction in the associated scan point.

If the property Mode is set to the value ptcMeasurementLocationModeVarying, then the returned array contains 3*N values, where N denotes the number of scan points and the measurement directions in the scan points are stored consecutively in the array. If a scan point is not measured, then the array elements for the corresponding measurement direction are set to the not-a-number special float value.


---

## MeasPointIndex Property

*Quelle: `POLYFILELib~MeasurementLocation~MeasPointIndex.html` · Polytec PolyFile Type Library · MeasurementLocation Object : MeasPointIndex Property*

### Description

The 1-based measurement point index in the MeasPoints collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MeasPointIndex As Long
```


---

## Mode Property

*Quelle: `POLYFILELib~MeasurementLocation~Mode.html` · Polytec PolyFile Type Library · MeasurementLocation Object : Mode Property*

### Description

Currently fixed to the value ptcMeasurementLocationModeFixed.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Mode As PTCMeasurementLocationMode
```


---

## Normal Property

*Quelle: `POLYFILELib~MeasurementLocation~Normal.html` · Polytec PolyFile Type Library · MeasurementLocation Object : Normal Property*

### Description

The normal vector or the normal vectors, depending on the value of the property Mode, of the measurement point(s) in the coordinate system of the measurement object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Normal As Single()
```

### Return Type

Please see Remarks.

### Remarks

If the measurement data is scalar-valued, then the returned array is empty. Otherwise:

If the property Mode is set to the value ptcMeasurementLocationModeFixed, then the returned array contains the three components of the normal vector in the associated scan point.

If the property Mode is set to the value ptcMeasurementLocationModeVarying, then the returned array contains 3*N values, where N denotes the number of scan points and the normal vectors in the scan points are stored consecutively in the array. If there is no information about the normal vector in some scan point, then the corresponding array elements are set to the not-a-number special float value.


---

## Status Property

*Quelle: `POLYFILELib~MeasurementLocation~Status.html` · Polytec PolyFile Type Library · MeasurementLocation Object : Status Property*

### Description

The measurement status of the referenced measurement point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Status As PTCScanStatus
```
