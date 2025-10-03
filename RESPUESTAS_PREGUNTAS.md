## 📝 PREGUNTAS TEÓRICAS (10 puntos)

### Pregunta 1: LSP (5 pts)

**a) (5 pts)** Explica qué es LSP y cómo se aplica al ejemplo:

```python
class Usuario:
    def calcular_limite_prestamos(self):
        return 3

class Estudiante(Usuario):
    def calcular_limite_prestamos(self):
        return 3
```

**Respuesta:**
```
LSP (Principio de Sustitución de Liskov) dice que un subtipo debe poder
sustituir a su supertipo sin romper el programa. 

En el ejemplo, Estudiante hereda de Usuario y mantiene el mismo contrato: mismo método y devuelven un entero válido.
```

**b) (5 pts)** Da un ejemplo que VIOLE LSP y explica por qué:

```python
# Tu código aquí
class Usuario:
    def calcular_limite_prestamos(self):
        return 3

class Invitado(Usuario):
    def calcular_limite_prestamos(self):
        # Cambia el contrato: ahora lanza excepción en lugar de devolver un int
        raise RuntimeError("Los invitados no pueden consultar el límite")
```

# Explicación:

Viola LSP porque el código que espera un int (como con Usuario) recibe
una excepción. El subtipo no respeta el contrato del supertipo: cambia
el efecto observable y rompe a los clientes que dependen del retorno.


---

### Pregunta 2: ISP (5 pts)

**a) (5 pts)** ¿Por qué esta interfaz VIOLA ISP?

```python
class IGestionBiblioteca:
    def agregar_libro(self): pass
    def buscar_libro(self): pass
    def realizar_prestamo(self): pass
    def generar_reporte(self): pass
    def hacer_backup(self): pass
```

**Respuesta:**
```
ISP (Interface Segregation Principle) dice que los clientes no
deben depender de métodos que no usan. Esta interfaz mezcla
responsabilidades (catálogo, préstamos, reportes y backups), obligando
a implementaciones a definir métodos irrelevantes para su rol.

```

**b) (5 pts)** Propón cómo segregar esta interfaz:

```
Interface 1: ICatalogo         - Métodos: agregar_libro, buscar_libro

Interface 2: IPrestamos        - Métodos: realizar_prestamo

Interface 3: IAdministracion   - Métodos: generar_reporte, hacer_backup
```

---