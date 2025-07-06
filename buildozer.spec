[app]

# (str) Title of your application
title = Medicine Finder

# (str) Package name
package.name = medicinefinder

# (str) Package domain (must be a valid domain)
package.domain = org.aadibaba

# (str) Source code where your main.py is located
source.dir = .

# (str) Main .py file to use as entry point
source.main = main.py

# (str) Supported orientation (portrait, landscape, all)
orientation = all

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions your app needs
android.permissions = INTERNET

# (str) Application versioning
version = 1.0

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (yes/no)
android.private_storage = True

# (str) Bootstrap to use (sdl2 is default)
android.bootstrap = sdl2

# (str) Supported architectures
android.arch = arm64-v8a

# (list) Requirements (dependencies)
requirements = python3,kivy,requests

# (str) Java JDK version
android.accept_sdk_license = True

# (bool) Copy library instead of symlink
android.copy_libs = 1

# (list) Patterns to whitelist when copying files
android.whitelist =

# (bool) Indicate if the app should be compiled in debug mode
android.debug = 1

# (list) Include additional .so libraries
android.add_libs_armeabi_v7a =

# (str) Custom package name
package.id = org.aadibaba.medicinefinder

# (str) Application icon
icon.filename = %(source.dir)s/icon.png

# (str) Presplash image
presplash.filename = %(source.dir)s/presplash.png

# (str) Entry point of the app
entrypoint = main.py

# (list) Additional jars to include in the APK
android.add_jars =

# (str) Path to custom keystore file (for release builds)
# android.keystore =

# (str) Keystore password
# android.keystore_password =

# (str) Key alias
# android.keyalias =

# (str) Key alias password
# android.keyalias_password =

# (bool) Add Android logcat support
log_level = 2

# (bool) Enable Android logcat on run
android.logcat = 1

# (str) Command to start logcat
android.logcat_filters = *:S python:D

# (bool) Enable the build cache
use_build_cache = 1

# (str) Android SDK path (leave blank to auto-download)
# android.sdk_path =

# (str) Android NDK path (leave blank to auto-download)
# android.ndk_path =

# (str) Android entry point
# (only set this if using a custom entry point)
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Additional arguments passed to python-for-android
# p4a.extra_args =

# (bool) Indicate whether to include source when packaging
# include_source = True

# (list) Files to copy into the .apk
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Directories to exclude from the project
source.exclude_dirs = tests, bin

# (list) File patterns to exclude from the project
source.exclude_patterns = *.pyc,*.swp,*.bak

# (str) Application theme
# android.theme = '@android:style/Theme.NoTitleBar'

# (bool) Automatically install the APK after building
# android.install = False

# (bool) Automatically run the app after install
# android.run = False

# (str) Custom entry point for app
# entrypoint = main.py
