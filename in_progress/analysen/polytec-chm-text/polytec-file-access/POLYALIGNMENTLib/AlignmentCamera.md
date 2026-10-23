# POLYALIGNMENTLib – AlignmentCamera

## AlignmentCamera Object

*Quelle: `POLYALIGNMENTLib~AlignmentCamera.html` · Polytec PolyAlignment Type Library*

### Description

Item of the AlignmentsCamera collection.

### Object Model


---

## AlignmentCamera Object Members

*Quelle: `POLYALIGNMENTLib~AlignmentCamera_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Calculate | Calculates the camera position, orientation, and view angle, given initial parameter data and a collection of 3D alignment points. |
|---|---|
| ChooseCameraPosition | Chooses a camera position to view the specified 3D points. |
| Coord3DToVideo | Converts the specified 3D object coordinates to video coordinates. |
| ResetCamera | Resets the camera alignement. |
| ScannerToVideo | Converts the specified scanner coordinates to video coordinates, given a point on the video plane. |
| SetCamera | Sets the camera parameters. |
| SetPersistentCamera | Sets the camera parameters for a persistent camera alignment. |
| VideoToCoord3D | Converts the specified video coordinates to 3D object coordinates, given a point on the video plane. |
| VideoToScanner | Converts the specified video coordinates to scanner coordinates, given a point on the video plane. |
| VideoToVector3D | Converts the specified video coordinate to a direction vector in the object coordinate system. |

### Public Properties

| Align3DPoints | Returns the collection of the 3D alignment points. |
|---|---|
| AspectRatio | Returns the aspect ratio of the video width and the video height. |
| CamPosX | Returns the x-coordinate of the camera position. |
| CamPosY | Returns the y-coordinate of the camera position. |
| CamPosZ | Returns the z-coordinate of the camera position. |
| CamVecX | Returns the x-coordinate of the camera view direction. |
| CamVecY | Returns the y-coordinate of the camera view direction. |
| CamVecZ | Returns the z-coordinate of the camera view direction. |
| CurrentQuality | Returns the current quality of the alignment. |
| Mirror | Returns the flag value indicating whether the object is viewed through a mirror. |
| Persistent | Returns the flag value indicating whether the camera alignment is persistent. |
| TargetQuality | Returns the desired target quality of the alignment. |
| Valid | Returns the flag value indicating whether the current alignment is valid. |
| ViewAngle | Returns the camera aperture angle in degree. |
| ViewUpX | Returns the x-coordinate of the camera view-up direction. |
| ViewUpY | Returns the y-coordinate of the camera view-up direction. |
| ViewUpZ | Returns the z-coordinate of the camera view-up direction. |


---

## Calculate Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~Calculate.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : Calculate Method*

### Description

Calculates the camera position, orientation, and view angle, given initial parameter data and a collection of 3D alignment points.

### Syntax

*Visual Basic:*
```
Public Sub Calculate( _
   ByVal pIAlign3DPoints As Align3DPoints, _
   ByVal dTargetQuality As Double, _
   ByVal dCamPosX As Double, _
   ByVal dCamPosY As Double, _
   ByVal dCamPosZ As Double, _
   ByVal dCamVecX As Double, _
   ByVal dCamVecY As Double, _
   ByVal dCamVecZ As Double, _
   ByVal dViewUpX As Double, _
   ByVal dViewUpY As Double, _
   ByVal dViewUpZ As Double, _
   ByVal dViewAngle As Double, _
   ByVal dAspectRatio As Double, _
   ByVal vbMirror As Boolean _
)
```

### Parameters

pIAlign3DPoints

The collection of points with known 3D and video coordinates ("alignment points").

dTargetQuality

The desired target quality of the alignment. This parameter is currently unused.

dCamPosX

The x-coordinate of the camera position.

dCamPosY

The y-coordinate of the camera position.

dCamPosZ

The z-coordinate of the camera position.

dCamVecX

The x-coordinate of the camera view direction.

dCamVecY

The y-coordinate of the camera view direction.

dCamVecZ

The z-coordinate of the camera view direction.

dViewUpX

The x-coordinate of the camera view-up direction.

dViewUpY

The y-coordinate of the camera view-up direction.

dViewUpZ

The z-coordinate of the camera view-up direction.

dViewAngle

The camera aperture angle in degree.

dAspectRatio

The aspect ratio of the video width and the video height.

vbMirror

The flag which indicates whether the object is viewed through a mirror.


---

## ChooseCameraPosition Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~ChooseCameraPosition.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : ChooseCameraPosition Method*

### Description

Chooses a camera position to view the specified 3D points.

### Syntax

*Visual Basic:*
```
Public Sub ChooseCameraPosition( _
   ByVal pointsParam() As Single, _
   ByVal dViewAngle As Double, _
   ByVal dAspectRatio As Double, _
   ByVal vbMirror As Boolean _
)
```

### Parameters

pointsParam

The array containing the coordinates of the points, where the points are stored consecutively.

dViewAngle

The camera aperture angle in degree.

dAspectRatio

The aspect ratio of the video width and the video height.

vbMirror

The flag which indicates whether the object is viewed through a mirror.


---

## Coord3DToVideo Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~Coord3DToVideo.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : Coord3DToVideo Method*

### Description

Converts the specified 3D object coordinates to video coordinates.

### Syntax

*Visual Basic:*
```
Public Sub Coord3DToVideo( _
   ByVal dCoordX As Double, _
   ByVal dCoordY As Double, _
   ByVal dCoordZ As Double, _
   ByRef dVideoX As Double, _
   ByRef dVideoY As Double _
)
```

### Parameters

dCoordX

The object x-coordinate.

dCoordY

The object y-coordinate.

dCoordZ

The object z-coordinate.

dVideoX

The computed video x-coordinate.

dVideoY

The computed video y-coordinate.


---

## ResetCamera Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~ResetCamera.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : ResetCamera Method*

### Description

Resets the camera alignement.

### Syntax

*Visual Basic:*
```
Public Sub ResetCamera()
```

### Remarks

Invalidates a valid camera alignment and clears the flag for a persistent camera alignment.


---

## ScannerToVideo Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~ScannerToVideo.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : ScannerToVideo Method*

### Description

Converts the specified scanner coordinates to video coordinates, given a point on the video plane.

### Syntax

*Visual Basic:*
```
Public Sub ScannerToVideo( _
   ByVal dScannerX As Double, _
   ByVal dScannerY As Double, _
   ByVal dFPX As Double, _
   ByVal dFPY As Double, _
   ByVal dFPZ As Double, _
   ByVal pAlign As IAlignment3D, _
   ByRef dVideoX As Double, _
   ByRef dVideoY As Double _
)
```

### Parameters

dScannerX

The horizontal scanner coordinate.

dScannerY

The vertical scanner coordinate.

dFPX

The x-coordinate of the point on the video plane.

dFPY

The y-coordinate of the point on the video plane.

dFPZ

The z-coordinate of the point on the video plane.

pAlign

A valid 3D alignment.

dVideoX

The computed video x-coordinate.

dVideoY

The computed video y-coordinate.

### Remarks

The scanner coordinates are expected to be specified as angles in degree.


---

## SetCamera Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~SetCamera.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : SetCamera Method*

### Description

Sets the camera parameters.

### Syntax

*Visual Basic:*
```
Public Sub SetCamera( _
   ByVal dCamPosX As Double, _
   ByVal dCamPosY As Double, _
   ByVal dCamPosZ As Double, _
   ByVal dCamVecX As Double, _
   ByVal dCamVecY As Double, _
   ByVal dCamVecZ As Double, _
   ByVal dViewUpX As Double, _
   ByVal dViewUpY As Double, _
   ByVal dViewUpZ As Double, _
   ByVal dViewAngle As Double, _
   ByVal dAspectRatio As Double, _
   ByVal vbMirror As Boolean _
)
```

### Parameters

dCamPosX

The x-coordinate of the camera position.

dCamPosY

The y-coordinate of the camera position.

dCamPosZ

The z-coordinate of the camera position.

dCamVecX

The x-coordinate of the camera view direction.

dCamVecY

The y-coordinate of the camera view direction.

dCamVecZ

The z-coordinate of the camera view direction.

dViewUpX

The x-coordinate of the camera view-up direction.

dViewUpY

The y-coordinate of the camera view-up direction.

dViewUpZ

The z-coordinate of the camera view-up direction.

dViewAngle

The camera aperture angle in degree.

dAspectRatio

The aspect ratio of the video width and the video height.

vbMirror

The flag which indicates whether the object is viewed through a mirror.

### Remarks

After calling this method the alignment is valid. The properties CurrentQuality and TargetQuality are set to zero, and the Align3DPoints collection is empty, i.e. no alignment points are available.


---

## SetPersistentCamera Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~SetPersistentCamera.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : SetPersistentCamera Method*

### Description

Sets the camera parameters for a persistent camera alignment.

### Syntax

*Visual Basic:*
```
Public Sub SetPersistentCamera( _
   ByVal dCamPosX As Double, _
   ByVal dCamPosY As Double, _
   ByVal dCamPosZ As Double, _
   ByVal dCamVecX As Double, _
   ByVal dCamVecY As Double, _
   ByVal dCamVecZ As Double, _
   ByVal dViewUpX As Double, _
   ByVal dViewUpY As Double, _
   ByVal dViewUpZ As Double, _
   ByVal dViewAngle As Double, _
   ByVal dAspectRatio As Double, _
   ByVal vbMirror As Boolean _
)
```

### Parameters

dCamPosX

The x-coordinate of the camera position.

dCamPosY

The y-coordinate of the camera position.

dCamPosZ

The z-coordinate of the camera position.

dCamVecX

The x-coordinate of the camera view direction.

dCamVecY

The y-coordinate of the camera view direction.

dCamVecZ

The z-coordinate of the camera view direction.

dViewUpX

The x-coordinate of the camera view-up direction.

dViewUpY

The y-coordinate of the camera view-up direction.

dViewUpZ

The z-coordinate of the camera view-up direction.

dViewAngle

The camera aperture angle in degree.

dAspectRatio

The aspect ratio of the video width and the video height.

vbMirror

The flag which indicates whether the object is viewed through a mirror.

### Remarks

A persistent camera alignment will be stored in scan files or settings files and is used for the positioning of lasers e.g. in the object alignment mode.


---

## VideoToCoord3D Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~VideoToCoord3D.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : VideoToCoord3D Method*

### Description

Converts the specified video coordinates to 3D object coordinates, given a point on the video plane.

### Syntax

*Visual Basic:*
```
Public Sub VideoToCoord3D( _
   ByVal dFPX As Double, _
   ByVal dFPY As Double, _
   ByVal dFPZ As Double, _
   ByVal dVideoX As Double, _
   ByVal dVideoY As Double, _
   ByRef dCoordX As Double, _
   ByRef dCoordY As Double, _
   ByRef dCoordZ As Double _
)
```

### Parameters

dFPX

The x-coordinate of the point on the video plane.

dFPY

The y-coordinate of the point on the video plane.

dFPZ

The z-coordinate of the point on the video plane.

dVideoX

The video x-coordinate.

dVideoY

The video y-coordinate.

dCoordX

The computed object x-coordinate.

dCoordY

The computed object y-coordinate.

dCoordZ

The computed object z-coordinate.


---

## VideoToScanner Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~VideoToScanner.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : VideoToScanner Method*

### Description

Converts the specified video coordinates to scanner coordinates, given a point on the video plane.

### Syntax

*Visual Basic:*
```
Public Sub VideoToScanner( _
   ByVal dVideoX As Double, _
   ByVal dVideoY As Double, _
   ByVal dFPX As Double, _
   ByVal dFPY As Double, _
   ByVal dFPZ As Double, _
   ByVal pAlign As IAlignment3D, _
   ByRef dScanX As Double, _
   ByRef dScanY As Double _
)
```

### Parameters

dVideoX

The video x-coordinate.

dVideoY

The video y-coordinate.

dFPX

The x-coordinate of the point on the video plane.

dFPY

The y-coordinate of the point on the video plane.

dFPZ

The z-coordinate of the point on the video plane.

pAlign

A valid 3D alignment.

dScanX

The computed horizontal coordinate of the scanner.

dScanY

The computed vertical coordinate of the scanner.

### Remarks

The scanner coordinates are returned as angles in degree.


---

## VideoToVector3D Method

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~VideoToVector3D.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : VideoToVector3D Method*

### Description

Converts the specified video coordinate to a direction vector in the object coordinate system.

### Syntax

*Visual Basic:*
```
Public Sub VideoToVector3D( _
   ByVal VideoX As Double, _
   ByVal VideoY As Double, _
   ByRef coordX As Double, _
   ByRef coordY As Double, _
   ByRef coordZ As Double _
)
```

### Parameters

VideoX

The video x-coordinate.

VideoY

The video y-coordinate.

coordX

The object x-coordinate of the direction vector.

coordY

The object y-coordinate of the direction vector.

coordZ

The object z-coordinate of the direction vector.


---

## Align3DPoints Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~Align3DPoints.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : Align3DPoints Property*

### Description

Returns the collection of the 3D alignment points.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Align3DPoints As Align3DPoints
```


