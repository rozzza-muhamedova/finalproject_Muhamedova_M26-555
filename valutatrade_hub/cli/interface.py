import shlex

from valutatrade_hub.core.usecases import register, login, show_portfolio, buy, sell, get_rate

while True:
    input_command = input(">>>Введите команду: ")
    args = shlex.split(input_command)
    if len(args) == 0:
        continue
    command = args[0]

    if command == 'register':
        pass

    elif command == 'login':
        pass

    elif command == 'show-portfolio':
        pass

    elif command == 'buy':
        pass

    elif command == 'sell':
        pass

    elif command == 'get-rate':
        pass

    elif command == "exit":
            break
    else:
        print(f'Функции {command} нет. Попробуйте снова.')
