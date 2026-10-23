# POLYFILELib – Infos

## Infos Collection

*Quelle: `POLYFILELib~Infos.html` · Polytec PolyFile Type Library*

### Description

Named and typed collection holding items of different type that are derived from Info.

### Object Model


---

## Infos Collection Members

*Quelle: `POLYFILELib~Infos_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new item with the given type to the collection and returns the added item. |
|---|---|

### Public Properties

| AcquisitionInfoModes | Returns the AcquisitionInfoModes item of the collection. |
|---|---|
| Alignments | Returns the Alignments item of the collection. |
| CameraSettings | Returns the CameraSettings item of the collection. |
| Count | Returns the number of items in the Infos collection. |
| DbReferences | Returns the DbReferences item of the collection. |
| Elements | Returns the Elements item of the collection. |
| Exists | Returns True if the item exists in the collection. |
| Hardware | Returns the Hardware item of the collection. |
| HasAcquisitionInfoModes | Returns whether the collection has an AcquisitionInfoModes item. |
| HasAlignments | Returns whether the collection has an Alignments item. |
| HasCameraSettings | Returns whether the collection has a CameraSettings item. |
| HasDbReferences | Returns whether the collection has a DbReferences item. |
| HasElements | Returns whether the collection has an Elements item. |
| HasHardware | Returns whether the collection has a Hardware item. |
| HasMeasPoints | Returns whether the collection has a MeasPoints item. |
| HasMeasurementLocations | Returns whether the collection has a MeasurementLocations item. |
| HasPositionDevice | Returns whether the collection has a PositionDevice item. |
| HasPositioningStage | Returns whether the collection has a PositioningStage item. |
| HasProfiles | Returns whether the collection has a Profiles item. |
| HasScanHeadDevicesInfo | Returns whether the collection has a ScanHeadDevicesInfo item. |
| HasSpectrogramInfo | Returns whether the collection has a SpectrogramInfo item. |
| HasTextures | Returns whether the collection has a Textures item. |
| HasVibrometers | Returns whether the collection has a Vibrometers item. |
| HasVideoBitmap | Returns whether the collection has a VideoBitmap item. |
| HasVideoMappingInfo | Returns whether the collection has a VideoMappingInfo item. |
| Item | Returns an item of the collection. |
| MeasPoints | Returns the MeasPoints item of the collection. |
| MeasurementLocations | Returns the MeasurementLocations item of the collection. |
| PositionDevice | Returns the PositionDevice item of the collection. |
| PositioningStage | Returns the PositioningStage item of the collection. |
| Profiles | Returns the Profiles item of the collection. |
| ScanHeadDevicesInfo | Returns the ScanHeadDevicesInfo item of the collection. |
| SpectrogramInfo | Returns the SpectrogramInfo item of the collection. |
| Textures | Returns the Textures item of the collection. |
| Type | Returns an item of the collection. |
| Vibrometers | Returns the Vibrometers item of the collection. |
| VideoBitmap | Returns the VideoBitmap item of the collection. |
| VideoMappingInfo | Returns the VideoMappingInfo item of the collection. |


---

## Add Method

*Quelle: `POLYFILELib~Infos~Add.html` · Polytec PolyFile Type Library · Infos Collection : Add Method*

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

## AcquisitionInfoModes Property

*Quelle: `POLYFILELib~Infos~AcquisitionInfoModes.html` · Polytec PolyFile Type Library · Infos Collection : AcquisitionInfoModes Property*

### Description

Returns the AcquisitionInfoModes item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcquisitionInfoModes As AcquisitionInfoModes
```

### Return Type

The AcquisitionInfoModes item.


---

## Alignments Property

*Quelle: `POLYFILELib~Infos~Alignments.html` · Polytec PolyFile Type Library · Infos Collection : Alignments Property*

### Description

Returns the Alignments item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Alignments As Alignments
```

### Return Type

The alignments item.


---

## CameraSettings Property

*Quelle: `POLYFILELib~Infos~CameraSettings.html` · Polytec PolyFile Type Library · Infos Collection : CameraSettings Property*

### Description

Returns the CameraSettings item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CameraSettings As CameraSettings
```

### Return Type

The CameraSettings item.


---

## Count Property

*Quelle: `POLYFILELib~Infos~Count.html` · Polytec PolyFile Type Library · Infos Collection : Count Property*

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

## DbReferences Property

*Quelle: `POLYFILELib~Infos~DbReferences.html` · Polytec PolyFile Type Library · Infos Collection : DbReferences Property*

### Description

Returns the DbReferences item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DbReferences As DbReferences
```

### Return Type

The DbReferences item.


---

## Elements Property

*Quelle: `POLYFILELib~Infos~Elements.html` · Polytec PolyFile Type Library · Infos Collection : Elements Property*

### Description

Returns the Elements item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Elements As Elements
```

### Return Type

The Elements item.


---

## Exists Property

*Quelle: `POLYFILELib~Infos~Exists.html` · Polytec PolyFile Type Library · Infos Collection : Exists Property*

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

## Hardware Property

