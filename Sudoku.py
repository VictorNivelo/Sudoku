import pygame
import random

pygame.init()

ANCHO, ALTO = 580, 600
TAMANO_CELDA = 60
MARGEN = 20
FPS = 60
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (0, 120, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sudoku")
reloj = pygame.time.Clock()

fuente_grande = pygame.font.Font(None, 74)
fuente_mediana = pygame.font.Font(None, 48)
fuente_pequeña = pygame.font.Font(None, 36)

controles = {
    "arriba": pygame.K_UP,
    "abajo": pygame.K_DOWN,
    "izquierda": pygame.K_LEFT,
    "derecha": pygame.K_RIGHT,
    "pausa": pygame.K_ESCAPE,
}


class Sudoku:
    def __init__(self):
        self.tablero = self.generar_tablero()
        self.tablero_original = [fila[:] for fila in self.tablero]
        self.seleccion = (0, 0)

    def generar_tablero(self):
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return random.sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        squares = side * side
        empties = squares * 3 // 4
        for p in random.sample(range(squares), empties):
            board[p // side][p % side] = 0
        return board

    def dibujar(self):
        for i in range(9):
            for j in range(9):
                x = MARGEN + j * TAMANO_CELDA
                y = MARGEN + i * TAMANO_CELDA
                valor = self.tablero[i][j]

                if (i, j) == self.seleccion:
                    pygame.draw.rect(pantalla, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                elif self.tablero_original[i][j] != 0:
                    pygame.draw.rect(pantalla, GRIS, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                else:
                    pygame.draw.rect(
                        pantalla, BLANCO, (x, y, TAMANO_CELDA, TAMANO_CELDA)
                    )

                pygame.draw.rect(pantalla, NEGRO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)

                if valor != 0:
                    texto = fuente_mediana.render(str(valor), True, NEGRO)
                    pantalla.blit(
                        texto,
                        (
                            x + TAMANO_CELDA // 2 - texto.get_width() // 2,
                            y + TAMANO_CELDA // 2 - texto.get_height() // 2,
                        ),
                    )
        for i in range(4):
            pygame.draw.line(
                pantalla,
                NEGRO,
                (MARGEN + i * 3 * TAMANO_CELDA, MARGEN),
                (MARGEN + i * 3 * TAMANO_CELDA, MARGEN + 9 * TAMANO_CELDA),
                3,
            )
            pygame.draw.line(
                pantalla,
                NEGRO,
                (MARGEN, MARGEN + i * 3 * TAMANO_CELDA),
                (MARGEN + 9 * TAMANO_CELDA, MARGEN + i * 3 * TAMANO_CELDA),
                3,
            )

    def seleccionar(self, pos):
        if (
            MARGEN <= pos[0] < MARGEN + 9 * TAMANO_CELDA
            and MARGEN <= pos[1] < MARGEN + 9 * TAMANO_CELDA
        ):
            x = (pos[0] - MARGEN) // TAMANO_CELDA
            y = (pos[1] - MARGEN) // TAMANO_CELDA
            self.seleccion = (y, x)

    def mover_seleccion(self, dx, dy):
        x, y = self.seleccion
        self.seleccion = ((y + dy) % 9, (x + dx) % 9)

    def insertar(self, valor):
        if self.tablero_original[self.seleccion[0]][self.seleccion[1]] == 0:
            self.tablero[self.seleccion[0]][self.seleccion[1]] = valor

    def verificar_victoria(self):
        for fila in self.tablero:
            if 0 in fila or len(set(fila)) != 9:
                return False
        for columna in zip(*self.tablero):
            if 0 in columna or len(set(columna)) != 9:
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                cuadro = [
                    self.tablero[x][y] for x in range(i, i + 3) for y in range(j, j + 3)
                ]
                if 0 in cuadro or len(set(cuadro)) != 9:
                    return False
        return True


def menu_principal():
    seleccion = 0
    opciones = ["Jugar", "Personalizar Controles", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente_grande.render("Sudoku", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else GRIS
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    return opciones[seleccion].lower()
        pygame.display.flip()
        reloj.tick(FPS)


def personalizar_controles():
    fuente = pygame.font.Font(None, 36)
    fuente_titulo = pygame.font.Font(None, 46)
    fuente_instrucciones = pygame.font.Font(None, 26)
    controles_orden = ["arriba", "abajo", "izquierda", "derecha", "pausa"]
    seleccion = 0
    esperando_tecla = False
    gris_claro = (200, 200, 200)
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente_titulo.render("Personalizar Controles", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 6)
        )
        for i, control in enumerate(controles_orden):
            color = AZUL if i == seleccion else BLANCO
            texto = f"{control.capitalize()}: {pygame.key.name(controles[control])}"
            if esperando_tecla and i == seleccion:
                texto = f"{control.capitalize()}: Presiona una tecla..."
            texto_renderizado = fuente.render(texto, True, color)
            pantalla.blit(
                texto_renderizado,
                (ANCHO // 2 - texto_renderizado.get_width() // 2, ALTO // 3 + i * 50),
            )
        texto_instruccion = fuente_instrucciones.render(
            "Presiona ENTER para personalizar", True, gris_claro
        )
        pantalla.blit(
            texto_instruccion,
            (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTO - 100),
        )
        texto_volver = fuente_instrucciones.render(
            "Presiona ESC para volver", True, gris_claro
        )
        pantalla.blit(
            texto_volver, (ANCHO // 2 - texto_volver.get_width() // 2, ALTO - 60)
        )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if esperando_tecla:
                    controles[controles_orden[seleccion]] = evento.key
                    esperando_tecla = False
                else:
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(controles_orden)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(controles_orden)
                    elif evento.key == pygame.K_RETURN:
                        esperando_tecla = True
                    elif evento.key == pygame.K_ESCAPE:
                        return
        pygame.display.flip()


def pausar():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Continuar", "Reiniciar", "Menu Principal"]
    while True:
        pantalla.fill(NEGRO)
        texto_pausa = fuente.render("Pausa", True, BLANCO)
        pantalla.blit(
            texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    return opciones[seleccion].lower()
        pygame.display.flip()


def juego():
    sudoku = Sudoku()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    sudoku.seleccionar(evento.pos)
            if evento.type == pygame.KEYDOWN:
                if evento.key == controles["pausa"]:
                    accion = pausar()
                    if accion == "continuar":
                        continue
                    elif accion == "reiniciar":
                        sudoku = Sudoku()
                        continue
                    elif accion == "menu principal":
                        return "menu principal"
                    elif accion == "salir":
                        return "salir"
                if evento.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                    pygame.K_KP1,
                    pygame.K_KP2,
                    pygame.K_KP3,
                    pygame.K_KP4,
                    pygame.K_KP5,
                    pygame.K_KP6,
                    pygame.K_KP7,
                    pygame.K_KP8,
                    pygame.K_KP9,
                ]:
                    if evento.key in [
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                        pygame.K_5,
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9,
                    ]:
                        sudoku.insertar(int(evento.unicode))
                    else:
                        sudoku.insertar(evento.key - pygame.K_KP1 + 1)
                elif (
                    evento.key == pygame.K_BACKSPACE
                    or evento.key == pygame.K_DELETE
                    or evento.key == pygame.K_KP0
                ):
                    sudoku.insertar(0)
                elif evento.key == controles["arriba"]:
                    sudoku.mover_seleccion(0, -1)
                elif evento.key == controles["abajo"]:
                    sudoku.mover_seleccion(0, 1)
                elif evento.key == controles["izquierda"]:
                    sudoku.mover_seleccion(-1, 0)
                elif evento.key == controles["derecha"]:
                    sudoku.mover_seleccion(1, 0)
        pantalla.fill(BLANCO)
        sudoku.dibujar()
        if sudoku.verificar_victoria():
            texto_victoria = fuente_grande.render("¡Ganaste!", True, VERDE)
            pantalla.blit(
                texto_victoria,
                (ANCHO // 2 - texto_victoria.get_width() // 2, ALTO - 100),
            )
        pygame.display.flip()
        reloj.tick(FPS)


def main():
    while True:
        accion = menu_principal()
        if accion == "jugar":
            resultado = juego()
            if resultado == "salir":
                break
        elif accion == "personalizar controles":
            personalizar_controles()
        elif accion == "salir":
            break
    pygame.quit()


if __name__ == "__main__":
    main()
