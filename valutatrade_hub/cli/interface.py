import shlex

from valutatrade_hub.core.usecases import register, login, show_portfolio, buy, sell, get_rate

def run_cli():
    while True:
        input_command = input(">>>Введите команду: ")
        args = shlex.split(input_command)
        if len(args) == 0:
            continue
        command = args[0]

        if command == 'register':
            if len(args) < 5 or args[1] != '--username' or args[3] != '--password':
                print("Неверный синтаксис команды. Использование: register --username <name> --password <pass>")
                continue
            username = args[2]
            password = args[4]
            try:
                register(username, password)
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif command == 'login':
            if len(args) < 5 or args[1] != '--username' or args[3] != '--password':
                print("Неверный синтаксис команды. Использование: login --username <name> --password <pass>")
                continue
            username = args[2]
            password = args[4]
            try:
                login(username, password)
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif command == 'show-portfolio':
            if len(args) == 1:
                base = 'USD'
            elif len(args) == 3 and args[1] == '--base':
                base = args[2]
            else:
                print("Неверный синтаксис. Использование: show-portfolio / show-portfolio --base <currency>")
                continue
            try:
                show_portfolio(base)
            except ValueError as e:
                print(f"Ошибка: {e}")
            
        elif command == 'buy':
            if len(args) < 5 or args[1] != '--currency' or args[3] != '--amount':
                print("Неверный синтаксис команды. Использование: buy --currency <currency> --amount <amount>")
                continue
            currency = args[2]
            try:
                amount = float(args[4])
            except ValueError:
                print("Ошибка: сумма должна быть числом")
                continue
            try:
                buy(currency, amount)
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif command == 'sell':
            if len(args) < 5 or args[1] != '--currency' or args[3] != '--amount':
                print("Неверный синтаксис команды. Использование: sell --currency <currency> --amount <amount>")
                continue
            currency = args[2]
            try:
                amount = float(args[4])
            except ValueError:
                print("Ошибка: сумма должна быть числом")
                continue
            try:
                sell(currency, amount)
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif command == 'get-rate':
            if len(args) < 5 or args[1] != '--from' or args[3] != '--to':
                print("Неверный синтаксис команды. Использование: get-rate --from <currency> --to <currency>")
                continue
            from_ = args[2]
            to_ = args[4]
            try:
                get_rate(from_, to_)
            except ValueError as e:
                print(f"Ошибка: {e}")


        elif command == "exit":
                break
        else:
            print(f'Команды {command} нет. Попробуйте снова.')