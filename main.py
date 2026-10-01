import pygame
import sys
import math
import random

pygame.init()

ANCHO_BASE = 1100
ALTO_BASE = 700
MIN_ANCHO = 960
MIN_ALTO = 680
ANCHO = ANCHO_BASE
ALTO = ALTO_BASE
FPS_OBJETIVO = 120

ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("🐔 Pollo Héroe: La Rebelión de la Granja")

pantalla = pygame.Surface((ANCHO_BASE, ALTO_BASE)).convert_alpha()
reloj = pygame.time.Clock()
dt = 1 / 60

NEGRO = (8, 8, 15)
BLANCO = (255, 255, 255)
ORO = (255, 215, 50)
AMARILLO = (255, 180, 30)
NARANJA = (255, 100, 30)
ROJO = (210, 55, 55)
ROJO_CLARO = (255, 80, 70)
MORADO = (75, 45, 120)
MORADO_CLARO = (110, 70, 170)
AZUL = (35, 80, 150)
AZUL_CLARO = (50, 130, 220)
VERDE = (45, 130, 80)
VERDE_CLARO = (70, 180, 100)
GRIS = (55, 55, 70)
GRIS_CLARO = (90, 90, 110)
CAFE = (105, 65, 35)
CAFE_CLARO = (150, 95, 50)
CESPED = (55, 130, 60)
CESPED_CLARO = (85, 165, 70)
TIERRA = (150, 105, 55)
TIERRA_CLARA = (178, 130, 72)
CIELO = (100, 180, 235)
CIELO_CLARO = (155, 215, 250)


def cargar_fuente(tamano, negrita=False):
    try:
        return pygame.font.Font("assets/font.ttf", tamano)
    except:
        return pygame.font.SysFont("Arial", tamano, bold=negrita)


fuente_titulo = cargar_fuente(78, True)
fuente_titulo_pequeno = cargar_fuente(48, True)
fuente_subtitulo = cargar_fuente(27, True)
fuente_boton = cargar_fuente(23, True)
fuente_texto = cargar_fuente(18)
fuente_mini = cargar_fuente(14)


try:
    imagen_fondo_original = pygame.image.load("assets/fondo.png").convert()
except:
    imagen_fondo_original = None


try:
    imagen_granja_original = pygame.image.load("assets/granja.png").convert()
except:
    imagen_granja_original = None


try:
    sprite_pollito_original = pygame.image.load(
        "assets/gallina.webp"
    ).convert_alpha()
except:
    sprite_pollito_original = None


sprite_pollito = None
sprite_pollito_flip = None
sprite_pollito_grande = None

if sprite_pollito_original:
    sprite_pollito = pygame.transform.smoothscale(
        sprite_pollito_original,
        (75, 75)
    )

    sprite_pollito_flip = pygame.transform.flip(
        sprite_pollito,
        True,
        False
    )

    sprite_pollito_grande = pygame.transform.smoothscale(
        sprite_pollito_original,
        (300, 300)
    )


fondo_menu_cache = None

if imagen_fondo_original:
    fondo_menu_cache = pygame.transform.smoothscale(
        imagen_fondo_original,
        (ANCHO_BASE, ALTO_BASE)
    )


fondo_granja_cache = None

if imagen_granja_original:
    fondo_granja_cache = pygame.transform.smoothscale(
        imagen_granja_original,
        (ANCHO_BASE, ALTO_BASE)
    )


ESTADO_MENU = "MENU"
ESTADO_HOME = "HOME"
ESTADO_MUNDOS = "MUNDOS"
ESTADO_JUGANDO = "JUGANDO"

estado_actual = ESTADO_MENU
mundo_seleccionado = ""

nombre_jugador = "SK BRYAN 🐔"
granja_jugador = "Granja: Los Mochos"

mouse_click = False

shake_intensidad = 0
shake_tiempo = 0

particulas = []
textos_flotantes = []


def clamp(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def lerp(a, b, t):
    return a + (b - a) * t


def distancia_entre(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def mouse_virtual():
    mx, my = pygame.mouse.get_pos()

    window_w, window_h = ventana.get_size()

    escala = min(
        window_w / ANCHO_BASE,
        window_h / ALTO_BASE
    )

    render_w = int(ANCHO_BASE * escala)
    render_h = int(ALTO_BASE * escala)

    offset_x = (window_w - render_w) // 2
    offset_y = (window_h - render_h) // 2

    mx -= offset_x
    my -= offset_y

    if escala <= 0:
        return 0, 0

    return mx / escala, my / escala


def dibujar_texto(texto, fuente, color, x, y, sombra=True):

    if sombra:
        sombra_render = fuente.render(texto, True, (0, 0, 0))

        pantalla.blit(
            sombra_render,
            (
                int(x - sombra_render.get_width() / 2 + 3),
                int(y - sombra_render.get_height() / 2 + 4)
            )
        )

    render = fuente.render(texto, True, color)

    pantalla.blit(
        render,
        (
            int(x - render.get_width() / 2),
            int(y - render.get_height() / 2)
        )
    )


def dibujar_texto_izquierda(texto, fuente, color, x, y, sombra=True):

    if sombra:
        render_sombra = fuente.render(texto, True, NEGRO)
        pantalla.blit(render_sombra, (x + 2, y + 3))

    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))


def dibujar_overlay(alpha=105):

    overlay = pygame.Surface(
        (ANCHO_BASE, ALTO_BASE),
        pygame.SRCALPHA
    )

    overlay.fill((5, 5, 15, alpha))
    pantalla.blit(overlay, (0, 0))


class Particula:

    def __init__(
        self,
        x,
        y,
        color,
        velocidad_min=50,
        velocidad_max=180,
        vida=0.5,
        tamano=5,
        gravedad=0
    ):

        angulo = random.uniform(0, math.tau)
        velocidad = random.uniform(velocidad_min, velocidad_max)

        self.x = x
        self.y = y

        self.vx = math.cos(angulo) * velocidad
        self.vy = math.sin(angulo) * velocidad

        self.color = color
        self.vida = vida
        self.vida_max = vida

        self.tamano = random.uniform(
            tamano * 0.6,
            tamano * 1.4
        )

        self.gravedad = gravedad

    def actualizar(self, delta):

        self.vida -= delta
        self.vy += self.gravedad * delta

        self.x += self.vx * delta
        self.y += self.vy * delta

        self.vx *= pow(0.08, delta)

    def dibujar(self):

        if self.vida <= 0:
            return

        alpha = int(
            255 * clamp(
                self.vida / self.vida_max,
                0,
                1
            )
        )

        radio = max(
            1,
            int(
                self.tamano *
                (self.vida / self.vida_max)
            )
        )

        superficie = pygame.Surface(
            (radio * 4, radio * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            superficie,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                alpha
            ),
            (radio * 2, radio * 2),
            radio
        )

        pantalla.blit(
            superficie,
            (
                int(self.x - radio * 2),
                int(self.y - radio * 2)
            )
        )


