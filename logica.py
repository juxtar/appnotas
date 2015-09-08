import almacenamiento as db
import interfaz as gui
from datetime import datetime
from threading import Lock, Thread
from base64 import b64encode, b64decode

# Para asegurar la exclusividad al acceso a la base de datos, se crea un lock
# De manera que solo un hilo puede utilizar la base de datos
lock_bd = Lock()

class GestorNotas:
	"""Aplicacion para gestionar notas"""
	def __init__(self):
		self.main_window = gui.MainWindow(self)
		self.gestordb = db.GestorBD(self)

	def recuperar_notas(self):
		hilo = Thread(target=self._recuperar_notas)
		hilo.start()

	def _recuperar_notas(self):
		"""Obtiene notas del gestor de base de datos y las muestra en pantalla"""
		lock_bd.acquire()
		notas_recuperadas = self.gestordb.recuperar_notas()
		lock_bd.release()
		for nota in notas_recuperadas:
			with gui.lock:
				self.main_window.agregar_nota(gui.InterfazNota(nota, fecha=self.fecha_a_string(nota.fecha), contenido=b64decode(nota.contenido)))

	def fecha_a_string(self, fecha):
		meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
				 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
		_, mes, dia = fecha.split('-')
		return '{:} de {:}'.format(int(dia), meses[int(mes)])

	def nueva_nota(self, texto, color):
		hilo = Thread(target=self._nueva_nota, args=(texto, color))
		hilo.start()

	def _nueva_nota(self, texto, color):
		"""Interfaz de la clase con las clases de Interfaz de usuario
			Crea nuevo thread para ejecutar la orden"""
		hexcolor = {'blanco': '#ffffff', 'amarillo': '#ffd45b', 'azul': '#5bafff', 'rojo': '#ff5b5d'}

		# Tomar fecha y hora actual
		ahora = datetime.now()
		fecha = "{:}-{:}-{:}".format(ahora.year, ahora.month, ahora.day)
		hora = "{:}:{:}".format(ahora.hour, '0'+str(ahora.minute) if ahora.minute<10 else ahora.minute)

		# Nueva instancia de Nota
		nota = db.Nota(fecha=fecha, hora=hora, contenido=b64encode(texto), color=hexcolor[color])
		# Hilo accede a base de datos
		lock_bd.acquire()
		# Agregar a la base de datos
		self.gestordb.insertar_nota(nota)
		# Hilo deja de trabajar con la base de datos
		lock_bd.release()
		# Agregar a la pantalla una InterfazNota con los datos de la nueva nota
		# Se cambia el formato de la fecha para que sea mas legible
		with gui.lock: # Modifica la pantalla y necesita exclusividad
			self.main_window.agregar_nota(gui.InterfazNota(nota, fecha=self.fecha_a_string(fecha), contenido=texto))

	def eliminar_notas(self, lista_notas):
		"""Interfaz de la clase con las clases de Interfaz de usuario
			Crea nuevo thread para ejecutar la orden"""
		hilo = Thread(target=self._eliminar_notas, args=(lista_notas,))
		hilo.start()

	def _eliminar_notas(self, lista_notas):
		"""Elimina las notas pasadas como argumento de la lista de notas
			y llama a remover_nota de la pantalla principal"""
		if len(lista_notas) == 0:
			with gui.lock: # Modifica pantalla
				self.main_window.mostrar_error(0, 'Debe seleccionar una nota a eliminar.')
		for id_nota in lista_notas:
			nota_a_borrar = self._buscar_nota(id_nota)	# Buscar la nota con la id analizada
			if nota_a_borrar != None:
				lock_bd.acquire() # Pide acceso a base de datos
				self.gestordb.remover_nota(nota_a_borrar)	# Remueve de la base de datos
				lock_bd.release() # Libera la base de datos para el uso a otros hilos
				with gui.lock: # Modifica pantalla
					self.main_window.remover_nota(id_nota)
			
	def _buscar_nota(self, id_nota):
		"""Devuelve la nota con la id especificada de la lista de notas, None si no encontrada"""
		try:
			return self.gestordb.buscar_nota(id_nota)
		except db.NoResultFound:
			return None

if __name__ == "__main__":
	gestor = GestorNotas()
	gestor.recuperar_notas()
	gui.main()