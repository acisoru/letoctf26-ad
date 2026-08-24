#!/usr/bin/env python3
import json
import random
import sys

import checklib
import requests

PORT = 2222
CHECK_URL_PATTERN = "http://{hostname}:{port}/check"
PUT_URL_PATTERN = "http://{hostname}:{port}/put"
GET_URL_PATTERN = "http://{hostname}:{port}/get?username={username}&token={token}"


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
        check_url = CHECK_URL_PATTERN.format(hostname=self.host, port=PORT)
        response = requests.get(check_url, timeout=self.timeout)
        response.raise_for_status()
        self.cquit(checklib.Status.OK)

    def put(self, _flag_id: str, flag: str, vuln: str):
        if vuln not in {"1", "2"}:
            self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

        rand_int = random.randint(0, 10000000)
        username = f"user_{rand_int}"
        token = f"token_{rand_int}"
        data = {"flag": flag, "username": username, "token": token}

        put_url = PUT_URL_PATTERN.format(hostname=self.host, port=PORT)
        response = requests.post(put_url, timeout=self.timeout, json=data)
        response.raise_for_status()
        self.cquit(checklib.Status.OK, username, json.dumps(data))

    def get(self, flag_id: str, flag: str, vuln: str):
        if vuln not in {"1", "2"}:
            self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

        data = json.loads(flag_id)
        get_url = GET_URL_PATTERN.format(
            hostname=self.host,
            port=PORT,
            username=data["username"],
            token=data["token"],
        )
        response = requests.get(get_url, timeout=self.timeout)
        response.raise_for_status()
        if response.text != flag:
            self.cquit(checklib.Status.CORRUPT, "Wrong flag", f"Wrong flag: {response.text!r}")
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
