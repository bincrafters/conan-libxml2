#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import platform

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    if platform.system() == "Windows":
        filtered_builds = []
        for build in builder.builds:
            if build.settings["compiler"] != "Visual Studio" or build.options[name + ":shared"]:
                filtered_builds.append(build)
        builder.builds = filtered_builds

    builder.run()
