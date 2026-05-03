def result_modifyer(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return f"Result is: {result}"

    return wrapper

@result_modifyer
def tsum(a, b):
    return a + b

@result_modifyer
def tmul(a, b):
    return a * b

assert(tsum(2, 3) == "Result is: 5")
assert(tmul(2, 3) == "Result is: 6")
print('Отлично, это работает! +2 балла тебе!')


def sized_cacher(size):
    cache = {}

    def cacher(fn):
        def wrapper(*args, **kwargs):
            par = f"{args}{kwargs}"
            if par not in cache:
                if len(cache) < size:
                    res = fn(*args, **kwargs)
                    cache[par] = res
                    return str(res)
                else:
                    res = fn(*args, **kwargs)
                    return str(res)
            else:
                return f"cached: {cache[par]}"
        return wrapper
    return cacher

@sized_cacher(2)
def tsum(a, b):
    return a + b

assert(tsum(3, 2) == '5')
assert(tsum(3, 2) == 'cached: 5')
assert(tsum(2, 2) == '4')
assert(tsum(2, 2) == 'cached: 4')
assert(tsum(4, 4) == '8')
assert(tsum(4, 4) == '8')
print('Сразу +4 балла! Not bad!')

from time import time, sleep


def timer(fn):
    '''Возвращает tuple, содержащий время выполнения функции и результат'''

    def wrapper(*args, **kwargs):
        start_time = time()  # Засекаем начальное время
        result = fn(*args, **kwargs)  # Выполняем исходную функцию
        elapsed_time = time() - start_time  # Считаем прошедшее время
        return elapsed_time, result  # Возвращаем время выполнения и результат


    return wrapper


@timer
def tsum(a, b):
    sleep(1)
    return a + b


@timer
def tmul(a, b):
    sleep(2)
    return a * b


result_1 = tsum(2, 3)
result_2 = tmul(2, 3)

assert (result_1[0] > 1)
assert (result_1[1] == 5)
assert (result_2[0] > 2)
assert (result_2[1] == 6)
print('Успешно задекорировано! Ещё +2 балла!')

from functools import wraps


def get_gift(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print('Я молодец! Я заслужил +2 балла!')
        return fn(*args, **kwargs)

    return wrapper


@get_gift
def last_func():
    print('Ура, на сегодня всё! Спасибо за внимание!')


last_func()