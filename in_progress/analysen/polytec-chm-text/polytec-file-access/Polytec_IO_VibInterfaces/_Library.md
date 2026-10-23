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
| DecoderInfo | The information about the decoder. |
| FilterSettings | The settings of a filter. Item of the FilterSettingsCollection . |
| FilterSettingsCollection | The collection of the filter settings. |
| QuantitySettings | The settings for a quantity. Item of the QuantitySettingsCollection . |
| QuantitySettingsCollection | The collection of the quantity settings. |
| SensorHeadInfo | The information about the sensor head. |
| SensorHeadSettings | The settings of the sensor head. |
| SensorHeadSettingsCollection | The collection of the sensor head settings. |
| VideoCameraSettings | The settings of the video camera. |

### Interfaces

| Class Module | Description |
|---|---|
| IControllerSettings | The settings of the vibrometer controller. |
| IMaxVelocityRange | Item of the IMaxVelocityRangeCollection Collection . The maximum velocity range of the decoder. |
| IMaxVelocityRangeCollection | The collection of the maximum velocity ranges of the decoder. |
| ISensorHead | The sensor head object allows to control and access information from the sensor head attached to the vibrometer controller. |
| IVideoCamera | The video camera of the sensor head. |

### Public Enumerations

| Enumeration | Description |
|---|---|
| AutoFocusRange | The autofocus range. |
| AutoFocusResult | The result of the autofocus process. |
| CoherenceOptimizerStatusValue | The current status of the coherence optimizer control circuit. |
| ControllerCaps | The capabilities of the controller. |
| FilterType | The type of the filter. |
| FocusLimitState | The limit state of the focus. |
| IlluminationStateType | The illumination state. |
| QuantityType | The type of the quantity. |
| SensitivityState | The sensitivity state of the sensor head. |
| SensorHeadCaps | The capabilities of the sensor head. |
| SensorHeadCaps2 | The extended capabilities of the sensor head. |
| SensorHeadIdentifier | The identifier of the sensor head. |
| SensorHeadTemperatureState | The temperature state of the sensor head. |
| SignalBalanceState | The signal balance state. |
| VibrometerProperty | The property that has changed. |
| VideoCameraCaps | The capabilities of the camera. |
| VideoCameraFormat | The video format of the camera. |


---

## References

*Quelle: `Polytec_IO_VibInterfaces_references.html` · Polytec IO VibInterfaces Type Library*


