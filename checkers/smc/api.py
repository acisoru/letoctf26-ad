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
    def register(self, username, personal_data, password):
        data = {'username': username, 'personalData': personal_data, 'password': password, 'passwordRep': password}
        res = self._session.post(f'{self._addr}/register', data=data)
        res.raise_for_status()

    @random_agent
    def create_app(self, name, date, ins_num, doctor):
        data = {'fio': name, 'timeStamp': date, 'insNum': ins_num, 'doctor': doctor}
        res = self._session.post(f'{self._addr}/appointments/create', data=data)
        res.raise_for_status()
        return res

    @random_agent
    def login(self, username, password):
        data = {'login': username, 'password': password}
        res = self._session.post(f'{self._addr}/login', data=data)
        res.raise_for_status()

    @random_agent
    def get_index(self):
        res = self._session.get(f'{self._addr}/index')
        res.raise_for_status()
        return res.text

    @random_agent
    def get_users(self):
        res = self._session.get(f'{self._addr}/api-dev/users')
        res.raise_for_status()
        return res.json()
    
    @random_agent
    def get_app_create(self):
        res = self._session.get(f'{self._addr}/appointments/create')
        res.raise_for_status()
        return res.text

    @random_agent
    def get_app(self, app_id):
        res = self._session.get(f'{self._addr}/appointments/{app_id}/info')
        res.raise_for_status()
        return res.text

    @random_agent
    def get_profile(self):
        res = self._session.get(f'{self._addr}/profile')
        res.raise_for_status()
        return res.text

    @random_agent
    def logout(self):
        res = self._session.get(f'{self._addr}/logout')
        res.raise_for_status()
