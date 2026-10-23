# POLYFILELib – VideoMappingInfo

## VideoMappingInfo Object

*Quelle: `POLYFILELib~VideoMappingInfo.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. Contains information of mapping the video image to distances on the measurement object for MSA and MSV systems.

### Object Model


---

## VideoMappingInfo Object Members

*Quelle: `POLYFILELib~VideoMappingInfo_members.html` · Polytec PolyFile Type Library*

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

*Quelle: `POLYFILELib~VideoMappingInfo~CoordXYFromVideo.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : CoordXYFromVideo Method*

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

*Quelle: `POLYFILELib~VideoMappingInfo~Save.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : Save Method*

### Description

Saves modifications to this object or one of the objects referenced by this object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## VideoXYFromCoord Method

*Quelle: `POLYFILELib~VideoMappingInfo~VideoXYFromCoord.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : VideoXYFromCoord Method*

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

*Quelle: `POLYFILELib~VideoMappingInfo~ActiveCalibration.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : ActiveCalibration Property*

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

*Quelle: `POLYFILELib~VideoMappingInfo~Calibrations.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : Calibrations Property*

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

*Quelle: `POLYFILELib~VideoMappingInfo~CameraSize.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : CameraSize Property*

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

*Quelle: `POLYFILELib~VideoMappingInfo~Name.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : Name Property*

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

*Quelle: `POLYFILELib~VideoMappingInfo~Type.html` · Polytec PolyFile Type Library · VideoMappingInfo Object : Type Property*

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
