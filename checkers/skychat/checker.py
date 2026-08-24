#!/usr/bin/env python3
import json
import sys
from string import ascii_letters, digits
from base64 import b64encode
from random import randint, choice

import requests
import checklib
from requests.auth import HTTPBasicAuth

PORT = 31337
LOGIN_HTML_PATTERN = "http://{host}:{port}/"
REGISTER_API_PATTERN = "http://{host}:{port}/api/v1/register"
LOGIN_API_PATTERN = "http://{host}:{port}/api/v1/login"
CHATS_API_PATTERN = "http://{host}:{port}/api/v1/chats"
CHAT_ID_API_PATTERN = "http://{host}:{port}/api/v1/chats/{chat_id}"
DELETE_CHAT_API_PATTERN = "http://{host}:{port}/api/v1/delete_chat"
UPDATE_MSG_API_PATTERN = "http://{host}:{port}/api/v1/update_msg"
user_agents = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36	22.69",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3	15.84",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.1	10.62",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79	10.02",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36	5.22",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15	4.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67	3.91",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.	2.61",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36	2.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0	1.91",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Geck	1.86",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0	1.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.6	1.49",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3	1.49",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.7	1.49",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.5	0.93",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43	0.84",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.6	0.75",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4450.0 Safari/537.36	0.65",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.	0.19",
    "Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.	0.19",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.6	0.19",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Geck	0.19",
    "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0	0.19",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.3	0.19",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.	0.19",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36	0.14",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0	0.14",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57	0.14",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36	0.14",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35	0.14",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.72	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36	0.09",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.674 Yowser/2.5 Safari/537.36	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0	0.09",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0	0.09",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)	0.05",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36	0.05",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0	0.05",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0	0.05",
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0	0.05",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36	0.05",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.115	0.05",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67	0.05",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50	0.05",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41	0.05",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36	0.05",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36	0.05",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36	0.05",
]


def generate_string():
    return "".join(choice(ascii_letters + digits) for _ in range(randint(8, 20)))


def generate_msg():
    msg = choice(
        [
            "Enjoy yourself",
            "Your kindness. So kind of you!",
            "Let me see...",
            "I don't care!",
            "I wonder why.",
            "I tend to think.",
            "I'm glad.",
            "I am delighted.",
            "I don't mind.",
            "I'm off.",
            "I give up.",
            "I think so.",
            "I suppose so.",
            "Don't say anything else.",
            "Don't say anymore.",
            "And how?",
            "And how else?",
            "Oh hey you!",
            "Come to the point.",
            "Oh! come on.",
            "So far so good.",
            "Oh, no! It can't be!",
            "Let me digress.",
            "My goodness!",
            "What a situation!",
            "Do it at once!",
            "It's my pleasure.",
            "It's a pleasure for me.",
            "That's fantastic",
            "Now it's your turn.",
            "Oh sure. And of course",
            "Forget it.",
            "Wow, what a sight!",
            "Who cares!",
            "What a strange thing!",
            "How strange!",
            "What a mess!",
            "What's up?",
            "What a pity!",
            "Can't think what to say!",
            "What nonsense!",
            "How absurd!",
            "What an idea!",
            "What's the matter?",
            "How peaceful!",
            "What happened?",
            "Who knows!",
            "But who cares!",
            "Why should I care?",
            "Nothing is impossible.",
            "Little by little.",
            "Bit by bit.",
            "Forgive me. Pardon me.",
            "Be careful.",
            "Be careful driving.",
            "Can you translate this for me?",
            "Chicago is very different from Boston.",
            "Don't worry.",
            "Everyone knows it.",
            "Everything is ready.",
            "Excellent.",
            "From time to time.",
            "Good idea.",
            "He likes it very much.",
            "Help!",
            "He's coming soon.",
            "He's right.",
            "He's very annoying.",
            "He's very famous.",
            "How are you?",
            "How's work going?",
            "Hurry!",
            "I ate already.",
            "I can't hear you.",
            "I'd like to go for a walk.",
            "I don't know how to use it.",
            "I don't like him.",
            "I don't like it.",
            "I don't speak very well.",
            "I don't understand.",
            "I don't want it.",
            "I don't want that.",
            "I don't want to bother you.",
            "I feel good.",
            "If you need my help, please let me know.",
            "I get off of work at 6.",
            "I have a headache.",
            "I hope you and your wife have a nice trip.",
            "I know.",
            "I like her.",
            "I'll call you when I leave.",
            "I'll come back later.",
            "I'll pay.",
            "I'll take it.",
            "I'll take you to the bus stop.",
            "I lost my watch.",
            "I love you.",
            "I'm an American.",
            "I'm cleaning my room.",
            "I'm cold.",
            "I'm coming to pick you up.",
            "I'm going to leave.",
            "I'm good, and you?",
            "I'm happy.",
            "I'm hungry.",
            "I'm married.",
            "I'm not busy.",
            "I'm not married.",
            "I'm not ready yet.",
            "I'm not sure.",
            "I'm sorry, we're sold out.",
            "I'm thirsty.",
            "I'm very busy. I don't have time now.",
            "I need to change clothes.",
            "I need to go home.",
            "I only want a snack.",
            "Is Mr. Smith an American?",
            "Is that enough?",
            "I think it's very good.",
            "I think it tastes good.",
            "I thought the clothes were cheaper.",
            "It's longer than 2 miles.",
            "I've been here for two days.",
            "I've heard Texas is a beautiful place.",
            "I've never seen that before.",
            "I was about to leave the restaurant when my friends arrived.",
            "Just a little.",
            "Just a moment.",
            "Let me check.",
            "Let me think about it.",
            "Let's go have a look.",
            "Let's practice English.",
            "May I speak to Mrs. Smith please?",
            "More than that.",
            "Never mind.",
            "Next time.",
            "No.",
            "Nonsense.",
            "No, thank you.",
            "Nothing else.",
            "Not recently.",
            "Not yet.",
            "Of course.",
            "Okay.",
            "Please fill out this form.",
            "Please take me to this address.",
            "Please write it down.",
            "Really?",
            "Right here.",
            "Right there.",
            "See you later.",
            "See you tomorrow.",
            "See you tonight.",
            "She's pretty.",
            "Sorry to bother you.",
            "Stop!",
            "Take a chance.",
            "Take it outside.",
            "Tell me.",
            "Thanks for everything.",
            "Thanks for your help.",
            "Thank you.",
            "Thank you miss.",
            "Thank you sir.",
            "Thank you very much.",
            "That looks great.",
            "That's alright.",
            "That's enough.",
            "That's fine.",
            "That's it.",
            "That smells bad.",
            "That's not fair.",
            "That's not right.",
            "That's right.",
            "That's too bad.",
            "That's too many.",
            "That's too much.",
            "The book is under the table.",
            "They'll be right back.",
            "They're the same.",
            "They're very busy.",
            "This doesn't work.",
            "This is very difficult.",
            "This is very important.",
            "Try it.",
            "Very good, thanks.",
            "We like it very much.",
            "Would you take a message please?",
            "Yes, really.",
            "You're beautiful.",
            "You're very nice.",
            "You're very smart.",
            "Your things are all here.",
        ]
    )
    return b64encode(msg.encode()).decode()


