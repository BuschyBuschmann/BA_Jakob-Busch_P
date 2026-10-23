# POLYPROPERTIESLib – _Library

## Project Overview

*Quelle: `POLYPROPERTIESLib_P.html` · Polytec PolyProperties Type Library*

### Description

The Polytec PolyProperties type library contains objects describing the data acquisition settings of MPV/PSV/VibSoft measurements.

### Classes

| Class Module | Description |
|---|---|
| AcquisitionPropertiesContainer | Collection of objects of different types representing the respective acquisition properties. |
| AverageAcqPropertiesContainer | Average acquisition properties. Item of the AcquisitionProperties Collection . |
| ChannelAcqPropertiesContainer | Channel acquisition properties. Item of the ChannelsAcqProperties Collection . |
| ChannelsAcqPropertiesContainer | Channels acquisition properties. Member of the AcquisitionProperties collection . |
| CoUIClippingPlaneSettings | The settings for the clipping plane functionality for the 3D view. |
| FastScanAcqPropertiesContainer | FastScan acquisition properties. Item of the FastScans collection . |
| FastScansAcqPropertiesContainer | Collection of the FastScan acquisition properties. Item of the AcquisitionProperties collection . |
| FftAcqPropertiesContainer | The FFT acquisition properties. Item of the AcquisitionProperties collection . |
| FrontEndAcqPropertiesContainer | The acquisition properties of the front end. Item of the AcquisitionProperties collection . |
| GeneralAcqPropertiesContainer | General acquisition properties. Item of the AcquisitonProperties collection . |
| GeneratorAcqPropertiesContainer | The generator acquisition properties. Item of the GeneratorsAcquisitonProperties collection . |
| GeneratorsAcqPropertiesContainer | Generators acquisition properties. Item of the AcquisitionProperties collection . |
| MultiFrameAcqPropertiesContainer | MultiFrame acquisition properties. Item of the AcquistionProperties collection . |
| SEAcqPropertiesContainer | The signal enhancement (SE) acquisition properties. Item of the AcquisitionProperties collection . |
| TimeAcqPropertiesContainer | The time mode acquisition properties. Item of the AcquisitionProperties collection . |
| TriggerAcqPropertiesContainer | The trigger acquisition properties. Item of the AcquisitionProperties Collection . |
| VibrometerAcqPropertiesContainer | The vibrometer acquisition properties. Item of the VibrometersAcqProperties Collection . |
| VibrometersAcqPropertiesContainer | Collection of the Vibrometer acquisition properties. Item of the AcquisitionProperties collection . |
| ZoomFftAcqPropertiesContainer | The Zoom-FFT acquisition properties. Item of the AcquisitionProperties collection . |

### Interfaces

| Class Module | Description |
|---|---|
| IAcquisitionProperties | Collection of objects of different types representing the respective acquisition properties. |
| IAcquisitionProperties3 | Collection of objects of different types representing the respective acquisition properties. |
| IFftAcqPropertiesValidator | The FFT properties validator acts as a validation buffer for FFT acquisition settings before they are committed to the actual acquisition settings. |
| IGeneralAcqProperties5 | General acquisition properties. Item of the AcquisitonProperties collection . |
| IGeneratorAcqProperties4 | The generator acquisition properties. Item of the GeneratorsAcquisitonProperties collection . |
| IGeneratorsAcqProperties4 | Generators acquisition properties. Item of the AcquisitionProperties collection . |
| ITimeAcqPropertiesValidator | The time properties validator acts as a staging/validation buffer for time-domain acquisition settings before they are committed to the actual acquisition settings. |
| ITriggerAcqProperties3 | The trigger acquisition properties. |
| IUIClippingPlaneSettings | The settings for the clipping plane functionality for the 3D view. |
| IVibrometerAcqProperties4 | The vibrometer acquisition properties. Item of the VibrometersAcqProperties Collection . |
| IVibrometerAcqProperties5 | The vibrometer acquisition properties. Item of the VibrometersAcqProperties Collection . |
| IVibrometersAcqProperties4 | Collection of the Vibrometer acquisition properties. Item of the AcquisitionProperties collection . |
| IVibrometersAcqProperties5 | Collection of the Vibrometer acquisition properties. Item of the AcquisitionProperties collection . |

### Public Enumerations

| Enumeration | Description |
|---|---|
| PTCAcqMode | The acquisition mode. |
| PTCAcqPropertiesType | The type of the acquisition properties. |
| PTCAreaCursorType | The type of cursors displayed in a SpectrogramAreaView . |
| PTCAreaShowIndices | Specifies whether the labels (displayed indices) of the scan points are shown. |
| PTCAreaView | The are view mode. |
| PTCAreaViewStyle | The area view style. |
| PTCAverageType | The averaging type. |
| PTCBandWidthExtension | The bandwidth extension for the UHF vibrometer. |
| PTCCameraProjection | The camera projection mode. |
| PTCChannelType | The signal type of the channel. |
| PTCClippingPlane | The supported clipping planes for a clipping of the geometry in the 3D view. |
| PTCColor | The available colors. |
| PTCCursorType | The type of the cursor. |
| PTCEncoderConnectionType | The type of the connection to the encoder. |
| PTCEncoderOperationMode | The operation mode of the encoder. |
| PTCEncoderPowerSupply | The power supply of the encoder. |
| PTCGridStyle | The style of the grid. |
| PTCLengthUnit | The length unit. |
| PTCLineStyle | The line style. |
| PTCMarkerStyle | The marker style. |
| PTCMultiFrameMode | The MultiFame mode. |
| PTCScanRangeStyle | The style for displaying the scan range in the 3D view. |
| PTCSignalDirection | The signal direction displayed in the in the analyzer view. |
| PTCSignalEnhancementMode | The signal enhancement (SE) mode. |
| PTCVibrationDirection | The vibration direction. |
| PTCVideoPlaneStyle | The style for displaying the video planes in the 3D view. |
| PTCViewMode | The view mode of the area view. |
| PTCWindowState | The state of the application window. |

### Public UDTs

| UDT | Description |
|---|---|
| PTSClippingPlaneSetting | The settings for a clipping plane. |
| PTSClippingPlaneSettings | The settings for the clipping plane functionality. |

### Remarks


---

## References

*Quelle: `POLYPROPERTIESLib_references.html` · Polytec PolyProperties Type Library*


