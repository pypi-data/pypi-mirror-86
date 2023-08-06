#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""
✉️💣 **LetterBomb**: A fork of the `classic Wii hacking tool
<https://wiibrew.org/wiki/LetterBomb>`_ from `fail0verflow
<https://github.com/fail0verflow/letterbomb>`_.

::

    ██╗     ███████╗████████╗████████╗███████╗██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗
    ██║     ██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
    ██║     █████╗     ██║      ██║   █████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝
    ██║     ██╔══╝     ██║      ██║   ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗
    ███████╗███████╗   ██║      ██║   ███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝
    ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝

----

This is the Flask module, rebuilt for modern web-browsers and better usage.

Obtain the latest copy of LetterBomb here:
https://gitlab.com/whoatemybutter/letterbomb

**Note:** *This exploit only works for System Menu 4.3. 4.2 and below will not work.*

LetterBomb is licensed under the GPLv3+ license. You can grab a copy here:
https://www.gnu.org/licenses/gpl-3.0.txt.
"""
import json
import logging
import urllib.parse
import urllib.request

import flask

import letterbomb

app = flask.Flask(__name__)
app.config.from_pyfile("config.py")

logging.basicConfig(filename=app.config["LOG_FILE"], level=logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.info("Starting...")

has_captcha: bool = (
    app.config["RECAPTCHA_PUBLICKEY"] or app.config["RECAPTCHA_PRIVATEKEY"]
)

if app.debug:
    logging.basicConfig(filename=app.config["LOG_FILE"], level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)


@app.route("/")
def index(error=None):
    """Index page."""
    flask.g.recaptcha_args = f'k={app.config["RECAPTCHA_PUBLICKEY"]}'
    return flask.make_response(
        flask.render_template(
            "index.html",
            captcha=has_captcha,
            error=error,
        )
    )


def captcha_check():
    """Check ReCaptcha."""
    try:
        oform = {
            "privatekey": app.config["RECAPTCHA_PRIVATEKEY"],
            "secret": app.config["RECAPTCHA_PRIVATEKEY"],
            "remoteip": flask.request.remote_addr,
            "challenge": flask.request.form.get("g-recaptcha-challenge-field", [""]),
            "response": flask.request.form.get("g-recaptcha-response", [""]),
        }

        with urllib.request.urlopen(
            "https://www.google.com/recaptcha/api/siteverify",
            bytes(json.dumps(oform)),
            timeout=10.0,
        ) as file:

            error = file.readline().replace("\n", "")
            serialized = json.load(file)
            result = serialized["success"]

        if not result:
            if error != "incorrect-captcha-sol":
                app.logger.info("ReCaptcha fail: %r, %r", oform, serialized)
                flask.g.recaptcha_args += "&error=" + error
            return False

    except ValueError:
        flask.g.recaptcha_args += "&error=unknown"
        return False
    return True


@app.route("/post", methods=["POST"])
def post(filename="LetterBomb.zip"):
    """Main POST endpoint."""
    if has_captcha and not captcha_check():
        return index("Are you a human?")

    try:
        try:
            bootmii = str(flask.request.form["bootmii"])
        except KeyError:
            bootmii = False

        return flask.make_response(
            letterbomb.write_stream(
                "".join(flask.request.form[i] for i in "abcdef"),
                str(flask.request.form["region"]),
                bootmii,
            ).getvalue(),
            {
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/zip",
            },
        )
    except letterbomb.BadLengthMACError:
        app.logger.debugg(
            'Rejected bad length MAC "%s" on: %s, region: %s, bundle: %s',
            letterbomb.serialize_mac("".join(flask.request.form[i] for i in "abcdef")),
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return index(error="MAC address must be 12 characters long")
    except letterbomb.EmulatedMACError:
        app.logger.debug(
            'Rejected emulated MAC "%s" on: %s, region: %s, bundle: %s',
            letterbomb.serialize_mac("".join(flask.request.form[i] for i in "abcdef")),
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return index(error="LetterBomb will not work on MAC addresses from emulators")
    except letterbomb.InvalidMACError:
        app.logger.debug(
            'Rejected invalid MAC "%s" on: %s, region: %s, bundle: %s',
            letterbomb.serialize_mac("".join(flask.request.form[i] for i in "abcdef")),
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return index(error="You must enter a valid Wii MAC address")
    except letterbomb.InvalidRegionError:
        app.logger.debug(
            "Rejected invalid region on: %s, region: %s, bundle: %s",
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return index("Region must be one of U, E, K, J")
    except KeyError:
        app.logger.debug("Rejected bad POST request on: %s", letterbomb.timestamp()[2])
        return index("All fields must be filled in")


@app.route("/get", methods=["GET"])
def get(filename="LetterBomb.zip"):
    """Main GET endpoint."""
    if has_captcha and not captcha_check():
        return index("Are you a human?")

    try:
        return flask.make_response(
            letterbomb.write_stream(
                str(flask.request.args.get("mac")),
                str(flask.request.args.get("region")),
                bool(int(flask.request.args.get("bootmii"))),
            ).getvalue(),
            {
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/zip",
            },
        )
    except letterbomb.BadLengthMACError:
        app.logger.debug(
            'Rejected bad length MAC "%s" on: %s, region: %s, bundle: %s',
            letterbomb.serialize_mac(flask.request.args.get("mac").upper()),
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return json_error("MAC address must be 12 characters long", "bad_length")
    except letterbomb.EmulatedMACError:
        app.logger.debug(
            'Rejected emulated MAC "%s" on: %s, region: %s, bundle: %s',
            letterbomb.serialize_mac(flask.request.args.get("mac").upper()),
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return json_error(
            "LetterBomb will not work on MAC addresses from emulators", "emulated"
        )
    except letterbomb.InvalidMACError:
        app.logger.debug(
            'Rejected invalid MAC "%s" on: %s, region: %s, bundle: %s',
            letterbomb.serialize_mac(flask.request.args.get("mac").upper()),
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return json_error("You must enter a valid Wii MAC address", "invalid")
    except letterbomb.InvalidRegionError:
        app.logger.debug(
            "Rejected invalid region on: %s, region: %s, bundle: %s",
            letterbomb.timestamp()[2],
            flask.request.args.get("region"),
            flask.request.args.get("bootmii"),
        )
        return json_error("Region must be one of U, E, K, J", "region")


def json_error(error: str, shorthand: str):
    """Return raw JSON as a response"""
    return flask.jsonify({"error": str(error), "error_shorthand": str(shorthand)})


def not_found(_):
    """Error handler for HTTP 404."""
    return json_error("Page does not exist", "no_exist")


def malformed(_):
    """Error handler for HTTP 500."""
    return json_error("Invalid POST request", "bad")


app.register_error_handler(404, not_found)
app.register_error_handler(505, malformed)

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, threaded=True)
