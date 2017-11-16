import os
from conans import ConanFile, CMake, tools

CMAKELISTS_PATCH = '''diff --git a/CMakeLists.txt b/CMakeLists.txt
index 3de896e5..2938b6a0 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -12,6 +12,8 @@ endif ()
 set (CMAKE_LEGACY_CYGWIN_WIN32 0)

 project (log4cplus)
+include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
+conan_basic_setup()
 cmake_minimum_required (VERSION 2.8.4)

 enable_language (CXX)
@@ -70,8 +72,6 @@ option(ENABLE_SYMBOLS_VISIBILITY
   "Enable compiler and platform specific options for symbols visibility"
   ON)

-set(_WIN32_WINNT 0x0500 CACHE STRING "Define Windows API version to use.")
-
 option(LOG4CPLUS_ENABLE_DECORATED_LIBRARY_NAME
   "Turns on resulting file name decoration for static and UNICODE builds." ON)
 if (LOG4CPLUS_ENABLE_DECORATED_LIBRARY_NAME)
'''

SRC_CMAKELISTS_PATCH = '''diff --git a/src/CMakeLists.txt b/src/CMakeLists.txt
index 82e52956..defc0831 100644
--- a/src/CMakeLists.txt
+++ b/src/CMakeLists.txt
@@ -71,7 +71,6 @@ if (UNICODE)
 endif (UNICODE)
 if (WIN32)
   add_definitions (-DMINGW_HAS_SECURE_API=1)
-  add_definitions (-D_WIN32_WINNT=${_WIN32_WINNT})

   if (BUILD_SHARED_LIBS)
     set(log4cplus_build_shared 1)
'''

class Log4cplusConan(ConanFile):
    name = "log4cplus"
    version = "1.2.0"
    license = "Multiple Licenses - https://github.com/log4cplus/log4cplus/blob/REL_1_2_0/LICENSE"
    url = "https://github.com/salessandri/conan-log4cplus"
    description = "log4cplus is a simple to use C++ logging API providing thread-safe, flexible, and arbitrarily granular control over log management and configuration. It is modelled after the Java log4j API."
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "singleThreaded": [True, False],
        "workingLocale": [None, True, False],
        "workingCLocale": [None, True, False],
        "withQt4Appender": [True, False],
        "withQt5Appender": [True, False],
        "unicode": [True, False],
        "iConv": [True, False],
        "enableSymbolVisibility": [True, False],
        "decorateLibName": [True, False]
    }
    default_options = \
        "shared=False", \
        "singleThreaded=False", \
        "workingLocale=None", \
        "workingCLocale=None", \
        "withQt4Appender=False", \
        "withQt5Appender=False", \
        "unicode=False", \
        "iConv=False", \
        "enableSymbolVisibility=True", \
        "decorateLibName=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/log4cplus/log4cplus.git")
        self.run("cd log4cplus && git checkout REL_1_2_0")
        tools.patch('log4cplus', patch_string=CMAKELISTS_PATCH)
        tools.patch('log4cplus', patch_string=SRC_CMAKELISTS_PATCH)

    def build(self):
        cmake = CMake(self)

        cmake.definitions["LOG4CPLUS_BUILD_LOGGINGSERVER"] = False
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["LOG4CPLUS_SINGLE_THREADED"] = self.options.singleThreaded
        if self.options.workingLocale != 'None':
            cmake.definitions["LOG4CPLUS_WORKING_LOCALE"] = self.options.workingLocale
        if self.options.workingCLocale != 'None':
            cmake.definitions["LOG4CPLUS_WORKING_C_LOCALE"] = self.options.workingCLocale
        cmake.definitions["LOG4CPLUS_QT4"] = self.options.withQt4Appender
        cmake.definitions["LOG4CPLUS_QT5"] = self.options.withQt5Appender
        cmake.definitions["UNICODE"] = self.options.unicode
        cmake.definitions["WITH_ICONV"] = self.options.iConv
        cmake.definitions["ENABLE_SYMBOLS_VISIBILITY"] = self.options.enableSymbolVisibility
        cmake.definitions["LOG4CPLUS_ENABLE_DECORATED_LIBRARY_NAME"] = self.options.decorateLibName
        cmake.configure(source_dir=self.name)
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join('include', self.name))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.options.shared:
            if self.settings.os == 'Linux':
                self.cpp_info.libs.append('pthread')
            elif self.settings.compiler == 'Visual Studio':
                self.cpp_info.libs.append('Ws2_32')
        if self.options.unicode:
            self.cpp_info.defines.append('UNICODE')