def open_main_page(hostname):
    r = requests.get(
        LOGIN_HTML_PATTERN.format(host=hostname, port=PORT),
        headers={"User-Agent": choice(user_agents)},
        timeout=5,
    )
    return r.status_code == 200


def create_user(hostname, login, password):
    r = requests.post(
        REGISTER_API_PATTERN.format(host=hostname, port=PORT),
        timeout=5,
        headers={"User-Agent": choice(user_agents)},
        json={"login": login, "password": password},
    )
    return r.json()["id"] if r.status_code == 201 else False


def login_user(hostname, login, password):
    r = requests.post(
        LOGIN_API_PATTERN.format(host=hostname, port=PORT),
        timeout=5,
        headers={"User-Agent": choice(user_agents)},
        json={"login": login, "password": password},
    )
    return r.json()["id"] if r.status_code == 200 else False


def create_chat(hostname, login, password):
    r = requests.post(
        CHATS_API_PATTERN.format(host=hostname, port=PORT),
        timeout=5,
        headers={"User-Agent": choice(user_agents)},
        auth=HTTPBasicAuth(login, password),
    )
    return r.status_code == 200


def get_chat(hostname, login, password):
    r = requests.get(
        CHATS_API_PATTERN.format(host=hostname, port=PORT),
        timeout=5,
        headers={"User-Agent": choice(user_agents)},
        auth=HTTPBasicAuth(login, password),
    )
    return r.json()["data"][0]["id"] if r.status_code == 200 else False


def post_message(hostname, login, password, chat_id, text, direction):
    r = requests.post(
        CHAT_ID_API_PATTERN.format(host=hostname, port=PORT, chat_id=chat_id),
        timeout=5,
        headers={"User-Agent": choice(user_agents)},
        auth=HTTPBasicAuth(login, password),
        json={"text": text, "direction": direction},
    )
    return r.status_code == 200


def get_messages(hostname, login, password, chat_id):
    r = requests.get(
        CHAT_ID_API_PATTERN.format(host=hostname, port=PORT, chat_id=chat_id),
        timeout=5,
        headers={"User-Agent": choice(user_agents)},
        auth=HTTPBasicAuth(login, password),
    )
    if r.status_code != 200:
        return False
    return [msg["text"] for msg in r.json()["data"]]


