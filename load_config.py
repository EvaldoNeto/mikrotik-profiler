

def load_influx_vars():
    try:
        with open("./influx-variables.env") as f:
            influx_data = {}
            for line in f:
                aux = line.split("=")
                influx_data[aux[0]] = aux[1].strip()
            return influx_data
    except Exception as err:
        print(err)


def load_mikrotik_vars():
    try:
        with open("./mikrotik-variables.env") as f:
            influx_data = {}
            for line in f:
                aux = line.split("=")
                if aux[0] in ["TIMEOUT", "API_PORT"]:
                    influx_data[aux[0]] = int(aux[1].strip())
                else:
                    influx_data[aux[0]] = aux[1].strip()
            return influx_data
    except Exception as err:
        print(err)

if __name__ == "__main__":
    x = load_mikrotik_vars()
    print(x)
