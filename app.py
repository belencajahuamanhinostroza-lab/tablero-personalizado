
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
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

# =====================================================
# OPCIONES DE HOJA
# =====================================================

PAPER_SIZES = {
    "A4 horizontal": (900, 640),
    "A4 vertical": (640, 900),
    "A5 horizontal": (760, 540),
    "Cuadrada": (700, 700),
    "Panorámica": (1100, 550)
}

PAPER_COLORS = {
    "Blanco": "#FFFFFF",
    "Crema": "#FFF9EE",
    "Rosa suave": "#FFF0F4",
    "Lila suave": "#F5F0FF",
    "Celeste suave": "#EEF8FF",
    "Verde menta": "#F0FAF4"
}

PALETTE = {
    "Morado": "#514A7E",
    "Rosa": "#F19AB5",
    "Durazno": "#F5B99B",
    "Amarillo": "#F4D477",
    "Menta": "#A8DCC5",
    "Celeste": "#9CCFE5",
    "Lavanda": "#BDB0E8",
    "Coral": "#E98282",
    "Rojo": "#D85D68",
    "Azul": "#477DB5",
    "Verde": "#579B78",
    "Negro": "#222222"
}

PAPER_PATTERNS = [
    "Lisa",
    "Punteada",
    "Cuadriculada",
    "Rayada",
    "Líneas horizontales",
    "Hexagonal"
]

TOOLS = [
    "Lápiz",
    "Borrador",
    "Línea",
    "Círculo",
    "Rectángulo",
    "Triángulo / Polígono"
]

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
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
    padding: 1.2rem 1.3rem 2rem 1.3rem !important;
}

[data-testid="stVerticalBlock"] {
    gap: .65rem;
}

/* CABECERA */

