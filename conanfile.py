#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class Libxml2Conan(ConanFile):
    name = "libxml2"
    version = "2.9.3"
    url = "https://github.com/bincrafters/conan-libxml2"
    description = "libxml2 is a software library for parsing XML documents"
    homepage = "https://xmlsoft.org"
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    requires = "zlib/1.2.11@conan/stable", "libiconv/1.15@bincrafters/stable"
    exports = ["LICENSE.md"]
    exports_sources = ["FindLibXml2.cmake"]
    source_subfolder = "source_subfolder"

    def source(self):
        tools.get("http://xmlsoft.org/sources/libxml2-{0}.tar.gz".format(self.version))
        os.rename("libxml2-{0}".format(self.version), self.source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os == "Windows" and not self.options.shared:
            self.output.warn("Warning! Static builds in Windows are unstable")

    def build(self):
        if self.settings.os == "Windows":
            self.build_windows()
        else:
            self.build_with_configure()

    def build_windows(self):

        with tools.chdir(os.path.join(self.source_subfolder, 'win32')):
            vcvars = tools.vcvars_command(self.settings)
            compiler = "msvc" if self.settings.compiler == "Visual Studio" else "gcc"
            debug = "yes" if self.settings.build_type == "Debug" else "no"

            includes = ";".join(self.deps_cpp_info["libiconv"].include_paths +
                                self.deps_cpp_info["zlib"].include_paths)
            libs = ";".join(self.deps_cpp_info["libiconv"].lib_paths +
                            self.deps_cpp_info["zlib"].lib_paths)
            configure_command = "%s && cscript configure.js " \
                    "zlib=1 compiler=%s cruntime=/%s debug=%s include=\"%s\" lib=\"%s\"" % (
                        vcvars,
                        compiler,
                        self.settings.compiler.runtime,
                        debug,
                        includes,
                        libs)
            self.output.info(configure_command)
            self.run(configure_command)

            # Fix library names because they can be not just zlib.lib
            libname = self.deps_cpp_info['zlib'].libs[0]
            if not libname.endswith('.lib'):
                libname += '.lib'
            tools.replace_in_file("Makefile.msvc",
                                  "LIBS = $(LIBS) zlib.lib",
                                  "LIBS = $(LIBS) %s" % libname)
            libname = self.deps_cpp_info['libiconv'].libs[0]
            if not libname.endswith('.lib'):
                libname += '.lib'
            tools.replace_in_file("Makefile.msvc",
                                  "LIBS = $(LIBS) iconv.lib",
                                  "LIBS = $(LIBS) %s" % libname)

            if self.settings.compiler == "Visual Studio":
                self.run("%s && nmake /f Makefile.msvc" % (vcvars))
            else:
                self.run("%s && make -f Makefile.mingw" % (vcvars))

    def build_with_configure(self):

        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = self.options.fPIC
        with tools.environment_append(env_build.vars):
            with tools.chdir(self.source_subfolder):
                # fix rpath
                if self.settings.os == "Macos":
                    tools.replace_in_file("configure", r"-install_name \$rpath/", "-install_name ")
                configure_args = ['--with-python=no', '--without-lzma']
                if self.options.shared:
                    configure_args.extend(['--enable-shared', '--disable-static'])
                else:
                    configure_args.extend(['--enable-static', '--disable-shared'])
                env_build.configure(args=configure_args)
                env_build.make()

    def package(self):
        self.copy("FindLibXml2.cmake", ".", ".")

        # copy package license
        self.copy("COPYING", src=self.source_subfolder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy(pattern="*.h", dst="include", src=os.path.join(self.source_subfolder, "include"))
        # specify glob with libxml name to avoid copying testdso.a
        self.copy(pattern="*libxml*.lib", dst="lib", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="*libxml*.dll", dst="bin", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="*libxml*.so*", dst="lib", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="*libxml*.dylib", dst="lib", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="*libxml*.a", dst="lib", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="xmllint", dst="bin", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="xmllint.exe", dst="bin", src=self.source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.cpp_info.libs.append('m')
