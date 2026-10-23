# PSV – InfosAcq

## InfosAcq Collection

*Quelle: `PSV~InfosAcq.html` · Polytec PSV Type Library*

### Description

Named and typed collection holding items of different type that are derived from Info.

### Object Model


---

## InfosAcq Collection Members

*Quelle: `PSV~InfosAcq_members.html` · Polytec PSV Type Library*

### Public Methods

| Add | Adds a new item with the given type to the collection and returns the added item. |
|---|---|

### Public Properties

| AcquisitionInfoModes | Returns the AcquisitionInfoModes item of the collection. |
|---|---|
| Alignments | Returns the AlignmentsAcq item of the collection. |
| CameraSettings | Returns the CameraSettings item of the collection. |
| Count | The number of items in the collection. |
| DbReferences | Returns the DbReferences item of the collection. |
| Elements | Returns the Elements item of the collection. |
| Exists | Returns whether an item with the given type or name exists in the collection. |
| Hardware | Returns the HardwareAcq item of the collection. |
| HasAcquisitionInfoModes | Returns whether the collection has an AcquisitionInfoModes item. |
| HasAlignments | Returns whether the collection has an Alignments item. |
| HasCameraSettings | Returns whether the collection has a CameraSettings item. |
| HasDbReferences | Returns whether the collection has a DbReferences item. |
| HasElements | Returns whether the collection has an Elements item. |
| HasHardware | Returns whether the collection has a HardwareAcq item. |
| HasMeasPoints | Returns whether the collection has a MeasPoints item. |
| HasMeasurementLocations | Returns whether the collection has a MeasurementLocations item. |
| HasPositionDevice | Returns whether the collection has a PositionDevice item. |
| HasPositioningStage | Returns whether the collection has a PositioningStage item. |
| HasProfiles | Returns whether the collection has a Profiles item. |
| HasScanHeadDevicesInfo | Returns whether the collection has a ScanHeadDevicesInfoAcq item. |
| HasTextures | Returns whether the collection has a Textures item. |
| HasVibrometers | Returns whether the collection has a Vibrometers item. |
| HasVideoBitmap | Returns whether the collection has a VideoBitmap item. |
| HasVideoMappingInfo | Returns whether the collection has a VideoMappingInfo item. |
| Item | Returns the item with the given index or name of the collection. |
| MeasPoints | Returns the MeasPoints item of the collection. |
| MeasurementLocations | Returns the MeasurementLocations item of the collection. |
| PositionDevice | Returns the PositionDevice item of the collection. |
| PositioningStage | Returns the PositioningStage item of the collection. Using PositioningStage is deprecated. Please use PositionDevice instead. |
| Profiles | Returns the Profiles item of the collection. |
| ScanHeadDevicesInfo | Returns the ScanHeadDevicesInfoAcq item of the collection. |
| Textures | Returns the Textures item of the collection. |
| Type | Returns the item with the given type of the collection. |
| Vibrometers | Returns the Vibrometers item of the collection. |
| VideoBitmap | Returns the VideoBitmap item of the collection. |
| VideoMappingInfo | Returns the VideoMappingInfo item of the collection. |


---

## Add Method

*Quelle: `PSV~InfosAcq~Add.html` · Polytec PSV Type Library · InfosAcq Collection : Add Method*

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

*Quelle: `PSV~InfosAcq~AcquisitionInfoModes.html` · Polytec PSV Type Library · InfosAcq Collection : AcquisitionInfoModes Property*

### Description

Returns the AcquisitionInfoModes item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcquisitionInfoModes As IAcquisitionInfoModes3
```

### Return Type

The AcquisitionInfoModes item.

### Remarks

This item is not available in the InfosAcq collection.


---

## Alignments Property

*Quelle: `PSV~InfosAcq~Alignments.html` · Polytec PSV Type Library · InfosAcq Collection : Alignments Property*

### Description

Returns the AlignmentsAcq item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Alignments As AlignmentsAcq
```

### Return Type

The AlignmentsAcq item.

### Remarks

This item is not available for VibSoft.


---

## CameraSettings Property

*Quelle: `PSV~InfosAcq~CameraSettings.html` · Polytec PSV Type Library · InfosAcq Collection : CameraSettings Property*

### Description

Returns the CameraSettings item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CameraSettings As ICameraSettings
```

### Return Type

The CameraSettings item.

### Remarks

This item is not available in the InfosAcq collection.


---

## Count Property

*Quelle: `PSV~InfosAcq~Count.html` · Polytec PSV Type Library · InfosAcq Collection : Count Property*

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

## DbReferences Property

*Quelle: `PSV~InfosAcq~DbReferences.html` · Polytec PSV Type Library · InfosAcq Collection : DbReferences Property*

### Description

Returns the DbReferences item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DbReferences As IDbReferences2
```

