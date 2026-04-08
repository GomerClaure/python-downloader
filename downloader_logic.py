import os
import re
import yt_dlp
import instaloader
import shutil
import sys
import requests
from urllib.parse import urlparse, unquote

class UniversalDownloader:
    # ... (el __init__ y los callbacks se mantienen igual) ...
    def __init__(self, status_callback=None, progress_callback=None):
        self.status_callback = status_callback
        self.progress_callback = progress_callback

    def _update_status(self, message, color="black"):
        if self.status_callback:
            self.status_callback(message, color)

    def _update_progress(self, percentage):
        if self.progress_callback:
            self.progress_callback(percentage)
            
    def detect_platform(self, url):
        # ... (sin cambios) ...
        url = url.lower()
        if 'youtube.com' in url or 'youtu.be' in url: return 'youtube'
        if 'instagram.com' in url: return 'instagram'
        if 'facebook.com' in url or 'fb.watch' in url: return 'facebook'
        if 'twitter.com' in url or 'x.com' in url: return 'twitter'
        if 'tiktok.com' in url: return 'tiktok'
        if 'reddit.com' in url: return 'reddit'
        return 'generic'

    def _yt_dlp_progress_hook(self, d):
        # ... (sin cambios) ...
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                downloaded_bytes = d.get('downloaded_bytes', 0)
                percentage = (downloaded_bytes / total_bytes) * 100
                self._update_progress(percentage)
                # Extraemos el nombre del archivo para mostrar un estado más claro
                filename = d.get('filename', '')
                if 'merger' in filename:
                    self._update_status("Fusionando archivos con FFmpeg...", "purple")
                else:
                    self._update_status(f"Descargando... {percentage:.1f}%", "orange")
        elif d['status'] == 'finished':
            # Evitamos el mensaje "procesando" si ya hemos terminado
            if "_merger" not in d.get('info_dict', {}).get('_filename', ''):
                 self._update_status("Descarga finalizada, procesando...", "purple")
        elif d['status'] == 'error':
            self._update_status("Error durante la descarga.", "red")
    
    # --- MÉTODO PRINCIPAL MODIFICADO ---
    def download_content(self, url, path, download_playlist=False, recode_video=False, download_type='video'):
        """
        Función principal de descarga.
        :param recode_video: Booleano para forzar la recodificación a H.264.
        """
        platform = self.detect_platform(url)
        
        # ... (lógica de nombre de carpeta sin cambios) ...
        folder_prefix = f"{platform}_playlist" if download_playlist and platform == 'youtube' else f"{platform}_content"
        sanitized_url = re.sub(r'https?://(www\.)?', '', url).split('/')[0].replace('.', '_')
        folder_name = f"{folder_prefix}_{sanitized_url}"
        download_folder = os.path.join(path, folder_name)
        os.makedirs(download_folder, exist_ok=True)
        
        self._update_status(f"Detectada plataforma: {platform.capitalize()}", "blue")

        try:
            if platform == 'instagram':
                return self.download_instagram_content(url, download_folder)
            
            # Pasamos las nuevas opciones a la función de yt-dlp
            if self.is_direct_media_url(url):
                return self.download_direct_file(url, download_folder)
            
            return self.download_with_yt_dlp(
                url,
                download_folder,
                platform,
                download_playlist,
                recode_video,
                download_type
            )
                
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self._update_status(error_msg, "red")
            return {'status': 'error', 'message': error_msg}

    def download_with_yt_dlp(self, url, path, platform, download_playlist=False, recode_video=False, download_type="video"):
        try:
            out_template = '%(playlist_index)s - %(title)s.%(ext)s' if download_playlist else '%(title)s.%(ext)s'

            ydl_opts = {
                'outtmpl': os.path.join(path, out_template),
                'progress_hooks': [self._yt_dlp_progress_hook],
                'ignoreerrors': True,
                'noplaylist': not download_playlist,
                'ffmpeg_location': self.find_ffmpeg(),
            }

            if download_type == "audio":
                self._update_status("Modo solo audio activado.", "purple")
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                })
            else:
                # Descarga de video normal
                if recode_video:
                    ydl_opts['format'] = 'bestvideo+bestaudio'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }]
                else:
                    ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                    ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self._update_status("Iniciando descarga con yt-dlp...", "orange")
                ydl.download([url])

            success_msg = f"¡Contenido de {platform.capitalize()} descargado exitosamente!"
            self._update_status(success_msg, "green")
            return {'status': 'success', 'message': success_msg, 'path': path}

        except Exception as e:
            error_msg = f"Error de yt-dlp: {str(e)}"
            self._update_status(error_msg, "red")
            return {'status': 'error', 'message': error_msg}


    def find_ffmpeg(self):
        """Busca ffmpeg en la misma carpeta o en el PATH."""
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # Para compatibilidad cruzada
        ffmpeg_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
        ffmpeg_path = os.path.join(base_path, ffmpeg_name)
        
        if os.path.exists(ffmpeg_path):
            self._update_status("FFmpeg encontrado localmente.", "blue")
            return ffmpeg_path

        self._update_status("FFmpeg no encontrado localmente. Se buscará en el PATH del sistema.", "grey")
        return None


    def download_instagram_content(self, url, path):
        # ... (sin cambios) ...
        self._update_status("Instagram detectado. Iniciando Instaloader...", "purple")
        self._update_status("Nota: Instagram puede requerir inicio de sesión.", "grey")
        try:
            loader = instaloader.Instaloader(
                dirname_pattern=path,
                download_video_thumbnails=False,
                save_metadata=False,
                compress_json=False
            )
            match = re.search(r'/(p|reel|tv)/([^/]+)', url)
            if match:
                shortcode = match.group(2)
                post = instaloader.Post.from_shortcode(loader.context, shortcode)
                loader.download_post(post, target="")
                success_msg = "Contenido de Instagram descargado."
                self._update_status(success_msg, "green")
                return {'status': 'success', 'message': success_msg}
            else:
                error_msg = "URL de Instagram no soportada (solo posts/reels)."
                self._update_status(error_msg, "red")
                return {'status': 'error', 'message': error_msg}
        except Exception as e:
            error_msg = f"Error de Instaloader: {str(e)}"
            self._update_status(error_msg, "red")
            return {'status': 'error', 'message': error_msg}
    
    def is_direct_media_url(self, url):
        url_lower = url.lower()
        media_exts = (
            '.mp4', '.mp3', '.m4a', '.webm', '.mkv',
            '.mov', '.avi', '.wav', '.flac', '.aac', '.ogg'
        )

        # Caso normal: URL termina en extensión multimedia
        if any(url_lower.split('?')[0].endswith(ext) for ext in media_exts):
            return True

        # Caso Wayback Machine apuntando a archivo multimedia
        if 'web.archive.org/web/' in url_lower and any(ext in url_lower for ext in media_exts):
            return True

        return False


    def _safe_filename_from_url(self, url, default_name="archivo"):
        parsed = urlparse(url)
        raw_name = os.path.basename(parsed.path)
        raw_name = unquote(raw_name).split('?')[0].strip()

        if not raw_name:
            raw_name = default_name

        # Sanitizar para evitar caracteres problemáticos
        raw_name = re.sub(r'[<>:"/\\|?*\n\r\t]', '_', raw_name)
        return raw_name


    def download_direct_file(self, url, path):
        try:
            self._update_status("Detectado archivo directo. Descargando con requests...", "orange")

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            with requests.get(url, stream=True, headers=headers, timeout=30) as r:
                r.raise_for_status()

                filename = self._safe_filename_from_url(url, "video.mp4")

                # Si Wayback deja un nombre raro o sin extensión, forzar una extensión razonable
                if '.' not in filename:
                    content_type = r.headers.get("Content-Type", "").lower()
                    if "mp4" in content_type:
                        filename += ".mp4"
                    elif "mpeg" in content_type or "mp3" in content_type:
                        filename += ".mp3"
                    else:
                        filename += ".bin"

                full_path = os.path.join(path, filename)

                total_size = int(r.headers.get("content-length", 0))
                downloaded = 0

                with open(full_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 256):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percentage = (downloaded / total_size) * 100
                            self._update_progress(percentage)
                            self._update_status(f"Descargando archivo directo... {percentage:.1f}%", "orange")

            self._update_progress(100)
            success_msg = f"Archivo descargado exitosamente: {filename}"
            self._update_status(success_msg, "green")
            return {"status": "success", "message": success_msg, "path": full_path}

        except Exception as e:
            error_msg = f"Error en descarga directa: {str(e)}"
            self._update_status(error_msg, "red")
            return {"status": "error", "message": error_msg}