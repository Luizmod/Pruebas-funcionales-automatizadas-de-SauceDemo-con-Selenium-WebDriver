# Pruebas funcionales de SauceDemo con Selenium WebDriver

Automatización de seis casos con Python, Selenium WebDriver, pytest y el patrón Page Object Model.

## Casos de prueba

| Caso | Funcionalidad |
|---|---|
| CP-01 | Inicio de sesión con credenciales válidas |
| CP-02 | Rechazo de credenciales inválidas |
| CP-03 | Ordenamiento de productos por precio ascendente |
| CP-04 | Adición de un producto al carrito |
| CP-05 | Eliminación de un producto del carrito |
| CP-06 | Finalización de una compra |

Cada prueba utiliza un navegador independiente, esperas explícitas y aserciones que comparan los valores esperados con los obtenidos.

## Instalación y ejecución

Se requiere Python 3.12, Google Chrome y conexión a Internet para instalar dependencias, obtener el controlador mediante Selenium Manager y acceder a SauceDemo.

En Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
$env:HEADLESS='1'
.\.venv\Scripts\python.exe -m pytest -v --html=reports/reporte.html --self-contained-html
```

Para observar el navegador, establece `$env:HEADLESS='0'` antes de ejecutar pytest.

Cada ejecución genera una carpeta fechada dentro de `reports/` con datos del entorno, resultados y capturas. El HTML se guarda en `reports/reporte.html`. Estos archivos se conservan localmente y se entregan por Moodle; están excluidos de Git.

La fixture utiliza un perfil temporal por prueba y desactiva el gestor y la detección de filtraciones de contraseñas de Chrome para evitar interferencias con las credenciales públicas de demostración.

## Estructura

- `config.py`: configuración de acceso y esperas.
- `pages/`: objetos de página de acceso, inventario, carrito y checkout.
- `tests/`: casos CP-01 a CP-06 y fixtures de navegador y evidencias.
- `scripts/diagnose_checkout.py`: diagnóstico de interacciones del checkout.
- `requirements.txt`: dependencias principales.
- `requirements-lock.txt`: versiones exactas de las dependencias.
- `pytest.ini`: configuración de pytest.

## Control de versiones

El repositorio contiene el código y las instrucciones para reproducir las pruebas. El entorno virtual, las cachés, las variables locales, los documentos de entrega y las evidencias quedan excluidos mediante `.gitignore`.

```powershell
git log --oneline
git status --short
```
