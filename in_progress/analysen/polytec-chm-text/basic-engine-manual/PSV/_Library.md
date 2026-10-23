# PSV – _Library

## Project Overview

*Quelle: `PSV_P.html` · Polytec PSV Type Library*

### Description

The Polytec PSV and VibSoft type libraries contain objects to control and access information about the respective application.

### Classes

| Class Module | Description |
|---|---|
| AcqModeProperties | The AcqModeProperties is a collection of AcquisitionProperities objects. It contains an AcquisitionProperties object for every acquisition mode. |
| Acquisition | The Acquisition object controls the hardware and data acquisition of PSV and VibSoft. |
| AcquisitionInstance | The AcquisitionInstance object represents the instance of the PSV application that runs in acquisition mode. |
| AcquisitionProperties | A typed collection of objects representing the respective acquisition properties. |
| AlignmentsAcq | Item of the InfosAcq collection . It contains the definition of 2D and 3D alignment objects. |
| AnalyzerView | The object representing the analyzer view pane of the analyzer window or area window. |
| AnalyzerWindow | The window for single point vibration data documents. Derived from the Window object . |
| Application | The object representing the application (PSV or VibSoft). |
| AreaCursor | The values of the current area cursor. |
| AreaView | The object for the area view pane of the AreaWindow . |
| AreaWindow | The window object for documents with vibration data of scans. Derived from the Window object . |
| AverageAcqProperties | Average acquisition properties. Item of the AcquisitionProperties Collection . |
| ChannelAcqProperties | Channel acquisition properties. Item of the ChannelsAcqProperties collection . |
| ChannelsAcqProperties | Channels acquisition properties. Member of the AcquisitionProperties collection . |
| DataCursor | Base object for the cursor objects: SingleCursor , DoubleCursor , HarmonicCursor and PeakCursor . |
| DigitalPort | Represents a digital i/o port of the PSV or VibSoft junction box (Aux In/Aux Out). |
| DigitalPorts | Collection of the available digital ports of the system. |
| Document | The document class is the base object of documents of different types: VibDocument for files containing vibration data and SigProDocument for the signal processor documents. |
| Documents | The collection of documents. |
| DoubleCursor | Object representing the current values of the double cursor. Derived from DataCursor . |
| Exporter | The Exporter object allows to export geometry and measurement data from a .pvd, .svd , .mvd or .set file to one of the supported file formats. |
| ExportParameters | The export parameters. |
| FastScanAcqProperties | FastScan acquisition properties. Item of the FastScans collection . |
| FastScansAcqProperties | Collection of FastScan acquisition properties. Item of the AcquisitionProperties collection . |
| FftAcqProperties | The FFT acquisition properties. Item of the AcquisitionProperties collection . |
| FrontEndAcqProperties | The acquisition properties of the front end. Item of the AcquisitionProperties collection . |
| GeneralAcqProperties | General acquisition properties. Item of the AcquisitonProperties collection . |
| GeneratorAcqProperties | The generator acquisition properties. Item of the GeneratorsAcquisitonProperties collection . |
| GeneratorsAcqProperties | Generators acquisition properties. Item of the AcquisitionProperties collection . |
| HardwareAcq | Item of the InfosAcq collection describing the hardware of the system. |
| HarmonicCursor | Object representing the current values of the harmonic cursor. Derived from BaseCursor . |
| InfosAcq | Named and typed collection holding items of different type that are derived from Info . |
| MultiFrameAcqProperties | MultiFrame acquisition properties. Item of the AcquisitionProperties collection . |
| PeakCursor | Object representing the current values of the peak cursor. Derived from DataCursor . |
| PointMarker | A point marker that is used to track position changes of the measurement object. |
| PointMarkers | A collection of point markers. |
| PositionDevice | The object controls the XY, Z or XYZ position device of the system. |
| PositioningStage | Item of the InfosAcq collection . The positioning stage object allows to control the x/y positioning stage that is optionally connected to MSA systems. |
| PresentationInstance | The PresentationInstance object represents the instance of the PSV application that runs in presentation mode. |
| PTCTimer | The PTCTimer object can be used to perform periodic tasks. |
| ScanHeadDevicesInfoAcq | Item of the InfosAcq collection . Contains information about the scanning head used for PSV measurement. Available in PSV files only. |
| SEAcqProperties | The signal enhancement (SE) acquisition properties. Item of the AcquisitionProperties collection . |
| Settings | The settings object that represents the current application settings (A/D Settings, scan point definition, camera and alignment, and window layout). |
| SigProAnalyzerView | The object for the analyzer view pane of the signal processor window . |
| SigProDocument | The document object for signal processor files. Derived from the Document object . |
| SigProWindow | The window object for signal processor documents. Derived from the Window object . |
| SingleCursor | Object representing the current values of the single cursor. Derived from the DataCursor Object . |
| SpectrogramAreaView | The object for the area view pane of the SpectrogramWindow Object . |
| SpectrogramWindow | The window object for documents with spectrograms or Campbell diagrams. Derived from the Window object . |
| TimeAcqProperties | The time mode acquisition properties. Item of the AcquisitionProperties collection . |
| TriggerAcqProperties | The trigger acquisition properties. Item of the AcquisitionProperties collection . |
| VibDocument | The document object for files containing vibration data. Derived from the Document object . |
| VibrometerAcqProperties | The vibrometer acquisition properties. Item of the VibrometersAcqProperties Collection . |
| VibrometerGroups | The collection of vibrometer controller groups. Item of the InfosAcq collection . |
| VibrometersAcqProperties | Collection of the Vibrometer acquisition properties. Item of the AcquisitionProperties collection . |
| Window | Item of the Windows collection . The window object is the base object of windows of different types: AnalyzerWindow for documents containing single point vibration data, AreaWindow for documents containing scans of vibration data and SigProWindow for the signal processor documents. |
| Windows | The collection of the windows. |
| ZoomFftAcqProperties | The Zoom-FFT acquisition properties. Item of the AcquisitionProperties collection . |

### Interfaces

| Class Module | Description |
|---|---|
| IApplication5 | The object representing the application (PSV or VibSoft). |
| IExporter | The exporter. |
| IPointData | The point data. |

### Public Enumerations

| Enumeration | Description |
|---|---|
| PTCAcqStartMode | The mode of the single point measurement. |
| PTCAcqState | The state of the acquisition. |
| PTCApplicationMode | The application mode. |
| PTCArrangeStyle | The arrange window style. |
| PTCAssignFocusAutomaticallyCaps | Specifies how the software executes the assign focus values automatically command. |
| PTCDigitalPort | The type of the digital i/o port. |
| PTCDigitalPortType | The type of the digital i/o port. |
| PTCDocumentType | The type of the document. |
| PTCExportType | The type of the export file. |
| PTCFileFormat | The file format. |
| PTCGeometryScanCaps | Specifies how the software performs a geometry scan. |
| PTCMessageAnswer | The answer to the message box. |
| PTCMessageStyle | The style of the message box. |
| PTCPrintOptions | The printing options. |
| PTCScanCaps | The capabilities for a scan. |
| PTCScanMode | The mode of the scan. |
| PTCScanState | The scan state. |
| PTCSettings | The type of the settings. |
| PTCSnapshotType | The type of the snapshot. |
| PTCViewSelection | The type of the view selection. |
| PTCWarningLevel | The warning level of the application. |
| PTCWindowType | The type of the window. |


---

## References

*Quelle: `PSV_references.html` · Polytec PSV Type Library*


