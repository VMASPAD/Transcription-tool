import tkinter as tk
from tkinter import filedialog, messagebox, Text
from tkinter import ttk
import subprocess
import threading

languages = [
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani", 
    "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian", "Breton", "Bulgarian", "Burmese", 
    "Cantonese", "Castilian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", 
    "English", "Estonian", "Faroese", "Finnish", "Flemish", "French", "Galician", "Georgian", 
    "German", "Greek", "Gujarati", "Haitian", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew", 
    "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Javanese", "Kannada", 
    "Kazakh", "Khmer", "Korean", "Lao", "Latin", "Latvian", "Letzeburgesch", "Lingala", "Lithuanian", 
    "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Mandarin", "Maori", 
    "Marathi", "Moldavian", "Moldovan", "Mongolian", "Myanmar", "Nepali", "Norwegian", "Nynorsk", 
    "Occitan", "Panjabi", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Pushto", 
    "Romanian", "Russian", "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Sinhalese", 
    "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tagalog", 
    "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tibetan", "Turkish", "Turkmen", "Ukrainian", 
    "Urdu", "Uzbek", "Valencian", "Vietnamese", "Welsh", "Yiddish", "Yoruba"
]

# Variables para construir el comando
comando_parts = {
    "archivo": "",
    "carpeta": "",
    "idioma_origen": "",
    "idioma_destino": "",
    "otros": ""
}

def construir_comando():
    return (
        f'whisper "{comando_parts["archivo"]}" '
        f'--language {comando_parts["idioma_origen"]} '
        f'--output_dir "{comando_parts["carpeta"]}" '
        f'{comando_parts["otros"]}'
        f' --language {comando_parts["idioma_destino"]} '.strip()
    )

# Función para seleccionar archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo de video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mkv")]
    )
    if archivo:
        archivo_var.set(archivo)
        comando_parts["archivo"] = archivo

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta de salida")
    if carpeta:
        carpeta_var.set(carpeta)
        comando_parts["carpeta"] = carpeta

# Función para ejecutar el comando Whisper
def ejecutar_comando():
    idioma_origen = idioma_origen_var.get()
    idioma_destino = idioma_destino_var.get()

    if not comando_parts["archivo"] or not comando_parts["carpeta"] or not idioma_origen or not idioma_destino:
        messagebox.showerror("Error", "Todos los campos deben estar completos.")
        return

    comando_parts["idioma_origen"] = idioma_origen
    comando_parts["idioma_destino"] = idioma_destino

    comando = construir_comando()

    log_text.config(state='normal')
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, f"Ejecutando comando: {comando}\n")
    log_text.config(state='disabled')

    def ejecutar():
        try:
            proceso = subprocess.Popen(
                comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )
            for linea in iter(proceso.stdout.readline, ''):
                log_text.config(state='normal')
                log_text.insert(tk.END, linea)
                log_text.config(state='disabled')
                log_text.see(tk.END)

            proceso.stdout.close()
            proceso.stderr.close()
            proceso.wait()

            log_text.config(state='normal')
            log_text.insert(tk.END, "Proceso finalizado.\n")
            log_text.config(state='disabled')
        except Exception as e:
            log_text.config(state='normal')
            log_text.insert(tk.END, f"Error: {e}\n")
            log_text.config(state='disabled')

    threading.Thread(target=ejecutar).start()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Video Transcription Tool")
root.geometry("1200x1200")

# Crear el contenedor de pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Crear el marco principal
frame_principal = ttk.Frame(notebook, padding=10)
notebook.add(frame_principal, text="Principal")

# Crear el marco de configuración
frame_configuracion = ttk.Frame(notebook, padding=10)
notebook.add(frame_configuracion, text="Configuración")

# Variables
archivo_var = tk.StringVar(value="No seleccionado")
carpeta_var = tk.StringVar(value="No seleccionado")
idioma_origen_var = tk.StringVar()
idioma_destino_var = tk.StringVar()