def crear_particulas(
    x,
    y,
    color,
    cantidad=8,
    velocidad_min=50,
    velocidad_max=180,
    vida=0.5,
    tamano=5
):

    for _ in range(cantidad):
        particulas.append(
            Particula(
                x,
                y,
                color,
                velocidad_min,
                velocidad_max,
                vida,
                tamano
            )
        )


class TextoFlotante:

    def __init__(self, texto, x, y, color):

        self.texto = texto
        self.x = x
        self.y = y
        self.color = color

        self.vida = 0.8
        self.vida_max = 0.8

    def actualizar(self, delta):

        self.vida -= delta
        self.y -= 35 * delta

    def dibujar(self):

        if self.vida <= 0:
            return

        alpha = int(
            255 *
            (self.vida / self.vida_max)
        )

        render = fuente_texto.render(
            self.texto,
            True,
            self.color
        )

        render.set_alpha(alpha)

        pantalla.blit(
            render,
            (
                int(self.x - render.get_width() / 2),
                int(self.y)
            )
        )


def aplicar_shake(intensidad=8, duracion=0.15):

    global shake_intensidad
    global shake_tiempo

    shake_intensidad = max(
        shake_intensidad,
        intensidad
    )

    shake_tiempo = max(
        shake_tiempo,
        duracion
    )


def boton(
    texto,
    x,
    y,
    ancho,
    alto,
    color,
    color_hover,
    icono=""
):

    mx, my = mouse_virtual()

    rect = pygame.Rect(x, y, ancho, alto)

    hover = rect.collidepoint(mx, my)

    crecimiento = 4 if hover else 0

    rect_dibujo = pygame.Rect(
        x - crecimiento // 2,
        y - crecimiento // 2,
        ancho + crecimiento,
        alto + crecimiento
    )

    sombra_rect = rect_dibujo.move(5, 7)

    pygame.draw.rect(
        pantalla,
        (0, 0, 0),
        sombra_rect,
        border_radius=18
    )

    color_actual = color_hover if hover else color

    pygame.draw.rect(
        pantalla,
        color_actual,
        rect_dibujo,
        border_radius=18
    )

    if hover:

        brillo = pygame.Surface(
            (
                rect_dibujo.width,
                rect_dibujo.height
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            brillo,
            (255, 255, 255, 22),
            brillo.get_rect(),
            border_radius=18
        )

        pantalla.blit(
            brillo,
            rect_dibujo.topleft
        )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        rect_dibujo,
        2,
        border_radius=18
    )

    texto_final = (
        f"{icono}  {texto}"
        if icono
        else texto
    )

    dibujar_texto(
        texto_final,
        fuente_boton,
        BLANCO,
        rect_dibujo.centerx,
        rect_dibujo.centery,
        False
    )

    return hover and mouse_click


def panel(
    x,
    y,
    ancho,
    alto,
    color=(20, 18, 35),
    alpha=220
):

    sombra = pygame.Surface(
        (ancho, alto),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        sombra,
        (0, 0, 0, 130),
        sombra.get_rect(),
        border_radius=25
    )

    pantalla.blit(
        sombra,
        (x + 7, y + 9)
    )

    superficie = pygame.Surface(
        (ancho, alto),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        superficie,
        (
            color[0],
            color[1],
            color[2],
            alpha
        ),
        superficie.get_rect(),
        border_radius=25
    )

    pantalla.blit(superficie, (x, y))

    pygame.draw.rect(
        pantalla,
        ORO,
        (x, y, ancho, alto),
        2,
        border_radius=25
    )


def panel_centrado(
    ancho,
    alto,
    color=(20, 18, 35),
    alpha=220
):

    x = (ANCHO_BASE - ancho) // 2
    y = (ALTO_BASE - alto) // 2

    panel(
        x,
        y,
        ancho,
        alto,
        color,
        alpha
    )

    return x, y


def pastilla_stat(
    x,
    y,
    ancho,
    alto,
    color,
    icono,
    valor
):

    rect = pygame.Rect(
        x,
        y,
        ancho,
        alto
    )

    pygame.draw.rect(
        pantalla,
        (0, 0, 0),
        rect.move(3, 4),
        border_radius=alto // 2
    )

    pygame.draw.rect(
        pantalla,
        color,
        rect,
        border_radius=alto // 2
    )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        rect,
        2,
        border_radius=alto // 2
    )

    dibujar_texto(
        f"{icono}  {valor}",
        fuente_texto,
        BLANCO,
        x + ancho // 2,
        y + alto // 2,
        False
    )


def dibujar_fondo():

    if fondo_menu_cache:
        pantalla.blit(
            fondo_menu_cache,
            (0, 0)
        )
    else:
        pantalla.fill((25, 20, 45))

    dibujar_overlay()


def menu_principal():

    global estado_actual

    panel_w = 610
    panel_h = 550

    panel_x, panel_y = panel_centrado(
        panel_w,
        panel_h,
        (18, 15, 32),
        215
    )

    cx = ANCHO_BASE // 2

    t = pygame.time.get_ticks() / 1000

    brillo_titulo = int(
        20 +
        (math.sin(t * 2) + 1) * 10
    )

    dibujar_texto(
        "🐔 PRESENTA",
        fuente_mini,
        AMARILLO,
        cx,
        panel_y + 40
    )

    dibujar_texto(
        "POLLO",
        fuente_titulo,
        (
            255,
            clamp(
                210 + brillo_titulo,
                0,
                255
            ),
            50
        ),
        cx,
        panel_y + 110
    )

    dibujar_texto(
        "HÉROE",
        fuente_titulo,
        NARANJA,
        cx,
        panel_y + 180
    )

    dibujar_texto(
        "LA REBELIÓN DE LA GRANJA",
        fuente_subtitulo,
        BLANCO,
        cx,
        panel_y + 235
    )

    pygame.draw.line(
        pantalla,
        ORO,
        (cx - 170, panel_y + 265),
        (cx + 170, panel_y + 265),
        3
    )

    dibujar_texto(
        "Una granja. Un héroe. Una rebelión.",
        fuente_texto,
        (210, 210, 220),
        cx,
        panel_y + 300
    )

    if boton(
        "INICIAR AVENTURA",
        cx - 195,
        panel_y + 350,
        390,
        65,
        (180, 65, 25),
        (240, 95, 30),
        "▶"
    ):
        estado_actual = ESTADO_HOME

    if boton(
        "SALIR",
        cx - 120,
        panel_y + 440,
        240,
        55,
        (70, 45, 60),
        (110, 55, 70),
        "✕"
    ):
        pygame.quit()
        sys.exit()

    dibujar_texto(
        "v2.0 • POLLO HÉROE",
        fuente_mini,
        (130, 130, 145),
        cx,
        panel_y + 520
    )


