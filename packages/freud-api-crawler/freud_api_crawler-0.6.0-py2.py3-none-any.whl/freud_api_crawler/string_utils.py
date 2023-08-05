CLEAN_UP_PATTERNS = [
    ('-<br />', '<lb break="no"/>'),
    ('<br />', '<lb />'),
    ('\n', ''),
]


def clean_markup(source, patterns=CLEAN_UP_PATTERNS):
    """ applies search and replace
    :param source: A string to clean
    :type source: string
    :param patterns: a list of tuples `[('-<br />', '<lb break="no"/>'),`]
    :type patterns: list

    :return: the cleaned string
    :rtype: string

    """
    for x in patterns:
        source = source.replace(x[0], x[1])
    return source
