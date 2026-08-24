#!/usr/bin/env python3
import json
import sys

import checklib
import requests

from api import API
from utils import generate_extended_str, generate_passport, generate_str, random_date

PORT = 1337


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
            self.cquit(
                checklib.Status.DOWN, "Connection error", f"Requests error {error!r}"
            )

    def check(self):
        api_user = API(self.host, PORT)
        username = generate_str()
        password = generate_extended_str()
        personal_data = generate_passport()
        api_user.register(username, personal_data, password)
        if "Logout" not in api_user.get_index():
            self.cquit(checklib.Status.MUMBLE, "User not registered")

        users = api_user.get_users()
        if username not in [user[1] for user in users["list"]]:
            self.cquit(checklib.Status.MUMBLE, "User not in list of users")

        api_user.logout()
        if "Create account" not in api_user.get_index():
            self.cquit(checklib.Status.MUMBLE, "User cannot logout")

        api_user.login(username, password)
        if "Logout" not in api_user.get_index():
            self.cquit(checklib.Status.MUMBLE, "User cannot login")

        profile = api_user.get_profile()
        if username not in profile or personal_data not in profile:
            self.cquit(checklib.Status.MUMBLE, "User profile works incorrectly")

        name = f"{generate_str()} {generate_str()}"
        date = random_date()
        insurance_num = generate_passport()
        doctor = "Ryan Gosling"
        response = api_user.create_app(name, date, insurance_num, doctor)
        if response.status_code != 200 or "info" not in response.url:
            self.cquit(checklib.Status.MUMBLE, "Cannot create appointment")

        app_id = response.url.split("/")[-2]
        app_text = api_user.get_app(app_id)
        if (
            name not in app_text
            or insurance_num not in app_text
            or doctor not in app_text
        ):
            self.cquit(checklib.Status.MUMBLE, "Appointment info works incorrectly")
        self.cquit(checklib.Status.OK)

    def put(self, _flag_id: str, flag: str, vuln: str):
        if vuln == "1":
            self._put_personal_data(flag)
        if vuln == "2":
            self._put_insurance_num(flag)
        self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

    def get(self, flag_id: str, flag: str, vuln: str):
        if vuln == "1":
            self._get_personal_data(flag_id, flag)
        if vuln == "2":
            self._get_insurance_num(flag_id, flag)
        self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

    def _put_personal_data(self, flag: str):
        api_user = API(self.host, PORT)
        username = generate_str()
        password = generate_extended_str()
        api_user.register(username, flag, password)
        if "Logout" not in api_user.get_index():
            self.cquit(checklib.Status.MUMBLE, "User not registered")
        self.cquit(
            checklib.Status.OK,
            username,
            json.dumps({"username": username, "password": password}),
        )

    def _get_personal_data(self, flag_id: str, flag: str):
        data = json.loads(flag_id)
        api_user = API(self.host, PORT)
        api_user.login(data["username"], data["password"])
        if "Logout" not in api_user.get_index():
            self.cquit(checklib.Status.CORRUPT, "Cannot login to retrieve flag")
        if flag not in api_user.get_profile():
            self.cquit(checklib.Status.CORRUPT, "Cannot retrieve flag")
        self.cquit(checklib.Status.OK)

    def _put_insurance_num(self, flag: str):
        api_user = API(self.host, PORT)
        username = generate_str()
        password = generate_extended_str()
        api_user.register(username, generate_passport(), password)
        if "Logout" not in api_user.get_index():
            self.cquit(checklib.Status.MUMBLE, "User not registered")

        response = api_user.create_app(
            f"{generate_str()} {generate_str()}", random_date(), flag, "Ryan Gosling"
        )
        if response.status_code != 200 or "info" not in response.url:
            self.cquit(checklib.Status.MUMBLE, "Cannot create appointment")
        app_id = response.url.split("/")[-2]
        private = json.dumps(
            {"username": username, "password": password, "app_id": app_id}
        )
        self.cquit(checklib.Status.OK, username, private)

    def _get_insurance_num(self, flag_id: str, flag: str):
        data = json.loads(flag_id)
        api_user = API(self.host, PORT)
        api_user.login(data["username"], data["password"])
        if "Logout" not in api_user.get_index():
            self.cquit(checklib.Status.CORRUPT, "Cannot login to retrieve flag")
        if flag not in api_user.get_app(data["app_id"]):
            self.cquit(checklib.Status.CORRUPT, "Cannot retrieve flag")
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
