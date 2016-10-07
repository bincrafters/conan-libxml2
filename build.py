from conan.packager import ConanMultiPackager
import platform


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="libxml2:shared", pure_c=True)
    if platform.system() == "Windows":
        filtered_builds = []
        for settings, options in builder.builds:
            if settings["os"] != "Windows" or options["libxml2:shared"] == True:
                filtered_builds.append([settings, options])
        builder.builds = filtered_builds
    builder.run()
