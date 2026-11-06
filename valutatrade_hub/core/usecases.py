import hashlib
import json
import os
from datetime import datetime

from valutatrade_hub.core.currencies import get_currency
from valutatrade_hub.core.exceptions import (
    InsufficientFundsError,
)
from valutatrade_hub.core.models import User
from valutatrade_hub.infra.settings import SettingsLoader

current_user = None

# Singleton: единая точка настроек (используется для путей к данным)
settings = SettingsLoader()
# Используем Singleton для получения пути к данным
DATA_DIR = settings.data_dir
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PORTFOLIOS_FILE = os.path.join(DATA_DIR, "portfolios.json")
EXCHANGE_RATES = {
    "USD_USD": 1.0,
    "EUR_USD": 1.0786,
    "BTC_USD": 59337.21,
    "ETH_USD": 3720.00,
    "RUB_USD": 0.01016,
}


# служебные функции
def create_files_if_not_exist():
    """Создаёт папку data и пустые JSON-файлы, если их нет."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for filepath in (USERS_FILE, PORTFOLIOS_FILE):
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f)


def load_json(filepath):
    """Читает JSON-файл."""
    create_files_if_not_exist()
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """Сохраняет данные в JSON-файл."""
    create_files_if_not_exist()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# бизнес-функции
def register(username: str, password: str):
    """Cоздать нового пользователя."""
    users = load_json(USERS_FILE)
    new_user_dic = {}

    for u in users:
        if u["username"] == username:
            raise ValueError(f"Имя пользователя {username} уже занято")

    new_user = User(len(users) + 1, username, password)
    new_user_dic["user_id"] = new_user.user_id
    new_user_dic["username"] = new_user.username
    new_user_dic["hashed_password"] = new_user.password
    new_user_dic["salt"] = new_user.salt
    new_user_dic["registration_date"] = new_user.registration_date.isoformat()
    users.append(new_user_dic)
    save_json(USERS_FILE, users)
    print(
        f"Пользователь {new_user.username} зарегистрирован (id={new_user.user_id}). "
        f"Войдите: login --username {new_user.username} --password **** "
    )

    portfolios = load_json(PORTFOLIOS_FILE)
    user_portfolios_dic = {}
    user_portfolios_dic["user_id"] = new_user.user_id
    user_portfolios_dic["wallets"] = {}
    portfolios.append(user_portfolios_dic)
    save_json(PORTFOLIOS_FILE, portfolios)


def login(username: str, password: str):
    """Войти и зафиксировать текущую сессию пользователя."""
    users = load_json(USERS_FILE)

    found_user = None
    for u in users:
        if u["username"] == username:
            found_user = u
            break

    if found_user is None:
        raise ValueError(f"Пользователь {username} не найден")

    if (
        found_user["hashed_password"]
        != hashlib.sha256((password + found_user["salt"]).encode("utf-8")).hexdigest()
    ):
        raise ValueError("Неверный пароль")

    global current_user
    current_user = found_user
    print(f"Вы вошли как '{username}'")


def show_portfolio(base: str = "USD"):
    """Показать все кошельки и итоговую стоимость в базовой валюте (по умолчанию USD)."""
    if current_user is None:
        raise ValueError("Сначала выполните login")

    portfolios = load_json(PORTFOLIOS_FILE)

    current_user_portfolio = None
    for portfolio in portfolios:
        if portfolio["user_id"] == current_user["user_id"]:
            current_user_portfolio = portfolio
            break

    if current_user_portfolio is None:
        raise ValueError("Портфель не найден")

    wallets = current_user_portfolio["wallets"]
    if not wallets:
        print("Портфель пуст. Купите валюту: buy --currency BTC --amount 0.05")
        return

    currency = base.upper()

    print(f"Портфель пользователя '{current_user['username']}' (база: {currency}):")
    total_sum = 0

    for currency in current_user_portfolio["wallets"]:
        current_user_portfolio_wallet_currency_balance = current_user_portfolio[
            "wallets"
        ][currency]["balance"]
        exchange_rate = EXCHANGE_RATES.get(f"{currency}_USD", 0)
        print(
            f"- {currency}: {current_user_portfolio_wallet_currency_balance} →  "
            f"{current_user_portfolio_wallet_currency_balance * exchange_rate:.2f} {base.upper()}"
        )
        total_sum += current_user_portfolio_wallet_currency_balance * exchange_rate
    print("---------------------------------")
    print(f"ИТОГО: {total_sum:,.2f} {base.upper()}")


def buy(currency: str, amount: float):
    """Купить валюту."""
    if current_user is None:
        raise ValueError("Сначала выполните login")

    portfolios = load_json(PORTFOLIOS_FILE)

    if not isinstance(amount, (int, float)):
        raise TypeError(f"Некорректный тип данных '{amount}'")

    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля")

    current_user_portfolio = None
    for portfolio in portfolios:
        if portfolio["user_id"] == current_user["user_id"]:
            current_user_portfolio = portfolio
            break

    if current_user_portfolio is None:
        raise ValueError("Портфель не найден")

    currency = currency.upper()
    get_currency(currency)

    if currency in current_user_portfolio["wallets"]:
        current_user_portfolio_balance_before = current_user_portfolio["wallets"][
            currency
        ]["balance"]
        current_user_portfolio["wallets"][currency]["balance"] += amount
    else:
        current_user_portfolio_balance_before = 0
        current_user_portfolio["wallets"][currency] = {"balance": amount}

    current_user_portfolio_balance_after = current_user_portfolio["wallets"][currency][
        "balance"
    ]

    save_json(PORTFOLIOS_FILE, portfolios)

    exchange_rate = EXCHANGE_RATES.get(f"{currency}_USD", 0)
    print(
        f"Покупка выполнена: {amount} {currency} по курсу {exchange_rate} USD/{currency}"
    )
    print("Изменения в портфеле:")
    print(
        f"- {currency}: было {current_user_portfolio_balance_before} → стало {current_user_portfolio_balance_after}"
    )
    print(f"Оценочная стоимость покупки: {exchange_rate * amount:.2f} USD")


def sell(currency: str, amount: float):
    """Продать валюту."""
    portfolios = load_json(PORTFOLIOS_FILE)

    if current_user is None:
        raise ValueError("Сначала выполните login")

    if not isinstance(amount, (int, float)):
        raise TypeError(f"Некорректный тип данных '{amount}'")

    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля")

    current_user_portfolio = None
    for portfolio in portfolios:
        if portfolio["user_id"] == current_user["user_id"]:
            current_user_portfolio = portfolio
            break

    if current_user_portfolio is None:
        raise ValueError("Портфель не найден")

    currency = currency.upper()
    get_currency(currency)

    if currency in current_user_portfolio["wallets"]:
        current_user_portfolio_balance_before = current_user_portfolio["wallets"][
            currency
        ]["balance"]
        if current_user_portfolio["wallets"][currency]["balance"] >= amount:
            current_user_portfolio["wallets"][currency]["balance"] -= amount
        else:
            raise InsufficientFundsError(
                f"Недостаточно средств: доступно {current_user_portfolio_balance_before} {currency}, "
                f"требуется {amount} {currency}"
            )
    else:
        raise ValueError(
            f"У вас нет кошелька '{currency}'. "
            f"Добавьте валюту: она создаётся автоматически при первой покупке."
        )

    current_user_portfolio_balance_after = current_user_portfolio["wallets"][currency][
        "balance"
    ]

    save_json(PORTFOLIOS_FILE, portfolios)

    exchange_rate = EXCHANGE_RATES.get(f"{currency}_USD", 0)
    print(
        f"Продажа выполнена: {amount} {currency} по курсу {exchange_rate} USD/{currency}"
    )
    print("Изменения в портфеле:")
    print(
        f"- {currency}: было {current_user_portfolio_balance_before} → стало {current_user_portfolio_balance_after}"
    )
    print(f"Оценочная выручка: {exchange_rate * amount:.2f} USD")


def get_rate(from_: str, to_: str):
    """Получить текущий курс одной валюты к другой."""
    get_currency(from_)
    get_currency(to_)

    pair = f"{from_}_{to_}"
    reverse_pair = f"{to_}_{from_}"

    if pair in EXCHANGE_RATES:
        rate = EXCHANGE_RATES[pair]
        print(f"Курс {pair}: {rate} (обновлено: {datetime.now()})")
        print(f"Обратный курс {reverse_pair}: {1 / EXCHANGE_RATES[pair]:.8f}")
        return

    if reverse_pair in EXCHANGE_RATES:
        rate = 1 / EXCHANGE_RATES[reverse_pair]
        print(f"Курс {pair}: {rate:.8f} (обновлено: {datetime.now()})")
        print(f"Обратный курс {reverse_pair}: {EXCHANGE_RATES[reverse_pair]}")
        return

    print(f"Курс {pair} недоступен. Повторите попытку позже.")