*Quelle: `POLYFILELib~Infos~Hardware.html` · Polytec PolyFile Type Library · Infos Collection : Hardware Property*

### Description

Returns the Hardware item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Hardware As Hardware
```

### Return Type

The Hardware item.


---

## HasAcquisitionInfoModes Property

*Quelle: `POLYFILELib~Infos~HasAcquisitionInfoModes.html` · Polytec PolyFile Type Library · Infos Collection : HasAcquisitionInfoModes Property*

### Description

Returns whether the collection has an AcquisitionInfoModes item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasAcquisitionInfoModes As Boolean
```

### Return Type

True when the collection has an AcquisitionInfoModes item.


---

## HasAlignments Property

*Quelle: `POLYFILELib~Infos~HasAlignments.html` · Polytec PolyFile Type Library · Infos Collection : HasAlignments Property*

### Description

Returns whether the collection has an Alignments item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasAlignments As Boolean
```

### Return Type

True when the collection has an Alignments item.


---

## HasCameraSettings Property

*Quelle: `POLYFILELib~Infos~HasCameraSettings.html` · Polytec PolyFile Type Library · Infos Collection : HasCameraSettings Property*

### Description

Returns whether the collection has a CameraSettings item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasCameraSettings As Boolean
```

### Return Type

True when the collection has a CameraSettings item.


---

## HasDbReferences Property

*Quelle: `POLYFILELib~Infos~HasDbReferences.html` · Polytec PolyFile Type Library · Infos Collection : HasDbReferences Property*

### Description

Returns whether the collection has a DbReferences item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasDbReferences As Boolean
```

### Return Type

True when the collection has a DbReferences item.


---

## HasElements Property

*Quelle: `POLYFILELib~Infos~HasElements.html` · Polytec PolyFile Type Library · Infos Collection : HasElements Property*

### Description

Returns whether the collection has an Elements item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasElements As Boolean
```

### Return Type

True when the collection has an Elements item.


---

## HasHardware Property

*Quelle: `POLYFILELib~Infos~HasHardware.html` · Polytec PolyFile Type Library · Infos Collection : HasHardware Property*

### Description

Returns whether the collection has a Hardware item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasHardware As Boolean
```

### Return Type

True when the collection has a Hardware item.


---

## HasMeasPoints Property

*Quelle: `POLYFILELib~Infos~HasMeasPoints.html` · Polytec PolyFile Type Library · Infos Collection : HasMeasPoints Property*

### Description

Returns whether the collection has a MeasPoints item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasMeasPoints As Boolean
```

### Return Type

True when the collection has a MeasPoints item.


---

## HasMeasurementLocations Property

*Quelle: `POLYFILELib~Infos~HasMeasurementLocations.html` · Polytec PolyFile Type Library · Infos Collection : HasMeasurementLocations Property*

### Description

Returns whether the collection has a MeasurementLocations item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasMeasurementLocations As Boolean
```

### Return Type

True when the collection has a MeasurementLocations item.


---

## HasPositionDevice Property

*Quelle: `POLYFILELib~Infos~HasPositionDevice.html` · Polytec PolyFile Type Library · Infos Collection : HasPositionDevice Property*

### Description

Returns whether the collection has a PositionDevice item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasPositionDevice As Boolean
```

### Return Type

True if the collection has a PositionDevice item.


---

## HasPositioningStage Property

*Quelle: `POLYFILELib~Infos~HasPositioningStage.html` · Polytec PolyFile Type Library · Infos Collection : HasPositioningStage Property*

### Description

Returns whether the collection has a PositioningStage item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasPositioningStage As Boolean
```

### Return Type

True if the collection has a PositioningStage item.


---

## HasProfiles Property

*Quelle: `POLYFILELib~Infos~HasProfiles.html` · Polytec PolyFile Type Library · Infos Collection : HasProfiles Property*

### Description

Returns whether the collection has a Profiles item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasProfiles As Boolean
```

### Return Type

True when the collection has a Profiles item.


---

## HasScanHeadDevicesInfo Property

*Quelle: `POLYFILELib~Infos~HasScanHeadDevicesInfo.html` · Polytec PolyFile Type Library · Infos Collection : HasScanHeadDevicesInfo Property*

### Description

Returns whether the collection has a ScanHeadDevicesInfo item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasScanHeadDevicesInfo As Boolean
```

### Return Type

True when the collection has a ScanHeadDevicesInfo item.


---

## HasSpectrogramInfo Property

*Quelle: `POLYFILELib~Infos~HasSpectrogramInfo.html` · Polytec PolyFile Type Library · Infos Collection : HasSpectrogramInfo Property*

### Description

Returns whether the collection has a SpectrogramInfo item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasSpectrogramInfo As Boolean
```

### Return Type

True when the collection has a SpectrogramInfo item.


---

## HasTextures Property

*Quelle: `POLYFILELib~Infos~HasTextures.html` · Polytec PolyFile Type Library · Infos Collection : HasTextures Property*

### Description

Returns whether the collection has a Textures item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasTextures As Boolean
```

### Return Type

True when the collection has a Textures item.


---

## HasVibrometers Property

*Quelle: `POLYFILELib~Infos~HasVibrometers.html` · Polytec PolyFile Type Library · Infos Collection : HasVibrometers Property*

### Description

Returns whether the collection has a Vibrometers item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasVibrometers As Boolean
```