.hero {
    background: linear-gradient(110deg, #F8DCE8, #FBEBD3, #E9E3FA);
    border: 1px solid white;
    border-radius: 20px;
    padding: 16px 24px;
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

/* PANEL IZQUIERDO */

.tools-panel {
    background: linear-gradient(145deg, #FFF0F5, #F2EAFF, #E8F8F2);
    border: 1px solid white;
    border-radius: 18px;
    padding: 15px 13px;
    box-shadow: 0 7px 25px rgba(90,70,110,.06);
}

.tools-title {
    color: #65566F;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 12px;
}

.tool-section {
    color: #756982;
    font-weight: 800;
    font-size: .88rem;
    margin-top: 12px;
    margin-bottom: 3px;
}

.stSelectbox label,
.stSlider label {
    color: #756982 !important;
    font-weight: 700 !important;
    font-size: .83rem !important;
}

.stSelectbox > div > div {
    border-radius: 10px;
    border-color: #E9DFED;
    background: rgba(255,255,255,.95);
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

/* LIENZO */

.canvas-heading {
    text-align: center;
    color: #796D83;
    font-weight: 800;
    padding: 12px;
    background: linear-gradient(90deg, #FFF8FC, #F8F4FF);
    border: 1px solid #E9DFED;
    border-radius: 15px 15px 0 0;
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

.footer {
    text-align: center;
    color: #A397AA;
    font-size: 12px;
    padding-top: 20px;
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
    "brush_size": 6,
    "paper_pattern": "Lisa",
    "paper_size": "A4 horizontal"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# FUNCIONES
# =====================================================

def clear_canvas():
    st.session_state.saved_drawing = None
    st.session_state.canvas_version += 1


def make_paper(color, pattern, width, height):
    """Genera una hoja con el patrón seleccionado."""

    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)

    pattern_color = "#E5DDEB"
    spacing = 25

    if pattern == "Lisa":
        return image

    elif pattern == "Punteada":
        for x in range(12, width, spacing):
            for y in range(12, height, spacing):
                draw.ellipse(
                    (x-1, y-1, x+1, y+1),
                    fill=pattern_color
                )

    elif pattern == "Cuadriculada":
        for x in range(0, width, spacing):
            draw.line(
                (x, 0, x, height),
                fill=pattern_color,
                width=1
            )

        for y in range(0, height, spacing):
            draw.line(
                (0, y, width, y),
                fill=pattern_color,
                width=1
            )

    elif pattern == "Rayada":
        for y in range(25, height, spacing):
            draw.line(
                (0, y, width, y),
                fill=pattern_color,
                width=1
            )

        # Margen vertical
        draw.line(
            (45, 0, 45, height),
            fill="#E9B9C7",
            width=2
        )

    elif pattern == "Líneas horizontales":
        for y in range(25, height, spacing):
            draw.line(
                (0, y, width, y),
                fill=pattern_color,
                width=1
            )

    elif pattern == "Hexagonal":
        hex_width = 28
        hex_height = 24

        for row, y in enumerate(range(-hex_height, height + hex_height, hex_height)):
            offset = (hex_width // 2) if row % 2 else 0

            for x in range(-hex_width, width + hex_width, hex_width):
                cx = x + offset
                cy = y

                points = [
                    (cx + hex_width//2, cy),
                    (cx + hex_width, cy + hex_height//4),
                    (cx + hex_width, cy + 3*hex_height//4),
                    (cx + hex_width//2, cy + hex_height),
                    (cx, cy + 3*hex_height//4),
                    (cx, cy + hex_height//4)
                ]

                draw.line(
                    points + [points[0]],
                    fill=pattern_color,
                    width=1
                )

    return image


def export_png(image_array):
    image = Image.fromarray(
        np.asarray(image_array).astype("uint8")
    ).convert("RGBA")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()


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
# DISTRIBUCIÓN PRINCIPAL
# =====================================================

tools_column, canvas_column = st.columns(
    [2.2, 7.8],
    gap="large",
    vertical_alignment="top"
)

# =====================================================
# PANEL DE HERRAMIENTAS
# =====================================================

with tools_column:

    st.markdown("""
    <div class="tools-panel">
        <div class="tools-title">✿ Herramientas</div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # INSTRUMENTO
    # -------------------------------------------------

    st.markdown(
        '<div class="tool-section">✏️ Instrumento</div>',
        unsafe_allow_html=True
    )

    selected_tool = st.selectbox(
        "Herramienta",
        TOOLS,
        index=TOOLS.index(st.session_state.tool),
        label_visibility="collapsed",
        key="tool_selector"
    )

    st.session_state.tool = selected_tool

    # -------------------------------------------------
    # GROSOR
    # -------------------------------------------------

    st.markdown(
        '<div class="tool-section">〰️ Grosor del trazo</div>',
        unsafe_allow_html=True
    )

    st.session_state.brush_size = st.slider(
        "Tamaño",
        min_value=1,
        max_value=30,
        value=st.session_state.brush_size,
        label_visibility="collapsed",
        key="brush_slider"
    )

    # -------------------------------------------------
    # COLOR
    # -------------------------------------------------

    st.markdown(
        '<div class="tool-section">🎨 Color del trazo</div>',
        unsafe_allow_html=True
    )

    color_names = list(PALETTE.keys())

    current_color_index = (
        list(PALETTE.values()).index(st.session_state.selected_color)
        if st.session_state.selected_color in PALETTE.values()
        else 0
    )

    selected_name = st.selectbox(
        "Color",
        color_names,
        index=current_color_index,
        label_visibility="collapsed",
        key="color_selector"
    )

    st.session_state.selected_color = PALETTE[selected_name]

    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:8px;
                    padding:6px 0;color:#756982;font-size:12px;">
            Color seleccionado:
            <div style="width:22px;height:22px;border-radius:50%;
                        background:{st.session_state.selected_color};
                        border:2px solid white;
                        box-shadow:0 1px 5px #C9BDCE;">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # TIPO DE HOJA
    # -------------------------------------------------

    st.markdown(
        '<div class="tool-section">📄 Tipo de hoja</div>',
        unsafe_allow_html=True
    )

    new_pattern = st.selectbox(
        "Patrón",
        PAPER_PATTERNS,
        index=PAPER_PATTERNS.index(st.session_state.paper_pattern),
        label_visibility="collapsed",
        key="pattern_selector"
    )

    if new_pattern != st.session_state.paper_pattern:
        st.session_state.paper_pattern = new_pattern
        clear_canvas()
        st.rerun()

    # -------------------------------------------------
    # TAMAÑO DE HOJA
    # -------------------------------------------------

    st.markdown(
        '<div class="tool-section">📐 Tamaño de hoja</div>',
        unsafe_allow_html=True
    )

    new_size = st.selectbox(
        "Formato",
        list(PAPER_SIZES.keys()),
        index=list(PAPER_SIZES.keys()).index(st.session_state.paper_size),
        label_visibility="collapsed",
        key="size_selector"
    )

    if new_size != st.session_state.paper_size:
        st.session_state.paper_size = new_size
        clear_canvas()
        st.rerun()

    # -------------------------------------------------
    # COLOR DEL PAPEL
    # -------------------------------------------------

    st.markdown(
        '<div class="tool-section">🖌️ Fondo del papel</div>',
        unsafe_allow_html=True
    )

    paper_names = list(PAPER_COLORS.keys())

    current_paper_index = (
        list(PAPER_COLORS.values()).index(st.session_state.paper_color)
        if st.session_state.paper_color in PAPER_COLORS.values()
        else 0
    )

    paper_name = st.selectbox(
        "Color de fondo",
        paper_names,
        index=current_paper_index,
        label_visibility="collapsed",
        key="paper_color_selector"
    )

    new_paper_color = PAPER_COLORS[paper_name]

    if new_paper_color != st.session_state.paper_color:
        st.session_state.paper_color = new_paper_color
        clear_canvas()
        st.rerun()

    # -------------------------------------------------
    # AYUDA DE HERRAMIENTAS
    # -------------------------------------------------

    with st.expander("ⓘ Cómo usar las formas"):

        st.markdown("""
        - **Lápiz:** dibuja libremente.
        - **Borrador:** pinta con el color base del papel.
        - **Línea:** arrastra para crear una línea recta.
        - **Círculo:** arrastra para crear una elipse.
        - **Rectángulo:** arrastra para crear un rectángulo.
        - **Triángulo / Polígono:** haz clic para marcar los vértices
          y cierra la figura según el comportamiento del lienzo.
        
        """)

# =====================================================
# LIENZO
# =====================================================

with canvas_column:

    canvas_width, canvas_height = PAPER_SIZES[
        st.session_state.paper_size
    ]

    paper_image = make_paper(
        st.session_state.paper_color,
        st.session_state.paper_pattern,
        canvas_width,
        canvas_height
    )

    # Modo de dibujo
    drawing_modes = {
        "Lápiz": "freedraw",
        "Borrador": "freedraw",
        "Línea": "line",
        "Círculo": "circle",
        "Rectángulo": "rect",
        "Triángulo / Polígono": "polygon"
    }

    drawing_mode = drawing_modes[st.session_state.tool]

    # Color del trazo
    if st.session_state.tool == "Borrador":
        stroke = st.session_state.paper_color
    else:
        stroke = st.session_state.selected_color

    st.markdown("""
    <div class="canvas-heading">
        ✿ Mi hoja de dibujo
    </div>
    """, unsafe_allow_html=True)

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=st.session_state.brush_size,
        stroke_color=stroke,
        background_image=paper_image,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        initial_drawing=st.session_state.saved_drawing,
        update_streamlit=True,
        return_image_data=True,
        key=f"creative_canvas_{st.session_state.canvas_version}"
    )

    # -------------------------------------------------
    # RECUPERAR DIBUJO
    # -------------------------------------------------

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

    # -------------------------------------------------
    # BOTONES
    # -------------------------------------------------

    clear_column, download_column = st.columns(2, gap="medium")

    with clear_column:

        if st.button(
            "🗑️ Limpiar hoja",
            use_container_width=True,
            key="clear_button"
        ):
            clear_canvas()
            st.rerun()

    with download_column:

        st.download_button(
            "⬇️ Guardar imagen",
            data=export_png(current_image),
            file_name="creative_notebook.png",
            mime="image/png",
            use_container_width=True,
            key="download_button"
        )

# =====================================================
# PIE
# =====================================================

st.markdown("""
<div class="footer">
    Creative Notebook · Un espacio para crear a tu manera ✿
</div>
""", unsafe_allow_html=True)
