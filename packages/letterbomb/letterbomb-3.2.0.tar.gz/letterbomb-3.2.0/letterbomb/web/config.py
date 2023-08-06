#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Flask configuration for LetterBomb's Web-Service."""

# Where to save logfile, can be an absolute or relative path
# Leave blank to not generate a log file
LOG_FILE: str = ""

# 10 - debug, 20 - info, 30 - warn, 40 - error, 50 - critical
LOG_LEVEL: int = 20

# Fill these in if you intend on having a Captcha.
# Leave BOTH of these blank if you do not want to include a captcha
RECAPTCHA_PUBLICKEY: str = ""
RECAPTCHA_PRIVATEKEY: str = ""

# Don't enable unless you know what you are doing
# If enabled, overrides LOG_LEVEL to 10, DEBUG
DEBUG: bool = False
