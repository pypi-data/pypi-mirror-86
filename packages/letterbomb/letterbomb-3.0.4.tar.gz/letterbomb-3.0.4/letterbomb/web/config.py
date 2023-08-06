#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Flask configuration."""

# Where to save logfile, can be an absolute or relative path
# Leave blank to not generate a log file
LOG_FILE: str = ""

# Fill these in if you intend on having a Captcha.
# Leave both of these blank if you do not want to include a captcha
RECAPTCHA_PUBLICKEY: str = ""
RECAPTCHA_PRIVATEKEY: str = ""

# Don't enable unless you know what you are doing
DEBUG: bool = True
