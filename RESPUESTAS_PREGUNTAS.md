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
class Auto:
    def recargar_combustible(self):
        print("El auto recarga gasolina en la estación de servicio")


class AutoElectrico(Auto):
    def recargar_combustible(self):
        raise NotImplementedError("Un auto eléctrico no usa gasolina")
```

**Explicación:**
```
Viola LSP porque el código que espera un Auto (que siempre puede recargar combustible) recibe una excepción al pasarle un AutoElectrico. 

El subtipo no respeta el contrato del supertipo: cambia el efecto observable y rompe a los clientes que dependen de recargar_combustible().
```

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
ISP (Interface Segregation Principle) dice que los clientes no deben depender de métodos que no usan. Esta interfaz mezcla responsabilidades (catálogo, préstamos, reportes y backups), obligando a implementaciones a definir métodos irrelevantes para su rol.

```

**b) (5 pts)** Propón cómo segregar esta interfaz:

```
Interface 1: ICatalogo         - Métodos: agregar_libro, buscar_libro

Interface 2: IPrestamos        - Métodos: realizar_prestamo

Interface 3: IAdministracion   - Métodos: generar_reporte, hacer_backup
```

---
