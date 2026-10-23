# PSV – Settings

## Settings Object

*Quelle: `PSV~Settings.html` · Polytec PSV Type Library*

### Description

The settings object that represents the current application settings (A/D Settings, scan point definition, camera and alignment, and window layout).


---

## Settings Object Members

*Quelle: `PSV~Settings_members.html` · Polytec PSV Type Library*

### Public Methods

| Delete | Deletes a settings file. |
|---|---|
| Load | Load settings from a file. |
| Save | Saves the current settings to a file. |


---

## Delete Method

*Quelle: `PSV~Settings~Delete.html` · Polytec PSV Type Library · Settings Object : Delete Method*

### Description

Deletes a settings file.

### Syntax

*Visual Basic:*
```
Public Sub Delete( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The name of the settings file.


---

## Load Method

*Quelle: `PSV~Settings~Load.html` · Polytec PSV Type Library · Settings Object : Load Method*

### Description

Load settings from a file.

### Syntax

*Visual Basic:*
```
Public Sub Load( _
   ByVal bstrFileName As String, _
   ByVal PTCSettings As PTCSettings _
)
```

### Parameters

bstrFileName

The name of the settings file or a measurement file.

PTCSettings

| Value | Description |
|---|---|
| ptcSettings2DAlignment | 2D alignment settings. |
| ptcSettings3DAlignment | 3D alignment settings. |
| ptcSettingsAcquisition | Acquisition settings. |
| ptcSettingsAlignment | Alignment settings. |
| ptcSettingsAll | All settings. |
| ptcSettingsAPS | Scan point definition settings. |
| ptcSettingsCamera | Camera settings. |
| ptcSettingsCameraAndAlignment | Camera and alignment settings. |
| ptcSettingsNone | No settings. |
| ptcSettingsWindows | Window layout settings. |
The type of settings to load.

### Remarks

By specifying a measurement file you can import the settings from this file.


---

## Save Method

*Quelle: `PSV~Settings~Save.html` · Polytec PSV Type Library · Settings Object : Save Method*

### Description

Saves the current settings to a file.

### Syntax

*Visual Basic:*
```
Public Sub Save( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The name of the settings file.
