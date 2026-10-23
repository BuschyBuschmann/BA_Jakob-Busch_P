# Polytec_IO_VibInterfaces – _Library

## Project Overview

*Quelle: `Polytec_IO_VibInterfaces_P.html` · Polytec IO VibInterfaces Type Library*

### Description

The Polytec.IO.VibInterfaces type library contains objects to access information about the vibrometer controller that was used during data acquisition with the MPV/PSV/VibSoft system and its settings.

To access the corresponding objects, navigate to the VibrometersAcqPropertiesContainer Collection of the active AcquisitionPropertiesContainer Collection. The following example shows how to access the laser wavelength of the Vibrometer that was used for a measurement opened in the corresponding PolyFile Object.

*Access to laser wavelength of the Vibrometer used for the measuremt:*
```
Dim oVibrometerAcqProperties As VibrometerAcqProperties
oVibrometerAcqProperties = oFile.Infos.AcquisitionInfoModes.ActiveProperties.VibrometersProperties(1)
Debug.Print oVibrometerAcqProperties.VibControllerSettings.SensorHeadSettingsCollection(0).SensorHeadInfo.LaserWavelength
```

Please note that the indices into the VibrometersAcqPropertiesContainer Collection are 1-based, whereas the indices into the SensorHeadSettingsCollection Collection are 0-based.

In MPV/PSV/VibSoft the objects allow you to specify the settings of the vibrometers attached to the system. Moreover, you can e.g. query the current signal level or overrange status of the vibrometers.

*Access to signal level of connected Vibrometer:*
```
Dim oInfosAcq As InfosAcq
oInfosAcq = Acquisition.Infos
Debug.Print oInfosAcq.Vibrometers(1).Controllers(0).SensorHeads(0).SignalLevel
```

MPV/PSV/VibSoft support up to two groups of Vibrometer controllers attached to the system. For a 3D system the first group contains three Vibrometers. The signal level of the first sensor head of the first controller of the first Vibrometer group is printed.

Please note that the Vibrometers collection uses 1-based indices, the Controllers and SensorHeads collections use 0-based indices.Type your Note Box content here.

### Classes

| Class Module | Description |
|---|---|
| ControllerInfo | The information about the controller. |
| ControllerSettings | The settings of the vibrometer controller. |
| DecoderClearMode | Item of the DecoderClearModeCollection Collection . Represents a mode for clearing displacement decoder offsets. |
| DecoderClearModeCollection | The collection of the decoder clear modes the controller supports. |
| DecoderInfo | The information about the decoder. |
| FilterSettings | The settings of a filter. Item of the FilterSettingsCollection . |
| FilterSettingsCollection | The collection of the filter settings. |
| GroupControllerUnitInfo | Provides summary information about the group controller unit. |
| GroupLaserUnitInfo | Provides summary information about the group laser unit. |
| OverrunMode | Item of the OverrunModeCollection Collection . The overrun mode of the decoder. |
| OverrunModeCollection | The collection of the overrun modes. |
| QuantitySettings | The settings for a quantity. Item of the QuantitySettingsCollection . |
| QuantitySettingsCollection | The collection of the quantity settings. |
| SensorHeadInfo | The information about the sensor head. |
| SensorHeadSettings | The settings of the sensor head. |
| SensorHeadSettingsCollection | The collection of the sensor head settings. |
| VideoCameraSettings | The settings of the video camera. |

### Interfaces