def pantalla_home():

    global estado_actual
    global mundo_seleccionado

    cx = ANCHO_BASE // 2

    stats = [
        ("🏆", "451", (55, 110, 185)),
        ("🌽", "28,006", (150, 110, 25)),
        ("🪶", "2,302", (45, 140, 95)),
    ]

    pill_w = 170
    pill_h = 46
    gap = 18

    total_w = pill_w * 3 + gap * 2
    x_start = cx - total_w // 2

    for i, (icono, valor, color) in enumerate(stats):

        x = x_start + i * (pill_w + gap)

        pastilla_stat(
            x,
            26,
            pill_w,
            pill_h,
            color,
            icono,
            valor
        )

    y_nombre = 108

    dibujar_texto(
        nombre_jugador,
        fuente_subtitulo,
        ORO,
        cx,
        y_nombre
    )

    dibujar_texto(
        granja_jugador,
        fuente_mini,
        (200, 200, 215),
        cx,
        y_nombre + 26
    )

    poderes = [
        ("⚔ Ataque", 0.82, ROJO_CLARO),
        ("🛡 Defensa", 0.64, AZUL_CLARO),
        ("⚡ Velocidad", 0.91, VERDE_CLARO),
    ]

    barra_w = 150
    barra_h = 10
    gap_barras = 40

    total_pw = barra_w * 3 + gap_barras * 2
    xp_start = cx - total_pw // 2

    y_poderes = 170

    for i, (etiqueta, valor, color) in enumerate(poderes):

        x = xp_start + i * (barra_w + gap_barras)

        dibujar_texto(
            etiqueta,
            fuente_mini,
            BLANCO,
            x + barra_w // 2,
            y_poderes,
            False
        )

        pygame.draw.rect(
            pantalla,
            (40, 40, 55),
            (
                x,
                y_poderes + 14,
                barra_w,
                barra_h
            ),
            border_radius=6
        )

        pygame.draw.rect(
            pantalla,
            color,
            (
                x,
                y_poderes + 14,
                int(barra_w * valor),
                barra_h
            ),
            border_radius=6
        )

    centro_pollo_y = ALTO_BASE // 2 - 25

    tiempo = pygame.time.get_ticks() / 1000

    bob = math.sin(tiempo * 2) * 8
    rotacion = math.sin(tiempo * 1.4) * 2.2

    if sprite_pollito_grande:

        img = pygame.transform.rotozoom(
            sprite_pollito_grande,
            rotacion,
            1
        )

        rect = img.get_rect(
            center=(
                cx,
                int(centro_pollo_y + bob)
            )
        )

        pygame.draw.ellipse(
            pantalla,
            (0, 0, 0, 100),
            (
                cx - 95,
                centro_pollo_y + 115,
                190,
                35
            )
        )

        pantalla.blit(img, rect)

    y_botones = ALTO_BASE - 130

    if boton(
        "CAMPAÑA",
        cx - 330,
        y_botones,
        170,
        70,
        (55, 90, 140),
        (75, 120, 175),
        "🗺"
    ):
        estado_actual = ESTADO_MUNDOS

    if boton(
        "BATALLA",
        cx - 110,
        y_botones - 15,
        220,
        100,
        (190, 60, 20),
        (240, 95, 30),
        "⚔"
    ):

        mundo_seleccionado = "Batalla Rápida"
        iniciar_nivel()
        estado_actual = ESTADO_JUGANDO

    if boton(
        "MODO BATALLA",
        cx + 160,
        y_botones,
        170,
        70,
        (95, 55, 140),
        (130, 80, 180),
        "🎮"
    ):

        mundo_seleccionado = "Modo Batalla"
        iniciar_nivel()
        estado_actual = ESTADO_JUGANDO


def tarjeta_mundo(
    nombre,
    numero,
    x,
    y,
    color,
    descripcion
):

    mx, my = mouse_virtual()

    rect = pygame.Rect(
        x,
        y,
        300,
        115
    )

    hover = rect.collidepoint(mx, my)

    elevacion = -4 if hover else 0

    rect_draw = rect.move(
        0,
        elevacion
    )

    color_actual = color

    if hover:
        color_actual = tuple(
            min(255, c + 30)
            for c in color
        )

    pygame.draw.rect(
        pantalla,
        (0, 0, 0),
        rect_draw.move(5, 7),
        border_radius=20
    )

    pygame.draw.rect(
        pantalla,
        color_actual,
        rect_draw,
        border_radius=20
    )

    pygame.draw.rect(
        pantalla,
        ORO if hover else (100, 100, 120),
        rect_draw,
        2,
        border_radius=20
    )

    pygame.draw.circle(
        pantalla,
        ORO,
        (
            x + 42,
            y + 38 + elevacion
        ),
        25
    )

    dibujar_texto(
        str(numero),
        fuente_boton,
        NEGRO,
        x + 42,
        y + 38 + elevacion,
        False
    )

    texto = fuente_boton.render(
        nombre,
        True,
        BLANCO
    )

    pantalla.blit(
        texto,
        (
            x + 80,
            y + 17 + elevacion
        )
    )

    desc = fuente_mini.render(
        descripcion,
        True,
        (215, 215, 225)
    )

    pantalla.blit(
        desc,
        (
            x + 80,
            y + 55 + elevacion
        )
    )

    return hover and mouse_click


def seleccionar_mundo():

    global mundo_seleccionado
    global estado_actual

    panel_w = 900
    panel_h = 630

    panel_x, panel_y = panel_centrado(
        panel_w,
        panel_h,
        (15, 13, 30),
        225
    )

    cx = ANCHO_BASE // 2

    dibujar_texto(
        "SELECCIONA TU MUNDO",
        fuente_titulo_pequeno,
        ORO,
        cx,
        panel_y + 50
    )

    dibujar_texto(
        "Elige dónde comenzará tu aventura",
        fuente_texto,
        BLANCO,
        cx,
        panel_y + 90
    )

    mundos = [
        ("LA GRANJA", 0, (55, 100, 65), "El comienzo de la rebelión"),
        ("VOLCÁN", 1, (125, 55, 40), "El reino del fuego"),
        ("DOJO LUNAR", 2, (70, 60, 125), "Entrena bajo la luna"),
        ("LABORATORIO", 3, (45, 85, 125), "Experimentos prohibidos"),
        ("CUEVAS HELADAS", 4, (50, 100, 130), "Un mundo congelado"),
        ("ARENA ANCESTRAL", 5, (130, 90, 45), "El desafío definitivo")
    ]

    tarjeta_w = 300
    tarjeta_h = 115
    gap_x = 40
    gap_y = 25

    grid_w = tarjeta_w * 2 + gap_x

    grid_x = (
        panel_x +
        (panel_w - grid_w) // 2
    )

    grid_y = panel_y + 150

    columnas = [
        grid_x,
        grid_x + tarjeta_w + gap_x
    ]

    mundo_click = None

    for i, mundo in enumerate(mundos):

        col = i % 2
        fila = i // 2

        x = columnas[col]

        y = grid_y + fila * (
            tarjeta_h + gap_y
        )

        if tarjeta_mundo(
            mundo[0],
            mundo[1],
            x,
            y,
            mundo[2],
            mundo[3]
        ):
            mundo_click = mundo[0]

    if mundo_click:

        mundo_seleccionado = mundo_click

        iniciar_nivel()

        estado_actual = ESTADO_JUGANDO

    if boton(
        "VOLVER",
        cx - 150,
        panel_y + panel_h - 70,
        300,
        50,
        (65, 65, 80),
        (95, 95, 115),
        "←"
    ):
        estado_actual = ESTADO_HOME


