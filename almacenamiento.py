from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

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
		self.engine = create_engine('sqlite:///data/appnotas.db', echo=True)
		Base.metadata.create_all(self.engine)
		self.Session = sessionmaker(bind=self.engine)

	def insertar_nota(self, nota):
		session = self.Session()
		session.add(nota)
		session.commit()

	def recuperar_notas(self):
		session = self.Session()
		notas_a_recuperar = session.query(Nota).all()
		session.close()
		return notas_a_recuperar

	def remover_nota(self, nota):
		session = self.Session()
		session.delete(nota)
		session.commit()
		session.close()

	def buscar_nota(self, id_nota):
		session = self.Session()
		nota = session.query(Nota).filter(Nota.id == id_nota).one()
		session.close()
		return nota