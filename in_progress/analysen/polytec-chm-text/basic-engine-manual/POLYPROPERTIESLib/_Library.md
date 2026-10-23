# POLYPROPERTIESLib – _Library

## Project Overview

*Quelle: `POLYPROPERTIESLib_P.html` · Polytec PolyProperties Type Library*

### Description

The Polytec PolyProperties type library contains objects describing the data acquisition settings of MPV/PSV/VibSoft measurements.

### Classes

| Class Module | Description |
|---|---|
| AcquisitionPropertiesContainer | Collection of objects of different types representing the respective acquisition properties. |
| AnalyzerPinSettings | The settings for pinning analyzer view settings to other open analyzer views. |
| AnalyzerViewSettings | User interface settings of an analyzer view. |
| AreaCursorSettings | The settings of the area cursor. |
| AreaPinSettings | The settings for pinning area view settings to other open area views. |
| AreaViewSettings | User interface settings of an area view. |
| AverageAcqPropertiesContainer | Average acquisition properties. Item of the AcquisitionProperties Collection . |
| ChannelAcqPropertiesContainer | Channel acquisition properties. Item of the ChannelsAcqProperties Collection . |
| ChannelsAcqPropertiesContainer | Channels acquisition properties. Member of the AcquisitionProperties collection . |
| CoUIClippingPlaneSettings | The settings for the clipping plane functionality for the 3D view. |
| DisplaySettings | User interface settings for the kind of data to display in an AnalyzerView or AreaView . |
| DoubleCursorSettings | The settings of the double cursor. |
| FastScanAcqPropertiesContainer | FastScan acquisition properties. Item of the FastScans collection . |
| FastScansAcqPropertiesContainer | Collection of the FastScan acquisition properties. Item of the AcquisitionProperties collection . |
| FftAcqPropertiesContainer | The FFT acquisition properties. Item of the AcquisitionProperties collection . |
| FrontEndAcqPropertiesContainer | The acquisition properties of the front end. Item of the AcquisitionProperties collection . |
| GeneralAcqPropertiesContainer | General acquisition properties. Item of the AcquisitonProperties collection . |
| GeneratorAcqPropertiesContainer | The generator acquisition properties. Item of the GeneratorsAcquisitonProperties collection . |
| GeneratorsAcqPropertiesContainer | Generators acquisition properties. Item of the AcquisitionProperties collection . |
| HarmonicCursorSettings | The settings of the harmonic cursor. |
| LineSettings | The settings of a line of a graph of an AnalyzerView . Member of the LineSettingsCollection . |
| LineSettingsColl | Collection of LineSettings objects. |
| MultiFrameAcqPropertiesContainer | MultiFrame acquisition properties. Item of the AcquistionProperties collection . |
| PeakCursorSettings | The settings of the peak (band) cursor. |
| RangeSettings | User interface settings of an axis range of an AnalyzerView or SpectrogramAreaView . |
| RangeSettingsColl | Collection of RangeSettings objects. |
| SEAcqPropertiesContainer | The signal enhancement (SE) acquisition properties. Item of the AcquisitionProperties collection . |
| SigProAnalyzerViewSettings | User interface settings of an analyzer view of a signal processor window . The object is derived from the AnalyzerViewSettings object . |
| SingleCursorSettings | The settings of the single cursor. |
| SpectrogramAnalyzerViewSettings | User interface settings of an analyzer view of a spectrogram or Campbell diagram. |
| SpectrogramAreaViewSettings | User interface settings of an area view of a spectrogram or Campbell diagram. |
| TimeAcqPropertiesContainer | The time mode acquisition properties. Item of the AcquisitionProperties collection . |
| TriggerAcqPropertiesContainer | The trigger acquisition properties. Item of the AcquisitionProperties Collection . |
| UICameraSettings | The settings of the virtual camera that is used for the 3D view. |
| VibrometerAcqPropertiesContainer | The vibrometer acquisition properties. Item of the VibrometersAcqProperties Collection . |
| VibrometersAcqPropertiesContainer | Collection of the Vibrometer acquisition properties. Item of the AcquisitionProperties collection . |
| WindowSettings | User interface settings of a window. |
| ZoomFftAcqPropertiesContainer | The Zoom-FFT acquisition properties. Item of the AcquisitionProperties collection . |

### Interfaces

| Class Module | Description |
|---|---|
| IAcquisitionProperties3 | Collection of objects of different types representing the respective acquisition properties. |
| IAnalyzerPinSettings2 | The settings for pinning analyzer view settings to other open analyzer views. |
| IAnalyzerViewSettings4 | User interface settings of an analyzer view. |
| IAreaPinSettings2 | The settings for pinning area view settings to other open area views. |
| IAreaViewSettings5 | User interface settings of an area view. |
| IDataCursorSettings | The settings of a data cursor . This interface is implemented by the DoubleCursorSettings object , the HarmonicCursorSettings object , the PeakCursorSettings object and the SingleCursorSettings object . |
| IFftAcqPropertiesValidator | The FFT properties validator acts as a validation buffer for FFT acquisition settings before they are committed to the actual acquisition settings. |
| IGeneralAcqProperties5 | General acquisition properties. Item of the AcquisitonProperties collection . |
| IGeneratorsAcqProperties4 | Generators acquisition properties. Item of the AcquisitionProperties collection . |
| ISpectrogramAreaViewSettings | It is recommended to cast to the SpectrogramAreaViewSettings Object . |
| ITimeAcqPropertiesValidator | The time properties validator acts as a staging/validation buffer for time-domain acquisition settings before they are committed to the actual acquisition settings. |
| ITriggerAcqProperties3 | The trigger acquisition properties. |
| IUICameraSettings | It is recommended to cast to the UICameraSettings Object . |
| IUISettings | Base interface for user interface settings. Several other classes are derived from this interface: WindowSettings , AnalyzerViewSettings , SigProAnalyzerViewSettings , AreaViewSettings , DisplaySettings , LineSettingsCollection , LineSettings , RangeSettingsCollection , RangeSettings , UICameraSettings , DataCursorSettings , CoUIClippingPlaneSettings , SpectrogramAnalyzerViewSettings , SpectrogramAreaViewSettings . |
| IWindowSettings | User interface settings of a window. |

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