class Jugador:

    def __init__(self):

        self.x = 150.0
        self.y = 450.0

        self.vx = 0.0
        self.vy = 0.0

        self.velocidad_max = 300.0
        self.aceleracion = 1500.0
        self.friccion = 10.0

        self.vida_max = 100
        self.vida = 100

        self.tamano = 75
        self.direccion = 1

        self.atacando = False
        self.duracion_ataque = 0.30
        self.tiempo_ataque = 0
        self.cooldown_ataque = 0
        self.cooldown_max = 0.12
        self.enemigos_golpeados = set()

        self.invulnerable = 0
        self.invulnerable_max = 0.65

        self.knockback_x = 0
        self.knockback_y = 0

        self.granos = 0
        self.enemigos_derrotados = 0

        self.tiempo_animacion = 0
        self.esta_moviendose = False

    def actualizar(self, delta):

        teclas = pygame.key.get_pressed()

        input_x = 0
        input_y = 0

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            input_x -= 1

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            input_x += 1

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            input_y -= 1

        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            input_y += 1

        magnitud = math.hypot(
            input_x,
            input_y
        )

        if magnitud > 0:

            input_x /= magnitud
            input_y /= magnitud

            self.esta_moviendose = True

            if input_x != 0:
                self.direccion = 1 if input_x > 0 else -1

            self.vx += (
                input_x *
                self.aceleracion *
                delta
            )

            self.vy += (
                input_y *
                self.aceleracion *
                delta
            )

        else:
            self.esta_moviendose = False

        factor_friccion = pow(
            0.0005,
            delta
        )

        if input_x == 0:
            self.vx *= factor_friccion

        if input_y == 0:
            self.vy *= factor_friccion

        velocidad = math.hypot(
            self.vx,
            self.vy
        )

        if velocidad > self.velocidad_max:

            factor = (
                self.velocidad_max /
                velocidad
            )

            self.vx *= factor
            self.vy *= factor

        self.x += self.knockback_x * delta
        self.y += self.knockback_y * delta

        self.knockback_x *= pow(
            0.01,
            delta
        )

        self.knockback_y *= pow(
            0.01,
            delta
        )

        self.x += self.vx * delta
        self.y += self.vy * delta

        self.x = clamp(
            self.x,
            45,
            1055
        )

        self.y = clamp(
            self.y,
            185,
            590
        )

        if self.invulnerable > 0:
            self.invulnerable -= delta

        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= delta

        if self.atacando:

            self.tiempo_ataque += delta

            if self.tiempo_ataque >= self.duracion_ataque:

                self.atacando = False
                self.tiempo_ataque = 0

                self.enemigos_golpeados.clear()

        self.tiempo_animacion += delta

    def atacar(self):

        if self.atacando or self.cooldown_ataque > 0:
            return

        self.atacando = True
        self.tiempo_ataque = 0
        self.cooldown_ataque = self.cooldown_max

        self.enemigos_golpeados.clear()

    def puede_golpear(self):

        if not self.atacando:
            return False

        progreso = (
            self.tiempo_ataque /
            self.duracion_ataque
        )

        return 0.15 <= progreso <= 0.75

    def recibir_dano(
        self,
        cantidad,
        origen_x=None,
        origen_y=None
    ):

        if self.invulnerable > 0:
            return False

        self.vida -= cantidad
        self.vida = max(0, self.vida)

        self.invulnerable = self.invulnerable_max

        if origen_x is not None and origen_y is not None:

            dx = self.x - origen_x
            dy = self.y - origen_y

            distancia = max(
                1,
                math.hypot(dx, dy)
            )

            dx /= distancia
            dy /= distancia

            self.knockback_x = dx * 280
            self.knockback_y = dy * 280

        crear_particulas(
            self.x,
            self.y,
            ROJO_CLARO,
            12,
            70,
            200,
            0.45,
            5
        )

        textos_flotantes.append(
            TextoFlotante(
                f"-{cantidad}",
                self.x,
                self.y - 55,
                ROJO_CLARO
            )
        )

        aplicar_shake(9, 0.18)

        return True

    def dibujar(self):

        pygame.draw.ellipse(
            pantalla,
            (25, 35, 25),
            (
                int(self.x - 30),
                int(self.y + 22),
                60,
                17
            )
        )

        movimiento = math.hypot(
            self.vx,
            self.vy
        )

        fuerza_mov = clamp(
            movimiento / self.velocidad_max,
            0,
            1
        )

        bob = (
            math.sin(
                self.tiempo_animacion * 12
            ) * 4 * fuerza_mov
        )

        inclinacion = clamp(
            self.vx / 75,
            -7,
            7
        )

        if self.atacando:

            progreso = clamp(
                self.tiempo_ataque /
                self.duracion_ataque,
                0,
                1
            )

            inclinacion += (
                math.sin(progreso * math.pi) *
                7 *
                self.direccion
            )

        if not sprite_pollito:

            pygame.draw.circle(
                pantalla,
                BLANCO,
                (
                    int(self.x),
                    int(self.y + bob)
                ),
                30
            )

        else:

            base = (
                sprite_pollito
                if self.direccion == 1
                else sprite_pollito_flip
            )

            imagen = pygame.transform.rotozoom(
                base,
                -inclinacion,
                1
            )

            if (
                self.invulnerable > 0
                and int(self.invulnerable * 18) % 2 == 0
            ):

                imagen = imagen.copy()
                imagen.set_alpha(90)

            rect = imagen.get_rect(
                center=(
                    int(self.x),
                    int(self.y + bob)
                )
            )

            pantalla.blit(
                imagen,
                rect
            )

        if self.atacando:
            self.dibujar_ataque()

    def dibujar_ataque(self):

        progreso = clamp(
            self.tiempo_ataque /
            self.duracion_ataque,
            0,
            1
        )

        if self.direccion == 1:
            angulo_inicio = -80 + progreso * 160
        else:
            angulo_inicio = 260 - progreso * 160

        angulo_rad = math.radians(
            angulo_inicio
        )

        largo = 78

        punta_x = (
            self.x +
            math.cos(angulo_rad) * largo
        )

        punta_y = (
            self.y +
            math.sin(angulo_rad) * largo
        )

        pygame.draw.line(
            pantalla,
            (40, 40, 50),
            (int(self.x), int(self.y)),
            (int(punta_x), int(punta_y)),
            10
        )

        pygame.draw.line(
            pantalla,
            BLANCO,
            (int(self.x), int(self.y)),
            (int(punta_x), int(punta_y)),
            6
        )

        pygame.draw.line(
            pantalla,
            ORO,
            (int(self.x), int(self.y)),
            (int(punta_x), int(punta_y)),
            3
        )

        radio = 85

        rect_arco = pygame.Rect(
            int(self.x - radio),
            int(self.y - radio),
            radio * 2,
            radio * 2
        )

        inicio = angulo_rad - 0.45
        fin = angulo_rad + 0.45

        try:
            pygame.draw.arc(
                pantalla,
                (255, 225, 100),
                rect_arco,
                inicio,
                fin,
                4
            )
        except:
            pass


