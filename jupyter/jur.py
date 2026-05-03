from math import gcd
from functools import reduce


def divisors(n):
    """Возвращает список делителей числа n."""
    n = abs(n)
    result = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            result.extend([i, -i, n // i, -n // i])
    return sorted(set(result))


def evaluate_polynomial(coeffs, x):
    """Вычисляет значение многочлена в точке x."""
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result


def roots(coeffs):
    """Находит все целые корни многочлена."""
    if not coeffs or coeffs[0] == 0:
        raise ValueError("Коэффициенты многочлена некорректны или равны нулю.")

    # Получаем коэффициенты старшей и свободной члена
    a_n = coeffs[-1]
    a_0 = coeffs[0]

    # Делители свободного члена и старшего коэффициента
    possible_roots = divisors(a_0)

    # Проверяем делители на корень
    result = []
    for root in possible_roots:
        if evaluate_polynomial(coeffs, root) == 0:
            result.append(root)
            # Уменьшаем степень многочлена, если корень найден
            while coeffs and evaluate_polynomial(coeffs, root) == 0:
                coeffs = synthetic_division(coeffs, root)

    return sorted(result)


def synthetic_division(coeffs, root):
    """Выполняет синтетическое деление многочлена на (x - root)."""
    new_coeffs = []
    remainder = 0
    for coeff in reversed(coeffs):
        remainder = coeff + remainder * root
        new_coeffs.append(remainder)
    new_coeffs.pop()  # Последний элемент — это остаток деления, его удаляем
    return list(reversed(new_coeffs))  # Инвертируем порядок


# Пример использования
coefficients = [6, -5, -17, 10]  # Многочлен 6 - 5x - 17x^2 + 10x^3
print(roots(coefficients))  # Выводит [-3, 2]