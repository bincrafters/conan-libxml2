from conans import ConanFile
import os, shutil
from conans.tools import download, unzip, replace_in_file, check_md5
from conans import CMake, ConfigureEnvironment


class LibxmlConan(ConanFile):
    name = "libxml2"
    version = "2.9.3"
    branch = "master"
    ZIP_FOLDER_NAME = "libxml2-%s" % version
    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindLibXml2.cmake"]
    url = "http://github.com/lasote/conan-libxml2"
    requires = "zlib/1.2.8@lasote/stable"

    def source(self):
        zip_name = "libxml2-%s.tar.gz" % self.version
        download("http://xmlsoft.org/sources/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        
    def config(self):
        try: # Try catch can be removed when conan 0.8 is released
            del self.settings.compiler.libcxx 
        except: 
            pass
        #self.options["zlib"].shared = self.options.shared
        self.requires.add("libiconv/1.14@lasote/stable", private=False)
        self.options.shared = True # Static in win doesn't work, runtime errors
        #self.options["zlib"].shared = True


    def build(self):
        if self.settings.os == "Windows":
            self.build_windows()
        else:
            self.build_with_configure()
            
        
    def build_windows(self):
        iconv_headers_paths = self.deps_cpp_info["winiconv"].include_paths[0]
        iconv_lib_paths= " ".join(['lib="%s"' % lib for lib in self.deps_cpp_info["winiconv"].lib_paths])
        
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        env_variables = env.command_line
        compiler = "msvc" if self.settings.compiler == "Visual Studio" else self.settings.compiler == "gcc"
        debug = "yes" if self.settings.build_type == "Debug" else "no"
        
        configure_command = "cd %s/win32 && %s && cscript configure.js " \
                            "zlib=1 compiler=%s cruntime=/%s debug=%s include=\"%s\" %s" % (self.ZIP_FOLDER_NAME, 
                                                                               env_variables,
                                                                               compiler, 
                                                                               self.settings.compiler.runtime,
                                                                               debug, 
                                                                               iconv_headers_paths, 
                                                                               iconv_lib_paths) 
        self.output.warn(configure_command)
        self.run(configure_command)
        
        makefile_path = os.path.join(self.ZIP_FOLDER_NAME, "win32", "Makefile.msvc")
        # Zlib library name is not zlib.lib always, it depends on configuration
        replace_in_file(makefile_path, "LIBS = $(LIBS) zlib.lib", "LIBS = $(LIBS) %s.lib" % self.deps_cpp_info["zlib"].libs[0])
        
        make_command = "nmake /f Makefile.msvc" if self.settings.compiler == "Visual Studio" else "make -f Makefile.mingw"
        make_command = "cd %s/win32 && %s && %s" % (self.ZIP_FOLDER_NAME, env_variables, make_command)
        self.output.warn(make_command)
        self.run(make_command)
        
    def build_with_configure(self): 
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
    
        if self.settings.os == "Macos":
            old_str = '-install_name \$rpath/\$soname'
            new_str = '-install_name \$soname'
            replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
                 
        self.run("cd %s && %s ./configure --with-python=no" % (self.ZIP_FOLDER_NAME, env.command_line))
        #self.run("cd %s && %s make check" % (self.ZIP_FOLDER_NAME, env.command_line))
        self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, env.command_line))
        
        
        #zlib = "--with-zlib=%s" % self.deps_cpp_info["zlib"].lib_paths[0]
        #configure_command = "cd %s && %s ./configure %s --with-python=no" % (self.ZIP_FOLDER_NAME, 
        #                                                                         self.generic_env_configure_vars(), 
        #                                                                         zlib)
        #self.output.warn(configure_command)
        #self.run(configure_command)
        #self.run("cd %s && make" % self.ZIP_FOLDER_NAME)
       

    def package(self):
        # Copy findZLIB.cmake to package
        self.copy("FindLibXml2.cmake", ".", ".")
       
       
        self.copy("*.h", "include", "%s/include" % (self.ZIP_FOLDER_NAME), keep_path=True)
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.dll*", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="%s" % self.ZIP_FOLDER_NAME, keep_path=False)
        
        self.copy(pattern="*.lib", dst="lib", src="%s" % self.ZIP_FOLDER_NAME, keep_path=False)
        
    def package_info(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.cpp_info.libs = ['xml2', 'm']
        else:
            self.cpp_info.libs = ['libxml2'] 
   
