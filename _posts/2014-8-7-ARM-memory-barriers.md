---
layout: post
title: ARM memory barriers 
---

Unlike on certain x86 memory models, the latest ARM processors (at least v6 onwards) do not provide any guarantees for order of writes
to memory. At first that may sound a little disconcerting, but by not providing such guarantees certain interesting 
optimisations can be made when it comes to power consumption. In this scenario more opportunities are presented for 
optimising the pipeline model. However, to prevent potentially abnormal program behaviour that
can occur during out-of-order operations, the modern ARM architectures provide *barrier instructions* that allow the programmer
to enforce points in code where stricter ordering requirements are necessary. Anything before the memory barrier must be 
commited. Polarising this, the guarantees offered by the x86 memory model include not reorderingloads with other loads, 
not remixing stores with other stores, and the same for stores and older loads. Today my eyes have opened a little wider. 
