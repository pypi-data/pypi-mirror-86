# screenselector

A small utility that allows selecting from running screen sessions by menu.

# Purpose

It happened several times to me that I closed a terminal window by accident or that
I lost something when my Xorg crashed.

So my Idea was to start a new screen session instead of a plain shell in my terminal.

This tool will now present me a list of unattached and attached screen sessions
and allow me to attach to them.

# Usage

I change the command to be invoked in my terminal emulator to be screenselector,
so whenever I open a new terminal, I can start a new screen session or reconnect
to an already running.

# Platform

Tested with debian and gnome-terminal and others.

# Bugs

Screen sessions that contain a whitespace it their name are not displayed.
