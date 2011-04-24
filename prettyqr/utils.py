import operator


def pointwise(op, list1, list2):
    # expand singletons
    if not isinstance(list1, (list, tuple)):
        list1 = [list1] * len(list2)
    if not isinstance(list2, (list, tuple)):
        list2 = [list2] * len(list1)

    function = getattr(operator, op)
    result = [function(*pair) for pair in zip(list1, list2)]

    if isinstance(list1, tuple) or isinstance(list2, tuple):
        return tuple(result)
    else:
        return result