# Configuración de la UI en la pestaña Principal
ttk.Label(frame_principal, text="Archivo de video").grid(row=0, column=0, sticky="w", pady=5)
ttk.Entry(frame_principal, textvariable=archivo_var, state="readonly").grid(row=0, column=1, sticky="ew", padx=5)
ttk.Button(frame_principal, text="Seleccionar", command=seleccionar_archivo).grid(row=0, column=2)

ttk.Label(frame_principal, text="Carpeta de salida").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(frame_principal, textvariable=carpeta_var, state="readonly").grid(row=1, column=1, sticky="ew", padx=5)
ttk.Button(frame_principal, text="Seleccionar", command=seleccionar_carpeta).grid(row=1, column=2)

ttk.Label(frame_principal, text="Idioma de origen").grid(row=2, column=0, sticky="w", pady=5)
ttk.Combobox(frame_principal, textvariable=idioma_origen_var, values=languages, state="readonly").grid(row=2, column=1, sticky="ew", padx=5)

ttk.Label(frame_principal, text="Idioma de destino").grid(row=3, column=0, sticky="w", pady=5)
ttk.Combobox(frame_principal, textvariable=idioma_destino_var, values=languages, state="readonly").grid(row=3, column=1, sticky="ew", padx=5)

ttk.Button(frame_principal, text="Generar", command=ejecutar_comando).grid(row=4, column=0, columnspan=3, pady=10)

log_frame = ttk.LabelFrame(frame_principal, text="Registro del proceso", padding=5)
log_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=10)

log_text = Text(log_frame, height=10, state="disabled", wrap="word")
log_text.pack(fill=tk.BOTH, expand=True)

frame_principal.columnconfigure(1, weight=1)

