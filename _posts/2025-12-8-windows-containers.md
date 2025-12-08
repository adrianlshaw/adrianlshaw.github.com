---
layout: post
title: Windows containers pitfalls
tags: [windows, docker]
---

I've had enough of the hassle of manually tuning Windows development environments and dealing with their brittle nature. Lately, I've had no choice but to use Windows to build some software, and the environment can make or break a piece of software.

So, I decided to automate the pain. Docker supports "Windows Containers." Unlike Linux containers which use OS-level namespaces and cgroups, Windows containers come in two flavours: process isolation (similar to Linux containers, but only available on Windows Server) and Hyper-V isolation (which spins up a lightweight VM). On Windows 10/11, you're typically stuck with Hyper-V isolation.

Even with a basic Windows container, you can't escape some confusing quirks. In this post, I'll share the challenges I've faced, some hard-won advice, and a complete Dockerfile example at the end.

## Base images

A good base image I use is `mcr.microsoft.com/windows/servercore:ltsc2019`. I believe it's a cut-down version of Windows Server.

Be aware that other images have disappeared from the registry. It's not clear when Microsoft decides to remove them, so try to stay informed.

## PowerShell

You should try to use PowerShell for everything when possible. It's the default shell in Windows containers and handles paths, environment variables, and Unicode much better than CMD. When downloading files, use `Invoke-WebRequest` or `Invoke-RestMethod` rather than shelling out to `curl`.

## CMD Shell

But it's not always possible to use PowerShell. The trick to using CMD in a container is to use the following flags in your Dockerfile:

```dockerfile
SHELL ["cmd", "/S", "/C"]
```

Here's what each part roughly means:

- **`SHELL`**: This Dockerfile instruction changes the default shell used for RUN commands.
- **`cmd`**: Specifies that the shell to be used is the Windows Command Prompt executable (cmd.exe).
- **`/S`**: This switch changes how commands are processed. It strips out certain extra processing that might interfere with commands, ensuring they run as intended.
- **`/C`**: This switch tells cmd.exe to carry out the command that follows and then terminate.

This ensures behaviour that is closely aligned with what Windows users might expect from a batch/Command Prompt environment rather than PowerShell.

## Paths in Dockerfile

Use `\\` instead of `\` wherever possible. You never know which program may strip them out because they are treated as escape characters. Without doing this, I had cases where environment variables would show `CUsersUser.sshid_rsa` instead of `C:\Users\User\.ssh\id_rsa`.

## Administrator vs Unprivileged User

The most important thing to note is that unprivileged users can't create symbolic links. This is annoying when you use software that requires them, like `gitman`.

At least with the `ltsc2019` image, I found you can't use the registry tweaks or turn on developer mode to enable this, like you would on a typical Windows install.

The best workaround is to run container software as Administrator. It's a bit sad, but I've not found a solution yet.

## Package management

I highly recommend the [scoop.sh](https://scoop.sh) package manager, especially over Chocolatey, NuGet, or WinGet. Scoop works without admin, but if you face the symlink issue then you can force Scoop to install and run as Administrator by using an extra install argument.

## Git and SSH agent

I found the following necessary for ssh-agent to work. Run these as Administrator:

```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
```

**Important:** Don't put `Start-Service ssh-agent` as a RUN command in the Dockerfile, because it won't be running when the container starts—services don't persist across image layers.

You also need the following, otherwise SSH agent won't work properly:

```bash
git config --global core.sshCommand "'C:\\Windows\\System32\\OpenSSH\\ssh.exe'"
git config --global core.symlinks true
```

If you run some git-based tool like gitman, you may not see any interactive prompts that normally appear. One case is that it was hung on an invisible prompt asking to accept a host key. Either connect to the server manually beforehand, or disable StrictHostKeyChecking:

```dockerfile
RUN echo Host * >> C:\Users\ContainerAdministrator\.ssh\config && \
    echo     StrictHostKeyChecking no >> C:\Users\ContainerAdministrator\.ssh\config
```

**Warning:** This is utterly insecure and I don't recommend it. It's better to scan the hosts at a known good time and save the known_hosts file somewhere that can then be copied into the container.

## Installing Visual Studio

The easiest way to install Visual Studio into a container is to create a `.vsconfig` file and pass it to the Visual Studio installer.

Here is an example:

```json
{
  "version": "1.0",
  "components": [
    "Microsoft.Component.MSBuild",
    "Microsoft.NetCore.Component.Runtime.5.0",
    "Microsoft.VisualStudio.Component.CoreBuildTools",
    "Microsoft.VisualStudio.Component.Roslyn.Compiler",
    "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
    "Microsoft.VisualStudio.Component.Windows10SDK.19041",
    "Microsoft.VisualStudio.Workload.MSBuildTools",
    "Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Core",
    "Microsoft.VisualStudio.Workload.NativeDesktop",
    "Microsoft.VisualStudio.Component.VC.ATLMFC"
  ]
}
```

You can find the component IDs you need in the [Visual Studio component directory](https://learn.microsoft.com/en-us/visualstudio/install/workload-component-id-vs-build-tools).

## Example Dockerfile

Here's a complete example bringing together most of the advice from this post:

```dockerfile
# escape=`
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Use CMD shell for compatibility
SHELL ["cmd", "/S", "/C"]

# Install Scoop as Administrator
RUN powershell -Command `
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; `
    iex (New-Object Net.WebClient).DownloadString('https://get.scoop.sh')

# Install essential tools via Scoop
RUN powershell -Command `
    scoop install git; `
    scoop install cmake; `
    scoop install ninja

# Configure Git for SSH
RUN git config --global core.sshCommand "'C:\\Windows\\System32\\OpenSSH\\ssh.exe'" && `
    git config --global core.symlinks true

# Enable and start SSH agent
RUN powershell -Command `
    Get-Service -Name ssh-agent | Set-Service -StartupType Automatic

# Set up working directory
WORKDIR C:\\workspace

# Entry point that starts ssh-agent
CMD powershell -Command "Start-Service ssh-agent; cmd"
```

**Note:** Remember that services don't persist across image layers, so `Start-Service ssh-agent` must be in the entry point or run script, not in a `RUN` command.

---

## Final thoughts

Windows containers are painful, but they can save hours of manual environment setup once you get them working.

Good luck, and may your builds be reproducible.
```