### Return Type

The DbReferences item.

### Remarks

This item is not available in the InfosAcq collection.


---

## Elements Property

*Quelle: `PSV~InfosAcq~Elements.html` · Polytec PSV Type Library · InfosAcq Collection : Elements Property*

### Description

Returns the Elements item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Elements As IElements3
```

### Return Type

The Elements item.

### Remarks

This item is not available for VibSoft.


---

## Exists Property

*Quelle: `PSV~InfosAcq~Exists.html` · Polytec PSV Type Library · InfosAcq Collection : Exists Property*

### Description

Returns whether an item with the given type or name exists in the collection.

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

The name or type of the item.


---

## Hardware Property

*Quelle: `PSV~InfosAcq~Hardware.html` · Polytec PSV Type Library · InfosAcq Collection : Hardware Property*

### Description

Returns the HardwareAcq item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Hardware As IHardware7
```

### Return Type

The HardwareAcq item.


---

## HasAcquisitionInfoModes Property

*Quelle: `PSV~InfosAcq~HasAcquisitionInfoModes.html` · Polytec PSV Type Library · InfosAcq Collection : HasAcquisitionInfoModes Property*

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

### Remarks

This item is not available in the InfosAcq collection.


---

## HasAlignments Property

*Quelle: `PSV~InfosAcq~HasAlignments.html` · Polytec PSV Type Library · InfosAcq Collection : HasAlignments Property*

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

### Remarks

This item is not available for VibSoft.


---

## HasCameraSettings Property

*Quelle: `PSV~InfosAcq~HasCameraSettings.html` · Polytec PSV Type Library · InfosAcq Collection : HasCameraSettings Property*

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

### Remarks

This item is not available in the InfosAcq collection.


---

## HasDbReferences Property

*Quelle: `PSV~InfosAcq~HasDbReferences.html` · Polytec PSV Type Library · InfosAcq Collection : HasDbReferences Property*

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

### Remarks

This item is not available in the InfosAcq collection.


---

## HasElements Property

*Quelle: `PSV~InfosAcq~HasElements.html` · Polytec PSV Type Library · InfosAcq Collection : HasElements Property*

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

### Remarks

This item is not available for VibSoft.


---

## HasHardware Property

*Quelle: `PSV~InfosAcq~HasHardware.html` · Polytec PSV Type Library · InfosAcq Collection : HasHardware Property*

### Description

Returns whether the collection has a HardwareAcq item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasHardware As Boolean
```

### Return Type

True when the collection has a HardwareAcq item.


---

## HasMeasPoints Property

*Quelle: `PSV~InfosAcq~HasMeasPoints.html` · Polytec PSV Type Library · InfosAcq Collection : HasMeasPoints Property*

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

### Remarks

This item is not available for VibSoft.


---

## HasMeasurementLocations Property

*Quelle: `PSV~InfosAcq~HasMeasurementLocations.html` · Polytec PSV Type Library · InfosAcq Collection : HasMeasurementLocations Property*

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

### Remarks

This item is not available for VibSoft.


---

## HasPositionDevice Property

*Quelle: `PSV~InfosAcq~HasPositionDevice.html` · Polytec PSV Type Library · InfosAcq Collection : HasPositionDevice Property*

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

*Quelle: `PSV~InfosAcq~HasPositioningStage.html` · Polytec PSV Type Library · InfosAcq Collection : HasPositioningStage Property*

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

### Remarks

This item is not available for VibSoft.


---

## HasProfiles Property

*Quelle: `PSV~InfosAcq~HasProfiles.html` · Polytec PSV Type Library · InfosAcq Collection : HasProfiles Property*

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

### Remarks

This item is not available in the InfosAcq collection.


---

## HasScanHeadDevicesInfo Property

*Quelle: `PSV~InfosAcq~HasScanHeadDevicesInfo.html` · Polytec PSV Type Library · InfosAcq Collection : HasScanHeadDevicesInfo Property*

### Description

Returns whether the collection has a ScanHeadDevicesInfoAcq item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasScanHeadDevicesInfo As Boolean
```

### Return Type

True when the collection has a ScanHeadDevicesInfoAcq item.

### Remarks

This item is not available for VibSoft.


---

## HasTextures Property

*Quelle: `PSV~InfosAcq~HasTextures.html` · Polytec PSV Type Library · InfosAcq Collection : HasTextures Property*

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

*Quelle: `PSV~InfosAcq~HasVibrometers.html` · Polytec PSV Type Library · InfosAcq Collection : HasVibrometers Property*

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

