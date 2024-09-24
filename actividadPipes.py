import os, sys, getopt


def invertirLinea(linea):
    return linea[::-1]


def leerLineas(rutaArchivo):
    with open(rutaArchivo, "r") as archivo:
        lineas = archivo.readlines()
    return [linea.strip() for linea in lineas]


def main():
    rutaArchivo = None
    try:
        (opt, arg) = getopt.getopt(sys.argv[1:], "f:")
        rutaArchivo = opt[0][1]
    except getopt.GetoptError as err:
        print(err)

    if not rutaArchivo:
        print("Error: no hay una ruta de archivo")

    lineas = leerLineas(rutaArchivo)

    padres = []
    hijos = []

    for _ in range(len(lineas)):
        padre_pipe, hijo_pipe = os.pipe()
        padres.append(padre_pipe)
        hijos.append(hijo_pipe)

    for i, linea in enumerate(lineas):
        pid = os.fork()
        if pid == 0:
            os.close(padres[i])
            with os.fdopen(hijos[i], "w") as pipe:
                linea_invertida = invertirLinea(linea)
                pipe.write(linea_invertida + "\n")
            os._exit(0)
        else:
            os.close(hijos[i])

    lineas_invertidas = []
    for padre_pipe in padres:
        with os.fdopen(padre_pipe, "r") as pipe:
            lineas_invertidas.append(pipe.read().strip())

    for _ in range(len(lineas)):
        os.wait()

    for linea_invertida in lineas_invertidas:
        print(linea_invertida)


if __name__ == "__main__":
    main()
