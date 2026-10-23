# POLYFILELib – IInfos8

## IInfos8 Collection

*Quelle: `POLYFILELib~IInfos8.html` · Polytec PolyFile Type Library*

### Description

IInfos8 Interface

### Object Model

### Remarks

It is recommended to cast to the Infos Collection.


---

## IInfos8 Collection Members

*Quelle: `POLYFILELib~IInfos8_members.html` · Polytec PolyFile Type Library*

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
| HasProfiles | Returns whether the collection has a Profiles item. |
| HasScanHeadDevicesInfo | Returns whether the collection has a ScanHeadDevicesInfo item. |
| HasTextures | Returns whether the collection has a Textures item. |
| HasVibrometers | Returns whether the collection has a Vibrometers item. |
| HasVideoBitmap | Returns whether the collection has a VideoBitmap item. |
| HasVideoMappingInfo | Returns whether the collection has a VideoMappingInfo item. |
| Item | Returns an item of the collection. |
| MeasPoints | Returns the MeasPoints item of the collection. |
| MeasurementLocations | Returns the MeasurementLocations item of the collection. |
| PositionDevice | Returns the PositionDevice item of the collection. |
| Profiles | Returns the Profiles item of the collection. |
| ScanHeadDevicesInfo | Returns the ScanHeadDevicesInfo item of the collection. |
| Textures | Returns the Textures item of the collection. |
| Type | Returns an item of the collection. |
| Vibrometers | Returns the Vibrometers item of the collection. |
| VideoBitmap | Returns the VideoBitmap item of the collection. |
| VideoMappingInfo | Returns the VideoMappingInfo item of the collection. |


---

## Add Method

*Quelle: `POLYFILELib~IInfos8~Add.html` · Polytec PolyFile Type Library · IInfos8 Collection : Add Method*

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

*Quelle: `POLYFILELib~IInfos8~AcquisitionInfoModes.html` · Polytec PolyFile Type Library · IInfos8 Collection : AcquisitionInfoModes Property*

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

*Quelle: `POLYFILELib~IInfos8~Alignments.html` · Polytec PolyFile Type Library · IInfos8 Collection : Alignments Property*

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

*Quelle: `POLYFILELib~IInfos8~CameraSettings.html` · Polytec PolyFile Type Library · IInfos8 Collection : CameraSettings Property*

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

*Quelle: `POLYFILELib~IInfos8~Count.html` · Polytec PolyFile Type Library · IInfos8 Collection : Count Property*

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

*Quelle: `POLYFILELib~IInfos8~DbReferences.html` · Polytec PolyFile Type Library · IInfos8 Collection : DbReferences Property*

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

*Quelle: `POLYFILELib~IInfos8~Elements.html` · Polytec PolyFile Type Library · IInfos8 Collection : Elements Property*

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

*Quelle: `POLYFILELib~IInfos8~Exists.html` · Polytec PolyFile Type Library · IInfos8 Collection : Exists Property*

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

*Quelle: `POLYFILELib~IInfos8~Hardware.html` · Polytec PolyFile Type Library · IInfos8 Collection : Hardware Property*

### Description

Returns the Hardware item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Hardware As IHardware7
```

### Return Type

The Hardware item.


---

## HasAcquisitionInfoModes Property

*Quelle: `POLYFILELib~IInfos8~HasAcquisitionInfoModes.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasAcquisitionInfoModes Property*

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

*Quelle: `POLYFILELib~IInfos8~HasAlignments.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasAlignments Property*

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

*Quelle: `POLYFILELib~IInfos8~HasCameraSettings.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasCameraSettings Property*

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

*Quelle: `POLYFILELib~IInfos8~HasDbReferences.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasDbReferences Property*

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

*Quelle: `POLYFILELib~IInfos8~HasElements.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasElements Property*

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

*Quelle: `POLYFILELib~IInfos8~HasHardware.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasHardware Property*

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

*Quelle: `POLYFILELib~IInfos8~HasMeasPoints.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasMeasPoints Property*

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

*Quelle: `POLYFILELib~IInfos8~HasMeasurementLocations.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasMeasurementLocations Property*

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

*Quelle: `POLYFILELib~IInfos8~HasPositionDevice.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasPositionDevice Property*

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

## HasProfiles Property

*Quelle: `POLYFILELib~IInfos8~HasProfiles.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasProfiles Property*

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

*Quelle: `POLYFILELib~IInfos8~HasScanHeadDevicesInfo.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasScanHeadDevicesInfo Property*

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

## HasTextures Property

*Quelle: `POLYFILELib~IInfos8~HasTextures.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasTextures Property*

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

*Quelle: `POLYFILELib~IInfos8~HasVibrometers.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasVibrometers Property*

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

*Quelle: `POLYFILELib~IInfos8~HasVideoBitmap.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasVideoBitmap Property*

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

*Quelle: `POLYFILELib~IInfos8~HasVideoMappingInfo.html` · Polytec PolyFile Type Library · IInfos8 Collection : HasVideoMappingInfo Property*

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

*Quelle: `POLYFILELib~IInfos8~Item.html` · Polytec PolyFile Type Library · IInfos8 Collection : Item Property*

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

*Quelle: `POLYFILELib~IInfos8~MeasPoints.html` · Polytec PolyFile Type Library · IInfos8 Collection : MeasPoints Property*

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

*Quelle: `POLYFILELib~IInfos8~MeasurementLocations.html` · Polytec PolyFile Type Library · IInfos8 Collection : MeasurementLocations Property*

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

*Quelle: `POLYFILELib~IInfos8~PositionDevice.html` · Polytec PolyFile Type Library · IInfos8 Collection : PositionDevice Property*

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

## Profiles Property

*Quelle: `POLYFILELib~IInfos8~Profiles.html` · Polytec PolyFile Type Library · IInfos8 Collection : Profiles Property*

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

*Quelle: `POLYFILELib~IInfos8~ScanHeadDevicesInfo.html` · Polytec PolyFile Type Library · IInfos8 Collection : ScanHeadDevicesInfo Property*

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

## Textures Property

*Quelle: `POLYFILELib~IInfos8~Textures.html` · Polytec PolyFile Type Library · IInfos8 Collection : Textures Property*

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

*Quelle: `POLYFILELib~IInfos8~Type.html` · Polytec PolyFile Type Library · IInfos8 Collection : Type Property*

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

*Quelle: `POLYFILELib~IInfos8~Vibrometers.html` · Polytec PolyFile Type Library · IInfos8 Collection : Vibrometers Property*

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

*Quelle: `POLYFILELib~IInfos8~VideoBitmap.html` · Polytec PolyFile Type Library · IInfos8 Collection : VideoBitmap Property*

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

*Quelle: `POLYFILELib~IInfos8~VideoMappingInfo.html` · Polytec PolyFile Type Library · IInfos8 Collection : VideoMappingInfo Property*

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
