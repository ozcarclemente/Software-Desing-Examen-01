
# 1er Examen Parcial | Diseño de Software
### Oscar Clemente López Labrador - 720371

<br>

## Correr Programa

```bash
python3 biblioteca_refactorizada.py
```

### Output esperado

```
=== AGREGANDO LIBROS ===
Libro 'Cien Años de Soledad' agregado exitosamente
Libro 'El Principito' agregado exitosamente
Libro '1984' agregado exitosamente

=== BÚSQUEDA POR AUTOR ===
- Cien Años de Soledad por Gabriel García Márquez

=== REALIZAR PRÉSTAMO ===
[NOTIFICACIÓN] Juan Pérez: Préstamo de 'Cien Años de Soledad'
Préstamo realizado a Juan Pérez

=== LIBROS DISPONIBLES ===
- El Principito
- 1984

=== DEVOLVER LIBRO ===
Libro devuelto exitosamente

=== PRÉSTAMOS ACTIVOS ===
Total de préstamos activos: 0
```

<br>

## Ejercicio 1

Para la **búsqueda de libros** se aplicó el Open/Closed Principle **(OCP)** mediante la definición de una interfaz `BusquedaLibro`, la cual es implementada por distintas clases según el criterio de búsqueda (título, autor, ISBN o disponibilidad).

Esto hace que el sistema sea flexible y extensible. Agregar un nuevo criterio solo requiere implementar una nueva clase sin modificar el código existente.

Además, se diseñó una **Factory (`FactoryBusquedaLibro`)** que encapsula la lógica de instanciación y devuelve la estrategia de búsqueda adecuada según el criterio solicitado. De esta forma, el método `buscar_libro` mantiene la misma firma que antes, pero delega el proceso de búsqueda a la clase correspondiente y regresa una lista de resultados, tal como lo hacía originalmente.

```python
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
```

```python
# Función refactorizada

def buscar_libro(self, criterio, valor):
    claseBusqueda = FactoryBusquedaLibro.crear(criterio)
    resultados = claseBusqueda.buscar(self.libros, valor)
    return resultados
```

<br>

## Ejercicio 2

### Validadores

para los validadores se tuvo que levantar una ValueError para que el programa no permita continuar con el flujo porque no se cumple las condiciones estipuladas. A diferencia del original que retornaba un string con el error aquí paramos con el flujo y le decimos al cliente que uno de sus libros tiene un criterio mal

```python
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
```

```bash
# Ejemplo de consola con criterio no correcto

python3 biblioteca_refactorizada.py

=== AGREGANDO LIBROS ===
Traceback (most recent call last):
  File "/Users/oz/Library/CloudStorage/OneDrive-ITESO/5° Semestre/Diseño de Software/code/Software-Desing-Examen-01/biblioteca_refactorizada.py", line 275, in <module>
    main()
    ~~~~^^
  File "/Users/oz/Library/CloudStorage/OneDrive-ITESO/5° Semestre/Diseño de Software/code/Software-Desing-Examen-01/biblioteca_refactorizada.py", line 248, in main
    print(sistema.agregar_libro("", "George Orwell", "9780451524935"))
          ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/oz/Library/CloudStorage/OneDrive-ITESO/5° Semestre/Diseño de Software/code/Software-Desing-Examen-01/biblioteca_refactorizada.py", line 150, in agregar_libro
    self.validador.validarTitulo(titulo)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/Users/oz/Library/CloudStorage/OneDrive-ITESO/5° Semestre/Diseño de Software/code/Software-Desing-Examen-01/biblioteca_refactorizada.py", line 92, in validarTitulo
    raise ValueError("Error: Título inválido")
ValueError: Error: Título inválido
```

### RespositorioArchivo

La clase `RepositorioArchivo` (antes `RepositorioBiblioteca`) implementa la interfaz `IRepositorio`. Para instanciarla basta con pasar el nombre del archivo donde se almacenarán y cargarán los datos. De esta manera, se libera a `SistemaBiblioteca` de esa responsabilidad, cumpliendo así con el **Principio de Responsabilidad Única (SRP)**.

```python
class RepositorioArchivo(IRepositorio):
    def __init__(self, archivo):
				# Nombre del archivo donde se guardará/cargará la información
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
```

```python
# Declaración

def main():
    repositorio = RepositorioArchivo("biblioteca.txt")
```

<br>

## Ejercicio 3

Dado que ahora nuestra biblioteca cumple con el **Principio de Inversión de Dependencias (DIP)**, antes de inicializar el sistema debemos declarar las clases de **validador**, **repositorio** y **notificador**. De esta forma, dichas dependencias se pasan al constructor e inyectan directamente en la clase `SistemaBiblioteca`, manteniendo la coherencia con el principio DIP.

```python
class SistemaBiblioteca:
    def __init__(self, repositorio, validador, notificador):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        
        # Inyección de dependencias (DIP)
        # El sistema no crea los objetos, los recibe listos para usar.
        self.repositorio: IRepositorio = repositorio
        self.validador: ValidadorBiblioteca = validador
        self.notificador: ServicioNotificaciones = notificador

```

```python
# Declaración

def main():

    validador = ValidadorBiblioteca()
    repositorio = RepositorioArchivo("biblioteca.txt")
    notificador = ServicioNotificaciones()

    sistema = SistemaBiblioteca(repositorio, validador, notificador)
```