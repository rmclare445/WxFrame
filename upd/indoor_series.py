'''

Record most recent thermopi retrieval to series

'''


def write_series( ):

    with open("./log.thermopi", "r") as f:
        current = f.read()

    try:
        with open("./log.indoor", "r") as f:
            content = f.readlines()
    except:
        content = []

    # Record entries from each minute up to 2 days out
    content.append(current)
    lim = min( len(content), 2880 )
    content = content[-lim:]

    with open("./log.indoor", "w") as f:
        for line in content:
            f.write( line )


if __name__ == "__main__":
    write_series()
