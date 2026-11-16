# Pruebas funcionales de SauceDemo con Selenium WebDriver

Seis casos automatizados con Python, Selenium WebDriver, pytest y Page Object Model.

## Ejecucion en Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v --html=reports/reporte.html --self-contained-html
```
