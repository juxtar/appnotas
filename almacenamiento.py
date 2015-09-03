

class Nota:
	"""Almacena informacion de una Nota"""
	def __init__(self, id_nota, fecha, hora, contenido, color):
		self.id = id_nota
		self.fecha = fecha
		self.hora = hora
		self.contenido = contenido
		self.color = color

class BaseDeDatos(object):
	"""Clase que interactua con la base de datos para guardar, eliminar y restaurar datos"""
	def __init__(self):
		self.bd = None

	def insertar_nota(self, nota):
		pass

	def remover_nota(self, id_nota):
		pass