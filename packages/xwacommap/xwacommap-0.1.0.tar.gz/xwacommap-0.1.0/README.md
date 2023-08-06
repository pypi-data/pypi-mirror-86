xwacommap - Interactively map Wacom table to screen area
========================================================

Synopsis
--------

`xwacommap` is a small utility that helps configuring a Wacom
tablet to map to a selected area of the screen. It allows to
draw a rectangular region on the screen, then passes the
geometry to the `xsetwacom` tool. If the selected area is higher
than wide, the tablet is also rotated.

Requirements
------------

This tool requires the `xsetwacom` tool from the
`xserver-xorg-input-wacom` package (on Debian systems).

Licence
-------

This tool is licenced under the Apache 2.0 licence.
