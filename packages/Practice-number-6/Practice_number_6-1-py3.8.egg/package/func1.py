def output(check, *args):
    if check == 1:
        args = args[0]
    if not args:
        return iter(((),))
    return (items + (item,)
            for items in output(0, *args[:-1]) for item in args[-1])


def filling():
    temp_list = []
    temp = ''
    while temp != 'exit':
        temp = input('Введите последовательность или exit для выхода')
        if temp != 'exit':
            temp_list.append(temp.split())
    return temp_list


def main():
    menu = ''
    while menu != 'exit':
        print('1.Декартовая сумма новых последовательностей(new)')
        menu = input('2.Выход(exit)\n')
        if menu == 'new':
            print(list(output(1, filling())))

