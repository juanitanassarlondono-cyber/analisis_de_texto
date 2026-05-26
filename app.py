import streamlit as st
import os
import time
import glob
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator


text=" "

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text




def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #e8fff5 0%, #d4f8e8 45%, #f5fffb 100%);
    color: #24433a;
}

section[data-testid="stSidebar"] {
    background-color: #c9f5df;
    border-right: 1px solid #9fe6c3;
}

h1 {
    color: #1f6f5b;
    font-weight: 800;
    letter-spacing: -0.5px;
}

h2, h3 {
    color: #26745f;
    font-weight: 700;
}

p, label, div, span {
    color: #24433a;
}

div.stButton > button {
    background-color: #66d9a3;
    color: #ffffff;
    border: none;
    border-radius: 14px;
    padding: 0.7rem 1.4rem;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(58, 155, 116, 0.22);
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    background-color: #3fc98b;
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(58, 155, 116, 0.28);
}

div.stButton > button:active {
    transform: translateY(0px);
}

div[data-testid="stFileUploader"] {
    background-color: rgba(255, 255, 255, 0.65);
    border: 1px dashed #78d9ad;
    border-radius: 16px;
    padding: 16px;
}

div[data-testid="stCameraInput"] {
    background-color: rgba(255, 255, 255, 0.65);
    border-radius: 16px;
    padding: 12px;
}

.stCheckbox, .stRadio, .stSelectbox {
    background-color: rgba(255, 255, 255, 0.48);
    border-radius: 14px;
    padding: 8px 10px;
    margin-bottom: 8px;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

hr {
    border: none;
    border-top: 1px solid #9fe6c3;
    margin: 22px 0;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
</style>
""", unsafe_allow_html=True)



st.title("Reconocimiento Óptico de Caracteres")
st.subheader("Elige la fuente de la imagen. Puedes usar la cámara o cargar un archivo.")

st.markdown("### 🖼️ Cargar imagen")
bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg"])

st.markdown("### 📷 Usar cámara")
cam_ = st.checkbox("Usar Cámara")

if cam_ :
   img_file_buffer = st.camera_input("Toma una Foto")
else :
   img_file_buffer = None
   
with st.sidebar:
      st.subheader("Procesamiento para Cámara")
      filtro = st.radio("Filtro para imagen con cámara",('Sí', 'No'))

if bg_image is not None:
    uploaded_file=bg_image
    st.image(uploaded_file, caption='Imagen cargada.', use_container_width=True)
    
    # Guardar la imagen en el sistema de archivos
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())
    
    st.success(f"Imagen guardada como {uploaded_file.name}")
    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text= pytesseract.image_to_string(img_rgb)
st.write(text)  
    
      
if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    
    if filtro == 'Con Filtro':
         cv2_img=cv2.bitwise_not(cv2_img)
    else:
        cv2_img= cv2_img
          
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text=pytesseract.image_to_string(img_rgb) 
    st.write(text) 

with st.sidebar:
      st.subheader("Parámetros de traducción")
      
      try:
          os.mkdir("temp")
      except:
          pass
      #st.title("Text to speech")
      translator = Translator()
      
      #text = st.text_input("Enter text")
      in_lang = st.selectbox(
          "Seleccione el lenguaje de entrada",
          ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
      )
      if in_lang == "Ingles":
          input_language = "en"
      elif in_lang == "Español":
          input_language = "es"
      elif in_lang == "Bengali":
          input_language = "bn"
      elif in_lang == "koreano":
          input_language = "ko"
      elif in_lang == "Mandarin":
          input_language = "zh-cn"
      elif in_lang == "Japones":
          input_language = "ja"
      
      out_lang = st.selectbox(
          "Select your output language",
          ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
      )
      if out_lang == "Ingles":
          output_language = "en"
      elif out_lang == "Español":
          output_language = "es"
      elif out_lang == "Bengali":
          output_language = "bn"
      elif out_lang == "koreano":
          output_language = "ko"
      elif out_lang == "Chinese":
          output_language = "zh-cn"
      elif out_lang == "Japones":
          output_language = "ja"
      
      english_accent = st.selectbox(
          "Seleccione el acento",
          (
              "Default",
              "India",
              "United Kingdom",
              "United States",
              "Canada",
              "Australia",
              "Ireland",
              "South Africa",
          ),
      )
      
      if english_accent == "Default":
          tld = "com"
      elif english_accent == "India":
          tld = "co.in"
      
      elif english_accent == "United Kingdom":
          tld = "co.uk"
      elif english_accent == "United States":
          tld = "com"
      elif english_accent == "Canada":
          tld = "ca"
      elif english_accent == "Australia":
          tld = "com.au"
      elif english_accent == "Ireland":
          tld = "ie"
      elif english_accent == "South Africa":
          tld = "co.za"

      display_output_text = st.checkbox("Mostrar texto")

      st.markdown("---")

      if st.button("Convertir a audio"):
          result, output_text = text_to_speech(input_language, output_language, text, tld)
          audio_file = open(f"temp/{result}.mp3", "rb")
          audio_bytes = audio_file.read()
          st.markdown(f"## Tu audio:")
          st.audio(audio_bytes, format="audio/mp3", start_time=0)
      
          if display_output_text:
              st.markdown(f"## Texto de salida:")
              st.write(f" {output_text}")
