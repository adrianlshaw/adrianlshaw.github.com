---
layout: post
title: Debian package example
---

Happy new year! It's been around a year since I've made a post,
but by no means has it been a quiet one. This is a short post
that describes how to make a simple Debain package, and mainly 
acts as a reminder to me for those rare occasions where I do find
the need to make one. 

There are at least a few advantages to using a Debian package.
Firstly, a well made package can be installed without any understanding 
of how an application works. Secondly, a relatively stateless 
application install can be cleanly uninstalled with relative ease. 
Lastly, it's a good way to declaratively describe the dependencies 
for the APT package manager; not all humans read the accompanied README files.

However, I've always felt that making a Debian package required 
some understanding and experience of the APT system. For instance,
an introduction to Debian packaging is 86 slides[1]. The detail 
provided is superb, yet still seems overkill for my limited needs.
It doesn't cleanly separate the minimal viable package from all the 
extras that can make a smart package, and extensive reading 
on the subject could quickly outweight the benefits. So this 
short post is a gross simplification of how to make a Debian package.
I recommend the slides and the full Debian documentation 
for those with further interest on the matter.


A subdirectory titled DEBIAN is required, though it isn't case-sensitive. 
Within here you include 
scripts that provide auxiliary functions during installation.
At the very least, you must include a file called **control**. Here 
are some some example fields that should be included:

{% highlight bash %}
Package: helloworld
Depends: bash
Version: 0.0.1
Section: blogpost
Architecture: all
Essential: no
Maintainer: adrianlshaw
Description: This is an example Debian package
{% endhighlight %}

Once that is done. You need to replicate subdirectories that will be used
on your target system. For instance, if you intend to have your file
installed in **/usr/local/bin** then you should recreate those folders
within your package root.

Here is the final example layout of a bare minimum (uncompressed) package:

{% highlight bash %}
$ tree
.
├── DEBIAN
│   └── control
└── usr
    └── local
        └── bin
            └── helloworld
{% endhighlight %}
 

You can optionally provide other scripts that can be invoked *before* or *after*
the files have been copied. These scripts, respectively known as 
**preinst** and **postinst** should be included in the DEBIAN directory.

Finally:

{% highlight bash %}
$ dpkg-deb --build package
{% endhighlight %}

Where **package** is the name of the directory of your package contents.
It should go without saying that you should also provide documentation 
using man pages or HTML within your package, but that is outside the
scope of this post. Ta-ra! 

[1] "Debian Packaging Tutorial", https://www.debian.org/doc/manuals/packaging-tutorial/packaging-tutorial.en.pdf
