# POLYFILELib – _Library

## Project Overview

*Quelle: `POLYFILELib_P.html` · Polytec PolyFile Type Library*

### Description

The Polytec PolyFile type library contains objects to open, read, modify, save and create Polytec files (MPV/PSV measurement files, VibSoft single point files, MPV/PSV/VibSoft settings files).

### Object Model

### Classes

| Class Module | Description |
|---|---|
| AcquisitionInfoModes | Item of the Infos collection . Typed collection of AcquisitionProperties . Contains the acquisition properties for the various acquisition modes. |
| Alignments | Item of the Infos collection . It contains 2D, 3D, and camera alignment objects. |
| BandDomain | Item of the BandDomains collection . |
| BandDomains | Named and typed collection of the available domains of the band data. |
| CameraSettings | Item of the Infos collection. |
| CameraSize | Size of a camera chip used for objective calibrations. |
| ContainedFile | Item of the ContainedFiles collection. It refers to one of the single files building a combined file. |
| ContainedFiles | Named collection of the ContainedFile objects. |
| DataBand | Item of the DataBands collection. |
| DataBands | Named collection of the data bands. |
| DataPoint | Item of the DataPoints collection . |
| DataPointReader | The data point reader allows to read data in large chunks, e.g. for several displays, scan points or frames at once. |
| DataPoints | Standard collection of the DataPoint objects. |
| DbReferences | Item of the Infos collection and the Preferences collection . Typed collection of Double. Contains the dB references for the various physical quantities. |
| Element | Item of the Elements collection . One geometrical element of the scan point geometry. An element is a polygon connecting scan measurement points. |
| Elements | Item of the Infos collection . Standard collection of Element objects. Elements represent the surface elements connecting the scan points. They are used for the graphical display of scan data in MPV/PSV. Available in MPV/PSV files only. |
| GeometryComponent | Component of the geometry. A hierarchy of components where each component can have a set of measurement points attached to it. |
| GeometryComponents | Collection of GeometryComponent objects. |
| Hardware | Item of the Infos collection . The hardware object contains information about the acquisition board and front end of the MPV/PSV/VibSoft system used to create the file. |
| IInfos8 | IInfos8 Interface |
| Info | Info is the base object of all objects returned by the Infos collection . This object is not directly accessible. |
| Infos | Named and typed collection holding items of different type that are derived from Info . |
| ITexture | ITexture Interface |
| ITextures | ITextures Interface |
| LensCalibration | Calibration of the objective of an MSV or MSA system. Item of the LensCalibrations collection . |
| LensCalibrations | Collection of LensCalibration objects. |
| MeasPoint | Item of the MeasPoints collection . The MeasPoint object contains properties of a measurement point (scan point) of a MPV/PSV measurement file or settings file. |
| MeasPoints | Item of the Infos collection . Standard collection of the measurement points. Available in MPV/PSV files only. |
| MeasurementLocation | Item of the MeasurementsLocations collection . The MeasurementLocation object contains the properties of the measurement location of a measurement point (scan point). |
| MeasurementLocations | Item of the Infos collection . Standard collection of the measurement locations. |
| PointAverageDomain | Item of the PointAverageDomains collection . A domain of the point average data. |
| PointAverageDomains | Named and typed collection of the available domains of the point average data. |
| PointDomain | Item of the PointDomains collection . One domain of the point data. |
| PointDomains | Named and typed collection of the available domains of the point data. |
| PolyFile | The PolyFile object represents a Polytec file. |
| Preferences | Preferences is a named and typed collection holding items of different type. |
| Profile | Item of the Profiles collection. |
| Profiles | Collection of Profile objects to hold all the profiles in a file. Member of the Infos collection . |
| ScanHeadDevicesInfo | Item of the Infos collection . Contains information about the scanning head used for PSV measurement. Available in PSV files only. |
| SpectrogramInfo | Item of the Infos Collection . Contains information about the parameters for a spectrogram or Campbell diagram that can be calculated from time traces. |
| SummaryInfo | The properties of the summery info are standard properties of a file in the Microsoft® Windows® compound file format. The properties can be displayed in the Windows® explorer. |
| Texture | Item of the Textures Collection . The Texture object represents a texture of an imported geometry. |
| Textures | Item of the Infos collection . Standard collection of the textures of an imported geometry. |
| Version | The version object contains properties for general version information of the file. |
| VideoBitmap | Item of the Infos collection . The VideoBitmap object allows to retrieve and set the video image used for MPV/PSV measurement files. |
| VideoMappingInfo | Item of the Infos collection . Contains information of mapping the video image to distances on the measurement object for MSA and MSV systems. |
| XAxis | Contains information about the x-axis for the data returned by GetData(). |
| YAxes | Collection that contains information about the y-axes used to display the data returned by GetData. For combined displays as e.g. ptcDisplayMagPhase or ptcDisplayRealImag YAxes contains two items of type YAxis one for each part of the data. |
| YAxis | Contains information about the y-axis used to display the data returned by GetData. Item of the YAxes collection. |