class Grano:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.tiempo = random.random() * 10

        self.recogido = False
        self.anim_recoleccion = 0

    def actualizar(
        self,
        delta,
        jugador
    ):

        self.tiempo += delta * 4

        if self.recogido:

            self.anim_recoleccion += delta
            return

        distancia = distancia_entre(
            jugador.x,
            jugador.y,
            self.x,
            self.y
        )

        if distancia < 95:

            fuerza = 1 - distancia / 95
            velocidad = 170 + fuerza * 250

            if distancia > 1:

                self.x += (
                    (jugador.x - self.x) /
                    distancia *
                    velocidad *
                    delta
                )

                self.y += (
                    (jugador.y - self.y) /
                    distancia *
                    velocidad *
                    delta
                )

        if distancia < 42:

            self.recogido = True
            jugador.granos += 1

            crear_particulas(
                self.x,
                self.y,
                ORO,
                14,
                80,
                220,
                0.55,
                5
            )

            textos_flotantes.append(
                TextoFlotante(
                    "+1 🌽",
                    self.x,
                    self.y - 20,
                    ORO
                )
            )

    def dibujar(self):

        if self.recogido:
            return

        rebote = math.sin(self.tiempo) * 5

        brillo = (
            math.sin(self.tiempo * 1.5) + 1
        ) / 2

        radio = int(
            13 + brillo * 4
        )

        pygame.draw.ellipse(
            pantalla,
            (25, 70, 30),
            (
                int(self.x - 10),
                int(self.y + 12),
                20,
                7
            )
        )

        pygame.draw.circle(
            pantalla,
            (255, 220, 50),
            (
                int(self.x),
                int(self.y + rebote)
            ),
            radio,
            2
        )

        pygame.draw.ellipse(
            pantalla,
            ORO,
            (
                int(self.x - 7),
                int(self.y - 10 + rebote),
                14,
                20
            )
        )

        pygame.draw.ellipse(
            pantalla,
            AMARILLO,
            (
                int(self.x - 3),
                int(self.y - 8 + rebote),
                5,
                13
            )
        )

        pygame.draw.line(
            pantalla,
            VERDE,
            (
                int(self.x),
                int(self.y - 10 + rebote)
            ),
            (
                int(self.x + 8),
                int(self.y - 17 + rebote)
            ),
            3
        )


class Enemigo:

    contador_ids = 0

    def __init__(self, x, y):

        self.id = Enemigo.contador_ids
        Enemigo.contador_ids += 1

        self.x = float(x)
        self.y = float(y)

        self.vx = 0
        self.vy = 0

        self.vida_max = 40
        self.vida = 40

        self.velocidad = random.uniform(
            95,
            125
        )

        self.direccion = random.choice(
            [-1, 1]
        )

        self.tiempo = random.random() * 10
        self.muerto = False

        self.ataque_cooldown = random.uniform(
            0.4,
            1.2
        )

        self.duracion_cooldown = 1.15

        self.knockback_x = 0
        self.knockback_y = 0

        self.flash = 0
        self.radio = 28

        self.punto_patrulla_x = self.x

    def actualizar(
        self,
        delta,
        jugador,
        lista_enemigos
    ):

        if self.muerto:
            return

        self.tiempo += delta

        if self.flash > 0:
            self.flash -= delta

        self.ataque_cooldown -= delta

        dx = jugador.x - self.x
        dy = jugador.y - self.y

        distancia = math.hypot(dx, dy)

        objetivo_vx = 0
        objetivo_vy = 0

        if distancia < 320:

            if distancia > 58 and distancia > 0:

                nx = dx / distancia
                ny = dy / distancia

                objetivo_vx = nx * self.velocidad
                objetivo_vy = ny * self.velocidad

                self.direccion = (
                    1 if nx > 0 else -1
                )

        else:

            objetivo_vx = (
                self.velocidad *
                0.45 *
                self.direccion
            )

            if self.x < 80:
                self.direccion = 1

            if self.x > 1020:
                self.direccion = -1

        separacion_x = 0
        separacion_y = 0

        for otro in lista_enemigos:

            if otro is self or otro.muerto:
                continue

            odx = self.x - otro.x
            ody = self.y - otro.y

            odist = math.hypot(
                odx,
                ody
            )

            if 0 < odist < 58:

                fuerza = 1 - odist / 58

                separacion_x += (
                    odx /
                    odist *
                    fuerza *
                    130
                )

                separacion_y += (
                    ody /
                    odist *
                    fuerza *
                    130
                )

        objetivo_vx += separacion_x
        objetivo_vy += separacion_y

        suavizado = (
            1 -
            math.exp(-8 * delta)
        )

        self.vx = lerp(
            self.vx,
            objetivo_vx,
            suavizado
        )

        self.vy = lerp(
            self.vy,
            objetivo_vy,
            suavizado
        )

        self.x += self.knockback_x * delta
        self.y += self.knockback_y * delta

        self.knockback_x *= pow(
            0.005,
            delta
        )

        self.knockback_y *= pow(
            0.005,
            delta
        )

        self.x += self.vx * delta
        self.y += self.vy * delta

        self.x = clamp(
            self.x,
            60,
            1040
        )

        self.y = clamp(
            self.y,
            190,
            570
        )

        if (
            distancia < 66
            and self.ataque_cooldown <= 0
        ):

            jugador.recibir_dano(
                8,
                self.x,
                self.y
            )

            self.ataque_cooldown = self.duracion_cooldown

    def recibir_dano(
        self,
        cantidad,
        jugador
    ):

        if self.muerto:
            return False

        self.vida -= cantidad
        self.flash = 0.11

        dx = self.x - jugador.x
        dy = self.y - jugador.y

        distancia = max(
            1,
            math.hypot(dx, dy)
        )

        self.knockback_x = (
            dx /
            distancia *
            320
        )

        self.knockback_y = (
            dy /
            distancia *
            320
        )

        crear_particulas(
            self.x,
            self.y,
            ROJO_CLARO,
            9,
            60,
            190,
            0.4,
            5
        )

        textos_flotantes.append(
            TextoFlotante(
                f"-{cantidad}",
                self.x,
                self.y - 70,
                BLANCO
            )
        )

        aplicar_shake(5, 0.09)

        if self.vida <= 0:

            self.vida = 0
            self.muerto = True

            crear_particulas(
                self.x,
                self.y,
                ORO,
                22,
                80,
                270,
                0.7,
                6
            )

            aplicar_shake(
                10,
                0.2
            )

            return True

        return False

    def dibujar(self):

        if self.muerto:
            return

        bob = (
            math.sin(
                self.tiempo * 5
            ) * 2
        )

        y = self.y + bob

        pygame.draw.ellipse(
            pantalla,
            (30, 55, 30),
            (
                int(self.x - 27),
                int(self.y + 23),
                54,
                14
            )
        )

        cuerpo_color = (
            (210, 100, 80)
            if self.flash > 0
            else (110, 70, 40)
        )

        cabeza_color = (
            (235, 125, 95)
            if self.flash > 0
            else (135, 85, 45)
        )

        pygame.draw.circle(
            pantalla,
            cuerpo_color,
            (
                int(self.x),
                int(y)
            ),
            28
        )

        pygame.draw.circle(
            pantalla,
            cabeza_color,
            (
                int(self.x),
                int(y - 25)
            ),
            22
        )

        pygame.draw.ellipse(
            pantalla,
            (160, 105, 70),
            (
                int(self.x - 14),
                int(y - 23),
                28,
                18
            )
        )

        ojo_offset = (
            2 if self.direccion == 1 else -2
        )

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (
                int(self.x - 8 + ojo_offset),
                int(y - 31)
            ),
            5
        )

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (
                int(self.x + 8 + ojo_offset),
                int(y - 31)
            ),
            5
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (
                int(self.x - 7 + ojo_offset),
                int(y - 30)
            ),
            2
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (
                int(self.x + 9 + ojo_offset),
                int(y - 30)
            ),
            2
        )

        pygame.draw.polygon(
            pantalla,
            ROJO,
            [
                (
                    int(self.x - 16),
                    int(y - 43)
                ),
                (
                    int(self.x - 25),
                    int(y - 58)
                ),
                (
                    int(self.x - 5),
                    int(y - 47)
                )
            ]
        )

        pygame.draw.polygon(
            pantalla,
            ROJO,
            [
                (
                    int(self.x + 16),
                    int(y - 43)
                ),
                (
                    int(self.x + 25),
                    int(y - 58)
                ),
                (
                    int(self.x + 5),
                    int(y - 47)
                )
            ]
        )

        ancho_barra = 55
        porcentaje = self.vida / self.vida_max

        pygame.draw.rect(
            pantalla,
            NEGRO,
            (
                int(self.x - ancho_barra / 2),
                int(y - 67),
                ancho_barra,
                7
            ),
            border_radius=4
        )

        if porcentaje > 0:

            pygame.draw.rect(
                pantalla,
                ROJO_CLARO,
                (
                    int(self.x - ancho_barra / 2),
                    int(y - 67),
                    int(ancho_barra * porcentaje),
                    7
                ),
                border_radius=4
            )


