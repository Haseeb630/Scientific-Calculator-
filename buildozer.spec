[app]
title = Scientific Calculator
package.name = scientificcalculator
package.domain = org.ranahaseeb
description = A scientific calculator application built with Kivy
author = Haseeb

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 0



android.permissions = INTERNET
android.features = android.hardware.keyboard

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.enable_androidx = True
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
