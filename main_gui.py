import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from downloader_logic import UniversalDownloader
import sys # Importante para la función find_ffmpeg

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador Universal de Contenido")
        self.root.geometry("700x550") # Un poco más de altura para la nueva opción
        self.root.resizable(False, False)

        self.downloader = UniversalDownloader(
            status_callback=self.update_status_label,
            progress_callback=self.update_progress_bar
        )
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=15, pady=15)
        frame.pack(expand=True, fill=tk.BOTH)

        # --- URL Input ---
        tk.Label(frame, text="URL del Contenido:", font=("Arial", 12)).pack(anchor="w")
        self.url_entry = tk.Entry(frame, width=80, font=("Arial", 11))
        self.url_entry.pack(fill="x", pady=5)
        self.url_entry.focus()

        # --- Destination Path ---
        tk.Label(frame, text="Guardar en:", font=("Arial", 12)).pack(anchor="w", pady=(10, 0))
        path_frame = tk.Frame(frame)
        path_frame.pack(fill="x", pady=5)
        
        self.path_entry = tk.Entry(path_frame, font=("Arial", 11))
        self.path_entry.pack(side="left", fill="x", expand=True)
        default_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.path_entry.insert(0, default_path)

        tk.Button(path_frame, text="Seleccionar...", command=self.select_folder).pack(side="right", padx=(5,0))

        # --- Checkbox para playlist ---
        self.playlist_var = tk.BooleanVar()
        playlist_check = tk.Checkbutton(
            frame, 
            text="Descargar playlist completa (si aplica para YouTube)",
            variable=self.playlist_var, 
            font=("Arial", 10)
        )
        playlist_check.pack(anchor="w", pady=10)

        # --- Selección de tipo de descarga ---
        self.download_type = tk.StringVar(value="video")  # Valor por defecto
        type_frame = tk.LabelFrame(frame, text="Tipo de descarga", font=("Arial", 11, "bold"))
        type_frame.pack(fill="x", pady=10)

        video_radio = tk.Radiobutton(
            type_frame, 
            text="Video (audio + video)", 
            variable=self.download_type, 
            value="video", 
            font=("Arial", 10)
        )
        audio_radio = tk.Radiobutton(
            type_frame, 
            text="Solo audio (MP3)", 
            variable=self.download_type, 
            value="audio", 
            font=("Arial", 10)
        )

        video_radio.pack(anchor="w", padx=10, pady=2)
        audio_radio.pack(anchor="w", padx=10, pady=2)

        # --- Botón Descargar ---
        self.download_button = tk.Button(
            frame, 
            text="Descargar", 
            command=self.start_download_thread,
            font=("Arial", 14, "bold"), 
            bg="#28a745", 
            fg="white",
            relief=tk.FLAT, 
            padx=10, 
            pady=5
        )
        self.download_button.pack(pady=10, fill="x", ipady=5)

        # --- Progress Bar y Status Label ---
        self.progress_bar = ttk.Progressbar(frame, orient="horizontal", length=100, mode="determinate")
        self.progress_bar.pack(fill="x", pady=10)
        self.status_label = tk.Label(frame, text="Introduce una URL para comenzar", fg="grey", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # --- Botón Salir ---
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        exit_button = tk.Button(frame, text="Salir", command=self.on_exit, font=("Arial", 12))
        exit_button.pack(pady=5)

    def select_folder(self):
        # ... (sin cambios) ...
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def start_download_thread(self):
        """Inicia la descarga, ahora pasando el valor del checkbox."""
        url = self.url_entry.get().strip()
        path = self.path_entry.get().strip()
        # Obtenemos el valor del checkbox (True o False)
        download_playlist = self.playlist_var.get()
        download_type = self.download_type.get()  # <-- NUEVO

        if not url or not path:
            messagebox.showerror("Error", "La URL y la carpeta de destino son obligatorias.")
            return
        
        self.download_button.config(state=tk.DISABLED, text="Descargando...")
        self.progress_bar['value'] = 0

        # Pasamos el valor de download_playlist a la función del hilo
        thread = threading.Thread(target=self.run_download, args=(url, path, download_playlist, download_type))
        thread.start()

    def run_download(self, url, path, download_playlist, download_type):
        """El hilo de descarga ahora recibe el parámetro de la playlist."""
        try:
            # Se lo pasamos a nuestra clase de lógica
            result = self.downloader.download_content(url, path, download_playlist, download_type=download_type)

            if result['status'] == 'success':
                messagebox.showinfo("Éxito", result['message'])
            else:
                messagebox.showerror("Error", result['message'])

        except Exception as e:
            self.update_status_label(f"Error crítico: {e}", "red")
            messagebox.showerror("Error Crítico", f"Ha ocurrido un error inesperado:\n{e}")
        finally:
            self.root.after(0, self.enable_download_button)
    
    def enable_download_button(self):
        # ... (sin cambios) ...
        self.download_button.config(state=tk.NORMAL, text="Descargar")

    def update_status_label(self, message, color="black"):
        # ... (sin cambios) ...
        self.root.after(0, lambda: self.status_label.config(text=message, fg=color))

    def update_progress_bar(self, percentage):
        # ... (sin cambios) ...
        self.root.after(0, lambda: self.progress_bar.config(value=percentage))

    def on_exit(self):
        if messagebox.askokcancel("Salir", "¿Seguro que deseas cerrar la aplicación?"):
            self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Descargador Universal de Contenido")

    try:
        root.wm_attributes("-type", "normal")
    except:
        pass
    app = DownloaderApp(root)
    root.mainloop()