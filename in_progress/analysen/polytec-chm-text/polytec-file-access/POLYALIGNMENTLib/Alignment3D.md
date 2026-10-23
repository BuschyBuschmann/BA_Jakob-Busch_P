# POLYALIGNMENTLib – Alignment3D

## Alignment3D Object

*Quelle: `POLYALIGNMENTLib~Alignment3D.html` · Polytec PolyAlignment Type Library*

### Description

Item of the Alignments3D collection.

### Object Model


---

## Alignment3D Object Members

*Quelle: `POLYALIGNMENTLib~Alignment3D_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Calculate | Calculates a new 3D alignment. |
|---|---|
| Coord3DToScanner | Converts the specified scan point coordinates to the scanner coordinates and the distance of the point from the second scanner mirror, i.e. the horizontal scanner mirror. |
| GetBeamLength | Retrieves the laser beam length from the focusing objective to the specified scan point. |
| GetBeamOrigin | Retrieves the coordinates of the point where the laser beam exits the scanning head at the second scanner mirror, i.e. the horizontal scanner mirror, for the given scanner coordinates. |
| GetScanHeadPosition | Retrieves the 3D coordinates of the scanning head at the first scanner mirror, i.e. the vertical scanner mirror. |
| Invalidate | Invalidates the current 3D alignment. |
| ScannerToCoord3D | Converts the specified scanner coordinates and distance from the second scanner mirror, i.e. the horizontal scanner mirror, to the coordinates of a scan point. |
| ScannerToVector3D | Calculates the coordinates of a scan point on the laser beam in 1.0 m distance from the second scanner mirror, i.e. the horizontal scanner mirror. Same as ScannerToCoord3D with dDistance = 1.0 . |

### Public Properties

| Align3DPoints | Returns a copy of the points collection of 3D alignment points. |
|---|---|
| Align3DPointsRef | Returns a read only reference of the points collection of 3D alignment points. |
| AngleUncertainty | Gets the uncertainty (accuracy) of the scanning head orientation of the current alignment in radian. |
| CoordDefinitionMode | The coordinates definition mode for the 3D alignment. |
| CurrentQuality | The current quality of the 3D alignment in meter. |
| Mirror | True if the 3D alignment was done with a mirror. |
| PositionUncertainty | Gets the uncertainty (accuracy) of the scanning head position of the current alignment in meter. |
| ScanHeadType | The scanning head type. |
| ScanQuantity | Returns the physical quantity of the scanner. |
| TargetQuality | The target quality of the 3D alignment in meter. |
| Valid | True if the alignment is valid. |


---

## Calculate Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~Calculate.html` · Polytec PolyAlignment Type Library · Alignment3D Object : Calculate Method*

### Description

Calculates a new 3D alignment.

### Syntax

*Visual Basic:*
```
Public Sub Calculate( _
   ByVal pIAlign3DPoints As Align3DPoints, _
   ByVal ptcMode As PTCCoordDefinitionMode, _
   ByVal vbMirror As Boolean, _
   ByVal dTargetQuality As Double, _
   ByVal pIScanHeadScanner As IScanHeadScanner _
)
```

### Parameters

pIAlign3DPoints

A collection of 3D alignment points.

ptcMode

| Value | Description |
|---|---|
| ptcCoordDefModeFreePoints | Free points (3  20) with geometry scan unit. |
| ptcCoordDefModeOff | Coordinate definition mode without geometry scan unit. |
| ptcCoordDefModeOrigPointOnAxisPointOnPlane | Origin, point on axis and point on plane with geometry scan unit. |
| ptcCoordDefModeThreePointsOnAxes | Three points on axes with geometry scan unit. |
The coordinate definition mode.

vbMirror

If true, a mirror is used for the 3D alignment.

dTargetQuality

The desired target quality.

pIScanHeadScanner

The scanner properties for this alignment.


---

## Coord3DToScanner Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~Coord3DToScanner.html` · Polytec PolyAlignment Type Library · Alignment3D Object : Coord3DToScanner Method*

### Description

Converts the specified scan point coordinates to the scanner coordinates and the distance of the point from the second scanner mirror, i.e. the horizontal scanner mirror.

### Syntax

*Visual Basic:*
```
Public Sub Coord3DToScanner( _
   ByVal dCoordX As Double, _
   ByVal dCoordY As Double, _
   ByVal dCoordZ As Double, _
   ByRef pdScannerX As Double, _
   ByRef pdScannerY As Double, _
   ByRef pdDistance As Double _
)
```

### Parameters

