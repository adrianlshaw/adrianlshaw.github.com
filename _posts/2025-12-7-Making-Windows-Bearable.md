---
layout: post
title: Making windows bearable
tags: [windows, tools]
---

Sometimes you have no choice but to use Windows. Whether it's for work, gaming, or that one piece of software that only runs on Microsoft's platform, we've all been there. After years of macOS, going back to Windows feels like I keep bumping my head
against something, where everything is *almost* familiar, but slightly off.

Here's my survival guide for making Windows feel less hostile.

## CPU Performance: ThrottleStop

Before anything else, make sure your hardware is actually performing. Many laptops aggressively throttle the CPU, leaving you with a sluggish experience for no good reason. [ThrottleStop](https://www.techpowerup.com/download/techpowerup-throttlestop/) can help you take back control of your CPU's performance. Without decent CPU performance, nothing else on this list will feel right.

## Scoop: A Proper Package Manager

If you miss `brew install`, you'll love [Scoop](https://scoop.sh/). It's a command-line package manager that doesn't require admin privileges and works exactly how you'd expect:

```bash
scoop install git
scoop install vim
```

Simple!

## Coreutils

Once you have Scoop, immediately run:

```bash
scoop install coreutils
```

Now you have `ls`, `grep`, `cat`, and so on. 
Your muscle memory will thank you.

## GlazeWM: Tiling Window Manager

If you like tiling window managers, [GlazeWM](https://github.com/glzr-io/glazewm) is one that doesn't require admin and 
does a reasonable job at filling available screen space. 
It has a sensible user license and actually works well.

```bash
scoop bucket add extras
scoop install extras/glazewm
scoop install extras/zebar
```

Important key bindings:
- `Alt + Arrow keys` - Navigate between windows
- `Alt + V` - Toggle vertical/horizontal split for the next window

In my opinion, once you go tiling, you never go back.

## PowerToys: Spotlight for Windows

Microsoft's [PowerToys](https://learn.microsoft.com/en-us/windows/powertoys/) is surprisingly good. Install it from the Windows Store, then immediately go to PowerToys Run settings and change the activation shortcut to `Windows + Space`. 

Now you have something that feels almost like Spotlight.

## TranslucentTB

I find the Windows 11 taskbar to be lacking aesthetically. [TranslucentTB](https://apps.microsoft.com/detail/9pf4kz2vn4w9) from the Windows Store makes it transparent, which somehow makes the whole desktop feel less cluttered.

## Quality of Life Settings

These are buried in the settings but worth finding:

### Right-click to End Task

No more opening Task Manager just to kill a frozen app.

`Settings → System → For developers → End Task`

### Show File Extensions

Why this isn't on by default in 2024 is beyond me.

`Settings → System → For developers → File Explorer`

### Focus Follows Mouse

If you're used to this from Linux/X11, you can [enable it in Windows 11](https://www.reddit.com/r/Winsides/comments/1ikkqpl/how_to_enable_focus_follows_mouse_in_windows_11/) too.

## Terminal: Windows Terminal or Alacritty

The default Windows Terminal is acceptable. It's miles better than the old cmd.exe, but I find it laggy at times. [Alacritty](https://alacritty.org/) is worth trying if you want something snappier.

## Other Useful Tools

- **[WinDirStat](https://windirstat.net/)** - Shows a visual treemap of what is consuming the disk space.
- **[Twinkle Tray](https://apps.microsoft.com/detail/9pljwwsv01lk)** - Control monitor brightness from your taskbar, which is useful if you have external monitors.
- **[Screenbox](https://apps.microsoft.com/detail/9ntsnmsvcb5l)** - A media player if VLC feels too heavy.
- **Chris Titus Tech's debloat script** - For removing the telemetry and bloatware.

## One Last Tip

Right-click the desktop, go to View, and uncheck "Show desktop icons." 

A clean desktop is like a real clean desk, it declutters the mind.

---

It would be better to not use Windows at all, but sometimes you have to. Bye for now.
