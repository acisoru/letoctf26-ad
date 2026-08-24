#!/usr/bin/env python3
import json
import sys

import checklib
import requests

from api import API
from utils import generate_email, generate_extended_str, generate_passport, generate_str

PORT = 8137


class Checker(checklib.BaseChecker):
    vulns = 2
    timeout = 10
    uses_attack_data = True

    def action(self, action, *args, **kwargs):
        try:
            super().action(action, *args, **kwargs)
        except self.get_check_finished_exception():
            raise
        except requests.RequestException as error:
            self.cquit(checklib.Status.DOWN, "Connection error", f"Requests error {error!r}")

    def check(self):
        api_user = API(self.host, PORT)
        username = generate_str()
        password = generate_extended_str()
        api_user.register(username, generate_email(), password)
        api_user.login(username, password)
        code = api_user.recovery_code()["code"]
        api_user.logout()

        new_password = generate_extended_str()
        api_user.reset_password(code, new_password)
        api_user.login(username, new_password)
        if api_user.user()["username"] != username:
            self.cquit(checklib.Status.MUMBLE, "Wrong user returned")
        if api_user.info() != {}:
            self.cquit(checklib.Status.MUMBLE, "Wrong info returned")

        fio = generate_str()
        passport = generate_passport()
        api_user.send_request(fio, passport)
        info = api_user.info()[0]
        if info["fio"] != fio or info["passport"] != passport or info["approved"] is not False:
            self.cquit(checklib.Status.MUMBLE, "Wrong info returned")
        self.cquit(checklib.Status.OK)

    def put(self, _flag_id: str, flag: str, vuln: str):
        if vuln == "1":
            self._put_username(flag)
        if vuln == "2":
            self._put_passport(flag)
        self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

    def get(self, flag_id: str, flag: str, vuln: str):
        if vuln == "1":
            self._get_username(flag_id, flag)
        if vuln == "2":
            self._get_passport(flag_id, flag)
        self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

    def _put_username(self, flag: str):
        password = generate_extended_str()
        email = generate_email()
        API(self.host, PORT).register(flag, email, password)
        self.cquit(checklib.Status.OK, email, json.dumps({"password": password}))

    def _get_username(self, flag_id: str, flag: str):
        password = json.loads(flag_id)["password"]
        api_user = API(self.host, PORT)
        try:
            api_user.login(flag, password)
        except requests.exceptions.HTTPError as error:
            self.cquit(checklib.Status.CORRUPT, "Cannot login to retrieve flag", str(error))
        if api_user.info() != {}:
            self.cquit(checklib.Status.CORRUPT, "Wrong info returned")
        if api_user.user()["username"] != flag:
            self.cquit(checklib.Status.CORRUPT, "Wrong user returned")
        self.cquit(checklib.Status.OK)

    def _put_passport(self, flag: str):
        api_user = API(self.host, PORT)
        username = generate_str()
        password = generate_extended_str()
        api_user.register(username, generate_email(), password)
        api_user.login(username, password)
        if api_user.info() != {}:
            self.cquit(checklib.Status.MUMBLE, "Wrong info returned")

        fio = generate_str()
        api_user.send_request(fio, flag)
        info = api_user.info()[0]
        if info["fio"] != fio or info["passport"] != flag or info["approved"] is not False:
            self.cquit(checklib.Status.MUMBLE, "Wrong info returned")
        private = json.dumps({"username": username, "password": password, "fio": fio})
        self.cquit(checklib.Status.OK, username, private)

    def _get_passport(self, flag_id: str, flag: str):
        data = json.loads(flag_id)
        api_user = API(self.host, PORT)
        api_user.login(data["username"], data["password"])
        info = api_user.info()[0]
        if info["fio"] != data["fio"] or info["passport"] != flag or info["approved"] is not False:
            self.cquit(checklib.Status.CORRUPT, "Wrong info returned")
        self.cquit(checklib.Status.OK)


if __name__ == "__main__":
    host = sys.argv[2]
    checker = Checker(host)

    try:
        action = sys.argv[1]
        arguments = sys.argv[3:]
        checker.action(action, *arguments)
    except checker.get_check_finished_exception():
        checklib.cquit(checklib.Status(checker.status), checker.public, checker.private)
