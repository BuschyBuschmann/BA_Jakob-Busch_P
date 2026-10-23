# POLYFILELib – DataPoints

## DataPoints Collection

*Quelle: `POLYFILELib~DataPoints.html` · Polytec PolyFile Type Library*

### Description

Standard collection of the DataPoint objects.

### Object Model


---

## DataPoints Collection Members

*Quelle: `POLYFILELib~DataPoints_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetScanStatus | Gets the scan status for the given signal for all measurement points. |
|---|---|
| SetScanStatus | Sets the scan status for the given signal for all measurement points. |

### Public Properties

| Count | Returns the number of DataPoint objects in the DataPoints collection. |
|---|---|
| Item | Returns an item of the DataPoints collection. |


---

## GetScanStatus Method

*Quelle: `POLYFILELib~DataPoints~GetScanStatus.html` · Polytec PolyFile Type Library · DataPoints Collection : GetScanStatus Method*

### Description

Gets the scan status for the given signal for all measurement points.

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

One dimensional 0-based array of integer values containing the scan status (PTCScanStatus Enumeration) for all scan points. The index into the array is the measurement point index  1.

### Example

If you want to get the scan status of a single measurement point it is easier to use the GetScanStatus Method.


---

## SetScanStatus Method

*Quelle: `POLYFILELib~DataPoints~SetScanStatus.html` · Polytec PolyFile Type Library · DataPoints Collection : SetScanStatus Method*

### Description

Sets the scan status for the given signal for all measurement points.

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

The signal to get the scan status for.

psaScanStatus

One dimensional 0-based array of integer values containing the scan status (PTCScanStatus Enumeration) for all scan points. The index into the array is the measurement point index  1.

### Remarks

You can only set the scan status for user-defined datasets. You can use this method to invalidate user-defined data at this scan point by adding the status ptcScanStatusInvalidated to the status you retrieved from GetScanStatus Method. The MPV/PSV software then will ignore the data of the signal of this point and interpolate it by using neighbor scan points, when interpolate invalid points is active in the presentation.

If you want to change the scan status of a single measurement point, it is easier to use the SetScanStatus Method.


---

## Count Property

*Quelle: `POLYFILELib~DataPoints~Count.html` · Polytec PolyFile Type Library · DataPoints Collection : Count Property*

### Description

Returns the number of DataPoint objects in the DataPoints collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYFILELib~DataPoints~Item.html` · Polytec PolyFile Type Library · DataPoints Collection : Item Property*

### Description

Returns an item of the DataPoints collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As DataPoint
```

### Parameters

Index

Index of the data point.