| Class Module | Description |
|---|---|
| IAdaptiveFilterRange | The range of an adaptive filter. This object is derived from the IBaseFilterRange interface . |
| IBandwidthRange | The bandwidth range of the decoder. |
| IBandwidthRangeCollection | The collection of the bandwidth ranges of the decoder. |
| IBaseFilterRange | The base object for the filter ranges. Item of the IBaseFilterRangeCollection . |
| IBaseFilterRangeCollection | The collection of the filter ranges of a filter. |
| IConnectionInfo | The information about the connection of the controller. |
| IController | The vibrometer controller. Item of the IControllerCollection . |
| IControllerBase | The base interface of the IController Interface and the IControllerGroup Interface . |
| IControllerCollection | The collection of the controllers. |
| IControllerGroup | A group of vibrometer controllers. |
| IControllerSettings | The settings of the vibrometer controller. |
| IDCResponseFilterRange | The range of the DC response filter. This object is derived from the IBaseFilterRange object . |
| IDecoder | The decoder of a controller. Item of the IDecoderCollection . |
| IDecoderCollection | The collection of the decoders of the vibrometer controller. |
| IDecoderRange | The range of a decoder. Item of the IDecoderRangeCollection . |
| IDecoderRangeCollection | The collection of the decoder ranges. |
| IDigitalDemodulation | The digital demodulation object gives access to the digital demodulation of the controller. |
| IFilter | One of the filters of the vibrometer controller. Item of the IFilterCollection . |
| IFilterCollection | The collection of the filters of the vibrometer controller. |
| IFilterRange | The range of a filter. This object is derived from the IBaseFilterRange object . |
| IGroupControllerUnit | This interface is provided for the MPV system , e.g. for the case where one hardware controller unit is used for all sensor heads/sondes of the controller group. Thus, some commands are only available for such unit and are not supported for the individual controller units. In particular, please note that this interface is not used to group individual controller units. |
| IGroupControllerUnitInfo | Provides summary information about the group controller unit. |
| IGroupLaserUnit | This interface is provided for MPV, e.g. for the case where one laser unit is used for all sensor head lasers of the controller group. Thus, some commands are only available for such unit and are not supported for the individual sensor head laser units. In particular, please note that this interface is not used to group individual sensor head laser units. |
| IGroupLaserUnitInfo | Provides summary information about the group laser unit. |
| IMaxVelocityRange | Item of the IMaxVelocityRangeCollection Collection . The maximum velocity range of the decoder. |
| IMaxVelocityRangeCollection | The collection of the maximum velocity ranges of the decoder. |
| IMeasurementModeInfo | The information about the measurement mode of the controller. |
| IPowerUp | The IPowerUp object provides access to the power up functionality of the vibrometer controller. |
| IQuantity | The quantity of the decoder. Item of the IQuantityCollection . |
| IQuantityCollection | The collection of quantities of the controller. |
| IRecorder | The recorder mode, e.g. of a VGO-200. |
| ISensorHead | The sensor head object allows to control and access information from the sensor head attached to the vibrometer controller. |
| ISensorHeadCollection | The collection of the sensor heads of the controller. |
| IServiceMode | The service mode object allows to control and access the service mode of the vibrometer controller. |
| ISignalEnhancement | The signal enhancement of the controller. |
| ITrackingFilter | The tracking filter. This object is derived from the IFilter Object . |
| ITrackingFilterRange | The range of the tacking filter. This object is derived from the IBaseFilterRange object . |
| IVideoCamera | The video camera of the sensor head. |

### Public Enumerations

| Enumeration | Description |
|---|---|
| AutoFocusRange | The autofocus range. |
| AutoFocusResult | The result of the autofocus process. |
| CoherenceOptimizerStatusValue | The current status of the coherence optimizer control circuit. |
| ConnectionMode | The connection mode. |
| ConnectionType | The type of the connection to the vibrometer controller. |
| ControllerCaps | The capabilities of the controller. |
| DCResponseFilterMode | The mode of the DC response filter. |
| DecoderCaps | The capabilities of the decoder. |
| DecoderMeasurementMode | The measurement modes of the decoder. |
| DecoderOutputMode | The output mode of the decoder. |
| DigitalDemodulationMode | The mode of the digital demodulation. |
| FilterCaps | The capabilities of the filter. |
| FilterType | The type of the filter. |
| FocusLimitState | The limit state of the focus. |
| GroupControllerUnitCaps | This enumeration is provided for MPV, e.g. for the case where one hardware controller unit is used for all sensor heads/sondes of the controller group. Thus, some capabilities are only available for such unit and are not supported for a single controller object. |
| GroupLaserUnitCaps | This enumeration is provided for the MPV system , e.g. for the case where one laser unit is used for all sensor heads/sondes of the controller group. Thus, some capabilities are only available for such unit and are not supported for the individual controller units. |
| IlluminationStateType | The illumination state. |
| ImpedanceType | The impedance type of the decoder. |
| MeasurementModeCaps | The capabilities of the measurement mode. |
| MeasurementModeType | The measurement mode of the controller. |
| PowerUpCaps | The capabilities of the power up mode. |
| PowerUPMode | The power up mode. |
| QuantityCaps | The capabilities of the quantity. |
| QuantityType | The type of the quantity. |
| SensitivityState | The sensitivity state of the sensor head. |
| SensorHeadCaps | The capabilities of the sensor head. |
| SensorHeadCaps2 | The extended capabilities of the sensor head. |
| SensorHeadIdentifier | The identifier of the sensor head. |
| SensorHeadTemperatureState | The temperature state of the sensor head. |
| ServiceCaps | The capabilities of the service mode. |
| ServiceTemperatureState | The state of the internal temperature. |
| ServiceTestSignal | The state of the service mode test signal. |
| SignalBalanceState | The signal balance state. |
| SignalEnhancementModeType | The signal enhancement mode of the controller. |
| TrackingFilterMode | The mode of the tracking filter. |
| TrackingFilterSeekRangeMode | The seek range mode of the tracking filter. |
| VibrometerProperty | The property that has changed. |
| VideoCameraCaps | The capabilities of the camera. |
| VideoCameraFormat | The video format of the camera. |


---

## References

*Quelle: `Polytec_IO_VibInterfaces_references.html` · Polytec IO VibInterfaces Type Library*


