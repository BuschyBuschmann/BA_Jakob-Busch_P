# POLYFILELib – IInfos2

## IInfos2 Collection

*Quelle: `POLYFILELib~IInfos2.html` · Polytec PolyFile Type Library*

### Description

Infos is a named and typed collection holding items of different type that are derived from Info.

### Object Model

### Remarks

It is recommended to cast to the Infos Collection.


---

## IInfos2 Collection Members

*Quelle: `POLYFILELib~IInfos2_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new item with the given type to the collection and returns the added item. |
|---|---|

### Public Properties

| Count | Returns the number of items in the Infos collection. |
|---|---|
| Exists | Returns True if the item exists in the collection. |
| Item | Returns an item of the collection. |
| Type | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYFILELib~IInfos2~Add.html` · Polytec PolyFile Type Library · IInfos2 Collection : Add Method*

### Description

Adds a new item with the given type to the collection and returns the added item.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   ByVal ptcInfoType As PTCInfoType _
) As IInfo
```

### Parameters

ptcInfoType

| Value | Description |
|---|---|
| ptcInfoAcquisition | AcquisitionInfoModes |
| ptcInfoAlignments | Alignments |
| ptcInfoAPS | not yet implemented |
| ptcInfoCameraSettings | CameraSettings |
| ptcInfoDbReferences | DbReferences |
| ptcInfoElements | Elements |
| ptcInfoHardware | Hardware |
| ptcInfoMeasPoints | MeasPoints |
| ptcInfoMeasurementLocations | MeasurementLocations |
| ptcInfoPositionDevice | Positioning device for MSA-100-3D and other systems, only available in the InfosAcq collection. |
| ptcInfoPositioningStage | Positioning stage for MSA systems, only available in the InfosAcq collection of PSV. |
| ptcInfoProfiles | Profiles |
| ptcInfoScanHead | deprecated, use ptcInfoScanHeadDevices instead. |
| ptcInfoScanHeadDevices | ScanheadDevices |
| ptcInfoSpectrogram | SpectrogramInfo |
| ptcInfoTextures | Textures |
| ptcInfoVibrometers | Vibrometers, only available in the InfosAcq collection of MPV/PSV/VibSoft. |
| ptcInfoVideo | deprecated, use ptcInfoVideoBitmap instead. |
| ptcInfoVideoBitmap | VideoBitmap |
| ptcInfoVideoMapping | Video mapping , objective calibration |
The type of the info to add to the collection.

### Remarks

This method is for internal use only.


---

## Count Property

*Quelle: `POLYFILELib~IInfos2~Count.html` · Polytec PolyFile Type Library · IInfos2 Collection : Count Property*

### Description

Returns the number of items in the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYFILELib~IInfos2~Exists.html` · Polytec PolyFile Type Library · IInfos2 Collection : Exists Property*

### Description

Returns True if the item exists in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal IndexOrType As Variant _
) As Boolean
```

### Parameters

IndexOrType

Index (integer) or type (PTCInfoType) of the item.


---

## Item Property

*Quelle: `POLYFILELib~IInfos2~Item.html` · Polytec PolyFile Type Library · IInfos2 Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal IndexOrName As Variant _
) As IInfo
```

### Parameters

IndexOrName

Index (integer) or name (string) of the item.


---

## Type Property

*Quelle: `POLYFILELib~IInfos2~Type.html` · Polytec PolyFile Type Library · IInfos2 Collection : Type Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal ptcInfoType As PTCInfoType _
) As IInfo
```

### Parameters

ptcInfoType

| Value | Description |
|---|---|
| ptcInfoAcquisition | AcquisitionInfoModes |
| ptcInfoAlignments | Alignments |
| ptcInfoAPS | not yet implemented |
| ptcInfoCameraSettings | CameraSettings |
| ptcInfoDbReferences | DbReferences |
| ptcInfoElements | Elements |
| ptcInfoHardware | Hardware |
| ptcInfoMeasPoints | MeasPoints |
| ptcInfoMeasurementLocations | MeasurementLocations |
| ptcInfoPositionDevice | Positioning device for MSA-100-3D and other systems, only available in the InfosAcq collection. |
| ptcInfoPositioningStage | Positioning stage for MSA systems, only available in the InfosAcq collection of PSV. |
| ptcInfoProfiles | Profiles |
| ptcInfoScanHead | deprecated, use ptcInfoScanHeadDevices instead. |
| ptcInfoScanHeadDevices | ScanheadDevices |
| ptcInfoSpectrogram | SpectrogramInfo |
| ptcInfoTextures | Textures |
| ptcInfoVibrometers | Vibrometers, only available in the InfosAcq collection of MPV/PSV/VibSoft. |
| ptcInfoVideo | deprecated, use ptcInfoVideoBitmap instead. |
| ptcInfoVideoBitmap | VideoBitmap |
| ptcInfoVideoMapping | Video mapping , objective calibration |
The type of the item.
