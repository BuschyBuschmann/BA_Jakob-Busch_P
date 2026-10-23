# POLYPROPERTIESLib – PeakCursorSettings

## PeakCursorSettings Object

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of the peak (band) cursor.

### Object Model

### Example


---

## PeakCursorSettings Object Members

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| CursorType | The type of the data cursor. |
|---|---|
| LeftPosition | The position of the left line of the peak cursor. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| RightPosition | The position of the right line of the peak cursor. |
| ShowDamping | Specifies whether the damping value is shown. |
| ShowFittedCurve | Specifies whether the curve fitted to the data is shown. |
| ShowFMax | Specifies whether the frequency of the maximum of the fitted curve is shown. |
| ShowHorizontalLine | Specifies whether a horizontal line is shown at the intersection of the cursor lines with the data. |
| ShowLeftXValue | Specifies whether the x value at the left cursor line is shown. |
| ShowLeftYValue | Specifies whether the y value at the left cursor line is shown. |
| ShowLineAtMax | Specifies whether a horizontal line is shown at the maximum of the data between the cursor lines. |
| ShowLineAtMin | Specifies whether a horizontal line is shown at the minimum of the data between the cursor lines. |
| ShowMaxXValue | Specifies whether the x value of the maximum of the data between the cursor lines is shown. |
| ShowMaxYValue | Specifies whether the y value of the maximum of the data between the cursor lines is shown. |
| ShowMeanValue | Specifies whether the mean value of the data between the cursor lines is shown. |
| ShowMinXValue | Specifies whether the x value of the minimum of the data between the cursor lines is shown. |
| ShowMinYValue | Specifies whether the y value of the minimum of the data between the cursor lines is shown. |
| ShowQFactor | Specifies whether the Q factor value is shown. |
| ShowRightXValue | Specifies whether the x value at the right cursor line is shown. |
| ShowRightYValue | Specifies whether the y value at the right cursor line is shown. |
| ShowRMSValue | Specifies whether the RMS of the data between the cursor lines is shown. |
| ShowStandardDeviation | Specifies whether the standard deviation of the data between the cursor lines is shown. |
| ShowZeta | Specifies whether the Zeta value is shown. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~Clone.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~Copy.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~Equal.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : Equal Method*

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

## CursorType Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~CursorType.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : CursorType Property*

### Description

The type of the data cursor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```

### Return Type

Always ptcCursorTypePeak.


---

## LeftPosition Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~LeftPosition.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : LeftPosition Property*

### Description

The position of the left line of the peak cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LeftPosition As Double
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~Modified.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~Parent.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```


---

## RightPosition Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~RightPosition.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : RightPosition Property*

### Description

The position of the right line of the peak cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RightPosition As Double
```


---

## ShowDamping Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowDamping.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowDamping Property*

### Description

Specifies whether the damping value is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowDamping As Boolean
```


---

## ShowFittedCurve Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowFittedCurve.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowFittedCurve Property*

### Description

Specifies whether the curve fitted to the data is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowFittedCurve As Boolean
```


---

## ShowFMax Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowFMax.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowFMax Property*

### Description

Specifies whether the frequency of the maximum of the fitted curve is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowFMax As Boolean
```


---

## ShowHorizontalLine Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowHorizontalLine.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowHorizontalLine Property*

### Description

Specifies whether a horizontal line is shown at the intersection of the cursor lines with the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowHorizontalLine As Boolean
```


---

## ShowLeftXValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowLeftXValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowLeftXValue Property*

### Description

Specifies whether the x value at the left cursor line is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowLeftXValue As Boolean
```


---

## ShowLeftYValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowLeftYValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowLeftYValue Property*

### Description

Specifies whether the y value at the left cursor line is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowLeftYValue As Boolean
```


---

## ShowLineAtMax Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowLineAtMax.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowLineAtMax Property*

### Description

Specifies whether a horizontal line is shown at the maximum of the data between the cursor lines.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowLineAtMax As Boolean
```


---

## ShowLineAtMin Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowLineAtMin.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowLineAtMin Property*

### Description

Specifies whether a horizontal line is shown at the minimum of the data between the cursor lines.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowLineAtMin As Boolean
```


---

## ShowMaxXValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowMaxXValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowMaxXValue Property*

### Description

Specifies whether the x value of the maximum of the data between the cursor lines is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowMaxXValue As Boolean
```


---

## ShowMaxYValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowMaxYValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowMaxYValue Property*

### Description

Specifies whether the y value of the maximum of the data between the cursor lines is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowMaxYValue As Boolean
```


---

## ShowMeanValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowMeanValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowMeanValue Property*

### Description

Specifies whether the mean value of the data between the cursor lines is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowMeanValue As Boolean
```


---

## ShowMinXValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowMinXValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowMinXValue Property*

### Description

Specifies whether the x value of the minimum of the data between the cursor lines is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowMinXValue As Boolean
```


---

## ShowMinYValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowMinYValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowMinYValue Property*

### Description

Specifies whether the y value of the minimum of the data between the cursor lines is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowMinYValue As Boolean
```


---

## ShowQFactor Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowQFactor.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowQFactor Property*

### Description

Specifies whether the Q factor value is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowQFactor As Boolean
```

### Example


---

## ShowRightXValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowRightXValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowRightXValue Property*

### Description

Specifies whether the x value at the right cursor line is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowRightXValue As Boolean
```


---

## ShowRightYValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowRightYValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowRightYValue Property*

### Description

Specifies whether the y value at the right cursor line is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowRightYValue As Boolean
```


---

## ShowRMSValue Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowRMSValue.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowRMSValue Property*

### Description

Specifies whether the RMS of the data between the cursor lines is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowRMSValue As Boolean
```


---

## ShowStandardDeviation Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowStandardDeviation.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowStandardDeviation Property*

### Description

Specifies whether the standard deviation of the data between the cursor lines is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowStandardDeviation As Boolean
```


---

## ShowZeta Property

*Quelle: `POLYPROPERTIESLib~PeakCursorSettings~ShowZeta.html` · Polytec PolyProperties Type Library · PeakCursorSettings Object : ShowZeta Property*

### Description

Specifies whether the Zeta value is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowZeta As Boolean
```

### Example