def dibujar_arbol(x, y):

    pygame.draw.ellipse(
        pantalla,
        (40, 90, 40),
        (
            x - 42,
            y + 48,
            84,
            25
        )
    )

    pygame.draw.rect(
        pantalla,
        CAFE,
        (
            x - 12,
            y,
            24,
            65
        ),
        border_radius=5
    )

    pygame.draw.rect(
        pantalla,
        CAFE_CLARO,
        (
            x - 5,
            y + 4,
            7,
            55
        ),
        border_radius=3
    )

    pygame.draw.circle(
        pantalla,
        (35, 110, 45),
        (x, y - 10),
        42
    )

    pygame.draw.circle(
        pantalla,
        CESPED_CLARO,
        (x - 22, y - 25),
        25
    )

    pygame.draw.circle(
        pantalla,
        (45, 125, 50),
        (x + 25, y - 20),
        27
    )

    pygame.draw.circle(
        pantalla,
        (100, 190, 90),
        (x - 12, y - 37),
        10
    )


def dibujar_piedra(x, y):

    pygame.draw.ellipse(
        pantalla,
        (40, 80, 45),
        (
            x - 29,
            y - 5,
            58,
            18
        )
    )

    pygame.draw.ellipse(
        pantalla,
        (95, 95, 100),
        (
            x - 25,
            y - 12,
            50,
            25
        )
    )

    pygame.draw.ellipse(
        pantalla,
        (135, 135, 140),
        (
            x - 15,
            y - 8,
            20,
            8
        )
    )


def dibujar_granero():

    x = 820
    y = 235

    pygame.draw.ellipse(
        pantalla,
        (45, 90, 45),
        (
            x - 10,
            y + 130,
            210,
            40
        )
    )

    pygame.draw.rect(
        pantalla,
        (155, 45, 45),
        (
            x,
            y,
            180,
            150
        )
    )

    for yy in range(
        y + 10,
        y + 145,
        18
    ):

        pygame.draw.line(
            pantalla,
            (135, 38, 38),
            (x, yy),
            (x + 180, yy),
            2
        )

    pygame.draw.polygon(
        pantalla,
        (95, 35, 35),
        [
            (x - 20, y),
            (x + 90, y - 90),
            (x + 200, y)
        ]
    )

    pygame.draw.polygon(
        pantalla,
        (125, 45, 45),
        [
            (x, y - 2),
            (x + 90, y - 75),
            (x + 180, y - 2)
        ],
        4
    )

    pygame.draw.rect(
        pantalla,
        CAFE,
        (
            x + 65,
            y + 70,
            50,
            80
        )
    )

    pygame.draw.line(
        pantalla,
        CAFE_CLARO,
        (x + 65, y + 75),
        (x + 115, y + 145),
        5
    )

    pygame.draw.line(
        pantalla,
        CAFE_CLARO,
        (x + 115, y + 75),
        (x + 65, y + 145),
        5
    )

    dibujar_texto(
        "GRANERO",
        fuente_mini,
        BLANCO,
        x + 90,
        y - 28
    )


# ============================================================
# FONDO DEL MUNDO JUGABLE
# ============================================================

def dibujar_mundo_granja():

    if fondo_granja_cache:

        pantalla.blit(
            fondo_granja_cache,
            (0, 0)
        )

        return

    # Si granja.jpg no existe, conserva el fondo original.

    pygame.draw.rect(
        pantalla,
        CIELO,
        (
            0,
            0,
            ANCHO_BASE,
            180
        )
    )

    pygame.draw.rect(
        pantalla,
        CIELO_CLARO,
        (
            0,
            0,
            ANCHO_BASE,
            80
        )
    )

    pygame.draw.circle(
        pantalla,
        (255, 238, 140),
        (75, 70),
        38
    )

    pygame.draw.circle(
        pantalla,
        (255, 245, 185),
        (75, 70),
        27
    )

    t = pygame.time.get_ticks() / 1000

    nubes = [
        (150, 80, 0.6),
        (450, 55, 0.35),
        (750, 95, 0.5),
        (1000, 50, 0.25)
    ]

    for x, y, velocidad in nubes:

        offset = (
            math.sin(
                t * velocidad
            ) * 9
        )

        nx = int(x + offset)

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (nx, y),
            25
        )

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (nx + 25, y + 5),
            20
        )

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (nx - 25, y + 7),
            18
        )

    pygame.draw.polygon(
        pantalla,
        (80, 145, 90),
        [
            (0, 180),
            (120, 125),
            (250, 180)
        ]
    )

    pygame.draw.polygon(
        pantalla,
        (75, 140, 85),
        [
            (150, 180),
            (340, 115),
            (520, 180)
        ]
    )

    pygame.draw.polygon(
        pantalla,
        (80, 145, 90),
        [
            (480, 180),
            (680, 130),
            (850, 180)
        ]
    )

    pygame.draw.rect(
        pantalla,
        CESPED,
        (
            0,
            180,
            ANCHO_BASE,
            520
        )
    )

    for y in range(
        200,
        610,
        45
    ):

        pygame.draw.line(
            pantalla,
            (58, 140, 62),
            (0, y),
            (ANCHO_BASE, y),
            2
        )

    pygame.draw.ellipse(
        pantalla,
        (120, 90, 52),
        (
            245,
            367,
            665,
            185
        )
    )

    pygame.draw.ellipse(
        pantalla,
        TIERRA,
        (
            250,
            360,
            650,
            180
        )
    )

    pygame.draw.ellipse(
        pantalla,
        TIERRA_CLARA,
        (
            290,
            390,
            560,
            100
        )
    )

    random.seed(7)

    for _ in range(75):

        gx = random.randint(
            10,
            1090
        )

        gy = random.randint(
            195,
            595
        )

        if (
            320 < gx < 850
            and 375 < gy < 520
        ):
            continue

        pygame.draw.line(
            pantalla,
            (40, 115, 48),
            (gx, gy),
            (
                gx + random.randint(-3, 3),
                gy - random.randint(4, 9)
            ),
            2
        )

    random.seed()

    for x in range(
        20,
        ANCHO_BASE,
        70
    ):

        pygame.draw.rect(
            pantalla,
            CAFE,
            (
                x,
                610,
                12,
                55
            )
        )

        pygame.draw.rect(
            pantalla,
            CAFE,
            (
                x,
                625,
                70,
                8
            )
        )

        pygame.draw.rect(
            pantalla,
            CAFE,
            (
                x,
                650,
                70,
                8
            )
        )

        pygame.draw.rect(
            pantalla,
            CAFE_CLARO,
            (
                x + 2,
                612,
                3,
                50
            )
        )

    dibujar_arbol(100, 260)
    dibujar_arbol(250, 220)
    dibujar_arbol(560, 250)
    dibujar_arbol(720, 225)

    dibujar_piedra(390, 270)
    dibujar_piedra(470, 560)
    dibujar_piedra(680, 500)

    dibujar_granero()


