
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# ---------------- CONFIGURACIÓN ----------------

st.set_page_config(
    page_title="Creative Notebook",
    page_icon="🎨",
    layout="wide"
)

# ---------------- ESTILOS ----------------

st.markdown("""
<style>
.stApp {
    background-color: #F8F6FC;
}

h1 {
    color: #65577A;
    text-align: center;
}

.subtitle {
    color: #8A8197;
    text-align: center;
    margin-bottom: 20px;
}

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid #E4DCEC;
    background-color: white;
    color: #65577A;
    font-weight: 600;
    width: 100%;
    min-height: 40px;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: #BDA9D6;
    color: #65577A;
}

section[data-testid="stSidebar"] {
    background-color: #F0EAF7;
}
</style>
""", unsafe_allow_html=True)

# ---------------- ESTADO ----------------

if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0

if "selected_color" not in st.session_state:
    st.session_state.selected_color = "#65577A"

if "brush_size" not in st.session_state:
    st.session_state.brush_size = 5

if "tool" not in st.session_state:
    st.session_state.tool = "Lápiz"

if "last_image" not in st.session_state:
    st.session_state.last_image = None

# ---------------- ENCABEZADO ----------------

st.markdown("<h1>🎨 Creative Notebook</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Un espacio para dibujar, crear y dejar volar tu imaginación.</p>',
    unsafe_allow_html=True
)

# ---------------- BOTONES PRINCIPALES ----------------

st.markdown("### Acciones principales")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🗑️ Borrar hoja"):
        st.session_state.canvas_version += 1
        st.session_state.last_image = None
        st.rerun()

with c2:
    if st.button("📄 Nuevo tablero"):
        st.session_state.canvas_version += 1
        st.session_state.last_image = None
        st.rerun()

with c3:
    if st.button("↩️ Reiniciar"):
        st.session_state.canvas_version += 1
        st.session_state.last_image = None
        st.rerun()

st.divider()

# ---------------- HERRAMIENTAS ----------------

st.markdown("### Herramientas de dibujo")

col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])

with col1:
    tool = st.selectbox(
        "Herramienta",
        ["Lápiz", "Pincel", "Marcador", "Borrador", "Línea", "Rectángulo", "Círculo"]
    )

with col2:
    brush_size = st.slider(
        "Grosor",
        min_value=1,
        max_value=30,
        value=5
    )

with col3:
    selected_color = st.color_picker(
        "Color",
        value="#65577A"
    )

with col4:
    background_color = st.selectbox(
        "Papel",
        ["Blanco", "Crema", "Rosa", "Lila", "Celeste", "Menta"]
    )

# ---------------- CONFIGURAR PAPEL ----------------

paper_colors = {
    "Blanco": "#FFFFFF",
    "Crema": "#FFF8E9",
    "Rosa": "#FCE8EF",
    "Lila": "#F0E9FA",
    "Celeste": "#E8F4FC",
    "Menta": "#E8F5ED"
}

paper = paper_colors[background_color]

# ---------------- CONFIGURAR HERRAMIENTA ----------------

drawing_modes = {
    "Lápiz": "freedraw",
    "Pincel": "freedraw",
    "Marcador": "freedraw",
    "Borrador": "freedraw",
    "Línea": "line",
    "Rectángulo": "rect",
    "Círculo": "circle"
}

drawing_mode = drawing_modes[tool]

if tool == "Pincel":
    brush_size = min(30, brush_size + 3)

if tool == "Marcador":
    brush_size = min(30, brush_size + 8)

if tool == "Borrador":
    selected_color = paper

# ---------------- TABLERO ----------------

st.markdown("### Mi tablero")

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.3)",
    stroke_width=brush_size,
    stroke_color=selected_color,
    background_color=paper,
    height=450,
    width=850,
    drawing_mode=drawing_mode,
    display_toolbar=True,
    key=f"creative_canvas_{st.session_state.canvas_version}"
)

# ---------------- GUARDAR Y DESCARGAR ----------------

if canvas_result.image_data is not None:
    image = Image.fromarray(canvas_result.image_data.astype("uint8"))
    image = image.convert("RGB")

    st.session_state.last_image = image

st.divider()
st.markdown("### Guardar mi creación")

if st.session_state.last_image is not None:

    buffer = io.BytesIO()
    st.session_state.last_image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    st.download_button(
        label="⬇️ Descargar mi dibujo en PNG",
        data=image_bytes,
        file_name="mi_creacion.png",
        mime="image/png",
        use_container_width=True
    )

else:
    st.info("Cuando realices un dibujo, podrás descargarlo aquí.")

st.markdown(
    "<p style='text-align:center; color:#A49AAA; font-size:12px;'>"
    "Creative Notebook · Tu espacio creativo"
    "</p>",
    unsafe_allow_html=True
)
