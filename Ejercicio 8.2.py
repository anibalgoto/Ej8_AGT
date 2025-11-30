import tkinter as tk
from tkinter import Toplevel, messagebox
import pygame
import math
import time

pygame.mixer.init()

# Cargar sonidos (puedes usar tus archivos)
sonido_misil = pygame.mixer.Sound("misil.wav")
sonido_torpedo = pygame.mixer.Sound("torpedo.wav")
sonido_ping = pygame.mixer.Sound("ping.wav")
sonido_explosion = pygame.mixer.Sound("explosion.wav")

class PlataformaGrafica:
    def __init__(self, canvas, x, y, color, nombre, tipo):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.nombre = nombre
        self.tipo = tipo
        self.estado = "OK"
        self.rango = 150 

        self.item = canvas.create_rectangle(x, y, x+60, y+40, fill=color)
        self.texto = canvas.create_text(x+30, y+20, text=tipo, fill="white")

    def mover(self, dx, dy):
        self.canvas.move(self.item, dx, dy)
        self.canvas.move(self.texto, dx, dy)
        self.x += dx
        self.y += dy

    def distancia(self, otra):
        cx = self.x + 30
        cy = self.y + 20
        ox = otra.x + 30
        oy = otra.y + 20
        return math.sqrt((cx - ox)**2 + (cy - oy)**2)

    def recibir_danio(self):
        self.estado = "Dañado"
        sonido_explosion.play()

    def info(self):
        return f"{self.nombre} ({self.tipo}) - Estado: {self.estado}"


def animar_proyectil(canvas, x1, y1, x2, y2):
    linea = canvas.create_line(x1, y1, x1, y1, width=4)
    pasos = 20
    for i in range(pasos):
        nx = x1 + (x2 - x1) * (i / pasos)
        ny = y1 + (y2 - y1) * (i / pasos)
        canvas.coords(linea, x1, y1, nx, ny)
        canvas.update()
        time.sleep(0.02)
    canvas.delete(linea)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador Naval")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="navy")
        self.canvas.pack(side="left")

        self.panel = tk.Frame(self.root, bg="gray20", width=250)
        self.panel.pack(side="right", fill="y")

        # Plataforma
        self.fragata = PlataformaGrafica(self.canvas, 50, 100, "green", "F-100", "Fragata")
        self.corbeta = PlataformaGrafica(self.canvas, 200, 300, "blue", "C-23", "Corbeta")
        self.submarino = PlataformaGrafica(self.canvas, 400, 200, "purple", "S-80", "Submarino")

        self.plataformas = [self.fragata, self.corbeta, self.submarino]

        # Botones
        tk.Button(self.panel, text="Mover Fragata", command=lambda:self.fragata.mover(10,0)).pack(pady=5)
        tk.Button(self.panel, text="Mover Corbeta", command=lambda:self.corbeta.mover(10,0)).pack(pady=5)
        tk.Button(self.panel, text="Mover Submarino", command=lambda:self.submarino.mover(10,0)).pack(pady=5)

        tk.Button(self.panel, text="Escanear sensores", command=self.escanear).pack(pady=5)
        tk.Button(self.panel, text="Lanzar arma", command=self.combate_manual).pack(pady=5)
        tk.Button(self.panel, text="Simular daño", command=self.daniar).pack(pady=5)
        tk.Button(self.panel, text="Mostrar flota", command=self.mostrar_flota).pack(pady=5)

        tk.Button(self.panel, text="Ordenar Ataque", command=self.ordenar_ataque).pack(pady=20)

        self.root.mainloop()

    def escanear(self):
        for p in self.plataformas:
            for o in self.plataformas:
                if p is not o and p.distancia(o) < p.rango:
                    sonido_ping.play()
                    messagebox.showinfo("Contacto detectado", f"{p.nombre} detecta a {o.nombre}")

    def combate_manual(self):
        objetivo = self.corbeta
        atacante = self.fragata

        sonido_misil.play()
        animar_proyectil(self.canvas, atacante.x+30, atacante.y, objetivo.x+30, objetivo.y)
        objetivo.recibir_danio()

    def daniar(self):
        self.fragata.recibir_danio()
        messagebox.showinfo("Daño", "La Fragata ha sido dañada")

    def mostrar_flota(self):
        ventana = Toplevel()
        ventana.title("Estado de la Flota")

        for p in self.plataformas:
            tk.Label(ventana, text=p.info()).pack()

    def ordenar_ataque(self):
        # Fragata
        sonido_misil.play()
        animar_proyectil(self.canvas, self.fragata.x, self.fragata.y, self.corbeta.x, self.corbeta.y)
        self.corbeta.recibir_danio()

        # Corbeta
        sonido_misil.play()
        animar_proyectil(self.canvas, self.corbeta.x, self.corbeta.y, self.submarino.x, self.submarino.y)
        self.submarino.recibir_danio()

        # Submarino
        sonido_torpedo.play()
        animar_proyectil(self.canvas, self.submarino.x, self.submarino.y, self.fragata.x, self.fragata.y)
        self.fragata.recibir_danio()


# Ejecutar app
App()
