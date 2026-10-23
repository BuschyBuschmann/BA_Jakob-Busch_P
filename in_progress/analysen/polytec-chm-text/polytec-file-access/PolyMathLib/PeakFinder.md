# PolyMathLib – PeakFinder

## PeakFinder Object

*Quelle: `PolyMathLib~PeakFinder.html` · Polytec PolyMath Type Library*

### Description

The peak finder allows to find peaks in a data array.

### Object Model


---

## PeakFinder Object Members

*Quelle: `PolyMathLib~PeakFinder_members.html` · Polytec PolyMath Type Library*

### Public Methods

| FindPeaks | Finds peaks in the specified data array by searching for local maxima. |
|---|---|

### Public Properties

| MinimumAmplitude | The minimum amplitude of a peak. |
|---|---|
| MinimumDistance | The minimum distance between peaks. |
| MinimumProminence | The minimum prominance of the peak. |
| RelativeHeightForWidth | The relative height of the peak for calculating its width. |


---

## FindPeaks Method

*Quelle: `PolyMathLib~PeakFinder~FindPeaks.html` · Polytec PolyMath Type Library · PeakFinder Object : FindPeaks Method*

### Description

Finds peaks in the specified data array by searching for local maxima.

### Syntax

*Visual Basic:*
```
Public Function FindPeaks( _
   ByVal data() As Single _
) As DataPeaks
```

### Parameters

data

One-dimensional array of Single with the data to search for peaks.

### Return Type

The collection of found data peaks.


---

## MinimumAmplitude Property

*Quelle: `PolyMathLib~PeakFinder~MinimumAmplitude.html` · Polytec PolyMath Type Library · PeakFinder Object : MinimumAmplitude Property*

### Description

The minimum amplitude of a peak.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MinimumAmplitude As Double
```


---

## MinimumDistance Property

*Quelle: `PolyMathLib~PeakFinder~MinimumDistance.html` · Polytec PolyMath Type Library · PeakFinder Object : MinimumDistance Property*

### Description

The minimum distance between peaks.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MinimumDistance As Long
```

### Remarks

Required minimal horizontal distance (>= 1) in samples between neighbouring peaks. Smaller peaks are removed first until the condition is fulfilled for all remaining peaks.


---

## MinimumProminence Property

*Quelle: `PolyMathLib~PeakFinder~MinimumProminence.html` · Polytec PolyMath Type Library · PeakFinder Object : MinimumProminence Property*

### Description

The minimum prominance of the peak.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MinimumProminence As Double
```

### Remarks

The prominence of a peak measures how much a peak stands out from the surrounding baseline of the signal and is defined as the vertical distance between the peak and its lowest contour line.


---

## RelativeHeightForWidth Property

*Quelle: `PolyMathLib~PeakFinder~RelativeHeightForWidth.html` · Polytec PolyMath Type Library · PeakFinder Object : RelativeHeightForWidth Property*

### Description

The relative height of the peak for calculating its width.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RelativeHeightForWidth As Double
```

### Remarks

Chooses the relative height at which the peak width is measured as a percentage of its prominence. 1.0 calculates the width of the peak at its lowest contour line while 0.5 evaluates at half the prominence height. Must be at least 0.
