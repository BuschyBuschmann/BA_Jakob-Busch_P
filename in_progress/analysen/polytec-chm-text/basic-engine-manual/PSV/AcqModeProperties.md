# PSV – AcqModeProperties

## AcqModeProperties Collection

*Quelle: `PSV~AcqModeProperties.html` · Polytec PSV Type Library*

### Description

The AcqModeProperties is a collection of AcquisitionProperities objects. It contains an AcquisitionProperties object for every acquisition mode.

### Object Model


---

## AcqModeProperties Collection Members

*Quelle: `PSV~AcqModeProperties_members.html` · Polytec PSV Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an AcquisitionProperties collection for the given acquisition mode. |


---

## Count Property

*Quelle: `PSV~AcqModeProperties~Count.html` · Polytec PSV Type Library · AcqModeProperties Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `PSV~AcqModeProperties~Item.html` · Polytec PSV Type Library · AcqModeProperties Collection : Item Property*

### Description

Returns an AcquisitionProperties collection for the given acquisition mode.

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
The acquisition mode to get the acquisition properties for.