def dibujar_hud(jugador):

    hud = pygame.Surface(
        (ANCHO_BASE, 95),
        pygame.SRCALPHA
    )

    hud.fill(
        (10, 15, 25, 235)
    )

    pantalla.blit(
        hud,
        (0, 0)
    )

    pygame.draw.line(
        pantalla,
        ORO,
        (0, 95),
        (ANCHO_BASE, 95),
        3
    )

    dibujar_texto(
        "🌾 MUNDO 1 • LA GRANJA",
        fuente_subtitulo,
        ORO,
        180,
        30
    )

    dibujar_texto(
        "LA REBELIÓN COMIENZA",
        fuente_mini,
        BLANCO,
        180,
        62
    )

    x_vida = 400
    y_vida = 25

    dibujar_texto(
        "❤️",
        fuente_texto,
        BLANCO,
        x_vida,
        y_vida + 12,
        False
    )

    vida_pct = clamp(
        jugador.vida /
        jugador.vida_max,
        0,
        1
    )

    pygame.draw.rect(
        pantalla,
        (45, 45, 55),
        (
            x_vida + 25,
            y_vida,
            200,
            22
        ),
        border_radius=10
    )

    if vida_pct > 0:

        pygame.draw.rect(
            pantalla,
            ROJO_CLARO,
            (
                x_vida + 25,
                y_vida,
                int(200 * vida_pct),
                22
            ),
            border_radius=10
        )

        pygame.draw.line(
            pantalla,
            (255, 130, 120),
            (
                x_vida + 33,
                y_vida + 5
            ),
            (
                x_vida + 25 +
                max(
                    5,
                    int(200 * vida_pct) - 8
                ),
                y_vida + 5
            ),
            2
        )

    dibujar_texto(
        f"{jugador.vida}/{jugador.vida_max}",
        fuente_mini,
        BLANCO,
        x_vida + 125,
        y_vida + 11,
        False
    )

    dibujar_texto(
        f"🌽 {jugador.granos}/10",
        fuente_texto,
        ORO,
        700,
        38,
        False
    )

    dibujar_texto(
        f"👹 {jugador.enemigos_derrotados}/5",
        fuente_texto,
        ROJO_CLARO,
        870,
        38,
        False
    )

    control_panel = pygame.Surface(
        (370, 55),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        control_panel,
        (10, 15, 25, 205),
        control_panel.get_rect(),
        border_radius=15
    )

    pantalla.blit(
        control_panel,
        (
            15,
            ALTO_BASE - 72
        )
    )

    dibujar_texto(
        "WASD / FLECHAS  Mover",
        fuente_mini,
        BLANCO,
        200,
        ALTO_BASE - 53,
        False
    )

    dibujar_texto(
        "ESPACIO / CLICK  Atacar",
        fuente_mini,
        ORO,
        200,
        ALTO_BASE - 30,
        False
    )

    dibujar_texto(
        "ESC = Salir del mundo",
        fuente_mini,
        (220, 220, 230),
        ANCHO_BASE - 130,
        ALTO_BASE - 30
    )


jugador = Jugador()

granos = []
enemigos = []

nivel_iniciado = False
victoria_activa = False
derrota_activa = False


def iniciar_nivel():

    global jugador
    global granos
    global enemigos
    global nivel_iniciado
    global victoria_activa
    global derrota_activa
    global particulas
    global textos_flotantes

    jugador = Jugador()

    particulas.clear()
    textos_flotantes.clear()

    victoria_activa = False
    derrota_activa = False

    granos = [
        Grano(170, 280),
        Grano(330, 330),
        Grano(480, 240),
        Grano(600, 390),
        Grano(760, 350),
        Grano(900, 450),
        Grano(250, 520),
        Grano(520, 500),
        Grano(700, 280),
        Grano(950, 300),
    ]

    enemigos = [
        Enemigo(420, 300),
        Enemigo(650, 350),
        Enemigo(850, 480),
        Enemigo(350, 500),
        Enemigo(780, 260),
    ]

    nivel_iniciado = True


def pantalla_victoria():

    global estado_actual
    global nivel_iniciado

    overlay = pygame.Surface(
        (ANCHO_BASE, ALTO_BASE),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 160)
    )

    pantalla.blit(
        overlay,
        (0, 0)
    )

    panel_w = 650
    panel_h = 430

    px, py = panel_centrado(
        panel_w,
        panel_h,
        (20, 25, 35),
        245
    )

    cx = ANCHO_BASE // 2

    t = pygame.time.get_ticks() / 1000

    bob = math.sin(t * 3) * 6

    dibujar_texto(
        "🏆",
        fuente_titulo,
        ORO,
        cx,
        py + 70 + bob,
        False
    )

    dibujar_texto(
        "¡MUNDO COMPLETADO!",
        fuente_titulo_pequeno,
        ORO,
        cx,
        py + 140
    )

    dibujar_texto(
        "La granja ha sido liberada.",
        fuente_subtitulo,
        BLANCO,
        cx,
        py + 195
    )

    dibujar_texto(
        "🌽 Granos recolectados: 10/10",
        fuente_texto,
        ORO,
        cx,
        py + 245
    )

    dibujar_texto(
        "👹 Enemigos derrotados: 5/5",
        fuente_texto,
        ROJO_CLARO,
        cx,
        py + 280
    )

    if boton(
        "VOLVER AL INICIO",
        cx - 160,
        py + 330,
        320,
        60,
        (60, 100, 150),
        (80, 135, 190),
        "🏠"
    ):

        nivel_iniciado = False
        estado_actual = ESTADO_HOME


