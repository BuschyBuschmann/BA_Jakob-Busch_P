# POLYFILELib – DataDescriptor

## DataDescriptor UDT

*Quelle: `POLYFILELib~DataDescriptor.html` · Polytec PolyFile Type Library*

### Description

Describes the data returned by the Read Method of the DataPointReader Object.

### UDT Members

| Member | Type | Description |
|---|---|---|
| blockIndex | Long | Zero-based block index. |
| dataLength | Long | Length of the data of the block described by this descriptor in the data array returned by the Read Method . |
| dataStartIndex | Long | Zero-based index into the data array returned by the Read Method , marking the start of the data described by this descriptor. |
| displayIndex | Long | Zero-based index into the array of displays passed to the CreateDataPointReaderAsync Method . |
| frameIndex | Long | Zero-based frame index. |
| frameStart | Long | Zero-based frame start index. |
| scanPointIndex | Long | Zero-based scan point index. |
| startIndex | Long | Zero-bases start index. |

### Example
