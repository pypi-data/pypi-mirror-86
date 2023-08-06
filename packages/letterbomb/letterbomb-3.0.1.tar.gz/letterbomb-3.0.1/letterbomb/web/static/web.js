var captcha_passed = false;

function set_listeners() {
    var ids = ["a", "b", "c", "d", "e", "f"];
    var regions = ["u", "e", "j", "k"];
    for (var i = 0; i < ids.length; i++) {
        if (i + 1 === ids.length) {
            document.getElementById(ids[i]).addEventListener("keydown", keyHandler, true);
            document.getElementById(ids[i]).addEventListener("keyup", update, true);
        } else {
            document.getElementById(ids[i]).addEventListener("keydown", keyHandler, true);
            document.getElementById(ids[i]).addEventListener("keydown", doNext, true);
            document.getElementById(ids[i]).addEventListener("keyup", update, true);
        }
    }
    for (var i = 0; i < regions.length; i++) {
        var x = (i + 1 === regions.length) ? i : i;
        document.getElementById("region_" + regions[x]).addEventListener("click", update);
    }
}

function keyHandler(e) {
    var keynum = String.fromCharCode(window.event ? event.keyCode : event.which)
    return keynum.match(/[0-9a-f]/i) !== null || (keynum === 13 || keynum === 16 || keynum === 17 || keynum === 20 ||
            keynum === 35 || keynum === 36 || keynum === 37 || keynum === 38 || keynum === 39 || keynum === 40) ?
        true : e.preventDefault();
}

function check() {
    var ids = ["a", "b", "c", "d", "e", "f"];
    var total = "";
    for (var i = 0; i < 6; i++) {
        total += document.getElementById(ids[i]).value;
    }
    if (total.match(/^[0-9a-f]{12}$/igm) == null) {
        return false;
    }
    var regions = ["u", "e", "j", "k"];
    var count = 0;
    for (var i = 0; i < regions.length; i++) {
        if (document.getElementById("region_" + regions[i]).checked === false) {
            count++;
        }
        if (count === 4) {
            return false;
        }
    }
    if (document.getElementById("recaptcha") === null) {
        return true;
    } else {
        return captcha_passed;
    }
}

function update() {
    var ok = check();
    document.getElementById("submit_btn").disabled = !ok;
    document.getElementById("submit_btn2").disabled = !ok;
    document.getElementById("submit_btn3").disabled = !ok;
    document.getElementById("submit_btn4").disabled = !ok;
}

function doNext(event) {
    var ids = ["a", "b", "c", "d", "e", "f"];
    var x = (ids.indexOf(event.target.id.toLowerCase()) + 1 === ids.length) ?
        null : ids[ids.indexOf(event.target.id) + 1];
    if (event.target.textLength === 2 && x !== null) {
        document.getElementById(x).value = "";
        document.getElementById(x).focus();
        return true;
    } else {
        return false;
    }
    update();
}

function captcha_ok() {
    captcha_passed = true;
    update();
}

function captcha_expired() {
    captcha_passed = false;
    update();
}

set_listeners();