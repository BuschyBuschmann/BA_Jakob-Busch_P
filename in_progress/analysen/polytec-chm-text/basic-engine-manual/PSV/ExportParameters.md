# PSV – ExportParameters

## ExportParameters Object

*Quelle: `PSV~ExportParameters.html` · Polytec PSV Type Library*

### Description

The export parameters.


---

## ExportParameters Object Members

*Quelle: `PSV~ExportParameters_members.html` · Polytec PSV Type Library*

### Public Methods

| Validate | Validates the state of all properties. |
|---|---|

### Public Properties

| BandSignals | The band signals. |
|---|---|
| DisplayObjects | The display objects. |
| ExportBinary | If set to true the binary dataset 58b is exported to universal file format files. |
| ExportFilteredData | The flag indicating whether the filtered data is exported. |
| ExportInterpolatedPoints | The flag indicating whether interpolated points are exported. |
| ExportInvalidatedPoints | The flag indicating whether the invalidated points are exported. |
| ExportOverrangePoints | The flag indicating whether the overrange points are exported. |
| FileName | The file name of the export file. |
| PointSignals | The point signals. |
| ReferencePointIndices | The reference point indices. |


---

## Validate Method

*Quelle: `PSV~ExportParameters~Validate.html` · Polytec PSV Type Library · ExportParameters Object : Validate Method*

### Description

Validates the state of all properties.

### Syntax

*Visual Basic:*
```
Public Sub Validate()
```


---

## BandSignals Property

*Quelle: `PSV~ExportParameters~BandSignals.html` · Polytec PSV Type Library · ExportParameters Object : BandSignals Property*

### Description

The band signals.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BandSignals As String()
```


---

## DisplayObjects Property

*Quelle: `PSV~ExportParameters~DisplayObjects.html` · Polytec PSV Type Library · ExportParameters Object : DisplayObjects Property*

### Description

The display objects.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DisplayObjects As Boolean
```


---

## ExportBinary Property

*Quelle: `PSV~ExportParameters~ExportBinary.html` · Polytec PSV Type Library · ExportParameters Object : ExportBinary Property*

### Description

If set to true the binary dataset 58b is exported to universal file format files.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ExportBinary As Boolean
```


---

## ExportFilteredData Property

*Quelle: `PSV~ExportParameters~ExportFilteredData.html` · Polytec PSV Type Library · ExportParameters Object : ExportFilteredData Property*

### Description

The flag indicating whether the filtered data is exported.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ExportFilteredData As Boolean
```

### Remarks

The same algorithms are used as for displaying the data in area view or for exporting data to the ASCII format. All data that is going to be exported must fit into the memory of the PC.


---

## ExportInterpolatedPoints Property

*Quelle: `PSV~ExportParameters~ExportInterpolatedPoints.html` · Polytec PSV Type Library · ExportParameters Object : ExportInterpolatedPoints Property*

### Description

The flag indicating whether interpolated points are exported.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ExportInterpolatedPoints As Boolean
```

### Remarks

The same algorithms are used as for displaying the data in area view or for exporting data to the ASCII format. All data that is going to be exported must fit into the memory of the PC.


---

## ExportInvalidatedPoints Property

*Quelle: `PSV~ExportParameters~ExportInvalidatedPoints.html` · Polytec PSV Type Library · ExportParameters Object : ExportInvalidatedPoints Property*

### Description

The flag indicating whether the invalidated points are exported.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ExportInvalidatedPoints As Boolean
```

### Remarks

.


---

## ExportOverrangePoints Property

*Quelle: `PSV~ExportParameters~ExportOverrangePoints.html` · Polytec PSV Type Library · ExportParameters Object : ExportOverrangePoints Property*

### Description

The flag indicating whether the overrange points are exported.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ExportOverrangePoints As Boolean
```


---

## FileName Property

*Quelle: `PSV~ExportParameters~FileName.html` · Polytec PSV Type Library · ExportParameters Object : FileName Property*

### Description

The file name of the export file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FileName As String
```


---

## PointSignals Property

*Quelle: `PSV~ExportParameters~PointSignals.html` · Polytec PSV Type Library · ExportParameters Object : PointSignals Property*

### Description

The point signals.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PointSignals As String()
```


---

## ReferencePointIndices Property

*Quelle: `PSV~ExportParameters~ReferencePointIndices.html` · Polytec PSV Type Library · ExportParameters Object : ReferencePointIndices Property*

### Description

The reference point indices.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ReferencePointIndices As Long()
```
