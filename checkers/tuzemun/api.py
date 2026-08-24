import checklib

class API:
    def __init__(self, host:str, port:int):
        self._addr = f'http://{host}:{port}'
        self._session = checklib.get_initialized_session()
    
    def random_agent(func):
        def wrapper(self, *args, **kwargs):
            self._session.headers['User-Agent'] = checklib.rnd_useragent()
            return func(self, *args, **kwargs)
        return wrapper

    @random_agent
    def register(self, username, email, password):
        data = {'username':username,
                'email':email,
                'password1':password,
                'password2':password}
        res = self._session.post(f'{self._addr}/api/register', json=data)
        res.raise_for_status()

    @random_agent
    def login(self, username, password):
        data = {'username': username,
                'password': password}
        res = self._session.post(f'{self._addr}/api/login', json=data)
        res.raise_for_status()

    @random_agent
    def info(self):
        res = self._session.get(f'{self._addr}/api/info')
        res.raise_for_status()
        return res.json()

    @random_agent
    def send_request(self, fio, passport):
        data = {'fio': fio,
                'passport': passport}
        res = self._session.post(f'{self._addr}/api/send-request', json=data)
        res.raise_for_status()

    @random_agent
    def recovery_code(self):
        res = self._session.get(f'{self._addr}/api/recovery-code')
        res.raise_for_status()
        return res.json()

    @random_agent
    def reset_password(self, code, newpassword):
        data = {'code': code,
                'newpassword': newpassword}
        res = self._session.post(f'{self._addr}/api/reset-password', json=data)
        res.raise_for_status()

    @random_agent
    def logout(self):
        res = self._session.post(f'{self._addr}/api/logout')
        res.raise_for_status()
    
    def user(self):
        res = self._session.get(f'{self._addr}/api/user')
        res.raise_for_status()
        return res.json()

    @random_agent
    def custom(self, path, method='get', data=None):
        if method == 'get':
            req_func = self._session.get
        elif method == 'post':
            req_func = self._session.post
        else:
            return False, {}

        if data:
            res = req_func(f'{self._addr}{path}', json=data)
        else:
            res = req_func(f'{self._addr}{path}')

        res.raise_for_status()
        try:
            answer = res.json()
        except Exception:
            answer = res.text
        return True, answer
