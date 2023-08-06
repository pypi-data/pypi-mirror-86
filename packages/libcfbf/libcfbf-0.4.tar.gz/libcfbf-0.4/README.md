# libcfbf
libcfbf is a Python implementation of Microsoft's Compound File Binary Format. Note this library does not have support for writing or modifying documents.

```python
from libcfbf import CfbfDocument

with CfbfDocument.open('foo.doc') as document:
    for x in document.root_entry.children:
        print(x.entry_name)
```

Specification:
https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/53989ce4-7b05-4f8d-829b-d08d6148375b
