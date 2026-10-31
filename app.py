
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
from io import BytesIO
import numpy as np

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Creative Notebook",
    page_icon="✿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fceef4, #f3efff, #eaf6f5);
}

.block-container {
    max-width: 1600px;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.hero {
    background: linear-gradient(110deg, #f9dce9, #e8dcf8, #dcefed);
    border: 1px solid rgba(255,255,255,.8);
    border-radius: 24px;
    padding: 17px 25px;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 5px 18px rgba(120,100,130,.07);
}

.hero h1 {
    color: #655879;
    font-size: 2rem;
    margin: 0;
    font-weight: 800;
}

.hero p {
    color: #81758d;
    margin: 3px 0 0 0;
    font-size: .95rem;
}

.intro-panel {
    background: rgba(255,255,255,.75);
    border: 1px solid #ffffff;
    border-radius: 22px;
    padding: 22px;
    color: #766b80;
    min-height: 650px;
}

.intro-panel h3 {
    color: #77658c;
    font-size: 1.05rem;
    margin-top: 16px;
}

.intro-panel p {
    color: #81788a;
    font-size: .9rem;
    line-height: 1.65;
}

.intro-panel hr {
    border: none;
    border-top: 1px solid #eadfeb;
    margin: 19px 0;
}

.workspace {
    background: rgba(255,255,255,.45);
    border: 1px solid rgba(255,255,255,.8);
    border-radius: 22px;
    padding: 14px;
}

.canvas-card {
    background: white;
    border-radius: 15px;
    padding: 8px;
    border: 1px solid #eee5f0;
    box-shadow: 0 4px 14px rgba(100,80,120,.07);
}

div.stButton > button {
    border-radius: 13px;
    border: 1px solid #eaddec;
    background: #fffafd;
    color: #756582;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    min-height: 39px;
    transition: .2s;
}

div.stButton > button:hover {
    background: #f5e8f2;
    border-color: #d8c4df;
    color: #655477;
}

div[data-testid="stPopover"] button {
    border-radius: 12px;
    background: #fffafd;
    border: 1px solid #eaddec;
    color: #756582;
}

div[data-testid="stDownloadButton"] button {
    border-radius: 13px;
    background: #e9f4ed;
    border: 1px solid #d4e8da;
    color: #587a65;
    font-weight: 700;
    width: 100%;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px;
}

.tool-label {
    color: #81758d;
    font-weight: 800;
    font-size: .82rem;
    text-align: center;
    margin-bottom: 8px;
}

.small-note {
    color: #9a8da1;
    font-size: .76rem;
    text-align: center;
}

@media (max-width: 850px) {
    .hero h1 {
        font-size: 1.6rem;
    }
    .intro-panel {
        min-height: auto;
    }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>✿ Creative Notebook</h1>
    <p>Your little creative space · Dibuja, experimenta y crea.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ESTADOS
# --------------------------------------------------

defaults = {
    "canvas_version": 0,
    "saved_drawing": None,
    "selected_color": "#514A7E",
    "paper_color": "#FFFFFF",
    "paper_type": "Lisa",
    "paper_size": "A4 horizontal",
    "tool": "Lápiz",
    "brush_size": 6,
    "opacity": 100,
    "finished": False,
    "final_image": None,
    "last_config": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# FUNCIONES
# --------------------------------------------------

def change_canvas():
    st.session_state.canvas_version += 1
    st.session_state.saved_drawing = None
    st.session_state.finished = False
    st.session_state.final_image = None


def make_paper(color, pattern, width, height):
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)

    pattern_color = "#E8E2EB"

    if pattern == "Cuadrícula":
        for x in range(0, width, 30):
            draw.line((x, 0, x, height), fill=pattern_color, width=1)
        for y in range(0, height, 30):
            draw.line((0, y, width, y), fill=pattern_color, width=1)

    elif pattern == "Puntos":
        for x in range(15, width, 25):
            for y in range(15, height, 25):
                draw.ellipse((x, y, x+2, y+2), fill=pattern_color)

    elif pattern == "Rayado":
        for y in range(35, height, 30):
            draw.line((0, y, width, y), fill=pattern_color, width=1)

    return image


def export_png(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def blend_color(foreground, background, alpha):
    fg = np.array(Image.new("RGB", (1, 1), foreground)).astype(float)
    bg = np.array(Image.new("RGB", (1, 1), background)).astype(float)
    result = fg * alpha + bg * (1 - alpha)
    return tuple(result[0, 0].astype(int))


# --------------------------------------------------
# DISTRIBUCIÓN PRINCIPAL
# --------------------------------------------------

intro_column, workspace_column = st.columns(
    [2.5, 7.5],
    gap="medium"
)

# --------------------------------------------------
# PANEL IZQUIERDO: INTRODUCCIÓN
# --------------------------------------------------

with intro_column:

    with st.container(height=680, border=False):

        st.markdown("""
        <div class="intro-panel">

            <div style="text-align:center;font-size:3.5rem;">
                🌷
            </div>

            <h3 style="text-align:center;">
                ¡Bienvenida!
            </h3>

            <p style="text-align:center;">
                Este es tu pequeño rincón creativo.
                Un espacio para imaginar, experimentar
                y convertir tus ideas en ilustraciones.
            </p>

            <hr>

            <h3>✿ Sobre Creative Notebook</h3>

            <p>
                Creative Notebook es una libreta digital
                diseñada para que puedas dibujar libremente,
                explorar colores y crear sin límites.
            </p>

            <hr>

            <h3>♡ ¿Qué puedes hacer?</h3>

            <p>✏️ Dibujar con diferentes herramientas.</p>
            <p>🎨 Explorar una paleta de colores.</p>
            <p>📄 Personalizar el tipo y color del papel.</p>
            <p>✨ Crear ilustraciones y guardar tus trabajos.</p>

            <hr>

            <h3>✦ Un pequeño consejo</h3>

            <p>
                No tengas miedo de probar. Combina colores,
                juega con las formas y deja que tu imaginación
                encuentre su propio camino.
            </p>

            <div style="text-align:center;font-size:1.8rem;padding-top:12px;">
                ♡ ✿ ♡
            </div>

            <p style="text-align:center;font-size:.75rem;">
                Your imagination starts here.
            </p>

        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# PANEL DERECHO: ESPACIO DE TRABAJO
# --------------------------------------------------

with workspace_column:

    st.markdown('<div class="tool-label">TU ESPACIO DE TRABAJO</div>',
                unsafe_allow_html=True)

    # --------------------------------------------------
    # BOTONES SUPERIORES
    # --------------------------------------------------

    action1, action2, action3 = st.columns([1, 1, 1.3])

    with action1:
        if st.button("🧹 Borrar hoja", use_container_width=True):
            change_canvas()
            st.rerun()

    with action2:
        download_placeholder = st.empty()

    with action3:
        if st.button("✨ Terminar dibujo", use_container_width=True):
            st.session_state.finished = True
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # TAMAÑOS DEL TABLERO
    # --------------------------------------------------

    paper_sizes = {
        "A4 horizontal": (790, 560),
        "A4 vertical": (400, 560),
        "A3 horizontal": (795, 560),
        "Cuadrada": (560, 560),
        "Panorámica": (900, 478),
        "Libre": (850, 530)
    }

    width, height = paper_sizes[st.session_state.paper_size]

    config = (
        st.session_state.paper_size,
        st.session_state.paper_color,
        st.session_state.paper_type
    )

    if st.session_state.last_config != config:
        if st.session_state.last_config is not None:
            st.session_state.canvas_version += 1
        st.session_state.last_config = config

    paper_image = make_paper(
        st.session_state.paper_color,
        st.session_state.paper_type,
        width,
        height
    )

    # --------------------------------------------------
    # HERRAMIENTAS + TABLERO + AJUSTES
    # --------------------------------------------------

    left_tools, canvas_area, right_tools = st.columns(
        [0.85, 8, 0.95],
        gap="small",
        vertical_alignment="center"
    )

    # --------------------------------------------------
    # HERRAMIENTAS IZQUIERDAS
    # --------------------------------------------------

    tools = [
        ("✏️", "Lápiz"),
        ("🖌️", "Pincel"),
        ("🖍️", "Marcador"),
        ("➖", "Línea"),
        ("▭", "Rectángulo"),
        ("◯", "Círculo"),
        ("⬠", "Polígono"),
        ("T", "Texto"),
        ("🧽", "Borrador")
    ]

    with left_tools:
        st.markdown('<div class="tool-label">HERRAMIENTAS</div>',
                    unsafe_allow_html=True)

        for icon, name in tools:
            if st.button(
                icon,
                key=f"tool_{name}",
                help=name,
                use_container_width=True
            ):
                st.session_state.tool = name
                st.rerun()

        st.markdown(
            f"<p class='small-note'>Activo: {st.session_state.tool}</p>",
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # TABLERO CENTRAL
    # --------------------------------------------------

    with canvas_area:

        st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

        drawing_mode = {
            "Lápiz": "freedraw",
            "Pincel": "freedraw",
            "Marcador": "freedraw",
            "Línea": "line",
            "Rectángulo": "rect",
            "Círculo": "circle",
            "Polígono": "polygon",
            "Texto": "text",
            "Borrador": "freedraw"
        }

        stroke_color = st.session_state.selected_color

        if st.session_state.tool == "Borrador":
            stroke_color = st.session_state.paper_color

        elif st.session_state.tool == "Marcador":
            stroke_color = blend_color(
                st.session_state.selected_color,
                st.session_state.paper_color,
                0.45
            )

        elif st.session_state.tool == "Pincel":
            stroke_color = st.session_state.selected_color

        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=st.session_state.brush_size,
            stroke_color=stroke_color,
            background_image=paper_image,
            initial_drawing=st.session_state.saved_drawing,
            update_streamlit=True,
            height=height,
            width=width,
            drawing_mode=drawing_mode[st.session_state.tool],
            display_toolbar=False,
            key=f"canvas_{st.session_state.canvas_version}"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if canvas_result.json_data is not None:
            st.session_state.saved_drawing = canvas_result.json_data

        # Imagen actual para descargar
        if canvas_result.image_data is not None:
            current_image = Image.fromarray(
                canvas_result.image_data.astype("uint8")
            ).convert("RGB")
        else:
            current_image = paper_image.copy()

        download_placeholder.download_button(
            label="⬇️ Guardar imagen",
            data=export_png(current_image),
            file_name="creative_notebook.png",
            mime="image/png",
            use_container_width=True,
            key="top_download"
        )

        if st.session_state.finished:
            st.success("¡Tu creación está lista! Puedes guardar tu ilustración.")

    # --------------------------------------------------
    # AJUSTES DERECHOS
    # --------------------------------------------------

    with right_tools:

        st.markdown('<div class="tool-label">AJUSTES</div>',
                    unsafe_allow_html=True)

        with st.popover("⚙️", use_container_width=True):
            st.markdown("### Ajustes del trazo")

            st.session_state.brush_size = st.slider(
                "Grosor",
                min_value=1,
                max_value=40,
                value=st.session_state.brush_size
            )

            st.session_state.opacity = st.slider(
                "Opacidad",
                min_value=10,
                max_value=100,
                value=st.session_state.opacity
            )

        with st.popover("🎨", use_container_width=True):
            st.markdown("### Paleta de colores")

            palette = {
                "Rosa": "#EBA6C5",
                "Durazno": "#F4B99B",
                "Amarillo": "#F2D47C",
                "Menta": "#9BCDB9",
                "Celeste": "#9CCBEA",
                "Lavanda": "#B9A6DE",
                "Lila": "#D5A9D8",
                "Coral": "#E98D85",
                "Carbón": "#33313A",
                "Blanco": "#FFFFFF"
            }

            for name, color in palette.items():
                if st.button(
                    f"● {name}",
                    key=f"color_{name}",
                    use_container_width=True
                ):
                    st.session_state.selected_color = color
                    st.rerun()

            st.markdown("Color personalizado")

            st.session_state.selected_color = st.color_picker(
                "Elige un color",
                st.session_state.selected_color,
                label_visibility="collapsed"
            )

        with st.popover("📄", use_container_width=True):
            st.markdown("### Personalizar papel")

            new_size = st.selectbox(
                "Tamaño",
                list(paper_sizes.keys()),
                index=list(paper_sizes.keys()).index(
                    st.session_state.paper_size
                )
            )

            new_pattern = st.selectbox(
                "Tipo de papel",
                ["Lisa", "Cuadrícula", "Puntos", "Rayado"],
                index=["Lisa", "Cuadrícula", "Puntos", "Rayado"].index(
                    st.session_state.paper_type
                )
            )

            new_color = st.color_picker(
                "Color del papel",
                st.session_state.paper_color
            )

            if st.button("Aplicar cambios", use_container_width=True):
                st.session_state.paper_size = new_size
                st.session_state.paper_type = new_pattern
                st.session_state.paper_color = new_color
                st.rerun()

        st.markdown(
            "<p class='small-note'>Trazo · Color · Papel</p>",
            unsafe_allow_html=True
        )

# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown("""
<p style="
    text-align:center;
    color:#9a8da1;
    font-size:.75rem;
    padding-top:12px;
">
    Made with ♡ · Creative Notebook
</p>
""", unsafe_allow_html=True)