---

## AspectRatio Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~AspectRatio.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : AspectRatio Property*

### Description

Returns the aspect ratio of the video width and the video height.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AspectRatio As Double
```


---

## CamPosX Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~CamPosX.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : CamPosX Property*

### Description

Returns the x-coordinate of the camera position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CamPosX As Double
```


---

## CamPosY Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~CamPosY.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : CamPosY Property*

### Description

Returns the y-coordinate of the camera position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CamPosY As Double
```


---

## CamPosZ Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~CamPosZ.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : CamPosZ Property*

### Description

Returns the z-coordinate of the camera position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CamPosZ As Double
```


---

## CamVecX Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~CamVecX.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : CamVecX Property*

### Description

Returns the x-coordinate of the camera view direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CamVecX As Double
```


---

## CamVecY Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~CamVecY.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : CamVecY Property*

### Description

Returns the y-coordinate of the camera view direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CamVecY As Double
```


---

## CamVecZ Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~CamVecZ.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : CamVecZ Property*

### Description

Returns the z-coordinate of the camera view direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CamVecZ As Double
```


---

## CurrentQuality Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~CurrentQuality.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : CurrentQuality Property*

### Description

Returns the current quality of the alignment.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CurrentQuality As Double
```


---

## Mirror Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~Mirror.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : Mirror Property*

