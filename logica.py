import almacenamiento
import interfaz
import datetime
import threading

class GestorNotas:
	"""Aplicacion para gestionar notas"""
	def __init__(self):
		self.notas = list()
		self.main_window = interfaz.MainWindow(self)

	def nueva_nota(self, texto, color):
		"""Interfaz de la clase con las clases de Interfaz de usuario
			Crea nuevo thread para ejecutar la orden"""
		hilo = threading.Thread(target=self._nueva_nota, args=(texto, color))
		hilo.start()

	def _nueva_nota(self, texto, color):
		hexcolor = {'blanco': '#ffffff', 'amarillo': '#ffd45b', 'azul': '#5bafff', 'rojo': '#ff5b5d'}
		meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
				 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}

		# Tomar fecha y hora actual
		ahora = datetime.datetime.now()
		fecha = "{:}-{:}-{:}".format(ahora.year, ahora.month, ahora.day)
		hora = "{:}:{:}".format(ahora.hour, '0'+str(ahora.minute) if ahora.minute<10 else ahora.minute)

		# Nueva instancia de Nota
		nota = almacenamiento.Nota(len(self.notas), fecha, hora, texto, hexcolor[color])
		# Hilo accede a lista de notas
		lock_lista_notas.acquire()
		# Agregar a la lista de Notas
		self.notas.append(nota)
		# Hilo deja de trabajar con la lista de notas
		lock_lista_notas.release()
		# Agregar a la pantalla una InterfazNota con los datos de la nueva nota
		# Se cambia el formato de la fecha para que sea mas legible
		with interfaz.lock: # Modifica la pantalla y necesita exclusividad
			self.main_window.agregar_nota(interfaz.InterfazNota(nota, fecha='{:} de {:}'.format(ahora.day,meses[ahora.month])))

	def eliminar_notas(self, lista_notas):
		"""Interfaz de la clase con las clases de Interfaz de usuario
			Crea nuevo thread para ejecutar la orden"""
		hilo = threading.Thread(target=self._eliminar_notas, args=(lista_notas,))
		hilo.start()

	def _eliminar_notas(self, lista_notas):
		"""Elimina las notas pasadas como argumento de la lista de notas
			y llama a remover_nota de la pantalla principal"""
		lock_lista_notas.acquire() # Pide acceso a lista de notas
		if len(self.notas) == 0:
			with interfaz.lock: # Modifica pantalla
				self.main_window.mostrar_error(0, 'No hay notas para eliminar.')
		elif len(lista_notas) == 0:
			with interfaz.lock: # Modifica pantalla
				self.main_window.mostrar_error(0, 'Debe seleccionar una nota a eliminar.')
		lista_id_notas = [nota.id for nota in self.notas]	# Lista con ids de las notas
		for id_nota in lista_notas:
			nota_a_borrar = self.buscar_nota(id_nota)	# Buscar la nota con la id analizada
			if nota_a_borrar != None:
				self.notas.remove(nota_a_borrar)	# Remueve de la lista la nota
				with interfaz.lock: # Modifica pantalla
					self.main_window.remover_nota(id_nota)
		lock_lista_notas.release() # Libera la lista de notas para el uso a otros hilos
			
	def buscar_nota(self, id_nota):
		"""Devuelve la nota con la id especificada de la lista de notas, None si no encontrada"""
		for nota in self.notas:
			if nota.id == id_nota:
				return nota
		else:
			print "GestorNotas.buscar_nota(): No se encontro nota con id: {:}".format(id_nota)
			return None

if __name__ == "__main__":
	# Para asegurar la exclusividad al acceso a la lista de notas, se crea un lock
	# De manera que solo un hilo puede utilizar la lista
	lock_lista_notas = threading.Lock()
	a = GestorNotas()
	interfaz.main()