*Quelle: `PSV~InfosAcq~HasVideoBitmap.html` · Polytec PSV Type Library · InfosAcq Collection : HasVideoBitmap Property*

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

### Remarks

This item is not available in the InfosAcq collection.


---

## HasVideoMappingInfo Property

*Quelle: `PSV~InfosAcq~HasVideoMappingInfo.html` · Polytec PSV Type Library · InfosAcq Collection : HasVideoMappingInfo Property*

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

### Remarks

This item is not available in the InfosAcq collection.


---

## Item Property

*Quelle: `PSV~InfosAcq~Item.html` · Polytec PSV Type Library · InfosAcq Collection : Item Property*

### Description

Returns the item with the given index or name of the collection.

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

The index or name of the item.


---

## MeasPoints Property

*Quelle: `PSV~InfosAcq~MeasPoints.html` · Polytec PSV Type Library · InfosAcq Collection : MeasPoints Property*

### Description

Returns the MeasPoints item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MeasPoints As IMeasPoints11
```

### Return Type

The MeasPoints item.

### Remarks

This item is not available for VibSoft.


---

## MeasurementLocations Property

*Quelle: `PSV~InfosAcq~MeasurementLocations.html` · Polytec PSV Type Library · InfosAcq Collection : MeasurementLocations Property*

### Description

Returns the MeasurementLocations item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MeasurementLocations As IMeasurementLocations2
```

### Return Type

The MeasurementLocations item.

### Remarks

This item is not available for VibSoft.


---

## PositionDevice Property

*Quelle: `PSV~InfosAcq~PositionDevice.html` · Polytec PSV Type Library · InfosAcq Collection : PositionDevice Property*

### Description

Returns the PositionDevice item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionDevice As PositionDevice
```

### Return Type

The PositionDevice item of the collection.


---

## PositioningStage Property

*Quelle: `PSV~InfosAcq~PositioningStage.html` · Polytec PSV Type Library · InfosAcq Collection : PositioningStage Property*

### Description

Returns the PositioningStage item of the collection. Using PositioningStage is deprecated. Please use PositionDevice instead.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositioningStage As PositioningStage
```

### Return Type

The PositioningStage item of the collection.

### Remarks

This item is not available for VibSoft.


---

## Profiles Property

*Quelle: `PSV~InfosAcq~Profiles.html` · Polytec PSV Type Library · InfosAcq Collection : Profiles Property*

### Description

Returns the Profiles item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Profiles As IProfiles
```

### Return Type

The Profiles item.

### Remarks

This item is not available in the InfosAcq collection.


---

## ScanHeadDevicesInfo Property

*Quelle: `PSV~InfosAcq~ScanHeadDevicesInfo.html` · Polytec PSV Type Library · InfosAcq Collection : ScanHeadDevicesInfo Property*

### Description

Returns the ScanHeadDevicesInfoAcq item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevicesInfo As ScanHeadDevicesInfoAcq
```

### Return Type

The ScanHeadDevicesInfoAcq item.

### Remarks

This item is not available for VibSoft.


---

## Textures Property

*Quelle: `PSV~InfosAcq~Textures.html` · Polytec PSV Type Library · InfosAcq Collection : Textures Property*

### Description

Returns the Textures item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Textures As ITextures
```


---

## Type Property

*Quelle: `PSV~InfosAcq~Type.html` · Polytec PSV Type Library · InfosAcq Collection : Type Property*

### Description

Returns the item with the given type of the collection.

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

*Quelle: `PSV~InfosAcq~Vibrometers.html` · Polytec PSV Type Library · InfosAcq Collection : Vibrometers Property*

### Description

Returns the Vibrometers item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Vibrometers As VibrometerGroups
```

### Return Type

The Vibrometers item.

### Example


---

## VideoBitmap Property

*Quelle: `PSV~InfosAcq~VideoBitmap.html` · Polytec PSV Type Library · InfosAcq Collection : VideoBitmap Property*

### Description

Returns the VideoBitmap item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VideoBitmap As IVideoBitmap5
```

### Return Type

The VideoBitmap item.

### Remarks

This item is not available in the InfosAcq collection.


---

## VideoMappingInfo Property

*Quelle: `PSV~InfosAcq~VideoMappingInfo.html` · Polytec PSV Type Library · InfosAcq Collection : VideoMappingInfo Property*

### Description

Returns the VideoMappingInfo item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VideoMappingInfo As IVideoMappingInfo3
```

### Return Type

The VideoMappingInfo item.

### Remarks

This item is not available in the InfosAcq collection.
