# PSV – PTCScanCaps

## PTCScanCaps Enumeration

*Quelle: `PSV~PTCScanCaps.html` · Polytec PSV Type Library*

### Description

The capabilities for a scan.

### Members

| Member | Value | Description |
|---|---|---|
| ptcScanCapsAsynchronousScanEvent | 16 | When passing this flag, the scan-progress/completion events are fired. asynchronously. On VibroScan systems this allows the software to use the faster, autonomous scan mode. In this case, you cannot rely on e.g. getting the current values of the scanner angles or being able to modify those before progressing to the next scan point, because the scan is performed asynchronously by the VibroScan system. |
| ptcScanCapsAutoFocusDuringScan | 8 | The autofocusing will be performed during the scan. |
| ptcScanCapsNone | 0 | No capabilities. |
| ptcScanCapsUseAssignedFocusValuesDuringScan | 1 | The assigned focus values will be used during the scan. |
| ptcScanCapsVideoTriangulation | 2 | The video triangulation will be performed during the scan. |
| ptcScanCapsVideoTriangulationFast | 4 | The fast video triangulation will be performed during the scan. |

### Remarks

ptcScanCapsVideoTriangulationFast is not supported anymore.