# Configuración de la UI en la pestaña Configuración
ttk.Label(frame_configuracion, text="Opciones avanzadas").grid(row=0, column=0, pady=10, sticky="w")
ttk.Label(frame_configuracion, text="En algunos valores al ser mas grandes o menores puede hacer que se consuma mas potencia del dispositivo y a su vez mas consumo energético").grid(row=1, column=0, pady=5, sticky="w")
opcion_var = tk.StringVar(value="")
ttk.Label(frame_configuracion, text="Modelo (e.g., base, large)").grid(row=3, column=0, pady=5, sticky="w")
model_var = tk.StringVar(value="base")  # Valor por defecto: base
ttk.Entry(frame_configuracion, textvariable=model_var).grid(row=3, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Especifica el modelo de transcripción, como 'tiny', 'base', 'small', 'medium', 'large' y 'turbo'. A mas grande mas uso de GPU").grid(row=3, column=2, pady=5, sticky="w")

# Descripción para 'Directorio del modelo'
ttk.Label(frame_configuracion, text="Directorio del modelo").grid(row=4, column=0, pady=5, sticky="w")
model_dir_var = tk.StringVar(value="")  # Directorio por defecto vacío
ttk.Entry(frame_configuracion, textvariable=model_dir_var).grid(row=4, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Ruta al directorio donde se encuentra el modelo.").grid(row=4, column=2, pady=5, sticky="w")

# Descripción para 'Dispositivo'
ttk.Label(frame_configuracion, text="Dispositivo (e.g., cpu, cuda)").grid(row=5, column=0, pady=5, sticky="w")
device_var = tk.StringVar(value="cpu")  # Valor por defecto: cpu
ttk.Entry(frame_configuracion, textvariable=device_var).grid(row=5, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="El dispositivo en el que ejecutar el modelo, como 'cpu' o 'cuda'.").grid(row=5, column=2, pady=5, sticky="w")

# Descripción para 'Formato de salida'
ttk.Label(frame_configuracion, text="Formato de salida (txt, vtt, srt, etc.)").grid(row=6, column=0, pady=5, sticky="w")
output_format_var = tk.StringVar(value="txt")  # Valor por defecto: txt
ttk.Entry(frame_configuracion, textvariable=output_format_var).grid(row=6, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Define el formato del archivo de salida (e.g., txt,vtt,srt,tsv,json,all).").grid(row=6, column=2, pady=5, sticky="w")

# Descripción para 'Verbose'
ttk.Label(frame_configuracion, text="Verbose (True/False)").grid(row=7, column=0, pady=5, sticky="w")
verbose_var = tk.StringVar(value="False")  # Valor por defecto: True
ttk.Entry(frame_configuracion, textvariable=verbose_var).grid(row=7, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Si es True, se muestra información detallada durante el proceso. (Solo usarse si no termina la tarea)").grid(row=7, column=2, pady=5, sticky="w")

# Descripción para 'Tarea'
ttk.Label(frame_configuracion, text="Tarea (transcribe, translate)").grid(row=8, column=0, pady=5, sticky="w")
task_var = tk.StringVar(value="transcribe")  # Valor por defecto: transcribe
ttk.Entry(frame_configuracion, textvariable=task_var).grid(row=8, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Si realizar el reconocimiento de voz X->X («transcribir») o la traducción X->inglés («traducir») (por defecto: transcribir)").grid(row=8, column=2, pady=5, sticky="w")

# Nuevas opciones avanzadas con descripción:

# Temperatura
ttk.Label(frame_configuracion, text="Temperatura (default: 0)").grid(row=9, column=0, pady=5, sticky="w")
temperature_var = tk.StringVar(value="0")  # Valor por defecto: 0
ttk.Entry(frame_configuracion, textvariable=temperature_var).grid(row=9, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Controla la aleatoriedad del modelo. Un valor más alto da más variedad.").grid(row=9, column=2, pady=5, sticky="w")

# Best of
ttk.Label(frame_configuracion, text="Best of (default: 5)").grid(row=10, column=0, pady=5, sticky="w")
best_of_var = tk.StringVar(value="5")  # Valor por defecto: 5
ttk.Entry(frame_configuracion, textvariable=best_of_var).grid(row=10, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Número de opciones generadas para seleccionar la mejor.").grid(row=10, column=2, pady=5, sticky="w")

# Beam size
ttk.Label(frame_configuracion, text="Beam size (default: 5)").grid(row=11, column=0, pady=5, sticky="w")
beam_size_var = tk.StringVar(value="5")  # Valor por defecto: 5
ttk.Entry(frame_configuracion, textvariable=beam_size_var).grid(row=11, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="El tamaño del haz de búsqueda para la decodificación.").grid(row=11, column=2, pady=5, sticky="w")

# Patience
ttk.Label(frame_configuracion, text="Patience (default: None)").grid(row=12, column=0, pady=5, sticky="w")
patience_var = tk.StringVar(value="None")  # Valor por defecto: None
ttk.Entry(frame_configuracion, textvariable=patience_var).grid(row=12, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Paciencia para la decodificación, usado para evitar sobreajuste.").grid(row=12, column=2, pady=5, sticky="w")

# Length penalty
ttk.Label(frame_configuracion, text="Length penalty (default: None)").grid(row=13, column=0, pady=5, sticky="w")
length_penalty_var = tk.StringVar(value="None")  # Valor por defecto: None
ttk.Entry(frame_configuracion, textvariable=length_penalty_var).grid(row=13, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Penalización de la longitud para controlar el largo de la respuesta.").grid(row=13, column=2, pady=5, sticky="w")

# Suppress tokens
ttk.Label(frame_configuracion, text="Suppress tokens (default: -1)").grid(row=14, column=0, pady=5, sticky="w")
suppress_tokens_var = tk.StringVar(value="-1")  # Valor por defecto: -1
ttk.Entry(frame_configuracion, textvariable=suppress_tokens_var).grid(row=14, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Tokens a suprimir durante la decodificación.").grid(row=14, column=2, pady=5, sticky="w")

# Initial prompt
ttk.Label(frame_configuracion, text="Initial prompt (default: None)").grid(row=15, column=0, pady=5, sticky="w")
initial_prompt_var = tk.StringVar(value="None")  # Valor por defecto: None
ttk.Entry(frame_configuracion, textvariable=initial_prompt_var).grid(row=15, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Mensaje inicial para proporcionar contexto al modelo.").grid(row=15, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Condition on previous text (default: True)").grid(row=16, column=0, pady=5, sticky="w")
condition_on_previous_text_var = tk.StringVar(value="True")  # Valor por defecto: True
ttk.Entry(frame_configuracion, textvariable=condition_on_previous_text_var).grid(row=16, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Si es True, el modelo se condiciona en el texto anterior.").grid(row=16, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="FP16 (default: True)").grid(row=17, column=0, pady=5, sticky="w")
fp16_var = tk.StringVar(value="True")  # Valor por defecto: True
ttk.Label(frame_configuracion, text="Si es True, usa FP16 para reducir el uso de memoria.").grid(row=17, column=2, pady=5, sticky="w")
ttk.Entry(frame_configuracion, textvariable=fp16_var).grid(row=17, column=1, pady=5, sticky="ew", padx=5)


ttk.Label(frame_configuracion, text="Temperature increment on fallback (default: 0.2)").grid(row=18, column=0, pady=5, sticky="w")
temperature_increment_on_fallback_var = tk.StringVar(value="0.2")  # Valor por defecto: 0.2
ttk.Entry(frame_configuracion, textvariable=temperature_increment_on_fallback_var).grid(row=18, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Incrementa la temperatura en el caso de un fallback.").grid(row=18, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Compression ratio threshold (default: 2.4)").grid(row=19, column=0, pady=5, sticky="w")
compression_ratio_threshold_var = tk.StringVar(value="2.4")  # Valor por defecto: 2.4
ttk.Entry(frame_configuracion, textvariable=compression_ratio_threshold_var).grid(row=19, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Umbral de compresión para controlar el tamaño del archivo de salida.").grid(row=19, column=2, pady=5, sticky="w")



ttk.Label(frame_configuracion, text="Logprob threshold (default: -1.0)").grid(row=20, column=0, pady=5, sticky="w")
logprob_threshold_var = tk.StringVar(value="-1.0")  # Valor por defecto: -1.0
ttk.Entry(frame_configuracion, textvariable=logprob_threshold_var).grid(row=20, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Umbral para la probabilidad del logaritmo, usado para filtrar palabras de baja probabilidad.").grid(row=20, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="No speech threshold (default: 0.6)").grid(row=21, column=0, pady=5, sticky="w")
no_speech_threshold_var = tk.StringVar(value="0.6")  # Valor por defecto: 0.6
ttk.Entry(frame_configuracion, textvariable=no_speech_threshold_var).grid(row=21, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Umbral para determinar si hay o no habla en el audio.").grid(row=21, column=2, pady=5, sticky="w")



ttk.Label(frame_configuracion, text="Word timestamps (default: False)").grid(row=22, column=0, pady=5, sticky="w")
word_timestamps_var = tk.StringVar(value="False")  # Valor por defecto: False
ttk.Entry(frame_configuracion, textvariable=word_timestamps_var).grid(row=22, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Si es True, incluye marcas de tiempo para cada palabra.").grid(row=22, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Prepend punctuations (default: \"'“¿([{-)\")").grid(row=23, column=0, pady=5, sticky="w")
prepend_punctuations_var = tk.StringVar(value="'“¿([{-)")  # Valor por defecto: "'“¿([{-)"
ttk.Entry(frame_configuracion, textvariable=prepend_punctuations_var).grid(row=23, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Puntuaciones que se añadirán al principio de las frases.").grid(row=23, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Append punctuations (default: \".。,，!！?？:：”)]}、)\")").grid(row=24, column=0, pady=5, sticky="w")
append_punctuations_var = tk.StringVar(value="'.。,，!！?？:：”)]}、)")  # Valor por defecto: "'.。,，!！?？:：”)]}、)"
ttk.Entry(frame_configuracion, textvariable=append_punctuations_var).grid(row=24, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Puntuaciones que se añadirán al final de las frases.").grid(row=24, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Highlight words (default: False)").grid(row=25, column=0, pady=5, sticky="w")
highlight_words_var = tk.StringVar(value="False")  # Valor por defecto: False
ttk.Entry(frame_configuracion, textvariable=highlight_words_var).grid(row=25, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Si es True, resalta las palabras al transcribirlas.").grid(row=25, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Max line width (default: None)").grid(row=26, column=0, pady=5, sticky="w")
max_line_width_var = tk.StringVar(value="None")  # Valor por defecto: None
ttk.Entry(frame_configuracion, textvariable=max_line_width_var).grid(row=26, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Ancho máximo de línea en el archivo de salida.").grid(row=26, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Max line count (default: None)").grid(row=27, column=0, pady=5, sticky="w")
max_line_count_var = tk.StringVar(value="None")  # Valor por defecto: None
ttk.Entry(frame_configuracion, textvariable=max_line_count_var).grid(row=27, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Número máximo de líneas en el archivo de salida.").grid(row=27, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Max words per line (default: None)").grid(row=28, column=0, pady=5, sticky="w")
max_words_per_line_var = tk.StringVar(value="None")  # Valor por defecto: None
ttk.Entry(frame_configuracion, textvariable=max_words_per_line_var).grid(row=28, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Número máximo de palabras por línea en el archivo de salida.").grid(row=28, column=2, pady=5, sticky="w")


ttk.Label(frame_configuracion, text="Threads (default: 0)").grid(row=29, column=0, pady=5, sticky="w")
threads_var = tk.StringVar(value="0")  # Valor por defecto: 0
ttk.Entry(frame_configuracion, textvariable=threads_var).grid(row=29, column=1, pady=5, sticky="ew", padx=5)
ttk.Label(frame_configuracion, text="Número de hilos a usar para la transcripción.").grid(row=29, column=2, pady=5, sticky="w")

# Modificar la función guardar_configuracion para incluir los nuevos campos
def guardar_configuracion():
    comando_parts["model"] = model_var.get()
    comando_parts["model_dir"] = model_dir_var.get()
    comando_parts["device"] = device_var.get()
    comando_parts["output_format"] = output_format_var.get()
    comando_parts["verbose"] = verbose_var.get()
    comando_parts["task"] = task_var.get()
    
    comando_parts["temperature"] = temperature_var.get()
    comando_parts["best_of"] = best_of_var.get()
    comando_parts["beam_size"] = beam_size_var.get()
    comando_parts["patience"] = patience_var.get()
    comando_parts["length_penalty"] = length_penalty_var.get()
    comando_parts["suppress_tokens"] = suppress_tokens_var.get()
    comando_parts["initial_prompt"] = initial_prompt_var.get()
    comando_parts["condition_on_previous_text"] = condition_on_previous_text_var.get()
    comando_parts["fp16"] = fp16_var.get()
    comando_parts["temperature_increment_on_fallback"] = temperature_increment_on_fallback_var.get()
    comando_parts["compression_ratio_threshold"] = compression_ratio_threshold_var.get()
    comando_parts["logprob_threshold"] = logprob_threshold_var.get()
    comando_parts["no_speech_threshold"] = no_speech_threshold_var.get()
    comando_parts["word_timestamps"] = word_timestamps_var.get()
    comando_parts["prepend_punctuations"] = prepend_punctuations_var.get()
    comando_parts["append_punctuations"] = append_punctuations_var.get()
    comando_parts["highlight_words"] = highlight_words_var.get()
    comando_parts["max_line_width"] = max_line_width_var.get()
    comando_parts["max_line_count"] = max_line_count_var.get()
    comando_parts["max_words_per_line"] = max_words_per_line_var.get()
    comando_parts["threads"] = threads_var.get()

    # Actualizar el comando con los nuevos valores
    if comando_parts["condition_on_previous_text"].lower() == "true":
        comando_parts["otros"] += " --condition_on_previous_text True"
    if comando_parts["fp16"].lower() == "true":
        comando_parts["otros"] += " --fp16 True"
    if comando_parts["temperature_increment_on_fallback"]:
        comando_parts["otros"] += f" --temperature_increment_on_fallback {comando_parts['temperature_increment_on_fallback']}"
    if comando_parts["compression_ratio_threshold"]:
        comando_parts["otros"] += f" --compression_ratio_threshold {comando_parts['compression_ratio_threshold']}"
    if comando_parts["logprob_threshold"]:
        comando_parts["otros"] += f" --logprob_threshold {comando_parts['logprob_threshold']}"
    if comando_parts["no_speech_threshold"]:
        comando_parts["otros"] += f" --no_speech_threshold {comando_parts['no_speech_threshold']}"
    if comando_parts["word_timestamps"].lower() == "true":
        comando_parts["otros"] += " --word_timestamps True"
    if comando_parts["prepend_punctuations"]:
        comando_parts["otros"] += f" --prepend_punctuations {comando_parts['prepend_punctuations']}"
    if comando_parts["append_punctuations"]:
        comando_parts["otros"] += f" --append_punctuations {comando_parts['append_punctuations']}"
    if comando_parts["highlight_words"].lower() == "true":
        comando_parts["otros"] += " --highlight_words True"
    if comando_parts["max_line_width"] and comando_parts["max_line_width"].lower() != "none":
        comando_parts["otros"] += f" --max_line_width {comando_parts['max_line_width']}"
    if comando_parts["max_line_count"] and comando_parts["max_line_count"].lower() != "none":
        comando_parts["otros"] += f" --max_line_count {comando_parts['max_line_count']}"
    if comando_parts["max_words_per_line"] and comando_parts["max_words_per_line"].lower() != "none":
        comando_parts["otros"] += f" --max_words_per_line {comando_parts['max_words_per_line']}"
    if comando_parts["threads"]:
        comando_parts["otros"] += f" --threads {comando_parts['threads']}"
    # Actualizar el comando con los nuevos valores
    if comando_parts["verbose"].lower() == "true":
        comando_parts["otros"] += " --verbose"
    if comando_parts["model"]:
        comando_parts["otros"] += f" --model {comando_parts['model']}"
    if comando_parts["model_dir"]:
        comando_parts["otros"] += f" --model_dir {comando_parts['model_dir']}"
    if comando_parts["device"]:
        comando_parts["otros"] += f" --device {comando_parts['device']}"
    if comando_parts["output_format"]:
        comando_parts["otros"] += f" --output_format {comando_parts['output_format']}"
    if comando_parts["task"]:
        comando_parts["otros"] += f" --task {comando_parts['task']}"
    if comando_parts["temperature"]:
        comando_parts["otros"] += f" --temperature {comando_parts['temperature']}"
    if comando_parts["best_of"]:
        comando_parts["otros"] += f" --best_of {comando_parts['best_of']}"
    if comando_parts["beam_size"]:
        comando_parts["otros"] += f" --beam_size {comando_parts['beam_size']}"
    if comando_parts["patience"] and comando_parts["patience"].lower() != "none":
        comando_parts["otros"] += f" --patience {comando_parts['patience']}"
    if comando_parts["length_penalty"] and comando_parts["length_penalty"].lower() != "none":
        comando_parts["otros"] += f" --length_penalty {comando_parts['length_penalty']}"
    if comando_parts["suppress_tokens"]:
        comando_parts["otros"] += f" --suppress_tokens {comando_parts['suppress_tokens']}"
    if comando_parts["initial_prompt"] and comando_parts["initial_prompt"].lower() != "none":
        comando_parts["otros"] += f" --initial_prompt {comando_parts['initial_prompt']}"
    
    messagebox.showinfo("Configuración", "Configuración guardada.")


ttk.Button(frame_configuracion, text="Guardar Configuración", command=guardar_configuracion).grid(row=2, column=0, pady=10, sticky="ew")

root.mainloop()
