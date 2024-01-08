class Ruta:
    def __init__(self, ciudad: str = "", rutaRecorrida: list = [], distanciaAcumulada: int = 0, distanciaFinal: int = 0) -> None:
        self.__ciudad = ciudad
        self.__rutaRecorrida = rutaRecorrida.copy()
        self.__distanciaAcumulada = distanciaAcumulada
        self.__distanciaFinal = distanciaFinal
    
    @property 
    def ciudad(self) -> str:
        return self.__ciudad
    
    @property
    def rutaRecorrida(self) -> list:
        return self.__rutaRecorrida
    
    @property
    def distanciaAcumulada(self) -> int:
        return self.__distanciaAcumulada
    
    @property
    def distanciaFinal(self) -> int:
        return self.__distanciaFinal

ciudades = {"Arad": 366, "Bucharest": 0, "Craiova": 160, "Dobreta": 242, "Eforie": 161, "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151,
            "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234, "Oradea": 380, "Pitesti": 101, "Rimnicu Vilcea": 193, 
            "Sibiu": 253, "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374}

conexiones = {"Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
              "Bucharest": {"Pitesti": 101, "Fagaras": 211, "Giurgiu": 90, "Urziceni": 85},
              "Craiova": {"Dobreta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
              "Dobreta": {"Mehadia": 75, "Craiova": 120},
              "Eforie": {"Hirsova": 86},
              "Fagaras": {"Sibiu": 99, "Bucharest": 211},
              "Giurgiu": {"Bucharest": 90},
              "Hirsova": {"Urziceni": 98, "Eforie": 86},
              "Iasi": {"Neamt": 87, "Vaslui": 92},
              "Lugoj": {"Timisoara": 111, "Mehadia": 75}, 
              "Mehadia": {"Lugoj": 70, "Dobreta": 75},
              "Neamt": {"Iasi": 87}, 
              "Oradea": {"Zerind": 71, "Sibiu": 151},
              "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
              "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 148, "Pitesti": 97},
              "Sibiu": {"Arad": 140, "Fagaras": 99, "Rimnicu Vilcea": 80},
              "Timisoara": {"Arad": 118, "Lugoj": 111},
              "Urziceni": {"Bucharest": 85, "Vaslui": 142, "Hirsova": 98},
              "Vaslui": {"Iasi": 92, "Urziceni": 142},
              "Zerind": {"Oradea": 71, "Arad": 75}}

estadosAbiertos: list [Ruta] = []
estadosCerrados: list [Ruta] = []
hijos: list [Ruta] = []
estadoActual: Ruta

def generarPrimer(ciudad):
    return Ruta(ciudad, [ciudad], 0, ciudades[ciudad])

def generarHijos(rutaActual: Ruta):
    ciudad = rutaActual.ciudad
    rutaRecorrida = rutaActual.rutaRecorrida
    distanciaAcumulada = rutaActual.distanciaAcumulada
    
    conexion = conexiones[ciudad]
    
    for key, value in conexion.items():
        rutaAnnadir = rutaRecorrida.copy()
        rutaAnnadir.append(key)
        distanciaAnnadir = distanciaAcumulada + value
        distanciaFinal = distanciaAnnadir + ciudades[key]
        hijo = Ruta(key, rutaAnnadir, distanciaAnnadir, distanciaFinal)
        hijos.append(hijo)

def tratarRepetidos():
    hijosEx = []
    
    for x in hijos:
        abiertoRepe = False
        cerradoRepe = False
        
        for y in estadosCerrados:
            if x.ciudad == y.ciudad:
                if x.distanciaFinal < y.distanciaFinal:
                    cerradoRepe = False
                else:
                    abiertoRepe = True
        
        for y in estadosAbiertos:
            if x.ciudad == y.ciudad:
                if x.distanciaFinal < y.distanciaFinal:
                    abiertoRepe = False
                    estadosAbiertos.remove(y)
                    break
                else:
                    abiertoRepe = True
                    
        if abiertoRepe is False and cerradoRepe is False:
            hijosEx.append(x)
    
    hijos.clear()
    hijos.extend(hijosEx)
    
def insertarHijos():
    estadosAbiertos.extend(hijos)
    estadosAbiertos.sort(key = lambda x: x.distanciaFinal)
    hijos.clear()
    
def principal(estadoInicial: Ruta):
    
    iteracion = 1
    
    estadosAbiertos.append(estadoInicial)
    estadoActual = estadosAbiertos[0]
    
    while(estadoActual.ciudad != "Bucharest" and len(estadosAbiertos) != 0):
        estadosAbiertos.pop(0)
        estadosCerrados.append(estadoActual)
        generarHijos(estadoActual)
        tratarRepetidos()
        insertarHijos()
        estadoActual = estadosAbiertos[0]
        
        iteracion += 1
        
        print("Estados abiertos ite %d: " % (iteracion))
        for x in estadosAbiertos:
            print("%s(%d)" % (x.ciudad, x.distanciaFinal), end=" ")
        print("")
        print("")
        
        print("Estados cerrados ite %d: " % (iteracion))
        for x in estadosCerrados:
            print("%s(%d)" % (x.ciudad, x.distanciaFinal), end=" ")
        print("")
        print("")
        
        
        print(("Estado actual ite %d: " + estadoActual.ciudad + " costo: %d, ruta recorrida %s") % (iteracion, estadoActual.distanciaFinal, estadoActual.rutaRecorrida))
        print("")

principal(generarPrimer("Lugoj"))