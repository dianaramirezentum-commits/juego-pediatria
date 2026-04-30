import streamlit as st
from difflib import SequenceMatcher

# --- CONFIGURACIÓN Y ESTILO ---
# Esto pone tu banner al principio de la página
st.image("banner.png.png", use_container_width=True)

def local_css():
    st.markdown("""
        <style>
        .main [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle, #1a3a5f 0%, #08111d 100%);
    }
        .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
        .answer-box {
            background: linear-gradient(145deg, #004AAD, #002B6B);
            border: 3px solid #FFD700;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: white;
            min-height: 90px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        }
        .score-box {
            background-color: #1E1E1E;
            border: 2px solid #FFD700;
            font-size: 45px;
            text-align: center;
            color: #FFD700;
            border-radius: 10px;
            padding: 5px;
        }
        .bank-box {
            background-color: #FFD700;
            color: #1E1E1E;
            font-size: 60px;
            text-align: center;
            font-weight: bold;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .strike-text { color: #FF4B4B; font-size: 80px; font-weight: bold; text-align: center; margin-top: -20px; }
        .question-text { background-color: #262730; padding: 20px; border-radius: 10px; border-left: 5px solid #004AAD; }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- BASE DE DATOS (Mismas 21 preguntas) ---
preguntas_db = [
    {"p": "Signos principales en un toxíndrome anticolinérgico", "r": [("Midriasis", 30), ("Taquicardia", 25), ("Piel seca", 20), ("Rubicundez", 15), ("Hipertermia", 10)]},
    {"p": "Principales agentes virales que generan resfriado común", "r": [("Rinovirus", 30), ("Coronavirus", 25), ("Virus Parainfluenza", 20), ("Virus Influenza", 15), ("Adenovirus", 10)]},
    {"p": "Pasos iniciales del RN (Algoritmo Reanimación Neonatal)", "r": [("Calor", 30), ("Posicionar vía aérea", 25), ("Aspiración de secreciones", 20), ("Secar", 15), ("Estimular", 10)]},
    {"p": "Agentes etiológicos más frecuentes en OMA", "r": [("Streptococcus pneumoniae", 30), ("Haemophilus influenzae", 25), ("Moraxella catarrhalis", 20), ("Streptococcus pyogenes", 15), ("Pseudomonas", 10)]},
    {"p": "Principales agentes de Diarrea Infecciosa en < 1 año", "r": [("Rotavirus", 30), ("Adenovirus entérico", 25), ("E. coli", 20), ("Campylobacter jejuni", 15), ("Salmonella", 10)]},
    {"p": "Datos de dificultad respiratoria (Silverman-Andersen) por orden", "r": [("Disociación toraco-abdominal", 30), ("Tiraje intercostal", 25), ("Retracción xifoidea", 20), ("Aleteo nasal", 15), ("Quejido respiratorio", 10)]},
    {"p": "Las 5 H de causas reversibles en paro cardiaco pediátrico", "r": [("Hipoxia", 30), ("Hipovolemia", 25), ("Hidrogeniones", 20), ("Hiper/Hipokalemia", 15), ("Hipotermia", 10)]},
    {"p": "Las 5 T de causas reversibles en paro cardiaco pediátrico", "r": [("Neumotórax a tensión", 30), ("Tóxicos", 25), ("Taponamiento cardiaco", 20), ("Trombosis pulmonar", 15), ("Trombosis coronaria", 10)]},
    {"p": "Características de deshidratación con Choque Hipovolémico", "r": [("Llenado capilar >2 seg", 30), ("Estado general hipotónico", 25), ("Pulso débil o ausente", 20), ("No puede beber", 15), ("Taquicardia", 10)]},
    {"p": "Pasos para aplicación de surfactante (Técnica INSURE)", "r": [("Administración de cafeína", 30), ("Intubación", 25), ("Aplicación de surfactante", 20), ("Extubación", 15), ("Paso a CPAP", 10)]},
    {"p": "Lesiones por trauma obstétrico más comunes", "r": [("Caput succedaneum", 30), ("Petequias y equimosis", 25), ("Cefalohematoma", 20), ("Fractura de clavícula", 15), ("Parálisis nerviosa", 10)]},
    {"p": "Causas de Ictericia Neonatal", "r": [("Ictericia fisiológica", 30), ("Lactancia materna", 25), ("Enfermedades hemolíticas", 20), ("Infecciones", 15), ("Patologías hepáticas", 10)]},
    {"p": "Signos Radiográficos de Bronquiolitis", "r": [("Hiperinsuflación", 30), ("Aplanamiento de diafragma", 25), ("Horizontalización de costillas", 20), ("Incremento espacio intercostal", 15), ("Atelectasias", 10)]},
    {"p": "Agentes etiológicos de diarrea invasiva (Con sangre)", "r": [("Shigella", 30), ("Campylobacter jejuni", 25), ("Salmonella", 20), ("E. coli enteroinvasiva", 15), ("Yersinia enterocolitica", 10)]},
    {"p": "Dispositivos para el manejo de la Vía Aérea", "r": [("Mascarilla facial", 30), ("BVM", 25), ("Cánula orofaríngea", 20), ("Mascarilla laríngea", 15), ("Tubo endotraqueal", 10)]},
    {"p": "Fármacos usados en tratamiento de crisis asmática", "r": [("Salbutamol", 30), ("Oxígeno", 25), ("Corticoides", 20), ("Bromuro de ipratropio", 15), ("Sulfato de magnesio", 10)]},
    {"p": "Orden de visualización en laringoscopia (Intubación)", "r": [("Base de la lengua", 30), ("Epiglotis", 25), ("Vallécula", 20), ("Glotis", 15), ("Cuerdas vocales", 10)]},
    {"p": "Criterios de Centor Modificados", "r": [("Exudado amigdalar", 30), ("Adenopatías cervicales", 25), ("Fiebre >38C", 20), ("Ausencia de tos", 15), ("Edad 3-14 años", 10)]},
    {"p": "Animales venenosos en México (Frecuencia)", "r": [("Alacrán", 30), ("Araña viuda negra", 25), ("Víbora de cascabel", 20), ("Araña violinista", 15), ("Serpiente coralillo", 10)]},
    {"p": "Factores de riesgo para sepsis neonatal temprana", "r": [("RPM >18 HR", 30), ("Corioamnionitis", 25), ("Prematurez extrema", 20), ("SGBB", 15), ("Sexo masculino", 10)]},
    {"p": "Factores de riesgo maternos para TTRN", "r": [("Cesárea programada", 30), ("Diabetes Mellitus", 25), ("Asma materna", 20), ("Tabaquismo", 15), ("Parto precipitado", 10)]}
]

# --- ESTADO DEL JUEGO ---
if 'idx' not in st.session_state:
    st.session_state.idx = 0
    st.session_state.puntos_a = 0
    st.session_state.puntos_b = 0
    st.session_state.banca = 0
    st.session_state.strikes = 0
    st.session_state.reveladas = []

def similitud(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def revelar_opcion(i, pts):
    if i not in st.session_state.reveladas:
        st.session_state.reveladas.append(i)
        st.session_state.banca += pts
        return True
    return False

# --- INTERFAZ PRINCIPAL ---
st.title("🩺 100 Pediatras Dijeron")

# Fila Superior: Marcadores y Banca
c1, c_bank, c2 = st.columns([1, 1, 1])

with c1:
    st.markdown("### Equipo A")
    st.markdown(f"<div class='score-box'>{st.session_state.puntos_a}</div>", unsafe_allow_html=True)
    if st.button("🏆 Banca -> Equipo A"):
        st.session_state.puntos_a += st.session_state.banca
        st.session_state.banca = 0
        st.rerun()

with c_bank:
    st.markdown("<h3 style='text-align: center;'>BANCA</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='bank-box'>{st.session_state.banca}</div>", unsafe_allow_html=True)

with c2:
    st.markdown("### Equipo B")
    st.markdown(f"<div class='score-box'>{st.session_state.puntos_b}</div>", unsafe_allow_html=True)
    if st.button("🏆 Banca -> Equipo B"):
        st.session_state.puntos_b += st.session_state.banca
        st.session_state.banca = 0
        st.rerun()

# Fila de Errores (Strikes)
st.markdown(f"<div class='strike-text'>{'X ' * st.session_state.strikes}</div>", unsafe_allow_html=True)
err_col1, err_col2, err_col3 = st.columns([2,1,2])
with err_col2:
    if st.button("❌ Marcar Error"): 
        st.session_state.strikes = (st.session_state.strikes + 1) % 4
        st.rerun()

# Pregunta
pregunta_actual = preguntas_db[st.session_state.idx]
st.markdown(f"<div class='question-text'><h2>{st.session_state.idx + 1}. {pregunta_actual['p']}</h2></div>", unsafe_allow_html=True)
st.write("")

# Panel de entrada del moderador
mod_c1, mod_c2 = st.columns([3, 1])
with mod_c1:
    entrada = st.text_input("Escribe la respuesta del alumno:", placeholder="Ej. Rinovirus...")
with mod_c2:
    st.write("##")
    if st.button("Validar ✅"):
        for i, (txt, pts) in enumerate(pregunta_actual['r']):
            if similitud(entrada, txt) > 0.75:
                if revelar_opcion(i, pts):
                    st.balloons()
                    st.rerun()

# Tablero de Respuestas (Grid)
st.write("---")
cols = st.columns(2)
for i, (txt, pts) in enumerate(pregunta_actual['r']):
    with cols[i % 2]:
        if i in st.session_state.reveladas:
            st.markdown(f"<div class='answer-box'>{txt.upper()} — {pts}</div>", unsafe_allow_html=True)
        else:
            # Botón oculto para revelar manualmente y sumar a banca
            if st.button(f"Revelar {i+1}", key=f"rev_{i}"):
                revelar_opcion(i, pts)
                st.rerun()
            st.markdown(f"<div class='answer-box'>{i+1}</div>", unsafe_allow_html=True)

# Barra Lateral de Navegación
st.sidebar.title("Configuración")
if st.sidebar.button("Siguiente Pregunta ➡️"):
    if st.session_state.idx < len(preguntas_db) - 1:
        st.session_state.idx += 1
        st.session_state.reveladas = []
        st.session_state.strikes = 0
        st.session_state.banca = 0 # Reiniciamos banca para la nueva pregunta
        st.rerun()

st.sidebar.write("---")
# Ajuste manual por si te equivocas
st.sidebar.subheader("Ajuste Manual")
manual_a = st.sidebar.number_input("Puntos Equipo A", value=st.session_state.puntos_a)
manual_b = st.sidebar.number_input("Puntos Equipo B", value=st.session_state.puntos_b)
if st.sidebar.button("Actualizar Marcadores"):
    st.session_state.puntos_a = manual_a
    st.session_state.puntos_b = manual_b
    st.rerun()

if st.sidebar.button("Reiniciar Todo 🔄"):
    st.session_state.clear()
    st.rerun()
