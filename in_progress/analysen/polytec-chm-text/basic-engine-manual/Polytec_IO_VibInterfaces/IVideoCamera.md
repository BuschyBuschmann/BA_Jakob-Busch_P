# Polytec_IO_VibInterfaces – IVideoCamera

## IVideoCamera Interface

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera.html` · Polytec IO VibInterfaces Type Library*

### Description

The video camera of the sensor head.

### Object Model


---

## IVideoCamera Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| GetShutterSpeeds | Gets the available shutter speeds of the camera. |
|---|---|
| HasCap | Returns true, if the camera has the given capability. |

### Public Properties

| Caps | The capabilities of the camera. |
|---|---|
| DefaultSettings | The default settings of the video camera. |
| Format | The video format of the camera. |
| GammaMax | The maximum gamma value of the camera. |
| GammaMin | The minimum gamma value of the camera. |
| ManualGainMax | The maximum manual gain value of the camera. |
| ManualGainMin | The minimum manual gain value of the camera. |
| Name | The name of the video camera. |


---

## GetShutterSpeeds Method

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~GetShutterSpeeds.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : GetShutterSpeeds Method*

### Description

Gets the available shutter speeds of the camera.

### Syntax

*Visual Basic:*
```
Public Function GetShutterSpeeds() As String()
```


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~HasCap.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : HasCap Method*

### Description

Returns true, if the camera has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As VideoCameraCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| VideoCameraCaps_AutomaticGain | The camera has automatic gain control. |
| VideoCameraCaps_Gamma | The camera has different gamma values. |
| VideoCameraCaps_ManualGain | The camera has manual gain control. |
| VideoCameraCaps_Mirror | The camera can flip the video. |
| VideoCameraCaps_None | No capabilities. |
| VideoCameraCaps_ShutterSpeed | The camera has different shutter speeds. |
The capability.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~Caps.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : Caps Property*

### Description

The capabilities of the camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As VideoCameraCaps
```


---

## DefaultSettings Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~DefaultSettings.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : DefaultSettings Property*

### Description

The default settings of the video camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DefaultSettings As VideoCameraSettings
```


---

## Format Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~Format.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : Format Property*

### Description

The video format of the camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Format As VideoCameraFormat
```


---

## GammaMax Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~GammaMax.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : GammaMax Property*

### Description

The maximum gamma value of the camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GammaMax As Long
```


---

## GammaMin Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~GammaMin.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : GammaMin Property*

### Description

The minimum gamma value of the camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GammaMin As Long
```


---

## ManualGainMax Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~ManualGainMax.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : ManualGainMax Property*

### Description

The maximum manual gain value of the camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ManualGainMax As Long
```


---

## ManualGainMin Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~ManualGainMin.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : ManualGainMin Property*

### Description

The minimum manual gain value of the camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ManualGainMin As Long
```

### Example


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~IVideoCamera~Name.html` · Polytec IO VibInterfaces Type Library · IVideoCamera Interface : Name Property*

### Description

The name of the video camera.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```
