
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
from io import BytesIO

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="Creative Notebook",
    page_icon="✿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# DISEÑO
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 10%, #FCEAF1, transparent 35%),
        radial-gradient(ellipse at 95% 15%, #EAE8FA, transparent 35%),
        radial-gradient(ellipse at 50% 100%, #E5F4EF, transparent 40%),
        #F9F7FA;
    min-height: 100vh;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 100% !important;
    padding: 1rem 2rem 1rem 2rem !important;
}

.hero {
    background: linear-gradient(110deg, #F8DCE8, #FBEBD3, #E9E3FA);
    border: 1px solid white;
    border-radius: 18px;
    padding: 12px 22px;
    margin-bottom: 12px;
}

.hero h1 {
    color: #51485F;
    font-size: 1.65rem;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #82768A;
    font-size: .85rem;
    margin: 0;
}

.toolbar {
    background: rgba(255,255,255,.92);
    border: 1px solid #E9E1ED;
    border-radius: 16px;
    padding: 10px 13px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(90,70,110,.05);
}

.canvas-area {
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(255,255,255,.55);
    border: 1px solid #E9E1ED;
    border-radius: 20px;
    padding: 14px;
    box-shadow: 0 6px 22px rgba(90,70,110,.05);
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 11px;
    border: 1px solid #E6DCEB;
    background: #FFFFFF;
    color: #5B5066;
    font-weight: 700;
    min-height: 39px;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #F6ECFA;
    border-color: #D5BCE3;
    color: #51445F;
}

.stPopover > button {
    border-radius: 11px;
    background: white;
    border: 1px solid #E6DCEB;
    color: #62566D;
    min-height: 39px;
}

[data-testid="stPopoverBody"] {
    background: #FFFCFF;
    border: 1px solid #E9DFED;
    border-radius: 16px;
}

div[data-testid="stHorizontalBlock"] {
    align-items: center;
}

footer, #MainMenu {
    visibility: hidden;
}

@media (max-width: 900px) {
    .block-container {
        padding: .6rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# ESTADOS
# ==================================================

defaults = {
    "canvas_version": 0,
    "saved_drawing": None,
    "selected_color": "#514A7E",
    "paper_color": "#FFFFFF",
    "paper_pattern": "Lisa",
    "tool": "Lápiz",
    "brush_size": 6,
    "opacity": 100
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# FUNCIONES
# ==================================================

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 520


def create_paper(color, pattern):
    """Genera una hoja horizontal con el patrón elegido."""

    paper = Image.new(
        "RGB",
        (CANVAS_WIDTH, CANVAS_HEIGHT),
        color
    )

    draw = ImageDraw.Draw(paper)
    pattern_color = "#DDE0E8"

    if pattern == "Cuadriculada":

        step = 28

        for x in range(0, CANVAS_WIDTH, step):
            draw.line(
                (x, 0, x, CANVAS_HEIGHT),
                fill=pattern_color,
                width=1
            )

        for y in range(0, CANVAS_HEIGHT, step):
            draw.line(
                (0, y, CANVAS_WIDTH, y),
                fill=pattern_color,
                width=1
            )

    elif pattern == "Punteada":

        step = 24

        for x in range(12, CANVAS_WIDTH, step):
            for y in range(12, CANVAS_HEIGHT, step):
                draw.ellipse(
                    (x-1, y-1, x+1, y+1),
                    fill=pattern_color
                )

    elif pattern == "Rayada":

        for y in range(35, CANVAS_HEIGHT, 35):
            draw.line(
                (0, y, CANVAS_WIDTH, y),
                fill=pattern_color,
                width=1
            )

    return paper


def make_png(image_data):
    """Convierte el resultado del lienzo en PNG."""

    image = Image.fromarray(image_data).convert("RGBA")

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return buffer.getvalue()


# ==================================================
# CABECERA
# ==================================================

st.markdown("""
<div class="hero">
    <h1>✿ Creative Notebook</h1>
    <p>Your little creative space · Dibuja, experimenta y crea.</p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# BARRA SUPERIOR: ACCIONES PRINCIPALES
# ==================================================

st.markdown('<div class="toolbar">', unsafe_allow_html=True)

top_left, top_middle, top_right = st.columns(
    [2.2, 2, 2.2]
)

with top_left:

    st.markdown("**✦ Acciones rápidas**")

with top_middle:

    st.caption("Deshacer y rehacer: controles sobre el lienzo")

with top_right:

    st.caption("Creative Notebook · Hoja horizontal")

# Placeholders para los botones que necesitan el resultado del lienzo
action_placeholder = st.empty()

st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# BARRA DE HERRAMIENTAS
# ==================================================

st.markdown('<div class="toolbar">', unsafe_allow_html=True)

tool_col, size_col, opacity_col, color_col, paper_col = st.columns(
    [2.1, 1.5, 1.5, 1.7, 1.7]
)

with tool_col:

    tool_options = [
        "✏️ Lápiz",
        "🖌️ Pincel",
        "🖍️ Marcador",
        "📏 Línea",
        "▭ Rectángulo",
        "⭕ Círculo",
        "⬡ Polígono",
        "• Punto",
        "T Texto",
        "🧽 Borrador"
    ]

    selected_tool = st.selectbox(
        "Herramienta",
        tool_options,
        index=tool_options.index(
            st.session_state.tool
        ) if st.session_state.tool in tool_options else 0
    )

    st.session_state.tool = selected_tool


with size_col:

    st.session_state.brush_size = st.slider(
        "Grosor",
        1,
        35,
        st.session_state.brush_size
    )


with opacity_col:

    st.session_state.opacity = st.slider(
        "Opacidad",
        10,
        100,
        st.session_state.opacity,
        step=5
    )


with color_col:

    st.session_state.selected_color = st.color_picker(
        "Color del trazo",
        st.session_state.selected_color,
        key="drawing_color"
    )


with paper_col:

    with st.popover("📄 Papel y formato", use_container_width=True):

        st.markdown("### Diseño de la hoja")

        paper_pattern = st.selectbox(
            "Tipo de papel",
            [
                "Lisa",
                "Cuadriculada",
                "Punteada",
                "Rayada"
            ],
            index=[
                "Lisa",
                "Cuadriculada",
                "Punteada",
                "Rayada"
            ].index(st.session_state.paper_pattern)
        )

        paper_colors = {
            "Blanco": "#FFFFFF",
            "Crema": "#FFF9EE",
            "Rosa pastel": "#FFF0F4",
            "Lila pastel": "#F5F0FF",
            "Celeste pastel": "#EEF8FF",
            "Menta": "#F0FAF4"
        }

        paper_name = st.selectbox(
            "Color de la hoja",
            list(paper_colors.keys()) + ["Personalizado"]
        )

        if paper_name == "Personalizado":
            paper_color = st.color_picker(
                "Elige tu color de papel",
                st.session_state.paper_color,
                key="paper_custom_color"
            )
        else:
            paper_color = paper_colors[paper_name]

        if st.button(
            "Aplicar papel",
            use_container_width=True
        ):
            st.session_state.paper_pattern = paper_pattern
            st.session_state.paper_color = paper_color

            # Cambia la versión para aplicar el nuevo fondo
            st.session_state.canvas_version += 1

            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# LIENZO CENTRAL
# ==================================================

st.markdown(
    '<div class="canvas-area">',
    unsafe_allow_html=True
)

tool_modes = {
    "✏️ Lápiz": "freedraw",
    "🖌️ Pincel": "freedraw",
    "🖍️ Marcador": "freedraw",
    "📏 Línea": "line",
    "▭ Rectángulo": "rect",
    "⭕ Círculo": "circle",
    "⬡ Polígono": "polygon",
    "• Punto": "point",
    "T Texto": "text",
    "🧽 Borrador": "freedraw"
}

stroke_color = st.session_state.selected_color
brush_size = st.session_state.brush_size
opacity = st.session_state.opacity

if st.session_state.tool == "✏️ Lápiz":
    brush_size = min(brush_size, 5)

elif st.session_state.tool == "🖌️ Pincel":
    brush_size = max(brush_size, 9)

elif st.session_state.tool == "🖍️ Marcador":
    brush_size = max(brush_size, 14)
    opacity = min(opacity, 45)

elif st.session_state.tool == "🧽 Borrador":
    stroke_color = st.session_state.paper_color
    opacity = 100

# Simulación de opacidad
def blend_colors(foreground, background, alpha):

    fg = tuple(
        int(foreground[i:i+2], 16)
        for i in (1, 3, 5)
    )

    bg = tuple(
        int(background[i:i+2], 16)
        for i in (1, 3, 5)
    )

    result = tuple(
        round(fg[i] * alpha / 100 + bg[i] * (1-alpha/100))
        for i in range(3)
    )

    return "#{:02X}{:02X}{:02X}".format(*result)


stroke_color = blend_colors(
    stroke_color,
    st.session_state.paper_color,
    opacity
)

paper = create_paper(
    st.session_state.paper_color,
    st.session_state.paper_pattern
)

canvas_result = st_canvas(
    fill_color=st.session_state.selected_color,
    stroke_width=brush_size,
    stroke_color=stroke_color,
    background_image=paper,
    background_image_fit="contain",
    height=CANVAS_HEIGHT,
    width=CANVAS_WIDTH,
    drawing_mode=tool_modes[st.session_state.tool],
    initial_drawing=st.session_state.saved_drawing,
    point_display_radius=4,
    update_streamlit=True,
    display_toolbar=True,
    return_image_data=True,
    key=f"creative_canvas_{st.session_state.canvas_version}"
)

st.markdown('</div>', unsafe_allow_html=True)

st.caption(
    "✿ Tu hoja horizontal está lista. "
    "Puedes deshacer, rehacer y editar tus trazos desde la barra del lienzo."
)


# ==================================================
# GUARDAR DIBUJO ACTUAL
# ==================================================

if canvas_result.json_data is not None:
    st.session_state.saved_drawing = canvas_result.json_data


# ==================================================
# BOTONES SUPERIORES
# ==================================================

with action_placeholder.container():

    btn_clear, btn_new, btn_save, btn_download = st.columns(
        [1.3, 1.3, 1.5, 1.7]
    )

    with btn_clear:

        if st.button(
            "🗑️ Borrar hoja",
            use_container_width=True
        ):
            st.session_state.saved_drawing = None
            st.session_state.canvas_version += 1
            st.rerun()

    with btn_new:

        if st.button(
            "✦ Nuevo tablero",
            use_container_width=True
        ):
            st.session_state.saved_drawing = None
            st.session_state.selected_color = "#514A7E"
            st.session_state.paper_color = "#FFFFFF"
            st.session_state.paper_pattern = "Lisa"
            st.session_state.tool = "✏️ Lápiz"
            st.session_state.canvas_version += 1
            st.rerun()

    with btn_save:

        if canvas_result.image_data is not None:

            st.download_button(
                "💾 Guardar imagen",
                data=make_png(canvas_result.image_data),
                file_name="mi_creative_notebook.png",
                mime="image/png",
                use_container_width=True
            )

    with btn_download:

        if canvas_result.image_data is not None:

            st.download_button(
                "⬇️ Descargar PNG",
                data=make_png(canvas_result.image_data),
                file_name="mi_dibujo.png",
                mime="image/png",
                use_container_width=True
            )


# ==================================================
# PIE
# ==================================================

st.markdown("""
<div style="text-align:center;color:#A397AA;
font-size:12px;padding-top:10px;">
Creative Notebook · Crea a tu manera ✿
</div>
""", unsafe_allow_html=True)
