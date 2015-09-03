#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import sys

def main():
    gtk.threads_init()
    gtk.main()

lock = gtk.gdk.lock

class MainWindow:
    def __init__(self, gestor):
        self.gestor = gestor
        # Importar de Glade
        self.gladefile = "data.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)    # Conectar seniales definidas en Glade
        self.glade.get_object("principal").show_all()   # Mostrar pantalla principal
        self.ventana_nueva_nota = self.glade.get_object("nueva_nota")
        
        # Que la ventana de nueva nota se cierre si se cierra la principal
        self.ventana_nueva_nota.set_transient_for(self.glade.get_object("principal"))
        # Cambiamos el evento delete para que no se borre la ventana, solo se oculte
        self.ventana_nueva_nota.connect("delete_event", self.delete_nueva_nota)
        self.ventana_nueva_nota.show_all()
        self.ventana_nueva_nota.hide()

        # Glade no pone nombre a los Widgets, este es un workaround
        nombres = ['rojo', 'azul', 'amarillo', 'blanco']
        for i, button in enumerate(self.glade.get_object("blanco").get_group()):
            button.set_name(nombres[i])
        self.glade.get_object("button1").set_name("button1")
        self.glade.get_object("button2").set_name("button2")

        # Cambiar a rojo el color del mensaje de error
        self.glade.get_object("infobar").modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#ff0000"))
        self.glade.get_object("infobar1").modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#ff0000"))

    def agregar_nota(self, nota):
        """Agrega un widget del tipo InterfazNota a la ventana principal"""
        self.glade.get_object("vbox4").pack_start(nota, False, True, 3) # Agrega la nota a la division
        self.glade.get_object("vbox4").reorder_child(nota, 0)   # La ordena para que la nota quede primera
        # Finalmente muestra la InterfazNota y todo su contenido
        nota.show_all()

    def remover_nota(self, id_nota):
        """Remueve el widget de la nota cuya id fue pasada como argumento"""
        padre = self.glade.get_object("vbox4")
        for nota in padre.get_children():   # Recorre los hijos de la division vertical
            if nota._id == id_nota:
                padre.remove(nota)
                return 0
        return 1

    def prueba(self, widget):
        self.mostrar_error(1, 'Apretaste el botón Cancelar', 'Mati se la come')

    def mostrar_error(self, ventana, *mensajes):
        """Muestra los errores definidos en mensajes en la parte superior de la ventana.
            Si ventana es 0 es la Principal, si es 1 es la de Nueva Nota"""
        datos_ventana = {0: ("infobar1", "vbox6"), 1: ("infobar", "vbox5")} # Define los widgets que cambian segun la ventana
        try:
            contenedor = self.glade.get_object(datos_ventana[ventana][1])
        except KeyError:
            print "mostrar_error(): argumento ventana erroneo, debe ser 0 o 1"
            return
        for hijo in contenedor.get_children():
            contenedor.remove(hijo)
        for mensaje in mensajes:
            label = gtk.Label(mensaje)
            contenedor.pack_start(label, True, True, 0)
            label.show()
        self.glade.get_object(datos_ventana[ventana][0]).show()

    def cerrar_error(self, widget):
        """Cierra el mensaje de error en la ventana correspondiente"""
        datos_ventana = {"button1": "infobar", "button2": "infobar1"}
        self.glade.get_object(datos_ventana[widget.get_name()]).hide()

    def destroy_principal(self, widget):
        """Cierra la aplicacion"""
        gtk.main_quit()
        sys.exit(0)

    def delete_nueva_nota(self, widget=None, data=None):
        """Esconde la ventana y vuelve los valores a los por defecto"""
        self.ventana_nueva_nota.hide()
        self.glade.get_object("contenido").set_buffer(gtk.TextBuffer())
        self.glade.get_object("blanco").set_active(True)
        self.glade.get_object("infobar").hide()
        return True

    def nueva_nota(self, widget):
        """Mostrar ventana de Nueva Nota"""
        self.ventana_nueva_nota.show()
        self.ventana_nueva_nota.set_focus(self.glade.get_object("contenido"))

    def guardar_nota(self, widget):
        """Obtiene la informacion de la ventana Nueva Nota y se la manda al gestor.
            Por ultimo cierra la ventana de Nueva Nota"""
        text_buffer = self.glade.get_object("contenido").get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())
        color = None
        for button in self.glade.get_object("blanco").get_group():
            if button.get_active():
                color = button.get_name()   # El color de fondo se obtiene mediante el nombre del boton activo
        self.gestor.nueva_nota(text, color)
        self.delete_nueva_nota()    # Una vez agregada la nota, se cierra la ventana

    def eliminar_notas(self, widget):
        """Obtiene lista con id de notas seleccionadas y se las manda al gestor para que las elimine"""
        notas_a_borrar = [nota._id for nota in self.glade.get_object("vbox4").get_children() if nota.seleccion()]
        self.gestor.eliminar_notas(notas_a_borrar)

class InterfazNota(gtk.EventBox):
    """Widget que muestra información de una Nota
        Los datos de los atributos individuales sobreescribiran al dato contenido
        en el objeto Nota pasado como argumento"""
    def __init__(self, nota=None, fecha=None, hora=None, contenido=None, color=None):
        super(InterfazNota, self).__init__()
        self._nota = nota
        self._id = nota.id
        self._fecha = gtk.Label(fecha if fecha != None else nota.fecha)
        self._hora = gtk.Label(hora if hora != None else nota.hora)
        self._contenido = gtk.Label(contenido if contenido != None else nota.contenido)
        self._contenido.set_line_wrap(True)
        self._seleccion = gtk.CheckButton()

        contentbox = gtk.HBox()

        # VBox que contendra la informacion de la fecha
        timebox = gtk.VBox(spacing=3)
        timebox.pack_start(self._fecha, True, True, 0)
        timebox.pack_start(self._hora, True, True, 0)

        # HBox principal con todos los datos
        contentbox.pack_start(timebox, False, True, 5)
        contentbox.pack_start(self._contenido, True, True, 0)
        contentbox.pack_start(self._seleccion, False, True, 0)

        # Agregar la HBox a la InterfazNota y cambiar el color de fondo
        self.add(contentbox)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(color if color != None else nota.color))

    def set_fecha(self, val):
        self._fecha.set_text(val)

    def set_hora(self, val):
        self._hora.set_text(val)

    def set_contenido(self, val):
        self._contenido.set_text(val)

    def seleccion(self):
        return self._seleccion.get_active()

    def fecha(self):
        return self._fecha.get_text()

    def hora(self):
        return self._hora.get_text()

    def contenido(self):
        return self._contenido.get_text()

    def nota(self):
        return self._nota

if __name__ == "__main__":
    a = MainWindow(None)
    gtk.main()