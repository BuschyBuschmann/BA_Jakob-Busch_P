# POLYFILELib – Element

## Element Object

*Quelle: `POLYFILELib~Element.html` · Polytec PolyFile Type Library*

### Description

Item of the Elements collection. One geometrical element of the scan point geometry. An element is a polygon connecting scan measurement points.


---

## Element Object Members

*Quelle: `POLYFILELib~Element_members.html` · Polytec PolyFile Type Library*

### Public Methods

| MeasPointIndicesByStatus | Returns an array of measurement point indices for a given ScanStatus bit pattern. The indices can be used as index to the MeasPoints collection. |
|---|---|
| MeasPointLabelsByStatus | Returns an array of measurement point labels for a given ScanStatus bit pattern. |

### Public Properties

| MeasPointIndices | Returns an array of measurement point indices. The indices can be used as index to the MeasPoints collection. |
|---|---|
| MeasPointLabels | Returns an array of measurement point labels. |


---

## MeasPointIndicesByStatus Method

*Quelle: `POLYFILELib~Element~MeasPointIndicesByStatus.html` · Polytec PolyFile Type Library · Element Object : MeasPointIndicesByStatus Method*

### Description

Returns an array of measurement point indices for a given ScanStatus bit pattern. The indices can be used as index to the MeasPoints collection.

### Syntax

*Visual Basic:*
```
Public Function MeasPointIndicesByStatus( _
   ByVal ptcStatusMask As PTCScanStatus, _
   ByVal ptcStatusCompare As PTCScanStatus, _
   ByVal vbAny As Boolean _
) As Long()
```

### Parameters

ptcStatusMask

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
Bit pattern to mask measurement points.

ptcStatusCompare

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
Bit pattern for comparing the result.

vbAny

True: Return Index if any bit is set. False: Return Index if all bits are set.

### Return Type

One dimensional, 0-based array of integers.


---

## MeasPointLabelsByStatus Method

*Quelle: `POLYFILELib~Element~MeasPointLabelsByStatus.html` · Polytec PolyFile Type Library · Element Object : MeasPointLabelsByStatus Method*

### Description

Returns an array of measurement point labels for a given ScanStatus bit pattern.

### Syntax

*Visual Basic:*
```
Public Function MeasPointLabelsByStatus( _
   ByVal ptcStatusMask As PTCScanStatus, _
   ByVal ptcStatusCompare As PTCScanStatus, _
   ByVal vbAny As Boolean _
) As Long()
```

### Parameters

ptcStatusMask

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
Bit pattern to mask measurement points.

ptcStatusCompare

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
Bit pattern for comparing the result.

vbAny

True: Return Index if any bit is set. False: Return Index if all bits are set.

### Return Type

One dimensional, 0-based array of integers.


---

## MeasPointIndices Property

*Quelle: `POLYFILELib~Element~MeasPointIndices.html` · Polytec PolyFile Type Library · Element Object : MeasPointIndices Property*

### Description

Returns an array of measurement point indices. The indices can be used as index to the MeasPoints collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MeasPointIndices As Long()
```

### Return Type

One dimensional, 0-based array of integers.


---

## MeasPointLabels Property

*Quelle: `POLYFILELib~Element~MeasPointLabels.html` · Polytec PolyFile Type Library · Element Object : MeasPointLabels Property*

### Description

Returns an array of measurement point labels.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MeasPointLabels As Long()
```

### Return Type

One dimensional, 0-based array of integers.
