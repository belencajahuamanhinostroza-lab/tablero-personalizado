
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from io import BytesIO
import numpy as np

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Creative Notebook",
    page_icon="✿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 650

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 10%, #FCEAF1 0%, transparent 35%),
        radial-gradient(ellipse at 90% 20%, #EAE8FA 0%, transparent 35%),
        radial-gradient(ellipse at 50% 100%, #E6F5F1 0%, transparent 45%),
        #F8F6FA;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1600px !important;
    padding: 1.2rem 1.5rem 2rem 1.5rem !important;
}

[data-testid="stVerticalBlock"] {
    gap: .65rem;
}

/* ENCABEZADO */

.hero {
    background: linear-gradient(
        110deg,
        #F8DCE8,
        #FBEBD3,
        #E9E3FA
    );
    border: 1px solid white;
    border-radius: 20px;
    padding: 17px 25px;
    margin-bottom: 20px;
}

.hero h1 {
    color: #51485F;
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #82768A;
    margin: 0;
    font-size: .9rem;
}

/* TÍTULO DE SECCIÓN */

.section-label {
    color: #756982;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 3px;
}

/* CONFIGURACIONES */

.stSelectbox label,
.stSlider label {
    color: #756982 !important;
    font-weight: 700 !important;
    font-size: .88rem !important;
}

.stSelectbox > div > div {
    border-radius: 11px;
    border-color: #E9DFED;
    background: rgba(255,255,255,.95);
}

/* LIENZO */

.canvas-heading {
    text-align: center;
    color: #796D83;
    font-weight: 800;
    padding: 12px;
    background: linear-gradient(90deg, #FFF8FC, #F8F4FF);
    border: 1px solid #E9DFED;
    border-radius: 15px 15px 0 0;
    margin-top: 8px;
}

.canvas-frame {
    background: #FFFFFF;
    border: 1px solid #E9DFED;
    border-top: none;
    border-radius: 0 0 15px 15px;
    padding: 10px;
    box-shadow: 0 7px 25px rgba(90,70,110,.06);
    width: 100%;
    box-sizing: border-box;
}

/* BOTONES */

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid #E9DFED;
    background: rgba(255,255,255,.95);
    color: #63566E;
    font-weight: 700;
    min-height: 42px;
    transition: .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #F6ECFA;
    border-color: #D8C1E5;
    color: #63566E;
}

/* PIE */

.footer {
    text-align: center;
    color: #A397AA;
    font-size: 12px;
    padding-top: 18px;
}

footer, #MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# ESTADOS
# =====================================================

defaults = {
    "canvas_version": 0,
    "saved_drawing": None,
    "selected_color": "#514A7E",
    "paper_color": "#FFFFFF",
    "tool": "Lápiz",
    "brush_size": 6
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# FUNCIONES
# =====================================================

def make_paper(color):
    return Image.new(
        "RGB",
        (CANVAS_WIDTH, CANVAS_HEIGHT),
        color
    )


def export_png(image_array):
    image = Image.fromarray(
        np.asarray(image_array).astype("uint8")
    ).convert("RGBA")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()


def clear_canvas():
    st.session_state.saved_drawing = None
    st.session_state.canvas_version += 1


# =====================================================
# ENCABEZADO
# =====================================================

st.markdown("""
<div class="hero">
    <h1>✿ Creative Notebook</h1>
    <p>Your little creative space · Dibuja, experimenta y crea.</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# ÁREA DE TRABAJO
# =====================================================

st.markdown(
    '<div class="section-label">✦ Tu espacio de creación</div>',
    unsafe_allow_html=True
)


# =====================================================
# CONFIGURACIONES
# =====================================================

config1, config2, config3, config4, config5 = st.columns(
    [1.2, 1.5, 1.8, 2.0, 1.3],
    gap="medium",
    vertical_alignment="bottom"
)

# HERRAMIENTA

with config1:

    tool_options = ["Lápiz", "Borrador"]

    st.session_state.tool = st.selectbox(
        "Herramienta",
        tool_options,
        index=tool_options.index(st.session_state.tool),
        key="tool_selector"
    )

# COLOR DEL TRAZO

with config2:

    palette = {
        "Morado": "#514A7E",
        "Rosa": "#F19AB5",
        "Durazno": "#F5B99B",
        "Amarillo": "#F4D477",
        "Menta": "#A8DCC5",
        "Celeste": "#9CCFE5",
        "Lavanda": "#BDB0E8",
        "Coral": "#E98282"
    }

    color_names = list(palette.keys())

    color_index = (
        list(palette.values()).index(st.session_state.selected_color)
        if st.session_state.selected_color in palette.values()
        else 0
    )

    selected_name = st.selectbox(
        "Color",
        color_names,
        index=color_index,
        key="color_selector"
    )

    st.session_state.selected_color = palette[selected_name]

# COLOR DEL PAPEL

with config3:

    paper_options = {
        "Blanco": "#FFFFFF",
        "Crema": "#FFF9EE",
        "Rosa suave": "#FFF0F4",
        "Lila suave": "#F5F0FF",
        "Celeste suave": "#EEF8FF",
        "Verde menta": "#F0FAF4"
    }

    paper_names = list(paper_options.keys())

    paper_index = (
        list(paper_options.values()).index(st.session_state.paper_color)
        if st.session_state.paper_color in paper_options.values()
        else 0
    )

    paper_name = st.selectbox(
        "Color del papel",
        paper_names,
        index=paper_index,
        key="paper_selector"
    )

    new_paper_color = paper_options[paper_name]

    if new_paper_color != st.session_state.paper_color:
        st.session_state.paper_color = new_paper_color
        clear_canvas()
        st.rerun()

# GROSOR DEL TRAZO

with config4:

    st.session_state.brush_size = st.slider(
        "Grosor del trazo",
        min_value=1,
        max_value=25,
        value=st.session_state.brush_size,
        key="brush_slider"
    )

# LIMPIAR

with config5:

    if st.button(
        "🗑️ Limpiar",
        use_container_width=True,
        key="clear_button"
    ):
        clear_canvas()
        st.rerun()


# =====================================================
# TABLERO DE DIBUJO
# =====================================================

paper_image = make_paper(
    st.session_state.paper_color
)

if st.session_state.tool == "Borrador":
    stroke = st.session_state.paper_color
else:
    stroke = st.session_state.selected_color


st.markdown("""
<div class="canvas-heading">
    ✿ Mi hoja de dibujo
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="canvas-frame">', unsafe_allow_html=True)

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=st.session_state.brush_size,
    stroke_color=stroke,
    background_image=paper_image,
    height=CANVAS_HEIGHT,
    width=CANVAS_WIDTH,
    drawing_mode="freedraw",
    initial_drawing=st.session_state.saved_drawing,
    update_streamlit=True,
    return_image_data=True,
    key=f"creative_canvas_{st.session_state.canvas_version}"
)

st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# RECUPERAR DIBUJO
# =====================================================

if canvas_result.json_data is not None:
    st.session_state.saved_drawing = canvas_result.json_data

current_image = None

try:
    current_image = canvas_result.image_data
except RuntimeError:
    current_image = None

if current_image is not None:
    current_image = np.asarray(current_image).astype("uint8")
else:
    current_image = np.asarray(
        paper_image.convert("RGBA")
    )


# =====================================================
# DESCARGAR
# =====================================================

st.download_button(
    "⬇️ Guardar mi dibujo",
    data=export_png(current_image),
    file_name="creative_notebook.png",
    mime="image/png",
    use_container_width=True,
    key="download_button"
)


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("""
<div class="footer">
    Creative Notebook · Un espacio para crear a tu manera ✿
</div>
""", unsafe_allow_html=True)
