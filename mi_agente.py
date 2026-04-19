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
        self.visitados = set()  #PARA GUARDAR LAS POSICIONES VISITADAS
        self.pasos = 0  #CONTADOR DE PASOS

    def al_iniciar(self):
        """Llamado al inicio para reiniciar las posiciones visitadas."""
        self.visitados = set()
        self.pasos = 0 #REINICIAMOS EL CONTADOR DE PASOS

    def decidir(self, percepcion):
        """
        Decide la siguiente acción del agente basándose en su percepción.
        
        Parámetros:
            percepcion – diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        pos_actual = percepcion['posicion']
        self.visitados.add(pos_actual)  #GUARDAMOS LA POSICIÓN ACTUAL COMO VISITADA

        # 1. SI LA META ESTÁ ADYACENTE, VAMOS HACIA ALLÁ
        for direccion in self.ACCIONES:
            if percepcion[direccion] == 'meta':
                self.pasos += 1  #INCREMENTAMOS EL CONTADOR DE PASOS
                return direccion
        
        # 2. DIRECCIONES IDEALES: AQUELLAS QUE NOS ACERCAN A LA META
        vert, horiz = percepcion['direccion_meta']
        direcciones_ideales = [vert, horiz]

        # 3. CLASIFICAMOS LAS DIRECCIONES DISPONIBLES
        no_visitadas_ideales = []  # DIRECCIONES IDEALES NO VISITADAS
        no_visitadas = []  # DIRECCIONES NO VISITADAS (NO IDEALES)
        visitadas = []  # DIRECCIONES YA VISITADAS

        # EVALUAMOS CADA DIRECCIÓN PARA CLASIFICARLA
        for direccion in self.ACCIONES:
            if percepcion[direccion] == 'libre':  # SOLO CONSIDERAMOS DIRECCIONES LIBRES
                # CALCULAMOS LA POSICIÓN FUTURA SI NOS MOVEMOS EN ESA DIRECCIÓN
                desplazamiento_fila, desplazamiento_columna = self.DELTAS[direccion]
                pos_futura = (pos_actual[0] + desplazamiento_fila, pos_actual[1] + desplazamiento_columna)

                # SI LA POSICIÓN FUTURA NO HA SIDO VISITADA, LA CLASIFICAMOS
                if pos_futura not in self.visitados:
                    if direccion in direcciones_ideales:
                        no_visitadas_ideales.append(direccion)
                    else:
                        no_visitadas.append(direccion)
                else:
                    visitadas.append(direccion)

        # 4. DECISION: PRIMERO INTENTAMOS MOVER EN DIRECCION HACIA LA META, SI ES POSIBLE
        if no_visitadas_ideales:
            self.pasos += 1  #INCREMENTAMOS EL CONTADOR DE PASOS
            return random.choice(no_visitadas_ideales)  # Escoge una dirección ideal no visitada al azar

        # 5. SI NO TENEMOS DIRECCIONES, EXPLORA NUEVOS CAMINOS
        if no_visitadas:
            self.pasos += 1  #INCREMENTAMOS EL CONTADOR DE PASOS
            return random.choice(no_visitadas)  # ESCOGE UNA DIRECCIÓN NO IDEAL NO VISITADA AL AZAR

        # 6. SI ESTAMOS ATRAPADOS, RETROCEDEMOS A UNA DIRECCIÓN YA VISITADA PARA INTENTAR OTRA RUTA
        if visitadas:
            self.pasos += 1  #INCREMENTAMOS EL CONTADOR DE PASOS
            return random.choice(visitadas)  # RETROCEDE A UNA DIRECCIÓN YA VISITADA AL AZAR

        # 7. SI FALLA ALGO, MOVEMOS HACIA ABAJO
        self.pasos += 1  #INCREMENTAMOS EL CONTADOR DE PASOS
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