# Descargador Universal de Contenido

Aplicacion de escritorio en Python con interfaz grafica (`tkinter`) para descargar contenido desde distintas plataformas usando `yt-dlp`, `Instaloader` y descargas directas con `requests`.

## Funcionalidades

- Descarga de video o solo audio.
- Soporte para enlaces de YouTube, Instagram y otras plataformas compatibles con `yt-dlp`.
- Descarga de archivos multimedia directos (`.mp4`, `.mp3`, etc.).
- Opcion para descargar playlists de YouTube.
- Barra de progreso y mensajes de estado en la interfaz.

## Requisitos

- Python 3.10 o superior recomendado.
- `pip`
- `tkinter`
- `ffmpeg` recomendado y, en varios casos, necesario

## Instalacion

### 1. Clonar el proyecto

```bash
git clone <URL_DEL_REPOSITORIO>
cd python-downloader
```

### 2. Crear y activar un entorno virtual

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

## Sobre `tkinter`

`tkinter` no suele instalarse desde `requirements.txt` porque normalmente viene como parte de Python o depende de paquetes del sistema operativo.

En otras palabras: no es recomendable intentar instalarlo con `pip` como si fuera una libreria normal del proyecto.

### Verificar si ya lo tienes

```bash
python -m tkinter
```

Si se abre una ventana, `tkinter` ya esta disponible.

### Instalar `tkinter` segun tu sistema

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install python3-tk
```

Fedora:

```bash
sudo dnf install python3-tkinter
```

Arch Linux:

```bash
sudo pacman -S tk
```

Windows:

- Normalmente viene incluido al instalar Python desde el instalador oficial.
- Si no esta disponible, reinstala Python asegurandote de incluir `tcl/tk and IDLE`.

macOS:

- En muchos casos ya viene disponible con Python.
- Si no funciona, instala Python desde `python.org` o mediante un gestor como `brew`, verificando luego con `python -m tkinter`.

## Sobre `ffmpeg`

El proyecto intenta encontrar `ffmpeg` automaticamente. Esta herramienta es importante para:

- fusionar audio y video;
- convertir formatos;
- extraer audio a MP3.

Si no esta instalado, algunas descargas pueden fallar o completarse sin conversion.

### Verificar instalacion

```bash
ffmpeg -version
```

### Instalacion rapida

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

Fedora:

```bash
sudo dnf install ffmpeg
```

Arch Linux:

```bash
sudo pacman -S ffmpeg
```

Windows:

- Instala `ffmpeg` y agregalo al `PATH`, o coloca `ffmpeg.exe` junto al ejecutable/script del proyecto.

macOS:

```bash
brew install ffmpeg
```

## Ejecucion

Con el entorno virtual activo:

```bash
python main_gui.py
```

## Uso

1. Abre la aplicacion.
2. Pega la URL del contenido.
3. Elige la carpeta de destino.
4. Selecciona si quieres descargar video o solo audio.
5. Activa la opcion de playlist si corresponde a un enlace de YouTube.
6. Pulsa `Descargar`.

## Dependencias principales

- `yt-dlp`: motor principal de descarga para multiples plataformas.
- `instaloader`: descarga de contenido compatible de Instagram.
- `requests`: descarga de archivos multimedia directos.

## Notas

- Instagram puede requerir inicio de sesion en algunos casos.
- No todo el contenido de todas las plataformas estara disponible debido a restricciones externas.
- `requirements.txt` solo cubre paquetes de Python; dependencias del sistema como `tkinter` o `ffmpeg` deben instalarse aparte cuando aplique.
