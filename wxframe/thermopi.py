'''

Reads retrieved thermopi data

'''


from tools.system_tools import upd_dir


def F_to_C( T ):
    return (T - 32)/1.8


def C_to_F( T ):
    return T * 1.8 + 32


def read_nowlog( path=upd_dir+"log.now" ):
    # Retrieve non-temporal data from log.now
    with open( path, "r") as f:
        data = f.read().replace("\n","").replace(" ","").split(",")
    return float(data[2]), int(data[3]), True if data[4] == "T" else False


def get_temps( metric=False ):
    t, h, s = read_nowlog()
    T = F_to_C(t)
    Td = T - ((100 - h)/5.)    # Approximation from Lawrence in BAMS, 2005
    if not metric:
        T  = C_to_F( T  )
        Td = C_to_F( Td )
    return str(round(T)), str(round(Td))


if __name__ == "__main__":
    print(get_temps())
