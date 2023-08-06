#!/usr/bin/env python3

# Copyright 2020 Dominik George <nik@naturalnet.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from sh import xsetwacom
from xrectsel import XRectSel

ROTATE_PORTRAIT = "cw"
ROTATE_LANDSCAPE = "None"


def main():
    xrect = XRectSel()
    geometry = xrect.select()

    width, height = geometry["width"], geometry["height"]
    x, y = geometry["start"]["x"], geometry["start"]["y"]

    xgeometry = f"{width}x{height}+{x}+{y}"
    rotate = ROTATE_PORTRAIT if width < height else ROTATE_LANDSCAPE

    device_ids = re.findall(r"(?<=\tid: )\d+", str(xsetwacom.list()))
    for device_id in device_ids:
        xsetwacom.set(device_id, "Rotate", rotate)
        xsetwacom.set(device_id, "MapToOutput", xgeometry)

if __name__ == "__main__":
    main()