dCoordX

The x-coordinate of the scan point in meter.

dCoordY

The y-coordinate of the scan point in meter.

dCoordZ

The z-coordinate of the scan point in meter.

pdScannerX

The computed horizontal scanner coordinate (in angle or displacement).

pdScannerY

The computed vertical scanner coordinate (in angle or displacement).

pdDistance

The computed distance of the scan point from the horizontal scanner mirror in meter.

### Remarks

For PSV systems the scanner coordinates are returned as angles in degree, and for MSA systems they are returned as displacements in meter.


---

## GetBeamLength Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~GetBeamLength.html` · Polytec PolyAlignment Type Library · Alignment3D Object : GetBeamLength Method*

### Description

Retrieves the laser beam length from the focusing objective to the specified scan point.

### Syntax

*Visual Basic:*
```
Public Function GetBeamLength( _
   ByVal dLensToMirrorDistance As Double, _
   ByVal dCoordX As Double, _
   ByVal dCoordY As Double, _
   ByVal dCoordZ As Double _
) As Double
```

### Parameters

dLensToMirrorDistance

The distance of the objective from the first scanner mirror, i.e. the vertical scanner mirror.

dCoordX

The x-coordinate of the scan point in meter.

dCoordY

The y-coordinate of the scan point in meter.

dCoordZ

The z-coordinate of the scan point in meter.

### Return Type

The laser beam length.

### Remarks

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## GetBeamOrigin Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~GetBeamOrigin.html` · Polytec PolyAlignment Type Library · Alignment3D Object : GetBeamOrigin Method*

### Description

Retrieves the coordinates of the point where the laser beam exits the scanning head at the second scanner mirror, i.e. the horizontal scanner mirror, for the given scanner coordinates.

### Syntax

*Visual Basic:*
```
Public Sub GetBeamOrigin( _
   ByVal dScannerX As Double, _
   ByVal dScannerY As Double, _
   ByRef pdCoordX As Double, _
   ByRef pdCoordY As Double, _
   ByRef pdCoordZ As Double _
)
```

### Parameters

dScannerX

The horizontal scanner coordinate (in angle or displacement).

dScannerY

The vertical scanner coordinate (in angle or displacement).

pdCoordX

The computed x-coordinate of the exit point in meter.

pdCoordY

The computed y-coordinate of the exit point in meter.

pdCoordZ

The computed z-coordinate of the exit point in meter.

### Remarks

For PSV systems the scanner coordinates are expected to be specified as angles in degree, and for MSA systems they are expected as displacements in meter.


---

## GetScanHeadPosition Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~GetScanHeadPosition.html` · Polytec PolyAlignment Type Library · Alignment3D Object : GetScanHeadPosition Method*

### Description

Retrieves the 3D coordinates of the scanning head at the first scanner mirror, i.e. the vertical scanner mirror.

### Syntax

*Visual Basic:*
```
Public Sub GetScanHeadPosition( _
   ByRef pdCoordX As Double, _
   ByRef pdCoordY As Double, _
   ByRef pdCoordZ As Double _
)
```

### Parameters

pdCoordX

The computed x-coordinate of the scanning head position.

pdCoordY

The computed y-coordinate of the scanning head position.

pdCoordZ

The computed z-coordinate of the scanning head position.


---

## Invalidate Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~Invalidate.html` · Polytec PolyAlignment Type Library · Alignment3D Object : Invalidate Method*

### Description

Invalidates the current 3D alignment.

### Syntax

*Visual Basic:*
```
Public Sub Invalidate()
```


---

## ScannerToCoord3D Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~ScannerToCoord3D.html` · Polytec PolyAlignment Type Library · Alignment3D Object : ScannerToCoord3D Method*

### Description

Converts the specified scanner coordinates and distance from the second scanner mirror, i.e. the horizontal scanner mirror, to the coordinates of a scan point.

### Syntax

*Visual Basic:*
```
Public Sub ScannerToCoord3D( _
   ByVal dScannerX As Double, _
   ByVal dScannerY As Double, _
   ByVal dDistance As Double, _
   ByRef pdCoordX As Double, _
   ByRef pdCoordY As Double, _
   ByRef pdCoordZ As Double _
)
```

### Parameters

dScannerX

The horizontal scanner coordinate (in angle or displacement).

dScannerY

The vertical scanner coordinate (in angle or displacement).

dDistance

The distance of the scan point from the horizontal scanner mirror in meter.

pdCoordX

The computed x-coordinate of the scan point in meter.

pdCoordY

The computed y-coordinate of the scan point in meter.

