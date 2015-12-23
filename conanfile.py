from conans import ConanFile
import os, shutil
from conans.tools import download, unzip, replace_in_file, check_md5
from conans import CMake


class Bzip2Conan(ConanFile):
    name = "libxml2"
    version = "2.9.3"
    branch = "master"
    ZIP_FOLDER_NAME = "libxml2-%s" % version
    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt"]
    url="http://github.com/lasote/conan-libxml2"
    requires = "zlib/1.2.8@lasote/stable"

    def source(self):
        zip_name = "libxml2-%s.tar.gz" % self.version
        download("ftp://xmlsoft.org/libxml2/%s" % zip_name, zip_name)
        check_md5(zip_name, "daece17e045f1c107610e137ab50c179")
        unzip(zip_name)        
        os.unlink(zip_name)

    def build(self):
        arch = "export CFLAGS=-m32 && " if self.settings.arch == "x86" else ""
        shared = ""# --enable-shared=yes --enable-static=no" if self.options.shared else "--enable-shared=no --enable-static=yes"
        zlib = "--with-zlib=%s" % self.deps_cpp_info["zlib"].lib_paths[0]
        configure_command = "%s cd %s && ./configure %s %s" % (arch, self.ZIP_FOLDER_NAME, shared, zlib)
        self.output.warn(configure_command)
        self.run(configure_command)
        self.run("cd %s && make" % self.ZIP_FOLDER_NAME)
       

    def package(self):
        self.copy("*.h", "include", "%s/include" % (self.ZIP_FOLDER_NAME), keep_path=True)
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="%s" % self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="%s" % self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.cpp_info.libs = ['xml2', 'm']
        else:
            self.cpp_info.libs = ['libxml2']
