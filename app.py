
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import numpy as np
import json

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Creative Notebook",
    page_icon="✿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #fce8f1 0%, transparent 30%),
        radial-gradient(circle at 90% 20%, #e9e3fa 0%, transparent 32%),
        linear-gradient(135deg, #fff9fc, #f5f0fb);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1600px;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="stVerticalBlock"] {
    gap: .45rem;
}

/* ENCABEZADO */
.hero {
    background: linear-gradient(110deg, #f7dce9, #e8e1f6);
    border: 1px solid #ead8eb;
    border-radius: 22px;
    padding: 18px 26px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.hero h1 {
    color: #756982;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #82758c;
    font-size: .9rem;
    margin: 4px 0 0 0;
}

.hero-decoration {
    color: #756982;
    font-size: 1.5rem;
}

/* PANEL DE BIENVENIDA */
.intro-panel {
    width: 100%;
    min-height: 620px;
    box-sizing: border-box;
    padding: 28px 18px;
    border-radius: 24px;
    background: rgba(255,255,255,.82);
    border: 1px solid #eaddec;
    text-align: center;
}

.intro-flower {
    font-size: 3.5rem;
    margin-bottom: 12px;
}

.intro-panel h2 {
    color: #756982;
    font-size: 1.7rem;
    margin: 0 0 18px 0;
}

.intro-description,
.intro-message {
    color: #777080;
    font-size: .95rem;
    line-height: 1.8;
}

.intro-panel hr {
    width: 75%;
    border: none;
    border-top: 1px solid #e8dce9;
    margin: 25px auto;
}

.intro-decoration {
    font-size: 1.8rem;
    color: #b69abf;
    margin-top: 25px;
}

.intro-footer {
    color: #a99bad;
    font-size: .75rem;
    margin-top: 15px;
    font-style: italic;
}

/* ESPACIO DE DIBUJO */
.canvas-card {
    background: rgba(255,255,255,.78);
    border: 1px solid #eaddec;
    border-radius: 20px;
    padding: 12px;
    overflow: hidden;
}

.section-label {
    color: #897b94;
    font-weight: 800;
    font-size: .85rem;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid #e4d5e9;
    background: #fffafd;
    color: #756982;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #c9afd4;
    color: #756982;
    background: #f8eff8;
}

[data-testid="stPopover"] button {
    border-radius: 12px;
}

div[data-testid="stColorPicker"] {
    width: 100%;
}

footer {
    display: none;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNCIONES
# ==========================================

def make_paper(color, pattern, width, height):
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)

    line_color = "#E8E1ED"

    if pattern == "Cuadriculado":
        for x in range(0, width, 25):
            draw.line((x, 0, x, height), fill=line_color, width=1)
        for y in range(0, height, 25):
            draw.line((0, y, width, y), fill=line_color, width=1)

    elif pattern == "Punteado":
        for x in range(10, width, 20):
            for y in range(10, height, 20):
                draw.ellipse((x, y, x + 2, y + 2), fill=line_color)

    elif pattern == "Rayado":
        for y in range(25, height, 28):
            draw.line((0, y, width, y), fill=line_color, width=1)

    return image


def export_png(image_array):
    image = Image.fromarray(
        np.uint8(image_array)
    ).convert("RGBA")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def blend(foreground, background, alpha):
    fg = tuple(
        int(foreground[i:i+2], 16)
        for i in (1, 3, 5)
    )
    bg = tuple(
        int(background[i:i+2], 16)
        for i in (1, 3, 5)
    )

    result = tuple(
        int(fg[i] * alpha + bg[i] * (1 - alpha))
        for i in range(3)
    )

    return "#%02x%02x%02x" % result


def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def add_text_to_image(image, content, color, size):
    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = load_font(size)

    x = image.width // 2
    y = image.height // 2

    draw.text(
        (x, y),
        content,
        fill=color,
        font=font,
        anchor="mm"
    )

    return image


# ==========================================
# ESTADO DE LA APLICACIÓN
# ==========================================

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
    "finish_requested": False,
    "text_content": "",
    "text_size": 30,
    "last_config": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def change_canvas():
    st.session_state.canvas_version += 1
    st.session_state.saved_drawing = None


# ==========================================
# ENCABEZADO
# ==========================================

st.markdown("""
<div class="hero">
    <div>
        <h1>✿ Creative Notebook</h1>
        <p>Your little creative space · Dibuja, experimenta y crea.</p>
    </div>
    <div class="hero-decoration">
        ♡ ✦ ✿
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# PANTALLA FINAL
# ==========================================

if st.session_state.finished:

    st.markdown(
        "<h2 style='text-align:center;color:#756982;'>"
        "¡Tu dibujo está listo! 🌷</h2>",
        unsafe_allow_html=True
    )

    if st.session_state.final_image is not None:
        st.image(
            st.session_state.final_image,
            use_container_width=True
        )

        buffer = BytesIO()
        st.session_state.final_image.save(
            buffer,
            format="PNG"
        )

        st.download_button(
            "⬇️ Descargar mi dibujo",
            data=buffer.getvalue(),
            file_name="creative_notebook.png",
            mime="image/png",
            use_container_width=True
        )

    if st.button("← Volver al cuaderno", use_container_width=True):
        st.session_state.finished = False
        st.session_state.final_image = None
        st.rerun()

    st.stop()


# ==========================================
# CONFIGURACIÓN DEL PAPEL
# ==========================================

paper_sizes = {
    "A4 horizontal": (790, 560),
    "A4 vertical": (400, 560),
    "A3 horizontal": (795, 560),
    "Cuadrada": (560, 560),
    "Panorámica": (900, 478),
    "Libre": (850, 530)
}

paper_width, paper_height = paper_sizes[
    st.session_state.paper_size
]

current_config = (
    st.session_state.paper_size,
    st.session_state.paper_type,
    st.session_state.paper_color
)

if st.session_state.last_config is None:
    st.session_state.last_config = current_config

elif st.session_state.last_config != current_config:
    st.session_state.last_config = current_config
    change_canvas()


# ==========================================
# COLUMNAS PRINCIPALES
# ==========================================

intro_column, workspace_column = st.columns(
    [2.4, 7.6],
    gap="medium"
)


# ==========================================
# PANEL IZQUIERDO CON SCROLL
# ==========================================

with intro_column:

    with st.container(height=680, border=False):

        st.markdown("""
        <div class="intro-panel">

            <div class="intro-flower">🌷</div>

            <h2>¡Bienvenida!</h2>

            <p class="intro-description">
                Este es tu pequeño rincón creativo,
                un espacio para imaginar, experimentar
                y dar vida a tus ideas.
            </p>

            <hr>

            <p class="intro-message">
                ✿ Dibuja a tu manera, explora colores
                y crea ilustraciones sin límites.
            </p>

            <div class="intro-decoration">
                ♡ ✿ ♡
            </div>

            <p class="intro-footer">
                Your imagination starts here.
            </p>

        </div>
        """, unsafe_allow_html=True)


# ==========================================
# ÁREA DE TRABAJO
# ==========================================

with workspace_column:

    st.markdown(
        '<p class="section-label">✿ TU ESPACIO DE CREACIÓN</p>',
        unsafe_allow_html=True
    )

    # --------------------------------------
    # ACCIONES SUPERIORES
    # --------------------------------------

    action1, action2, action3 = st.columns(3)

    with action1:
        if st.button("🗑️ Borrar hoja", use_container_width=True):
            change_canvas()
            st.rerun()

    with action2:
        st.caption("Tu dibujo se puede descargar en PNG.")

    with action3:
        if st.button("✓ Terminar dibujo", use_container_width=True):
            st.session_state.finish_requested = True

    st.write("")

    # --------------------------------------
    # HERRAMIENTAS Y LIENZO
    # --------------------------------------

    left_tools, canvas_area, right_tools = st.columns(
        [0.9, 8, 1.1],
        gap="small",
        vertical_alignment="center"
    )

    # --------------------------------------
    # HERRAMIENTAS IZQUIERDAS
    # --------------------------------------

    tool_modes = {
        "Lápiz": "freedraw",
        "Pincel": "freedraw",
        "Marcador": "freedraw",
        "Línea": "line",
        "Rectángulo": "rect",
        "Círculo": "circle",
        "Polígono": "polygon",
        "Borrador": "freedraw",
        "Texto": "transform"
    }

    with left_tools:

        st.markdown(
            '<p class="section-label">HERRAMIENTAS</p>',
            unsafe_allow_html=True
        )

        tool_options = [
            ("✏️", "Lápiz"),
            ("🖌️", "Pincel"),
            ("🖍️", "Marcador"),
            ("╱", "Línea"),
            ("▭", "Rectángulo"),
            ("◯", "Círculo"),
            ("⬡", "Polígono"),
            ("⌫", "Borrador"),
            ("T", "Texto")
        ]

        for symbol, tool_name in tool_options:
            if st.button(
                f"{symbol}",
                key=f"tool_{tool_name}",
                help=tool_name,
                use_container_width=True
            ):
                st.session_state.tool = tool_name

        st.caption(f"Seleccionado: {st.session_state.tool}")

    # --------------------------------------
    # LIENZO
    # --------------------------------------

    with canvas_area:

        st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

        paper_image = make_paper(
            st.session_state.paper_color,
            st.session_state.paper_type,
            paper_width,
            paper_height
        )

        tool = st.session_state.tool

        stroke_color = st.session_state.selected_color
        brush_size = st.session_state.brush_size

        if tool == "Borrador":
            stroke_color = st.session_state.paper_color

        if tool == "Marcador":
            stroke_color = blend(
                st.session_state.selected_color,
                st.session_state.paper_color,
                0.35
            )

        if tool == "Pincel":
            brush_size = max(brush_size, 12)

        if tool == "Texto":
            brush_size = 1

        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.0)",
            stroke_width=brush_size,
            stroke_color=stroke_color,
            background_image=paper_image,
            height=paper_height,
            width=paper_width,
            drawing_mode=tool_modes[tool],
            point_display_radius=4,
            initial_drawing=st.session_state.saved_drawing,
            update_streamlit=True,
            key=f"creative_canvas_{st.session_state.canvas_version}"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Guardar los trazos actuales
        if canvas_result.json_data is not None:
            st.session_state.saved_drawing = canvas_result.json_data

        # Texto: se incorpora a la imagen final
        if tool == "Texto":

            st.info(
                "Para añadir texto, escribe el contenido aquí. "
                "Se colocará en el centro de la hoja al guardar."
            )

            st.session_state.text_content = st.text_input(
                "Texto para tu dibujo",
                value=st.session_state.text_content,
                key="canvas_text_input"
            )

            st.session_state.text_size = st.slider(
                "Tamaño del texto",
                12,
                80,
                st.session_state.text_size,
                key="canvas_text_size"
            )

        # Imagen actual
        current_image = None

        if canvas_result.image_data is not None:
            current_image = Image.fromarray(
                np.uint8(canvas_result.image_data)
            ).convert("RGBA")

        # ----------------------------------
        # DESCARGAR IMAGEN
        # ----------------------------------

        if current_image is not None:

            download_image = current_image.copy()

            if (
                st.session_state.tool == "Texto"
                and st.session_state.text_content.strip()
            ):
                download_image = add_text_to_image(
                    download_image,
                    st.session_state.text_content,
                    st.session_state.selected_color,
                    st.session_state.text_size
                )

            image_buffer = BytesIO()
            download_image.save(image_buffer, format="PNG")

            st.download_button(
                "⬇️ Guardar imagen",
                data=image_buffer.getvalue(),
                file_name="mi_creative_notebook.png",
                mime="image/png",
                use_container_width=True
            )

        # ----------------------------------
        # TERMINAR DIBUJO
        # ----------------------------------

        if (
            st.session_state.finish_requested
            and current_image is not None
        ):

            final_image = current_image.copy()

            if (
                st.session_state.tool == "Texto"
                and st.session_state.text_content.strip()
            ):
                final_image = add_text_to_image(
                    final_image,
                    st.session_state.text_content,
                    st.session_state.selected_color,
                    st.session_state.text_size
                )

            st.session_state.final_image = final_image
            st.session_state.finished = True
            st.session_state.finish_requested = False
            st.rerun()

    # --------------------------------------
    # CONFIGURACIÓN DERECHA
    # --------------------------------------

    with right_tools:

        st.markdown(
            '<p class="section-label">AJUSTES</p>',
            unsafe_allow_html=True
        )

        with st.popover("⚙️", use_container_width=True):

            st.markdown("**Tamaño del pincel**")

            st.session_state.brush_size = st.slider(
                "Grosor",
                1,
                40,
                st.session_state.brush_size,
                key="brush_size_control"
            )

            st.markdown("**Opacidad**")

            st.session_state.opacity = st.slider(
                "Intensidad",
                10,
                100,
                st.session_state.opacity,
                key="opacity_control"
            )

        with st.popover("🎨", use_container_width=True):

            st.markdown("**Paleta de colores**")

            palette = [
                "#514A7E",
                "#A78BBA",
                "#E8A9C5",
                "#F2A6A6",
                "#F4C98B",
                "#B5CDAA",
                "#91B9C8",
                "#333333",
                "#FFFFFF"
            ]

            color_columns = st.columns(3)

            for index, color in enumerate(palette):
                with color_columns[index % 3]:
                    if st.button(
                        "●",
                        key=f"color_{index}",
                        help=color
                    ):
                        st.session_state.selected_color = color

            st.markdown("**Color personalizado**")

            st.session_state.selected_color = st.color_picker(
                "Elige un color",
                st.session_state.selected_color,
                key="custom_color"
            )

        with st.popover("📄", use_container_width=True):

            st.markdown("**Formato de hoja**")

            st.session_state.paper_size = st.selectbox(
                "Tamaño",
                list(paper_sizes.keys()),
                index=list(paper_sizes.keys()).index(
                    st.session_state.paper_size
                ),
                key="paper_size_control"
            )

            st.markdown("**Tipo de papel**")

            st.session_state.paper_type = st.selectbox(
                "Diseño",
                ["Lisa", "Cuadriculado", "Punteado", "Rayado"],
                index=[
                    "Lisa",
                    "Cuadriculado",
                    "Punteado",
                    "Rayado"
                ].index(st.session_state.paper_type),
                key="paper_type_control"
            )

            st.markdown("**Color de la hoja**")

            st.session_state.paper_color = st.color_picker(
                "Fondo",
                st.session_state.paper_color,
                key="paper_color_control"
            )

        with st.popover("➕", use_container_width=True):

            st.markdown("**Nuevo cuaderno**")

            st.write(
                "Puedes comenzar una hoja nueva "
                "con otra configuración."
            )

            if st.button(
                "Crear nueva hoja",
                use_container_width=True
            ):
                change_canvas()
                st.session_state.text_content = ""
                st.rerun()
