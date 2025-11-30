class SistemaArmas:
    def __init__(self, misiles_aa=0, misiles_antibuque=0, torpedos=0):
        self.misiles_aa = misiles_aa
        self.misiles_antibuque = misiles_antibuque
        self.torpedos = torpedos

    def __str__(self):
        return f"Misiles AA: {self.misiles_aa}, Antibuque: {self.misiles_antibuque}, Torpedos: {self.torpedos}"

class SistemaSensores:
    def __init__(self, radar="OK", sonar="OK"):
        self.radar = radar
        self.sonar = sonar

    def __str__(self):
        return f"Radar: {self.radar}, Sonar: {self.sonar}"

class Capitan:
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return f"Capitán: {self.nombre}"

class PlataformaNaval:
    def __init__(self, nombre, pais, rol):
        self.nombre = nombre
        self.pais = pais
        self.rol = rol
        self.capitan = None
        self.sensores = SistemaSensores()
        self.armas = SistemaArmas()

    def asignar_capitan(self, capitan):
        self.capitan = capitan

    def recibir_danio(self):
        print(f"{self.nombre} ha recibido daño.")

    def imprimir_info(self):
        print("\n--- INFORMACIÓN DE LA PLATAFORMA ---")
        print(f"Nombre: {self.nombre}")
        print(f"País: {self.pais}")
        print(f"Rol: {self.rol}")
        if self.capitan:
            print(self.capitan)
        print("Sensores:", self.sensores)
        print("Armas:", self.armas)

class Fragata(PlataformaNaval):
    def __init__(self, nombre, pais, misiles_aa, helicopteros):
        super().__init__(nombre, pais, "Fragata")
        self.armas.misiles_aa = misiles_aa
        self.helicopteros = helicopteros

    def disparar_misil_aa(self):
        if self.armas.misiles_aa > 0:
            self.armas.misiles_aa -= 1
            print(f"{self.nombre} disparó un misil AA.")
        else:
            print("No quedan misiles AA.")

    def despegar_helicoptero(self):
        if self.helicopteros > 0:
            print(f"Helicóptero despegó de {self.nombre}.")
        else:
            print("No hay helicópteros.")

class Corbeta(PlataformaNaval):
    def __init__(self, nombre, pais):
        super().__init__(nombre, pais, "Corbeta")

    def patrullar(self, costera=True):
        if costera:
            print(f"{self.nombre} patrulla zona costera.")
        else:
            print(f"{self.nombre} patrulla en mar abierto.")

class Submarino(PlataformaNaval):
    def __init__(self, nombre, pais):
        super().__init__(nombre, pais, "Submarino")

    def sumergirse(self):
        print(f"{self.nombre} se sumerge.")

    def detectar(self):
        print(f"{self.nombre} detecta un contacto.")

    def lanzar_torpedo(self):
        print(f"{self.nombre} lanza un torpedo.")

class Flota:
    def __init__(self):
        self.plataformas = []

    def agregar(self, plataforma):
        self.plataformas.append(plataforma)

    def mostrar(self):
        print("\n===== LISTADO DE LA FLOTA =====")
        for p in self.plataformas:
            p.imprimir_info()

# PROGRAMA PRINCIPAL

fragata = Fragata("F-100", "España", misiles_aa=4, helicopteros=1)
corbeta = Corbeta("C-23", "España")
submarino = Submarino("S-80", "España")

capitan = Capitan("Juan Pérez")
fragata.asignar_capitan(capitan)

flota = Flota()
flota.agregar(fragata)
flota.agregar(corbeta)
flota.agregar(submarino)

fragata.disparar_misil_aa()
fragata.despegar_helicoptero()

corbeta.patrullar()

submarino.sumergirse()
submarino.detectar()
submarino.lanzar_torpedo()

corbeta.recibir_danio()

fragata.sensores.radar = "Daño leve"
submarino.armas.torpedos = 3

flota.mostrar()
