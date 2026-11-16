# Instrucciones para Codex — Simulación S10

Actúa como asistente de programación y revisión académica. Este repositorio es para una actividad INDIVIDUAL de Calidad del Software, Universidad Fidélitas.

## Fuente de verdad
Lee primero `docs/CONSIGNA_S10.pdf` y `docs/CASOS_DE_PRUEBA.md`. La consigna pide Selenium WebDriver, al menos seis casos automatizados, control de versiones, informe de resultados reales, conclusiones, recomendaciones, referencias y PDF en APA/IEEE. La rúbrica tiene 8 criterios/16 puntos.

## Reglas
- Mantén Python + Selenium WebDriver + pytest + patrón Page Object Model.
- No sustituyas Selenium por Playwright; puedes proponer mejoras con fundamento.
- Mantén los identificadores CP-01...CP-06 y aserciones concretas para comparar esperado/obtenido.
- Usa esperas explícitas, localizadores estables y fixtures independientes.
- No inventes ejecuciones, capturas, tiempos ni defectos. Si no es posible correr el navegador, indica "No ejecutado".
- Conserva archivos de evidencia en `reports/` y documenta entorno/fecha/versiones cuando se ejecuten.
- Versiona código con Git, pero evita subir `.venv`, credenciales sensibles o reportes temporales.
- Para el informe en APA 7, redacta en español formal y cita fuentes verificables; no inventes referencias.
- Antes de considerar completo el proyecto, revisa uno por uno los 8 criterios de la rúbrica.

## Próximas tareas recomendadas
1. Instalar dependencias y revisar selectores contra el sitio en vivo.
2. Ejecutar `python -m pytest -v --html=reports/reporte.html --self-contained-html`.
3. Corregir fallos reproducibles, reejecutar y guardar evidencia.
4. Registrar resultados reales en la matriz y preparar informe APA 7 PDF.
5. Verificar estado Git y documentar commits y URL de repositorio si se publica.
