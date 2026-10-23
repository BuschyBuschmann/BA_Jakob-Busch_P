# PSV – PTCScanMode

## PTCScanMode Enumeration

*Quelle: `PSV~PTCScanMode.html` · Polytec PSV Type Library*

### Description

The mode of the scan.

### Members

| Member | Value | Description |
|---|---|---|
| ptcScanAll | 0 | Starts a complete scan of all measurement points. |
| ptcScanContinue | 1 | Continues a previously started scan. |
| ptcScanRemeasure | 2 | Starts a re-measurement of a previously started scan. |
| ptcScanRemeasureAutoRange | 3 | Starts a re-measurement of a previously started scan with automatic adjustment of the vibrometer range for scan points with scan status overrange. |
| ptcScanRemeasureFile | 4 | Starts a re-measurement of the scan file specified in the ScanFileName Property . |