pdCoordZ

The computed z-coordinate of the scan point in meter.

### Remarks

For PSV systems the scanner coordinates are expected to be specified as angles in degree, and for MSA systems they are expected as displacements in meter.


---

## ScannerToVector3D Method

*Quelle: `POLYALIGNMENTLib~Alignment3D~ScannerToVector3D.html` · Polytec PolyAlignment Type Library · Alignment3D Object : ScannerToVector3D Method*

### Description

Calculates the coordinates of a scan point on the laser beam in 1.0 m distance from the second scanner mirror, i.e. the horizontal scanner mirror. Same as ScannerToCoord3D with dDistance = 1.0.

### Syntax

*Visual Basic:*
```
Public Sub ScannerToVector3D( _
   ByVal dScannerX As Double, _
   ByVal dScannerY As Double, _
   ByRef pdVectorX As Double, _
   ByRef pdVectorY As Double, _
   ByRef pdVectorZ As Double _
)
```

### Parameters

dScannerX

The horizontal scanner coordinate (in angle or displacement).

dScannerY

The vertical scanner coordinate (in angle or displacement).

pdVectorX

The computed x-component of the scan point in meter.

pdVectorY

The computed y-component of the scan point in meter.

pdVectorZ

The computed z-component of the scan point in meter.

### Remarks

For PSV systems the scanner coordinates are expected to be specified as angles in degree, and for MSA systems they are expected as displacements in meter.


---

## Align3DPoints Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~Align3DPoints.html` · Polytec PolyAlignment Type Library · Alignment3D Object : Align3DPoints Property*

### Description

Returns a copy of the points collection of 3D alignment points.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Align3DPoints As Align3DPoints
```


---

## Align3DPointsRef Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~Align3DPointsRef.html` · Polytec PolyAlignment Type Library · Alignment3D Object : Align3DPointsRef Property*

### Description

Returns a read only reference of the points collection of 3D alignment points.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Align3DPointsRef As Align3DPoints
```


---

## AngleUncertainty Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~AngleUncertainty.html` · Polytec PolyAlignment Type Library · Alignment3D Object : AngleUncertainty Property*

### Description

Gets the uncertainty (accuracy) of the scanning head orientation of the current alignment in radian.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AngleUncertainty As Double
```

### Return Type

The angle uncertainty (accuracy) in radian.


---

## CoordDefinitionMode Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~CoordDefinitionMode.html` · Polytec PolyAlignment Type Library · Alignment3D Object : CoordDefinitionMode Property*

### Description

The coordinates definition mode for the 3D alignment.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CoordDefinitionMode As PTCCoordDefinitionMode
```


---

## CurrentQuality Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~CurrentQuality.html` · Polytec PolyAlignment Type Library · Alignment3D Object : CurrentQuality Property*

### Description

The current quality of the 3D alignment in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CurrentQuality As Double
```


---

## Mirror Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~Mirror.html` · Polytec PolyAlignment Type Library · Alignment3D Object : Mirror Property*

### Description

True if the 3D alignment was done with a mirror.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Mirror As Boolean
```


---

## PositionUncertainty Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~PositionUncertainty.html` · Polytec PolyAlignment Type Library · Alignment3D Object : PositionUncertainty Property*

### Description

Gets the uncertainty (accuracy) of the scanning head position of the current alignment in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionUncertainty As Double
```

### Return Type

The position uncertainty (accuracy) in meter.


---

## ScanHeadType Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~ScanHeadType.html` · Polytec PolyAlignment Type Library · Alignment3D Object : ScanHeadType Property*

### Description

The scanning head type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadType As PTCScanHeadType
```


---

## ScanQuantity Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~ScanQuantity.html` · Polytec PolyAlignment Type Library · Alignment3D Object : ScanQuantity Property*

### Description

Returns the physical quantity of the scanner.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanQuantity As PTCPhysicalQuantity
```

### Remarks

The possible physical quantities are ptcPhysicalQuantityAngle for the default scanning head and ptcPhysicalQuantityDisplacement for the MSV and MSA scanning heads.


---

## TargetQuality Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~TargetQuality.html` · Polytec PolyAlignment Type Library · Alignment3D Object : TargetQuality Property*

### Description

The target quality of the 3D alignment in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TargetQuality As Double
```


---

## Valid Property

*Quelle: `POLYALIGNMENTLib~Alignment3D~Valid.html` · Polytec PolyAlignment Type Library · Alignment3D Object : Valid Property*

### Description

True if the alignment is valid.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Valid As Boolean
```
