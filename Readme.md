# Estado del Proyecto

Actualmente, el proyecto se encuentra en una etapa inicial y el archivo `Readme.md` está vacío. No hay código ni documentación implementada aún.

# Arquitectura

La arquitectura propuesta para el proyecto es la siguiente:

- **Interfaz de usuario**: Aplicación de línea de comandos (CLI) para descargar videos de YouTube.
- **Módulo principal**: Gestiona la lógica de descarga y procesamiento de videos.
- **Gestor de dependencias**: Uso de `requirements.txt` para administrar las librerías necesarias.

# Dependencias

Las dependencias principales sugeridas para este tipo de proyecto son:

- [`pytube`](https://pytube.io/): Para descargar videos de YouTube.
- [`argparse`](https://docs.python.org/3/library/argparse.html): Para gestionar argumentos de la línea de comandos.
- [`requests`](https://docs.python-requests.org/en/latest/): Para realizar peticiones HTTP si es necesario.

Puedes instalar las dependencias ejecutando:

```bash
pip install pytube requests
```

Se recomienda crear un entorno virtual para aislar las dependencias del proyecto.
