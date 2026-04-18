"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""
import random
from entorno import Agente

class MiAgente(Agente):
    """
    Agente de navegación que toma decisiones para llegar a la meta de forma eficiente.
    """
    
    def __init__(self):
        super().__init__(nombre="Mi Agente")
        self.visitados = set()  # Para almacenar posiciones ya visitadas

    def al_iniciar(self):
        """Llamado al inicio para reiniciar las posiciones visitadas."""
        self.visitados = set()

    def decidir(self, percepcion):
        """
        Decide la siguiente acción del agente basándose en su percepción.
        
        Parámetros:
            percepcion – diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        pos_actual = percepcion['posicion']
        self.visitados.add(pos_actual)  # Guardamos la posición actual para no repetirla

        # 1. Si la meta está cerca, vamos directamente hacia ella
        for direccion in self.ACCIONES:
            if percepcion[direccion] == 'meta':
                return direccion
        
        # 2. Direcciones ideales para acercarse a la meta
        vert, horiz = percepcion['direccion_meta']
        direcciones_ideales = [vert, horiz]

        # 3. Clasificamos las opciones de movimiento
        no_visitadas_ideales = []  # Direcciones que nos acercan a la meta y no hemos visitado
        no_visitadas = []  # Direcciones no visitadas
        visitadas = []  # Direcciones ya visitadas

        # Evaluamos las direcciones disponibles
        for direccion in self.ACCIONES:
            if percepcion[direccion] == 'libre':  # Solo consideramos las celdas libres
                # Calculamos la nueva posición si nos movemos en esa dirección
                desplazamiento_fila, desplazamiento_columna = self.DELTAS[direccion]
                pos_futura = (pos_actual[0] + desplazamiento_fila, pos_actual[1] + desplazamiento_columna)

                # Si no hemos visitado esta posición, la agregamos a las opciones
                if pos_futura not in self.visitados:
                    if direccion in direcciones_ideales:
                        no_visitadas_ideales.append(direccion)
                    else:
                        no_visitadas.append(direccion)
                else:
                    visitadas.append(direccion)

        # 4. Decisión: Primero intentamos mover hacia la meta
        if no_visitadas_ideales:
            return random.choice(no_visitadas_ideales)  # Escoge una dirección ideal

        # 5. Si no tenemos direcciones ideales, exploramos caminos nuevos
        if no_visitadas:
            return random.choice(no_visitadas)  # Escoge un camino no visitado

        # 6. Si estamos atrapados, retrocedemos
        if visitadas:
            return random.choice(visitadas)  # Retrocedemos a una dirección ya visitada

        # 7. Si todo falla, movemos hacia abajo (última opción)
        return 'abajo'
        # Ejemplo básico (bórralo y escribe tu propia lógica):
        #
        # vert, horiz = percepcion['direccion_meta']
        #
        # if percepcion[vert] == 'libre' or percepcion[vert] == 'meta':
        #     return vert
        # if percepcion[horiz] == 'libre' or percepcion[horiz] == 'meta':
        #     return horiz
        #
        # return 'abajo'
        #print('Hola decidir')
        #for direccion in self.ACCIONES:
        #    celda = percepcion[direccion]
        #    if celda == 'meta':
        #        return direccion
        #    if celda == 'libre':
        #        return direccion

        #return 'abajo'  # ← Reemplazar con tu lógica