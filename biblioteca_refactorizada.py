"""
EXAMEN PRINCIPIOS SOLID - 2 HORAS
Sistema de Mini-Biblioteca

INSTRUCCIONES:
1. NO modifiques este archivo
2. Crea archivos nuevos para tus refactorizaciones
3. Asegúrate que el código siga funcionando

CÓDIGO BASE CON VIOLACIONES DELIBERADAS DE SOLID
"""

# =============================================
# AUTOR: OSCAR CLEMENTE LOPEZ LABRADOR - 720371
# =============================================

from abc import ABC, abstractmethod

class Libro:
    def __init__(self, id, titulo, autor, isbn, disponible=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible

class Prestamo:
    def __init__(self, id, libro_id, usuario, fecha):
        self.id = id
        self.libro_id = libro_id
        self.usuario = usuario
        self.fecha = fecha
        self.devuelto = False


# ======================================================
# 🟢 EJERCICIO 1: Open/Closed Principle (30 pts - 25 min)
# ======================================================

# Intefaz Busqueda de Libro para Open/Closed Principle
class BusquedaLibro(ABC):
    @abstractmethod
    def buscar(self, libros, valor):
        pass

class BusquedaPorTitulo(BusquedaLibro):
    def buscar(self, libros, valor):
        return [libro for libro in libros if libro.titulo == valor]


class BusquedaPorAutor(BusquedaLibro):
    def buscar(self, libros, valor):
        return [libro for libro in libros if libro.autor == valor]


class BusquedaPorISBN(BusquedaLibro):
    def buscar(self, libros, valor):
        return [libro for libro in libros if libro.isbn == valor]


class BusquedaPorDisponibilidad(BusquedaLibro):
    def buscar(self, libros, valor):
        if isinstance(valor, str):
            disponible = valor.lower() == "true"
        else:
            disponible = bool(valor)
        return [libro for libro in libros if libro.disponible == disponible]

# Factory para crear la instancia correspondiente según el criterio     
class FactoryBusquedaLibro:
    _map = {
        "titulo": BusquedaPorTitulo,
        "autor": BusquedaPorAutor,
        "isbn": BusquedaPorISBN,
        "disponible": BusquedaPorDisponibilidad,
    }

    @staticmethod
    def crear(criterio: str):
        clase = FactoryBusquedaLibro._map.get(criterio)
        if not clase:
            raise ValueError(f"Estrategia de búsqueda '{criterio}' no soportada")
        return clase() 


# ================================================================
# 🟡 EJERCICIO 2: Single Responsibility Principle (30 pts - 40 min)
# ================================================================

# Validadores de la Biblioteca
class ValidadorBiblioteca:
    def validarTitulo(self, titulo):
        if not titulo or len(titulo) < 2:
            raise ValueError("Error: Título inválido")
    
    def validarAutor(self, autor):
        if not autor or len(autor) < 3:
            raise ValueError("Error: Autor inválido")
        
    def validarISBN(self, isbn):
        if not isbn or len(isbn) < 10:
            raise ValueError("Error: ISBN inválido")
    
    def validarUsuario(self, usuario):
        if not usuario or len(usuario) < 3:
            raise ValueError("Error: Nombre de usuario inválido")

# Servicio de Notificaciones de Biblioteca
class ServicioNotificaciones:
    def enviar(self, usuario, libro):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro}'")

# Interface de Repositorio de Biblioteca
class IRepositorio(ABC):
    @abstractmethod
    def guardar(self, libros, prestamos):
        pass

    @abstractmethod
    def cargar(self):
        pass

# Clase que implementea la interface de IRepositorio
# Esta clase se enfoca en Repositorio de Archivo
class RepositorioArchivo(IRepositorio):
    def __init__(self, archivo):
        self._archivo = archivo

    def guardar(self, libros, prestamos):
       with open(self._archivo, 'w') as f:
            f.write(f"Libros: {len(libros)}\n")
            f.write(f"Préstamos: {len(prestamos)}\n")

    def cargar(self):
        try:
            with open(self._archivo, 'r') as f:
                data = f.read()
            return True
        except:
            return False
        
        
# Clase que gestiona la biblioteca
class SistemaBiblioteca:
    def __init__(self, repositorio, validador, notificador):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.repositorio:IRepositorio = repositorio
        self.validador:ValidadorBiblioteca = validador
        self.notificador:ServicioNotificaciones = notificador
    
    def agregar_libro(self, titulo, autor, isbn):
        self.validador.validarTitulo(titulo)
        self.validador.validarAutor(autor)
        self.validador.validarISBN(isbn)
        
        # Lógica de negocio
        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1
        
        self.repositorio.guardar(self.libros, self.prestamos)
        
        return f"Libro '{titulo}' agregado exitosamente"
    
    # Método refactorizado (OCP)
    def buscar_libro(self, criterio, valor):
        claseBusqueda = FactoryBusquedaLibro.crear(criterio)
        resultados = claseBusqueda.buscar(self.libros, valor)
        return resultados
    
    def realizar_prestamo(self, libro_id, usuario):
        self.validador.validarUsuario(usuario)

        # Buscar libro
        libro = None
        for l in self.libros:
            if l.id == libro_id:
                libro = l
                break
        
        if not libro:
            return "Error: Libro no encontrado"
        
        if not libro.disponible:
            return "Error: Libro no disponible"
        
        # Lógica de negocio
        from datetime import datetime
        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d")
        )
        
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False
        
        # Persistencia
        self.repositorio.guardar(self.libros, self.prestamos)
        
        # Notificación
        self.notificador.enviar(usuario, libro.titulo)
        
        return f"Préstamo realizado a {usuario}"
    
    def devolver_libro(self, prestamo_id):
        prestamo = None
        for p in self.prestamos:
            if p.id == prestamo_id:
                prestamo = p
                break
        
        if not prestamo:
            return "Error: Préstamo no encontrado"
        
        if prestamo.devuelto:
            return "Error: Libro ya devuelto"
        
        for libro in self.libros:
            if libro.id == prestamo.libro_id:
                libro.disponible = True
                break
        
        prestamo.devuelto = True
        self.repositorio.guardar(self.libros, self.prestamos)
        
        return "Libro devuelto exitosamente"
    
    def obtener_todos_libros(self):
        return self.libros
    
    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros if libro.disponible]
    
    def obtener_prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]
    
   

def main():

    # Instanciar dependencias antes de Sistema de la Biblioteca
    validador = ValidadorBiblioteca()
    repositorio = RepositorioArchivo("biblioteca.txt")
    notificador = ServicioNotificaciones()

    # Se pasan las instancias de clase en el constructor del Sistema Biblioteca
    sistema = SistemaBiblioteca(repositorio, validador, notificador)
    
    print("=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))
    
    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Gabriel García Márquez")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
    print("\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Pérez"))
    
    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")
    
    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))
    
    print("\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")


if __name__ == "__main__":
    main()