### Description

Returns the flag value indicating whether the object is viewed through a mirror.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Mirror As Boolean
```


---

## Persistent Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~Persistent.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : Persistent Property*

### Description

Returns the flag value indicating whether the camera alignment is persistent.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Persistent As Boolean
```

### Remarks

A persistent camera alignment will be stored in scan files or settings files and is used for the positioning of lasers e.g. in the object alignment mode.


---

## TargetQuality Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~TargetQuality.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : TargetQuality Property*

### Description

Returns the desired target quality of the alignment.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TargetQuality As Double
```


---

## Valid Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~Valid.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : Valid Property*

### Description

Returns the flag value indicating whether the current alignment is valid.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Valid As Boolean
```


---

## ViewAngle Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~ViewAngle.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : ViewAngle Property*

### Description

Returns the camera aperture angle in degree.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ViewAngle As Double
```


---

## ViewUpX Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~ViewUpX.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : ViewUpX Property*

### Description

Returns the x-coordinate of the camera view-up direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ViewUpX As Double
```


---

## ViewUpY Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~ViewUpY.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : ViewUpY Property*

### Description

Returns the y-coordinate of the camera view-up direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ViewUpY As Double
```


---

## ViewUpZ Property

*Quelle: `POLYALIGNMENTLib~AlignmentCamera~ViewUpZ.html` · Polytec PolyAlignment Type Library · AlignmentCamera Object : ViewUpZ Property*

### Description

Returns the z-coordinate of the camera view-up direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ViewUpZ As Double
```
