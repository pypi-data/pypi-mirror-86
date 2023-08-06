from errornumbers import ErrorNumber
import math


def sin(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the sinus of that ErrorNumber

    :example:
    >>> x = ErrorNumber(1.5708, 0.1)
    >>> sin(x).value
    0.9999999999932537
    >>> sin(x).absolute_error
    3.673205103346574e-07
    '''
    value = math.sin(e_n.value)
    abs_error = abs(math.cos(e_n.value) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def cos(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the cosinus of that ErrorNumber

    :example:
    >>> x = ErrorNumber(1.3, 0.1)
    >>> cos(x).value
    0.26749882862458735
    >>> cos(x).absolute_error
    0.0963558185417193
    '''
    value = math.cos(e_n.value)
    abs_error = abs(math.sin(e_n.value) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def tan(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the tangens of that ErrorNumber

    :example:
    >>> x = ErrorNumber(0.5, 0.1)
    >>> tan(x).value
    0.5463024898437905
    >>> tan(x).absolute_error
    0.11394939273245491
    '''
    value = math.sin(e_n.value) / math.cos(e_n.value)
    abs_error = abs((1 / math.cos(e_n.value)) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def cot(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the cotangens of that ErrorNumber

    :example:
    >>> x = ErrorNumber(0.5, 0.1)
    >>> cot(x).value
    0.5463024898437905
    >>> cot(x).absolute_error
    0.20858296429334883
    '''
    value = math.cos(e_n.value) / math.sin(e_n.value)
    abs_error = abs((1 / math.sin(e_n.value)) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def exp(e_n):
    '''
    :param e_n: an ErrorNumber
    :return: e^x of that ErrorNumber

    :example:
    >>> x = ErrorNumber(1, 0.1)
    >>> exp(x).value
    2.718281828459045
    >>> exp(x).absolute_error
    0.27182818284590454
    '''
    value = math.e ** e_n.value
    error = value * e_n.absolute_error
    return ErrorNumber(value, error)


def expbase(e_n, base):
    '''
    :param e_n: an ErrorNumber
    :param base: a base (any real number)
    :return: base^x of that ErrorNumber

    :example:
    >>> x = ErrorNumber(2, 0.1)
    >>> expbase(x, 3).value
    9
    >>> expbase(x, 3).absolute_error
    0.9
    '''
    value = base ** e_n.value
    error = value * e_n.absolute_error
    return ErrorNumber(value, error)


def from_non_reproducible(lort):
    '''
    creates an ErrorNumber from input data, calculating an average and an standard deviation
    The absolute error that is returned is three times the standard deviation calculated

    The stdev is calculated using factor 1/ (n(n-1))

    :param lort: List or tuple containing the datapoints

    :example:
    >>> x = from_non_reproducible([1, 2, 3, 4])
    >>> x.value
    2.5
    >>> x.absolute_error
    1.9364916731037085
    '''
    # compute an average
    average = sum(lort) / len(lort)
    sum_of_of_quad_diffs = sum([(x - average) ** 2 for x in lort])
    fout = math.sqrt((1 / (len(lort) * (len(lort) - 1))) * sum_of_of_quad_diffs)
    return ErrorNumber(average, fout * 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
