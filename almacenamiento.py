from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Nota(Base):
	"""Almacena informacion de una Nota"""
	__tablename__ = 'notas'

	id = Column(Integer, primary_key=True)
	contenido = Column(String, nullable=False)
	fecha = Column(String, nullable=False)
	hora = Column(String(5), nullable=False)
	color = Column(String(7), nullable=False)

class GestorBD(object):
	"""Clase que interactua con la base de datos para guardar, eliminar y restaurar datos"""
	def __init__(self, gestor):
		self.gestor = gestor
		self.engine = create_engine('sqlite:///appnotas.db', echo=True)
		Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def insertar_nota(self, nota):
		session.add(nota)
		session.commit()

	def recuperar_notas(self):
		return session.query(Nota).all()

	def remover_nota(self, id_nota):
		pass