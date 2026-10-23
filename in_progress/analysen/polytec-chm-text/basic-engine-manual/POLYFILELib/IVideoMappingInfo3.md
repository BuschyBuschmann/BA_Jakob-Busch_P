# POLYFILELib – IVideoMappingInfo3

## IVideoMappingInfo3 Interface

*Quelle: `POLYFILELib~IVideoMappingInfo3.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos Collection. Contains information of mapping the video image to distances on the measurement object for MSA and MSV systems.

### Object Model

### Remarks

It is recommended to cast to the VideoMappingInfo Object.


---

## IVideoMappingInfo3 Interface Members

*Quelle: `POLYFILELib~IVideoMappingInfo3_members.html` · Polytec PolyFile Type Library*

### Public Methods

| CoordXYFromVideo | Retrieves the world coordinates in meter of the point specified by the given video coordinates. |
|---|---|
| Save | Saves modifications to this object or one of the objects referenced by this object to the file. |
| VideoXYFromCoord | Retrieves the video coordinates of the point specified by the given world coordinates in meter. |

### Public Properties

| ActiveCalibration | Returns or specifies the name of the active objective calibration. |
|---|---|
| Calibrations | Returns the collection of LensCalibration objects. |
| CameraSize | Returns the CameraSize object. |
| Name | Returns "VideoMapping. Can be used as index to the Infos collection . |
| Type | Returns ptcInfoVideoMapping. Can be used as index to the Infos collection . |


---

## CoordXYFromVideo Method

*Quelle: `POLYFILELib~IVideoMappingInfo3~CoordXYFromVideo.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : CoordXYFromVideo Method*

### Description

Retrieves the world coordinates in meter of the point specified by the given video coordinates.

### Syntax

*Visual Basic:*
```
Public Sub CoordXYFromVideo( _
   ByVal video_X As Single, _
   ByVal video_Y As Single, _
   ByRef coordX As Double, _
   ByRef coordY As Double _
)
```

### Parameters

video_X

The x-coordinate in the video coordinate system.

video_Y

The y-coordinate in the video coordinate system.

coordX

The queried x-coordinate in the world coordinate system.

coordY

The queried y-coordinate in the world coordinate system.


---

## Save Method

*Quelle: `POLYFILELib~IVideoMappingInfo3~Save.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : Save Method*

### Description

Saves modifications to this object or one of the objects referenced by this object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## VideoXYFromCoord Method

*Quelle: `POLYFILELib~IVideoMappingInfo3~VideoXYFromCoord.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : VideoXYFromCoord Method*

### Description

Retrieves the video coordinates of the point specified by the given world coordinates in meter.

### Syntax

*Visual Basic:*
```
Public Sub VideoXYFromCoord( _
   ByVal coordX As Double, _
   ByVal coordY As Double, _
   ByRef video_X As Single, _
   ByRef video_Y As Single _
)
```

### Parameters

coordX

The x-coordinate in the world coordinate system.

coordY

The y-coordinate in the world coordinate system.

video_X

The queried x-coordinate in the video coordinate system.

video_Y

The queried y-coordinate in the video coordinate system.


---

## ActiveCalibration Property

*Quelle: `POLYFILELib~IVideoMappingInfo3~ActiveCalibration.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : ActiveCalibration Property*

### Description

Returns or specifies the name of the active objective calibration.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ActiveCalibration As String
```

### Remarks

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## Calibrations Property

*Quelle: `POLYFILELib~IVideoMappingInfo3~Calibrations.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : Calibrations Property*

### Description

Returns the collection of LensCalibration objects.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Calibrations As ILensCalibrations
```


---

## CameraSize Property

*Quelle: `POLYFILELib~IVideoMappingInfo3~CameraSize.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : CameraSize Property*

### Description

Returns the CameraSize object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CameraSize As CameraSize
```


---

## Name Property

*Quelle: `POLYFILELib~IVideoMappingInfo3~Name.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : Name Property*

### Description

Returns "VideoMapping. Can be used as index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "VideoMapping".


---

## Type Property

*Quelle: `POLYFILELib~IVideoMappingInfo3~Type.html` · Polytec PolyFile Type Library · IVideoMappingInfo3 Interface : Type Property*

### Description

Returns ptcInfoVideoMapping. Can be used as index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoVideoMapping.
