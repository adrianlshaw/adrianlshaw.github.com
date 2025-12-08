# Windows containers pitfalls and escape hatches

I’ve had enough of the hassle of manually tuning Windows development environments and dealing with their brittle nature. Lately, I’ve had no choice but to use it to build some software, and the environment can make or break a piece of software.

So, I decided to automate the pain. Docker supports “Windows Containers.” As far as I understand, Windows doesn’t have OS-level containers. Instead, it creates a virtual machine whenever you want a container.

Even with a basic Windows container, you can’t escape some of the confusing quirks. So, I’ll share some of the challenges I’ve faced, some advice, and, in the end, give you a Dockerfile that’s worth its weight in gold.

## Base images

A good that I use is `mcr.microsoft.com/windows/servercore:ltsc2019`
I believe it's a cut down version of Windows Server.

Other images have disappeared from the registry. It's not clear when Microsoft decides to remove them, so try and be aware.

## PowerShell

You should try and use powershell for everything, if you can.

## CMD Shell

But that's not always possible. The trick to using CMD in a container is to 
use the following flags. 

In the Dockerfile I can use: SHELL ["cmd", "/S", "/C"]

Here’s a breakdown of what each part means:

- `SHELL`: This Dockerfile instruction changes the default shell used for RUN commands.

- `cmd`: This specifies that the shell to be used is the Windows Command Prompt executable (cmd.exe).

- `/S`: This is a switch for cmd.exe that changes how commands are processed. It generally strips out certain extra processing that might interfere with commands, ensuring that the following commands run as intended.

- `/C`: This switch tells cmd.exe to carry out the command that follows and then terminate.

This helps ensure compatibility and behavior more closely aligned with what Windows users might expect from a batch/Command Prompt environment rather than PowerShell.


## Paths in Dockerfile

Use "\\" instead of '\' wherever possible. You never know which program may strip them out 
because they are some escape character. Without doing this, I certainly had cases where
environment variables would show "CUsersUser.sshid_rsa" instead of C:\Users\User\.ssh\id_rsa

## Administrator and unprivileged User

The most important thing to note is that unprivileged users can't create symbolic links.
This is annoying when you use software that requires them, like `gitman`.

At least with the `ltsc2019 ` image, I found you can't use the registry tweaks or turn on developer mode to enable this, like you would on a typical Windows install.

Best workaround is to run that container software as Administrator. It's a bit sad, but
I've not found a solution yet.

## Package management

I highly recommend the scoop.sh package manager. Especially over Chocolaty, Nuget or Winget.
Scoop works without admin, but if you face the symlink issue then you can force
Scoop to install and run as administator by using an extra install argument. 

## Git and SSH agent

I found the following necessary for ssh-agent to work


Run the followin as administrator:
- `Get-Service -Name ssh-agent | Set-Service -StartupType Automatic`
- `Start-Service ssh-agent`

Don't put these Start-Service ssh-agent as a RUN command in the Dockerfile, because it 
won't be started on 

You also need to the following otherwise SSH agent won't work properly:

- git config --global core.sshCommand "'C:\\Windows\\System32\\OpenSSH\\ssh.exe'"


- git config --global core.symlinks true

If you run some git-based tool like gitman, you may not see any interactive prompts that normally appear. One case is that it was hung on an invisible prompt asking to accept host key. 
Either connect to the server manually or disable StrictHostKeyChecking using the following:

RUN echo "Host *\n    StrictHostKeyChecking no" >> C:\Users\ContainerAdministrator\.ssh\config

This is utterly insecure and I don't recommedn this. 
It's better to scan the hosts at a known good time and save the host file in a place that can
then be copied into the container.

## Installing Visual Studio

The easiest way to install visual studio into a container is to 
create a vsproj file and pass it into the Visual Studo installer.

Here is an example:

```
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