def pantalla_derrota():

    global estado_actual

    overlay = pygame.Surface(
        (ANCHO_BASE, ALTO_BASE),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 175)
    )

    pantalla.blit(
        overlay,
        (0, 0)
    )

    panel_w = 600
    panel_h = 350

    px, py = panel_centrado(
        panel_w,
        panel_h,
        (30, 15, 20),
        245
    )

    cx = ANCHO_BASE // 2

    dibujar_texto(
        "💀",
        fuente_titulo,
        ROJO_CLARO,
        cx,
        py + 65,
        False
    )

    dibujar_texto(
        "¡EL POLLO HA CAÍDO!",
        fuente_titulo_pequeno,
        ROJO_CLARO,
        cx,
        py + 130
    )

    dibujar_texto(
        "La rebelión tendrá que esperar...",
        fuente_texto,
        BLANCO,
        cx,
        py + 180
    )

    if boton(
        "REINTENTAR",
        cx - 150,
        py + 230,
        300,
        60,
        (170, 55, 35),
        (220, 75, 40),
        "↻"
    ):

        iniciar_nivel()
        estado_actual = ESTADO_JUGANDO


def actualizar_ataques():

    if not jugador.puede_golpear():
        return

    for enemigo in enemigos:

        if enemigo.muerto:
            continue

        if enemigo.id in jugador.enemigos_golpeados:
            continue

        dx = enemigo.x - jugador.x
        dy = enemigo.y - jugador.y

        distancia = math.hypot(
            dx,
            dy
        )

        if distancia > 105:
            continue

        if (
            jugador.direccion == 1
            and dx < -15
        ):
            continue

        if (
            jugador.direccion == -1
            and dx > 15
        ):
            continue

        jugador.enemigos_golpeados.add(
            enemigo.id
        )

        derrotado = enemigo.recibir_dano(
            20,
            jugador
        )

        if derrotado:
            jugador.enemigos_derrotados += 1


def actualizar_efectos(delta):

    for particula in particulas[:]:

        particula.actualizar(delta)

        if particula.vida <= 0:
            particulas.remove(particula)

    for texto in textos_flotantes[:]:

        texto.actualizar(delta)

        if texto.vida <= 0:
            textos_flotantes.remove(texto)


def dibujar_efectos():

    for particula in particulas:
        particula.dibujar()

    for texto in textos_flotantes:
        texto.dibujar()


def jugar_mundo():

    global victoria_activa
    global derrota_activa

    if not nivel_iniciado:
        iniciar_nivel()

    dibujar_mundo_granja()

    if not victoria_activa and not derrota_activa:

        jugador.actualizar(dt)

        for grano in granos:
            grano.actualizar(
                dt,
                jugador
            )

        for enemigo in enemigos:
            enemigo.actualizar(
                dt,
                jugador,
                enemigos
            )

        actualizar_ataques()
        actualizar_efectos(dt)

    objetos = []

    for grano in granos:

        if not grano.recogido:
            objetos.append(
                (
                    grano.y,
                    "grano",
                    grano
                )
            )

    for enemigo in enemigos:

        if not enemigo.muerto:
            objetos.append(
                (
                    enemigo.y,
                    "enemigo",
                    enemigo
                )
            )

    objetos.append(
        (
            jugador.y,
            "jugador",
            jugador
        )
    )

    objetos.sort(
        key=lambda item: item[0]
    )

    for _, tipo, objeto in objetos:
        objeto.dibujar()

    dibujar_efectos()
    dibujar_hud(jugador)

    if (
        jugador.granos >= 10
        and jugador.enemigos_derrotados >= 5
    ):
        victoria_activa = True

    if jugador.vida <= 0:
        derrota_activa = True

    if victoria_activa:
        pantalla_victoria()

    elif derrota_activa:
        pantalla_derrota()


def pantalla_juego():
    jugar_mundo()


def presentar_pantalla():

    global shake_tiempo
    global shake_intensidad

    window_w, window_h = ventana.get_size()

    escala = min(
        window_w / ANCHO_BASE,
        window_h / ALTO_BASE
    )

    render_w = max(
        1,
        int(ANCHO_BASE * escala)
    )

    render_h = max(
        1,
        int(ALTO_BASE * escala)
    )

    superficie_final = pantalla

    offset_shake_x = 0
    offset_shake_y = 0

    if shake_tiempo > 0:

        shake_tiempo -= dt

        offset_shake_x = random.randint(
            -int(shake_intensidad),
            int(shake_intensidad)
        )

        offset_shake_y = random.randint(
            -int(shake_intensidad),
            int(shake_intensidad)
        )

        shake_intensidad *= pow(
            0.02,
            dt
        )

    else:
        shake_intensidad = 0

    escalada = pygame.transform.smoothscale(
        superficie_final,
        (
            render_w,
            render_h
        )
    )

    ventana.fill(NEGRO)

    pos_x = (
        window_w - render_w
    ) // 2

    pos_y = (
        window_h - render_h
    ) // 2

    ventana.blit(
        escalada,
        (
            pos_x + offset_shake_x,
            pos_y + offset_shake_y
        )
    )

    pygame.display.flip()


while True:

    dt = reloj.tick(
        FPS_OBJETIVO
    ) / 1000

    dt = min(
        dt,
        0.033
    )

    mouse_click = False

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1:

                mouse_click = True

                if (
                    estado_actual == ESTADO_JUGANDO
                    and not victoria_activa
                    and not derrota_activa
                ):
                    jugador.atacar()

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_SPACE:

                if (
                    estado_actual == ESTADO_JUGANDO
                    and not victoria_activa
                    and not derrota_activa
                ):
                    jugador.atacar()

            if evento.key == pygame.K_ESCAPE:

                if estado_actual == ESTADO_JUGANDO:

                    nivel_iniciado = False
                    victoria_activa = False
                    derrota_activa = False

                    estado_actual = ESTADO_HOME

                elif estado_actual == ESTADO_MUNDOS:

                    estado_actual = ESTADO_HOME

                elif estado_actual == ESTADO_HOME:

                    estado_actual = ESTADO_MENU

        if evento.type == pygame.VIDEORESIZE:

            nuevo_ancho = max(
                evento.w,
                MIN_ANCHO
            )

            nuevo_alto = max(
                evento.h,
                MIN_ALTO
            )

            ventana = pygame.display.set_mode(
                (
                    nuevo_ancho,
                    nuevo_alto
                ),
                pygame.RESIZABLE
            )

    pantalla.fill(NEGRO)

    if estado_actual != ESTADO_JUGANDO:
        dibujar_fondo()

    if estado_actual == ESTADO_MENU:

        menu_principal()

    elif estado_actual == ESTADO_HOME:

        pantalla_home()

    elif estado_actual == ESTADO_MUNDOS:

        seleccionar_mundo()

    elif estado_actual == ESTADO_JUGANDO:

        pantalla_juego()

    presentar_pantalla()