def delete_chat(hostname, login, password, chat_id, user_id):
    r = requests.post(
        DELETE_CHAT_API_PATTERN.format(host=hostname, port=PORT),
        timeout=5,
        headers={"User-Agent": choice(user_agents)},
        auth=HTTPBasicAuth(login, password),
        json={"chat_id": chat_id, "user_id": user_id},
    )
    return r.status_code == 200


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
        if not open_main_page(self.host):
            self.cquit(checklib.Status.DOWN, "Can't open main page")
        username, password = generate_string(), generate_string()
        if not (user_id := create_user(self.host, username, password)):
            self.cquit(checklib.Status.MUMBLE, "Can't register")
        if not login_user(self.host, username, password):
            self.cquit(checklib.Status.MUMBLE, "Can't login")
        if not create_chat(self.host, username, password):
            self.cquit(checklib.Status.MUMBLE, "Can't create chat")
        if not (chat_id := get_chat(self.host, username, password)):
            self.cquit(checklib.Status.MUMBLE, "Can't get list of chats")
        msg1, msg2 = generate_msg(), generate_msg()
        if not post_message(self.host, username, password, chat_id, msg1, True):
            self.cquit(checklib.Status.MUMBLE, "Can't post message")
        if not post_message(self.host, username, password, chat_id, msg2, False):
            self.cquit(checklib.Status.MUMBLE, "Can't post message")
        messages = get_messages(self.host, username, password, chat_id)
        if not messages:
            self.cquit(checklib.Status.MUMBLE, "Can't get list of messages")
        if len(messages) < 2 or messages[0] != msg1 or messages[1] != msg2:
            self.cquit(checklib.Status.MUMBLE, "Retrieved messages are not the same")
        if not delete_chat(self.host, username, password, chat_id, user_id):
            self.cquit(checklib.Status.MUMBLE, "Can't delete chat")
        self.cquit(checklib.Status.OK)

    def put(self, _flag_id: str, flag: str, vuln: str):
        if vuln == "1":
            self._put_password(flag)
        if vuln == "2":
            self._put_message(flag)
        self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

    def get(self, flag_id: str, flag: str, vuln: str):
        if vuln == "1":
            self._get_password(flag_id)
        if vuln == "2":
            self._get_message(flag_id, flag)
        self.cquit(checklib.Status.ERROR, "Checker failed", f"Invalid vuln: {vuln}")

    def _put_password(self, flag: str):
        username = generate_string()
        if not create_user(self.host, username, flag):
            self.cquit(checklib.Status.MUMBLE, "Can't register")
        private = json.dumps({"username": username, "password": flag})
        self.cquit(checklib.Status.OK, username, private)

    def _get_password(self, flag_id: str):
        data = json.loads(flag_id)
        if not login_user(self.host, data["username"], data["password"]):
            self.cquit(checklib.Status.CORRUPT, "Can't login")
        if login_user(
            self.host, data["username"], data["password"] + generate_string()
        ):
            self.cquit(checklib.Status.CORRUPT, "Invalid password accepted")
        self.cquit(checklib.Status.OK)

    def _put_message(self, flag: str):
        username, password = generate_string(), generate_string()
        if not create_user(self.host, username, password):
            self.cquit(checklib.Status.MUMBLE, "Can't register")
        if not create_chat(self.host, username, password):
            self.cquit(checklib.Status.MUMBLE, "Can't create chat")
        chat_id = get_chat(self.host, username, password)
        if not chat_id:
            self.cquit(checklib.Status.MUMBLE, "Can't get list of chats")
        message2 = generate_msg()
        if not post_message(self.host, username, password, chat_id, flag, True):
            self.cquit(checklib.Status.MUMBLE, "Can't post message")
        if not post_message(self.host, username, password, chat_id, message2, False):
            self.cquit(checklib.Status.MUMBLE, "Can't post message")
        private = json.dumps(
            {"username": username, "password": password, "message2": message2}
        )
        self.cquit(checklib.Status.OK, username, private)

    def _get_message(self, flag_id: str, flag: str):
        data = json.loads(flag_id)
        if not login_user(self.host, data["username"], data["password"]):
            self.cquit(checklib.Status.MUMBLE, "Can't login")
        chat_id = get_chat(self.host, data["username"], data["password"])
        if not chat_id:
            self.cquit(checklib.Status.MUMBLE, "Can't get list of chats")
        messages = get_messages(self.host, data["username"], data["password"], chat_id)
        if not messages:
            self.cquit(checklib.Status.MUMBLE, "Can't get list of messages")
        if len(messages) < 2 or messages[0] != flag or messages[1] != data["message2"]:
            self.cquit(checklib.Status.CORRUPT, "Can't get messages")
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
