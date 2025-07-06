[app]

title = Medicine Finder
package.name = medicinefinder
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0
orientation = portrait
fullscreen = 0
log_level = 2

# Permissions and dependencies
android.permissions = INTERNET
requirements = python3,kivy,requests

# Android SDK/NDK versions
android.api = 33
android.ndk = 25b
android.accept_sdk_license = True
android.build_cache = true
android.strip_debug = False
