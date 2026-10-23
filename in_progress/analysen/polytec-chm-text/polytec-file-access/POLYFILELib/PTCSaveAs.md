# POLYFILELib – PTCSaveAs

## PTCSaveAs Enumeration

*Quelle: `POLYFILELib~PTCSaveAs.html` · Polytec PolyFile Type Library*

### Description

Using the PTCSaveAs enumeration you can control what is copied to the destination file in the SaveAs and SaveAsEx methods.

### Members

| Member | Value | Description |
|---|---|---|
| ptcSaveAsAll | 0 | Save the complete file. Deprecated, see remarks. |
| ptcSaveAsAverageSpectrum | 3 | Save the average spectrum of a PSV scan file. Note that GetData or GetDataSection of such a file return the uncorrected average spectrum only. |
| ptcSaveAsBands | 1 | Save bands of a PSV scan file. Deprecated, see remarks. |
| ptcSaveAsSinglePoint | 2 | Save single measurement point data of a PSV scan file - specify the point index. Deprecated, see remarks. |
| ptcSaveAsTypeAll | 508 | Save the complete file. |
| ptcSaveAsTypeAllNoOriginal | 420 | Save the complete file with the user-defined data excluding the original single point and average spectrum data. |
| ptcSaveAsTypeAllNoSinglePoint | 460 | Save the complete file with the user-defined data excluding the original single point but including the average spectrum data. |
| ptcSaveAsTypeAllNoUser | 92 | Save the complete file excluding the user-defined data. |
| ptcSaveAsTypeAverageSpectrum | 64 | Save the average spectrum of a PSV scan file. |
| ptcSaveAsTypeAverageSpectrumUser | 128 | Save user data for the average spectrum of a PSV scan file. |
| ptcSaveAsTypeBands | 8 | Save bands only. |
| ptcSaveAsTypeBandsUser | 256 | Save user-defined bands. |
| ptcSaveAsTypeInfos | 4 | Save Infos only (as a Settings file if no other option is selected). |
| ptcSaveAsTypeSinglePoint | 16 | Save single measurement point data of a MPV/PSV measurement file  specify a valid point index. |
| ptcSaveAsTypeSinglePointUser | 32 | Save user data for a single measurement point of a MPV/PSV measurement file  specify a valid point index. |

### Remarks

Either use one of the first four constants or a combination of the following constants. New code should use the constants starting with ptcSaveAsTypeInfos.
