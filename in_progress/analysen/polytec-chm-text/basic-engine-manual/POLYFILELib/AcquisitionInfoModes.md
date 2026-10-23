# POLYFILELib – AcquisitionInfoModes

## AcquisitionInfoModes Collection

*Quelle: `POLYFILELib~AcquisitionInfoModes.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. Typed collection of AcquisitionProperties. Contains the acquisition properties for the various acquisition modes.

### Object Model

### Remarks

Measurement files contain only acquisition properties for a single acquisition mode whereas settings files contain acquisition properties for all available acquisition modes.


---

## AcquisitionInfoModes Collection Members

*Quelle: `POLYFILELib~AcquisitionInfoModes_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new AcquisitonProperties object to the collection and returns it. |
|---|---|
| Save | Commits the changes to the AcquisitionInfoModes collection to the file. |

### Public Properties

| ActiveMode | Returns the active acquisition mode (the single acquisition mode in measurement files). |
|---|---|
| ActiveProperties | Returns the active acquisition properties (the single acquisition properties in measurement files). |
| Count | Number of items of the AcquisitionInfoModes collection. |
| Item | Returns an item of the AcquisitionInfoModes collection. |
| Name | Returns "Acquisition. Can be used as index to the Infos collection . |
| Type | Returns ptcInfoAcquisition. Can be used as index to the Infos collection . |


---

## Add Method

*Quelle: `POLYFILELib~AcquisitionInfoModes~Add.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : Add Method*

### Description

Adds a new AcquisitonProperties object to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   ByVal ptcInfo As PTCAcqMode _
) As IAcquisitionProperties3
```

### Parameters

ptcInfo

| Value | Description |
|---|---|
| ptcAcqModeFastScan | Acquisition mode FastScan. |
| ptcAcqModeFft | Acquisition mode FFT. |
| ptcAcqModeInplane | Acquisition mode for the PMA software. |
| ptcAcqModeIQ | Acquisition mode IQ for digital demodulation (VDD) |
| ptcAcqModeMultiFrame | Acquisition mode MultiFrame. |
| ptcAcqModeOrderTracking | Acquisition mode OrderTracking. |
| ptcAcqModeTime | Acquisition mode time. |
| ptcAcqModeZoomFft | Acquisition mode Zoom-FFT. |
The acquisition mode.


---

## Save Method

*Quelle: `POLYFILELib~AcquisitionInfoModes~Save.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : Save Method*

### Description

Commits the changes to the AcquisitionInfoModes collection to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## ActiveMode Property

*Quelle: `POLYFILELib~AcquisitionInfoModes~ActiveMode.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : ActiveMode Property*

### Description

Returns the active acquisition mode (the single acquisition mode in measurement files).

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ActiveMode As PTCAcqMode
```


---

## ActiveProperties Property

*Quelle: `POLYFILELib~AcquisitionInfoModes~ActiveProperties.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : ActiveProperties Property*

### Description

Returns the active acquisition properties (the single acquisition properties in measurement files).

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ActiveProperties As IAcquisitionProperties3
```


---

## Count Property

*Quelle: `POLYFILELib~AcquisitionInfoModes~Count.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : Count Property*

### Description

Number of items of the AcquisitionInfoModes collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```

### Remarks

Includes those items that are not present in the file.


---

## Item Property

*Quelle: `POLYFILELib~AcquisitionInfoModes~Item.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : Item Property*

### Description

Returns an item of the AcquisitionInfoModes collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal ptcAcqMode As PTCAcqMode _
) As IAcquisitionProperties3
```

### Parameters

ptcAcqMode

| Value | Description |
|---|---|
| ptcAcqModeFastScan | Acquisition mode FastScan. |
| ptcAcqModeFft | Acquisition mode FFT. |
| ptcAcqModeInplane | Acquisition mode for the PMA software. |
| ptcAcqModeIQ | Acquisition mode IQ for digital demodulation (VDD) |
| ptcAcqModeMultiFrame | Acquisition mode MultiFrame. |
| ptcAcqModeOrderTracking | Acquisition mode OrderTracking. |
| ptcAcqModeTime | Acquisition mode time. |
| ptcAcqModeZoomFft | Acquisition mode Zoom-FFT. |
The acquisition mode.

### Remarks

Returns Nothing if the acquisition properties of this mode are not present in the file.


---

## Name Property

*Quelle: `POLYFILELib~AcquisitionInfoModes~Name.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : Name Property*

### Description

Returns "Acquisition. Can be used as index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "Acquisition".


---

## Type Property

*Quelle: `POLYFILELib~AcquisitionInfoModes~Type.html` · Polytec PolyFile Type Library · AcquisitionInfoModes Collection : Type Property*

### Description

Returns ptcInfoAcquisition. Can be used as index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoAcquisition.