### Interfaces

| Class Module | Description |
|---|---|
| IAcquisitionInfoModes3 | Item of the Infos collection . Typed collection of AcquisitionProperties . Contains the acquisition properties for the various acquisition modes. |
| IAlignments2 | Item of the Infos collection . It contains 2D and 3D alignment objects. |
| IBandDomain | Item of the BandDomains collection . |
| ICameraSettings | Item of the Infos collection. |
| IDataBand | Item of the DataBands collection . |
| IDataBands | Named collection of the data bands. |
| IDbReferences2 | Item of the Infos collection and the Preferences collection . Typed collection of Double. Contains the dB references for the various physical quantities. |
| IElements3 | Item of the Infos collection . Standard collection of Element objects. Elements represent the surface elements connecting the scan points. They are used for the graphical display of scan data in MPV/PSV. Available in MPV/PSV files only. |
| IHardware3 | Item of the Infos collection . The hardware object contains information about the acquisition board and front end of the MPV/PSV/VibSoft system used to create the file. |
| IHardware7 | Item of the Infos collection . The hardware object contains information about the acquisition board and front end of the MPV/PSV/VibSoft system used to create the file. |
| IInfos2 | Infos is a named and typed collection holding items of different type that are derived from Info . |
| ILensCalibration | ILensCalibration Interface |
| ILensCalibrations | ILensCalibrations Interface |
| IMeasPoint11 | IMeasPoint11 Interface |
| IMeasPoint8 | Item of the MeasPoints collection . The MeasPoint object contains properties of a measurement point (scan point) of a MPV/PSV measurement file or settings file. |
| IMeasPoint9 | IMeasPoint9 Interface |
| IMeasPoints11 | IMeasPoints11 Interface |
| IMeasurementLocations2 | Standard collection of the measurement locations. |
| IPolyFile8 | The PolyFile object represents a Polytec file. |
| IPositionDevice | The object controls the XY, Z or XYZ position device of the system. |
| IPositioningStage | The positioning stage object allows to control the x/y positioning stage that is optionally connected to MSA systems. |
| IPreferences | IPreferences Interface |
| IProfile | Item of the Profiles collection. |
| IProfiles | Collection of Profile objects to hold all the profiles in a file. Member of the Infos collection . |
| ISummaryInfo2 | ISummaryInfo2 Interface |
| IVersion2 | IVersion2 Interface |
| IVibrometerGroups | The collection of vibrometer controller groups. |
| IVideoBitmap5 | Item of the Infos collection . The VideoBitmap object allows to retrieve and set the video image used for MPV/PSV measurement files. |
| IVideoMappingInfo3 | Item of the Infos Collection . Contains information of mapping the video image to distances on the measurement object for MSA and MSV systems. |
| IXAxis | Contains information about the x-axis for the data returned by GetData(). |
| IYAxes | Collection that contains information about the y-axes used to display the data returned by GetData. For combined displays as e.g. ptcDisplayMagPhase or ptcDisplayRealImag YAxes contains two items of type YAxis one for each part of the data. |
| IYAxis | Contains information about the y-axis used to display the data returned by GetData. Item of the YAxes collection. |

### Public Enumerations

| Enumeration | Description |
|---|---|
| PTCContainedCaps | Type of relation of a contained file with the combined file. |
| PTCCreateFlags | The create flags. |
| PTCFileID | Type of the Polytec file. |
| PTCFocusStatus | Focus status of a scan point. The status can be a combination of several bit constants defined in the enumeration. |
| PTCGeometryStatus | Geometry status of a scan point. The status can be a combination of several bit constants defined in the enumeration. |
| PTCGraphicFormatType | The graphic format. |
| PTCLensCalibrationCapsType | Specifies the capabilities of an objective in an objective calibration . |
| PTCMeasurementLocationMode | The possible measurement location modes. |
| PTCPathLengthStatus | The status of the optical path length value for the MSA-650. |
| PTCProfileType | Describes the type of Profile in the Profiles collection . |
| PTCSaveAs | Using the PTCSaveAs enumeration you can control what is copied to the destination file in the SaveAs and SaveAsEx methods. |
| PTCScanStatus | Scan status of a scan point. The status can be a combination of several bit constants defined in the enumeration. |

### Public UDTs

| UDT | Description |
|---|---|
| DataDescriptor | Describes the data returned by the Read Method of the DataPointReader Object . |


---

## References

*Quelle: `POLYFILELib_references.html` · Polytec PolyFile Type Library*


