import sys
import numpy as np
from termcolor import cprint as __,\
                      colored as _c
from copy import deepcopy
from random import choice, randint as ri



def int_to_list(num):
    """Преобразование числа в список цифр"""
    result = []

    while num > 0:
        result.append(num % 10)
        num //= 10
    result.reverse()

    return result


def list_to_int(arr):
    """Преобразование списока цифр в число"""
    num = 0
    for i, v in enumerate(reversed(arr)):
        num += v * 10 ** i
    return num


def rules(num):
    """
    Метод для генерации перестановок по прямому и обратному правилу

    :param num: начальное число
    :return: список чисел или одно число
    """
    result = []
    lenght = len(str(num))
    digits = int_to_list(num)

    for i in range(len(digits)-1):
        copy = deepcopy(digits)
        first = copy.pop(i)
        second = copy.pop(i)

        if lenght & 1:
            copy.insert(0, first)
            copy.append(second)
        elif not lenght & 1:
            copy.insert(0, second)
            copy.append(first)
        else:
            raise ValueError

        result.append(list_to_int(copy))

    return result


def pair(num):
    """
    Случайная перестановка числа

    :param num: целевое число
    :return: одна случайная перестановка
    """
    length = len(str(num))
    rnd = ri(0, length-2)
    digits = int_to_list(num)

    if length & 1:
        digits.insert(0, digits.pop(rnd))
        digits.append(digits.pop(rnd+1))
    elif not length & 1:
        digits.append(digits.pop(rnd))
        digits.insert(0, digits.pop(rnd))
    else:
        raise ValueError

    return list_to_int(digits)


def in_width(start, find):
    """
    Генерация в глубину

    :param start: начальное число
    :param find: целевое число
    :return: количество итераций,
             за которое было найдено целевое число
    """
    if start == find:
        return 0

    iterations = 0
    queue = [start]

    while len(queue) > 0:
        new_queue = []
        for elem in queue:
            swap = rules(elem)
            new_queue.extend(swap)
        iterations += 1
        queue = deepcopy(new_queue)

        if find in queue:
            return iterations


def in_depth(start, find, tests):
    """
    Генерация в глубину

    :param start: начальное число
    :param find: целевое число
    :param tests: кол-во испытаний
    :return: список из test элементов,
             содержащий количество итераций,
             которое потребовалось на каждом из испытаний,
             чтобы найти целевое число
    """
    iterations = [0 for i in range(tests)]

    for i in range(tests):
        following = start

        while True:
            swap = rules(following)
            iterations[i] += 1

            if find not in swap:
                following = choice(swap)
            else:
                break

    return iterations


def by_beam(start, find, tests):
    """
    Генерация по лучу

    :param start: начальное число
    :param find: целевое число
    :param tests: кол-во испытаний
    :return: список из test элементов,
             содержащий количество итераций,
             которое потребовалось на каждом из испытаний,
             чтобы найти целевое число
    """
    iterations = [0 for i in range(tests)]

    for i in range(tests):
        if start == find:
            iterations[i] = 0
            continue

        following = start

        while True:
            swap = pair(following)
            iterations[i] += 1

            if swap != find:
                following = swap
            else:
                break

    return iterations


def parallel(start, find, tests):
    """
    Генерация Параллельная

    :param start: начальное число
    :param find: целевое число
    :param tests: кол-во испытаний
    :return: список из test элементов,
             содержащий количество итераций,
             которое потребовалось на каждом из испытаний,
             чтобы найти целевое число
    """
    iterations = [0 for i in range(tests)]

    for i in range(tests):
        queue = [i for i in rules(start)]

        if start == find:
            iterations[i] = 0
            continue
        elif find in queue:
            iterations[i] = 1
            continue

        iterations[i] += 1

        while True:
            for q in range(len(queue)):
                queue[q] = pair(queue[q])

            iterations[i] += 1

            if find in queue:
                break

    return iterations


def dialog():
    check = False
    first_num, find_num, tests_count = '', '', ''

    while not check:
        try:
            first_num = int(input('Введите начальное число: '))
            find_num = int(input('Ввелите целевое число: '))
            tests_count = int(input('Введите кол-во испытаний: '))
            check = True
        except ValueError:
            print('Какие-то данные были введены некорректно! Повторите попытку.')

    return first_num, find_num, tests_count


def test():
    s, f, t = dialog()

    width = in_width(s, f)
    depth = in_depth(s, f, t)
    beam = by_beam(s, f, t)
    along = parallel(s, f, t)

    print('\nРезультаты испытаний: ')
    print(f'Генерация в ширину: {width}')
    print(f'Генерация в глубину: {depth}')
    print(f'Генерация по лучу: {beam}')
    print(f'Генерация параллельным методом: {along}')

    print('\nДанные:\nГенерация в ширину:')
    print(f'\tМатематическое ожидание - {width}\n\tСреднеквадратическое отклонение - 0')
    print(f'Генарация в глубину:\n\tМатематическое ожидание - {round(np.mean(depth), 2)}\n\tСреднеквадратическое отклонение - {round(np.std(depth), 2)}')
    print(f'Генерация по лучу:\n\tМатематическое ожидание - {round(np.mean(beam), 2)}\n\tСреднеквадратическое отклонение - {round(np.std(beam), 2)}')
    print(f'Генерация параллельным методом:\n\tМатематическое ожидание - {round(np.mean(along), 2)}\n\tСреднеквадратическое отклонение - {round(np.std(along), 2)}')

    input('Нажмите [Enter], чтобы завершить работу программы...')


if __name__ == '__main__':
    sys.exit(test())
