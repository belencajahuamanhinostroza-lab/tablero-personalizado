
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
from io import BytesIO
import numpy as np

st.set_page_config(
    page_title="Creative Notebook",
    page_icon="✿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    max-width: 1500px !important;
    padding: 1rem 1.2rem !important;
    margin: auto !important;
}

.hero {
    background: linear-gradient(110deg,#F8DCE8,#FBEBD3,#E9E3FA);
    border: 1px solid white;
    border-radius: 18px;
    padding: 12px 22px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
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

.intro-panel {
    background: rgba(255,255,255,.65);
    border: 1px solid #E9DFED;
    border-radius: 20px;
    padding: 18px;
    min-height: 300px;
    box-shadow: 0 7px 25px rgba(90,70,110,.05);
}

.intro-panel h3 {
    color: #65566F;
    margin-top: 5px;
    font-size: 1.1rem;
}

.intro-panel p {
    color: #82768A;
    font-size: .88rem;
    line-height: 1.65;
}

.intro-panel hr {
    border: none;
    border-top: 1px solid #EAE0ED;
    margin: 18px 0;
}

.canvas-card {
    background: rgba(255,255,255,.78);
    border: 1px solid #E9E2ED;
    border-radius: 18px;
    padding: 10px;
    box-shadow: 0 7px 25px rgba(90,70,110,.06);
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid #E9DFED;
    background: rgba(255,255,255,.95);
    color: #63566E;
    font-weight: 700;
    min-height: 39px;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #F6ECFA;
    border-color: #D8C1E5;
}

.stPopover > button {
    border-radius: 12px;
    background: white;
    border: 1px solid #E9DFED;
    color: #665A72;
    min-height: 42px;
    font-size: 1.1rem;
}

[data-testid="stPopoverBody"] {
    background: #FFFCFF;
    border: 1px solid #E9DFED;
    border-radius: 15px;
}

.section-label {
    color: #756982;
    font-size: .9rem;
    font-weight: 800;
    margin-bottom: 5px;
}

footer, #MainMenu {
    visibility: hidden;
}

[data-testid="stVerticalBlock"] {
    gap: .45rem;
}

@media (max-width: 850px) {
    .hero h1 {
        font-size: 1.4rem;
    }

    .intro-panel {
        min-height: auto;
    }
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
    "paper_type": "Lisa",
    "paper_size": "A4 horizontal",
    "finished": False,
    "final_image": None,
    "last_config": None,
    "tool": "Lápiz",
    "brush_size": 6,
    "opacity": 100,
    "finish_requested": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# FUNCIONES
# =====================================================

def make_paper(color, pattern, width, height):
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)
    pattern_color = "#DCE0E8"

    if pattern == "Cuadriculado":
        for x in range(0, width, 30):
            draw.line((x, 0, x, height), fill=pattern_color, width=1)

        for y in range(0, height, 30):
            draw.line((0, y, width, y), fill=pattern_color, width=1)

    elif pattern == "Punteado":
        for x in range(12, width, 25):
            for y in range(12, height, 25):
                draw.ellipse(
                    (x-1, y-1, x+1, y+1),
                    fill=pattern_color
                )

    elif pattern == "Rayado":
        for y in range(35, height, 35):
            draw.line(
                (0, y, width, y),
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

    return buffer.getvalue()


def change_canvas():
    st.session_state.canvas_version += 1


def blend(fg, bg, alpha):
    fg_rgb = tuple(
        int(fg[i:i+2], 16) for i in (1, 3, 5)
    )

    bg_rgb = tuple(
        int(bg[i:i+2], 16) for i in (1, 3, 5)
    )

    result = tuple(
        round(
            fg_rgb[i] * alpha / 100
            + bg_rgb[i] * (1-alpha/100)
        )
        for i in range(3)
    )

    return "#{:02X}{:02X}{:02X}".format(*result)


# =====================================================
# CABECERA
# =====================================================

st.markdown("""
<div class="hero">
    <div>
        <h1>✿ Creative Notebook</h1>
        <p>Your little creative space · Dibuja, experimenta y crea.</p>
    </div>

    <div style="color:#756982;font-size:1.5rem;">
        ♡ ✦ ✿
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# PANTALLA FINAL
# =====================================================

if st.session_state.finished:

    st.markdown("## ✨ Tu creación está lista")

    if st.session_state.final_image is not None:

        st.image(
            st.session_state.final_image,
            use_container_width=True
        )

        st.download_button(
            "⬇️ Descargar ilustración PNG",
            data=export_png(st.session_state.final_image),
            file_name="creative_notebook.png",
            mime="image/png"
        )

    if st.button("↩ Volver a dibujar"):
        st.session_state.finished = False
        st.rerun()

    st.stop()


# =====================================================
# TAMAÑOS
# =====================================================

paper_sizes = {
    "A4 horizontal": (790, 560),
    "A4 vertical": (400, 560),
    "A3 horizontal": (795, 560),
    "Cuadrada": (560, 560),
    "Panorámica": (900, 478),
    "Libre": (850, 530)
}

canvas_width, canvas_height = paper_sizes[
    st.session_state.paper_size
]

config = (
    st.session_state.paper_color,
    st.session_state.paper_type,
    st.session_state.paper_size
)

if st.session_state.last_config is None:

    st.session_state.last_config = config

elif st.session_state.last_config != config:

    st.session_state.last_config = config
    change_canvas()


# =====================================================
# DOS GRANDES PANELES
# =====================================================

intro_column, workspace_column = st.columns(
    [2.4, 7.6],
    gap="medium"
)


# =====================================================
# PANEL IZQUIERDO: INTRODUCCIÓN BREVE
# =====================================================

with intro_column:

    with st.container(height=680, border=False):

        st.markdown("""
        <div class="intro-panel">

            <div style="text-align:center; font-size:3.5rem;">
                🌷
            </div>

            <h3 style="text-align:center;">
                ¡Bienvenida!
            </h3>

            <p style="text-align:center;">
                Este es tu pequeño rincón creativo,
                un espacio para imaginar, experimentar
                y dar vida a tus ideas.
            </p>

            <hr>

            <p style="text-align:center;">
                ✿ Dibuja a tu manera, explora colores
                y crea ilustraciones sin límites.
            </p>

            <div style="text-align:center; font-size:1.8rem; padding-top:18px;">
                ♡ ✿ ♡
            </div>

            <p style="text-align:center; font-size:.75rem;">
                Your imagination starts here.
            </p>

        </div>
        """, unsafe_allow_html=True)


# =====================================================
# PANEL DERECHO: ESPACIO DE TRABAJO
# =====================================================

with workspace_column:

    st.markdown(
        '<div class="section-label">✦ Tu espacio de creación</div>',
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # ACCIONES SUPERIORES
    # -------------------------------------------------

    action1, action2, action3 = st.columns([1, 1, 2])

    with action1:

        if st.button(
            "🗑️ Borrar hoja",
            use_container_width=True
        ):
            st.session_state.saved_drawing = None
            st.session_state.finish_requested = False
            change_canvas()
            st.rerun()

    with action2:
        download_placeholder = st.empty()

    with action3:

        if st.button(
            "✨ Terminar dibujo",
            use_container_width=True
        ):
            st.session_state.finish_requested = True
            st.rerun()

    # -------------------------------------------------
    # HERRAMIENTAS Y TABLERO
    # -------------------------------------------------

    left_tools, canvas_area, right_tools = st.columns(
        [0.8, 8, 0.8],
        gap="small",
        vertical_alignment="center"
    )

    # -------------------------------------------------
    # HERRAMIENTAS IZQUIERDAS
    # -------------------------------------------------

    with left_tools:

        if st.button("✏️", help="Lápiz", use_container_width=True):
            st.session_state.tool = "Lápiz"

        if st.button("🖌️", help="Pincel", use_container_width=True):
            st.session_state.tool = "Pincel"

        if st.button("🖍️", help="Marcador", use_container_width=True):
            st.session_state.tool = "Marcador"

        if st.button("╱", help="Línea", use_container_width=True):
            st.session_state.tool = "Línea"

        if st.button("▭", help="Rectángulo", use_container_width=True):
            st.session_state.tool = "Rectángulo"

        if st.button("◯", help="Círculo", use_container_width=True):
            st.session_state.tool = "Círculo"

        if st.button("⬡", help="Polígono", use_container_width=True):
            st.session_state.tool = "Polígono"

        if st.button("T", help="Texto", use_container_width=True):
            st.session_state.tool = "Texto"

        if st.button("🧽", help="Borrador", use_container_width=True):
            st.session_state.tool = "Borrador"

    # -------------------------------------------------
    # AJUSTES DERECHOS
    # -------------------------------------------------

    with right_tools:

        with st.popover(
            "⚙️",
            help="Ajustes",
            use_container_width=True
        ):

            st.markdown("### 🖌️ Ajustes del trazo")

            st.session_state.brush_size = st.slider(
                "Grosor",
                1,
                40,
                st.session_state.brush_size
            )

            st.session_state.opacity = st.slider(
                "Opacidad",
                10,
                100,
                st.session_state.opacity,
                step=5
            )

        with st.popover(
            "🎨",
            help="Colores",
            use_container_width=True
        ):

            st.markdown("### Paleta de colores")

            palette = {
                "Rosa": "#F19AB5",
                "Durazno": "#F5B99B",
                "Amarillo": "#F4D477",
                "Menta": "#A8DCC5",
                "Celeste": "#9CCFE5",
                "Lavanda": "#BDB0E8",
                "Lila": "#D9A9D8",
                "Coral": "#E98282",
                "Carbón": "#454052",
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

            st.session_state.selected_color = st.color_picker(
                "Color personalizado",
                value=st.session_state.selected_color,
                key="custom_color"
            )

        with st.popover(
            "📄",
            help="Papel",
            use_container_width=True
        ):

            st.markdown("### 📄 Mi papel")

            new_size = st.selectbox(
                "Formato",
                list(paper_sizes.keys()),
                index=list(paper_sizes.keys()).index(
                    st.session_state.paper_size
                )
            )

            new_pattern = st.selectbox(
                "Tipo de hoja",
                ["Lisa", "Cuadriculado", "Punteado", "Rayado"],
                index=[
                    "Lisa",
                    "Cuadriculado",
                    "Punteado",
                    "Rayado"
                ].index(st.session_state.paper_type)
            )

            new_color = st.selectbox(
                "Color del papel",
                [
                    "Blanco",
                    "Crema",
                    "Rosa suave",
                    "Lila suave",
                    "Celeste suave",
                    "Verde menta",
                    "Personalizado"
                ]
            )

            paper_colors = {
                "Blanco": "#FFFFFF",
                "Crema": "#FFF9EE",
                "Rosa suave": "#FFF0F4",
                "Lila suave": "#F5F0FF",
                "Celeste suave": "#EEF8FF",
                "Verde menta": "#F0FAF4"
            }

            if new_color == "Personalizado":

                chosen_paper_color = st.color_picker(
                    "Elige el color",
                    st.session_state.paper_color,
                    key="custom_paper"
                )

            else:
                chosen_paper_color = paper_colors[new_color]

            if st.button(
                "Aplicar cambios",
                use_container_width=True
            ):

                st.session_state.paper_size = new_size
                st.session_state.paper_type = new_pattern
                st.session_state.paper_color = chosen_paper_color
                st.rerun()

        with st.popover(
            "✨",
            help="Más acciones",
            use_container_width=True
        ):

            st.markdown("### Acciones")

            if st.button(
                "↻ Nuevo cuaderno",
                use_container_width=True
            ):

                st.session_state.saved_drawing = None
                st.session_state.selected_color = "#514A7E"
                st.session_state.paper_color = "#FFFFFF"
                st.session_state.paper_type = "Lisa"
                st.session_state.paper_size = "A4 horizontal"
                st.session_state.last_config = None
                st.session_state.finish_requested = False

                change_canvas()
                st.rerun()

    # -------------------------------------------------
    # TABLERO CENTRAL
    # -------------------------------------------------

    with canvas_area:

        tool_modes = {
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

        stroke = st.session_state.selected_color
        size = st.session_state.brush_size
        opacity = st.session_state.opacity

        if st.session_state.tool == "Lápiz":
            size = min(size, 5)

        elif st.session_state.tool == "Pincel":
            size = max(size, 9)

        elif st.session_state.tool == "Marcador":
            size = max(size, 14)
            opacity = min(opacity, 45)

        elif st.session_state.tool == "Borrador":
            stroke = st.session_state.paper_color
            opacity = 100

        stroke = blend(
            stroke,
            st.session_state.paper_color,
            opacity
        )

        paper_image = make_paper(
            st.session_state.paper_color,
            st.session_state.paper_type,
            canvas_width,
            canvas_height
        )

        st.markdown(
            '<div class="canvas-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                color:#796D83;
                font-weight:700;
                padding:4px 0 10px;
            ">
                ✿ {st.session_state.paper_size}
                · {st.session_state.paper_type}
            </div>
            """,
            unsafe_allow_html=True
        )

        canvas_result = st_canvas(
            fill_color=st.session_state.selected_color,
            stroke_width=size,
            stroke_color=stroke,
            background_image=paper_image,
            height=canvas_height,
            width=canvas_width,
            drawing_mode=tool_modes[st.session_state.tool],
            point_display_radius=4,
            initial_drawing=st.session_state.saved_drawing,
            update_streamlit=True,
            return_image_data=True,
            key=f"creative_canvas_{st.session_state.canvas_version}"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if canvas_result.json_data is not None:
            st.session_state.saved_drawing = canvas_result.json_data

        if canvas_result.image_data is not None:

            current_image = np.asarray(
                canvas_result.image_data
            ).astype("uint8")

        else:

            current_image = np.asarray(
                paper_image.convert("RGBA")
            )

        current_png = export_png(current_image)

        with download_placeholder.container():

            st.download_button(
                "⬇️ Guardar imagen",
                data=current_png,
                file_name="creative_notebook.png",
                mime="image/png",
                use_container_width=True,
                key="top_download"
            )

        # TERMINAR DIBUJO

        if st.session_state.finish_requested:

            if canvas_result.image_data is not None:

                st.session_state.final_image = current_image
                st.session_state.finished = True
                st.session_state.finish_requested = False
                st.rerun()

            else:

                st.warning("Primero realiza un dibujo.")
                st.session_state.finish_requested = False


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("""
<div style="
    text-align:center;
    color:#A397AA;
    font-size:12px;
    padding-top:10px;
">
    Creative Notebook · Un espacio para crear a tu manera ✿
</div>
""", unsafe_allow_html=True)
