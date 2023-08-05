import IPython.core.ultratb
from IPython import get_ipython
import requests
import json
import time
import sys
from pathlib import Path


def slack_message(message):
    config_file = str(Path.home() / ".slack_magic")

    try:
        with open(config_file) as f:
            webhook_url = f.read()
    except FileNotFoundError:
        webhook_url = input("Enter your slack app webhook: ")
        with open(config_file, "w") as f:
            f.write(webhook_url)

    slack_data = {"text": message}

    response = requests.post(
        url=webhook_url,
        data=json.dumps(slack_data),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 200:
        raise ValueError(
            f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}"
        )


def slack_code(code):
    message = f"```\n{code}\n```"
    return message


def slack_error(traceback):
    message = f":x::x::x:\nYour code failed at {time.strftime('at %H:%M:%S on %a %b %Y')[:-2]} :sob::sob:\n{slack_code(traceback)}"
    slack_message(message)


def slack_success():
    message = f":white_check_mark::white_check_mark::white_check_mark:\nYour code completed at {time.strftime('at %H:%M:%S on %a %b %Y')[:-2]} :relaxed::relaxed:"
    slack_message(message)


def notify(line, cell=None):
    try:
        get_ipython().ex(cell if cell else line)
        slack_success()
    except Exception as exc:
        tb = IPython.core.ultratb.VerboseTB(color_scheme="NoColor", include_vars=False)
        error = tb.text(*sys.exc_info())
        slack_error(error)
        raise

def load_ipython_extension(ipython):
    ipython.register_magic_function(notify, "line_cell")

