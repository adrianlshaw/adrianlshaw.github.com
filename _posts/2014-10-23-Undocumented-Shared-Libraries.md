---
layout: post
title: Undocumented shared libraries
tags: [linux, tools]
---

Typically I find myself working with some really awkward, undocumented open source libraries. 
Sometimes you don't know there's a static or dynamic library available until you find an option in **configure**.
Thanks to the authors for A) not letting me know in the README about this, and B) providing no information about the exported symbols.

Rest assured, there is another way. I'm making a useful note here so I won't forget and for readers to enjoy.
Exported symbols can be seen thanks to the GNU nm tool. 

```
  nm -D /usr/local/lib/<your_library>.so | grep T | less
```

Now you just need to figure out which header files to use.
