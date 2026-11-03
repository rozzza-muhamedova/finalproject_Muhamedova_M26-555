import hashlib
import random


class User:
    """Класс User (пользователь системы)."""
    def __init__(self, user_id: int, username: str, password: str):
        self._user_id = user_id
        self.username = username
        self._salt = str(random.randint(10000, 99999))
        self.password = password
        
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        if username == '':
            raise ValueError('Имя не может быть пустым')
        else:
            self._username = username

    @property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, password: str):
        if len(password) < 4:
            raise ValueError('Пароль должен содержать более 4 символов')
        else:
            self._hashed_password = hashlib.sha256((password + self._salt).encode('utf-8')).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        input_password = hashlib.sha256((password + self._salt).encode('utf-8')).hexdigest()
        return input_password == self._hashed_password
    
    def change_password(self, new_password: str):
        self.password = new_password

    def get_user_info(self):
        return (f'Информация о пользователе с user_id: {self._user_id}\n'
               f'Имя пользователя: {self._username}')

    
class Wallet:
    """Класс Wallet (кошелёк пользователя для одной конкретной валюты)."""
    def __init__(self, currency_code: str, balance: float = 0.0):
        self.currency_code = currency_code.upper()
        self._balance = 0.0
        self.balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError('Отрицательное значение запрещено')
        elif not isinstance(amount, (int, float)):
            raise ValueError('Некорректный тип данных')
        else:
            self._balance = amount

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("На текущем балансе недостаточно средств")

    def get_balance_info(self):
        return f'Текущий баланс {self._balance}'

class Portfolio:
    """Класс Portfolio (управление всеми кошельками одного пользователя)."""
    def __init__(self, user_id: int):
        self._user_id = user_id
        self._wallets = {}

    @property
    def user_id(self):
        return self._user_id

    @property
    def wallets(self):
        return self._wallets.copy()

    def add_currency(self, currency_code: str):
        if currency_code in self._wallets:
            raise ValueError(f"Кошелёк для {currency_code} уже существует")
        else:
            self._wallets[currency_code] = Wallet(currency_code)
    
    def get_wallet(self, currency_code):
        if currency_code not in self._wallets:
            raise ValueError(f"Кошелёка для {currency_code} не существует")
        else:
            return self._wallets[currency_code]
    
    def get_total_value(self, base_currency='USD'):
        exchange_rates = {
            'USD': 1.0,
            'EUR': 1.07,
            'BTC': 59337.21,
            'ETH': 3720.00,
            'RUB': 0.01016,
        }
        
        total_value = 0.0
        for code, wallet in self._wallets.items():
            if code in exchange_rates:
                total_value += wallet.balance * exchange_rates[code]
        
        return total_value
    




    





    
