import shutil


def create_dir(path, parents=True):
    """
    create directory if dose not exists.
    :param path: Path: create dir path object
    :param parents: boolean: weather create parents dir, default is True.
    :return:
    """
    if not path.exists():
        path.mkdir(parents=parents)


def create_new_dir(path, parents=True):
    """
    create directory and delete it if exists.
    :param path: Path: create dir path object
    :param parents: boolean: weather create parents dir, default is True.
    :return:
    """
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=parents)


def array_split(ary, indices):
    """
    simple and ugly re-implenmention version of np.array_split().
    but must do more work to make the same behaver as np.array_split()

    e.g.
    >>> ary = list(range(10))
    >>> array_split(ary, 4)
    [[0, 1], [2, 3], [4, 5], [6, 7, 8, 9]]
    >>> np.array_split(ary, 4)
    [array([0, 1, 2]), array([3, 4, 5]), array([6, 7]), array([8, 9])]

    :param ary: array or list
    :param indices: int: how many sections to be divided
    """
    sections = []

    n_total = len(ary)
    n_each = round(n_total / indices)

    for i in range(indices):
        if i != indices - 1:
            sections.append(ary[i * n_each: (i + 1) * n_each])
        else:
            sections.append(ary[i * n_each:])

    return sections
