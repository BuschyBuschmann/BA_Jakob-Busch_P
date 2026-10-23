# POLYPROPERTIESLib – IUISettings

## IUISettings Interface

*Quelle: `POLYPROPERTIESLib~IUISettings.html` · Polytec PolyProperties Type Library*

### Description

Base interface for user interface settings. Several other classes are derived from this interface: WindowSettings, AnalyzerViewSettings, SigProAnalyzerViewSettings, AreaViewSettings, DisplaySettings, LineSettingsCollection, LineSettings, RangeSettingsCollection, RangeSettings, UICameraSettings, DataCursorSettings, CoUIClippingPlaneSettings, SpectrogramAnalyzerViewSettings, SpectrogramAreaViewSettings.

### Object Model

### Remarks

This object can either be attached to a parent object or not. If it is attached, the Parent property returns the attached parent. In this case, changes to the object are directly applied to the user interface. You can create settings objects that are not attached to a parent by calling Clone() on a settings object or by creating a new settings object. Assigning such an object to a suitable Settings property of a parent object applies all properties to the user interface at the time of the assignment. Assignment of a settings object copies all properties to the settings object attached to its parent. The detached settings object will be still detached after the assignment.

You can quickly copy settings e.g. between different windows by directly assigning the settings object of one window to the settings property of the other.


---

## IUISettings Interface Members

*Quelle: `POLYPROPERTIESLib~IUISettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Modified | Returns whether the settings object has been modified. |
|---|---|
| Parent | The parent of the settings object, if the object is attached, or nothing. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~IUISettings~Clone.html` · Polytec PolyProperties Type Library · IUISettings Interface : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~IUISettings~Copy.html` · Polytec PolyProperties Type Library · IUISettings Interface : Copy Method*

### Description

Copies the properties of the given settings object to this settings object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal UISettings As IUISettings _
)
```

### Parameters

UISettings

The other settings object.


---

## Equal Method

*Quelle: `POLYPROPERTIESLib~IUISettings~Equal.html` · Polytec PolyProperties Type Library · IUISettings Interface : Equal Method*

### Description

Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values.

### Syntax

*Visual Basic:*
```
Public Function Equal( _
   ByVal UISettings As IUISettings _
) As Boolean
```

### Parameters

UISettings

The other settings object.

### Return Type

True if all properties are equal.


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~IUISettings~Modified.html` · Polytec PolyProperties Type Library · IUISettings Interface : Modified Property*

### Description

Returns whether the settings object has been modified.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Modified As Boolean
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~IUISettings~Parent.html` · Polytec PolyProperties Type Library · IUISettings Interface : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```