### Return Type

True when the collection has a Vibrometers item.


---

## HasVideoBitmap Property

*Quelle: `POLYFILELib~Infos~HasVideoBitmap.html` · Polytec PolyFile Type Library · Infos Collection : HasVideoBitmap Property*

### Description

Returns whether the collection has a VideoBitmap item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasVideoBitmap As Boolean
```

### Return Type

True when the collection has a VideoBitmap item.


---

## HasVideoMappingInfo Property

*Quelle: `POLYFILELib~Infos~HasVideoMappingInfo.html` · Polytec PolyFile Type Library · Infos Collection : HasVideoMappingInfo Property*

### Description

Returns whether the collection has a VideoMappingInfo item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasVideoMappingInfo As Boolean
```

### Return Type

True when the collection has a VideoMappingInfo item.


---

## Item Property

*Quelle: `POLYFILELib~Infos~Item.html` · Polytec PolyFile Type Library · Infos Collection : Item Property*

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

## MeasPoints Property

*Quelle: `POLYFILELib~Infos~MeasPoints.html` · Polytec PolyFile Type Library · Infos Collection : MeasPoints Property*

### Description

Returns the MeasPoints item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MeasPoints As MeasPoints
```

### Return Type

The MeasPoints item.


---

## MeasurementLocations Property

*Quelle: `POLYFILELib~Infos~MeasurementLocations.html` · Polytec PolyFile Type Library · Infos Collection : MeasurementLocations Property*

### Description

Returns the MeasurementLocations item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MeasurementLocations As MeasurementLocations
```

### Return Type

The MeasurementLocations item.


---

## PositionDevice Property

*Quelle: `POLYFILELib~Infos~PositionDevice.html` · Polytec PolyFile Type Library · Infos Collection : PositionDevice Property*

### Description

Returns the PositionDevice item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionDevice As IPositionDevice
```

### Return Type

The PositionDevice item of the collection.

### Remarks

This item is available in the PSV and VibSoft software only as a member of the InfosAcq collection.


---

## PositioningStage Property

*Quelle: `POLYFILELib~Infos~PositioningStage.html` · Polytec PolyFile Type Library · Infos Collection : PositioningStage Property*

### Description

Returns the PositioningStage item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositioningStage As IPositioningStage
```

### Return Type

The PositioningStage item of the collection.

### Remarks

This item is available in the PSV software only as a member of the InfosAcq collection.


---

## Profiles Property

*Quelle: `POLYFILELib~Infos~Profiles.html` · Polytec PolyFile Type Library · Infos Collection : Profiles Property*

### Description

Returns the Profiles item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Profiles As Profiles
```

### Return Type

The Profiles item.


---

## ScanHeadDevicesInfo Property

*Quelle: `POLYFILELib~Infos~ScanHeadDevicesInfo.html` · Polytec PolyFile Type Library · Infos Collection : ScanHeadDevicesInfo Property*

### Description

Returns the ScanHeadDevicesInfo item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevicesInfo As ScanHeadDevicesInfo
```

### Return Type

The ScanHeadDevicesInfo item.


---

## SpectrogramInfo Property

*Quelle: `POLYFILELib~Infos~SpectrogramInfo.html` · Polytec PolyFile Type Library · Infos Collection : SpectrogramInfo Property*

### Description

Returns the SpectrogramInfo item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SpectrogramInfo As SpectrogramInfo
```

### Return Type

The SpectrogramInfo item.


---

## Textures Property

*Quelle: `POLYFILELib~Infos~Textures.html` · Polytec PolyFile Type Library · Infos Collection : Textures Property*

### Description

Returns the Textures item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Textures As Textures
```

### Return Type

The Textures item.


---

## Type Property

*Quelle: `POLYFILELib~Infos~Type.html` · Polytec PolyFile Type Library · Infos Collection : Type Property*

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


---

## Vibrometers Property

*Quelle: `POLYFILELib~Infos~Vibrometers.html` · Polytec PolyFile Type Library · Infos Collection : Vibrometers Property*

### Description

Returns the Vibrometers item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Vibrometers As IVibrometerGroups
```

### Return Type

The Vibrometers item.

### Remarks

This item is available in the MPV/PSV/VibSoft software only as a member of the InfosAcq collection.

### Example


---

## VideoBitmap Property

*Quelle: `POLYFILELib~Infos~VideoBitmap.html` · Polytec PolyFile Type Library · Infos Collection : VideoBitmap Property*

### Description

Returns the VideoBitmap item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VideoBitmap As VideoBitmap
```

### Return Type

The VideoBitmap item.


---

## VideoMappingInfo Property

*Quelle: `POLYFILELib~Infos~VideoMappingInfo.html` · Polytec PolyFile Type Library · Infos Collection : VideoMappingInfo Property*

### Description

Returns the VideoMappingInfo item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VideoMappingInfo As VideoMappingInfo
```

### Return Type

The VideoMappingInfo item.
