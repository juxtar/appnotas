import logica
import interfaz as gui

if __name__=='__main__':
	gestor = logica.GestorNotas()
	gestor.recuperar_notas()
	gui.main()