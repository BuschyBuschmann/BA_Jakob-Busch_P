# POLYPROPERTIESLib – IAnalyzerPinSettings2

## IAnalyzerPinSettings2 Interface

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2.html` · Polytec PolyProperties Type Library*

### Description

The settings for pinning analyzer view settings to other open analyzer views.

### Object Model

### Remarks

It is recommended to cast to the AnalyzerPinSettings Object.


---

## IAnalyzerPinSettings2 Interface Members

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Abscissa | Specifies the abscissa pin state. |
|---|---|
| Axes | Specifies whether the axes settings of the analyzer should be pinned to other analyzers. |
| Cursor | Specifies whether the cursor settings of the analyzer should be pinned to other analyzers. |
| General | Specifies whether the general settings of the analyzer should be pinned to other analyzers. |
| Lines | Specifies whether the lines settings of the analyzer should be pinned to other analyzers. |
| Modified | Returns whether the settings object has been modified. |
| Ordinate | Specifies the ordinate pin state. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Signal | Specifies whether the signal settings of the analyzer should be pinned to other analyzers. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Clone.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Copy.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Equal.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Equal Method*

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

## Abscissa Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Abscissa.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Abscissa Property*

### Description

Specifies the abscissa pin state.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Abscissa As Boolean
```


---

## Axes Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Axes.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Axes Property*

### Description

Specifies whether the axes settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Axes As Boolean
```


---

## Cursor Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Cursor.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Cursor Property*

### Description

Specifies whether the cursor settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Cursor As Boolean
```


---

## General Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~General.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : General Property*

### Description

Specifies whether the general settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property General As Boolean
```


---

## Lines Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Lines.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Lines Property*

### Description

Specifies whether the lines settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Lines As Boolean
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Modified.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Modified Property*

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

## Ordinate Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Ordinate.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Ordinate Property*

### Description

Specifies the ordinate pin state.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Ordinate As Boolean
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Parent.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Parent Property*

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

## Signal Property

*Quelle: `POLYPROPERTIESLib~IAnalyzerPinSettings2~Signal.html` · Polytec PolyProperties Type Library · IAnalyzerPinSettings2 Interface : Signal Property*

### Description

Specifies whether the signal settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Signal As Boolean
```
