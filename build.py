#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import platform

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    if platform.system() == "Windows":
        items = []
        for item in builder.items:
            if item.settings["compiler"] != "Visual Studio" or item.options.get("libxml2:shared", False):
                items.append(item)
        builder.items = items

    builder.run()
