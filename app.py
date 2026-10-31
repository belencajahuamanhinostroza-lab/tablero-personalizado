
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
    max-width: 1450px !important;
    padding: 1rem 1.2rem !important;
}

.hero {
    background: linear-gradient(110deg, #F8DCE8, #FBEBD3, #E9E3FA);
    border: 1px solid white;
    border-radius: 20px;
    padding: 16px 24px;
    margin-bottom: 18px;
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

.intro-panel {
    background: linear-gradient(
        145deg,
        #FFF0F5 0%,
        #F2EAFF 50%,
        #E8F8F2 100%
    );
    border: 1px solid white;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 7px 25px rgba(90,70,110,.06);
}

.intro-panel h3 {
    color: #65566F;
    font-size: 1.1rem;
    margin-bottom: 8px;
}

.intro-panel p {
    color: #756D80;
    font-size: .9rem;
    line-height: 1.7;
}

.intro-panel hr {
    border: none;
    border-top: 1px solid rgba(145,125,165,.2);
    margin: 18px 0;
}

.canvas-card {
    background: rgba(255,255,255,.8);
    border: 1px solid #E9DFED;
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 7px 25px rgba(90,70,110,.06);
}

.section-label {
    color: #756982;
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 10px;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid #E9DFED;
    background: rgba(255,255,255,.95);
    color: #63566E;
    font-weight: 700;
    min-height: 40px;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #F6ECFA;
    border-color: #D8C1E5;
    color: #63566E;
}

.stPopover > button {
    border-radius: 12px;
    background: white;
    border: 1px solid #E9DFED;
    color: #665A72;
}

[data-testid="stVerticalBlock"] {
    gap: .55rem;
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

def make_paper(color, width, height):
    return Image.new("RGB", (width, height), color)


def export_png(image_array):
    image = Image.fromarray(
        np.asarray(image_array).astype("uint8")
    ).convert("RGBA")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def clear_canvas():
    st.session_state.saved_drawing = None
    st.session_state.canvas_version += 1


# =====================================================
# CABECERA
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

intro_column, workspace_column = st.columns(
    [2.5, 7.5],
    gap="medium"
)


# =====================================================
# PANEL IZQUIERDO
# =====================================================

with intro_column:

    with st.container(height=650, border=False):

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

            <h3>✿ ¿Cómo empezar?</h3>

            <p>✏️ <b>1. Dibuja:</b> utiliza el lápiz sobre tu hoja.</p>

            <p>🎨 <b>2. Elige:</b> selecciona tu color favorito.</p>

            <p>📄 <b>3. Personaliza:</b> cambia el color del papel.</p>

            <p>⬇️ <b>4. Guarda:</b> descarga tu creación en PNG.</p>

            <hr>

            <h3>♡ Un pequeño consejo</h3>

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


# =====================================================
# PANEL DERECHO
# =====================================================

with workspace_column:

    st.markdown(
        '<div class="section-label">✦ Tu espacio de creación</div>',
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # HERRAMIENTAS
    # -------------------------------------------------

    tool_col, color_col, paper_col, size_col = st.columns(
        [1.3, 2.2, 2.2, 2]
    )

    with tool_col:
        selected_tool = st.selectbox(
            "Herramienta",
            ["Lápiz", "Borrador"],
            index=["Lápiz", "Borrador"].index(
                st.session_state.tool
            )
        )

        st.session_state.tool = selected_tool

    with color_col:
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

        selected_name = st.selectbox(
            "Color",
            list(palette.keys()),
            index=list(palette.values()).index(
                st.session_state.selected_color
            ) if st.session_state.selected_color in palette.values() else 0
        )

        st.session_state.selected_color = palette[selected_name]

    with paper_col:
        paper_options = {
            "Blanco": "#FFFFFF",
            "Crema": "#FFF9EE",
            "Rosa suave": "#FFF0F4",
            "Lila suave": "#F5F0FF",
            "Celeste suave": "#EEF8FF",
            "Verde menta": "#F0FAF4"
        }

        paper_name = st.selectbox(
            "Color del papel",
            list(paper_options.keys()),
            index=list(paper_options.values()).index(
                st.session_state.paper_color
            ) if st.session_state.paper_color in paper_options.values() else 0
        )

        new_paper_color = paper_options[paper_name]

        if new_paper_color != st.session_state.paper_color:
            st.session_state.paper_color = new_paper_color
            clear_canvas()
            st.rerun()

    with size_col:
        st.session_state.brush_size = st.slider(
            "Grosor del lápiz",
            min_value=1,
            max_value=25,
            value=st.session_state.brush_size
        )

    # -------------------------------------------------
    # BOTONES
    # -------------------------------------------------

    button1, button2 = st.columns(2)

    with button1:
        if st.button("🗑️ Limpiar hoja", use_container_width=True):
            clear_canvas()
            st.rerun()

    with button2:
        st.markdown(
            '<div style="height:1px;"></div>',
            unsafe_allow_html=True
        )

    # -------------------------------------------------
    # LIENZO
    # -------------------------------------------------

    paper_image = make_paper(
        st.session_state.paper_color,
        790,
        560
    )

    stroke = (
        st.session_state.paper_color
        if st.session_state.tool == "Borrador"
        else st.session_state.selected_color
    )

    st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center;color:#796D83;'
        'font-weight:700;padding:4px 0 12px;">'
        '✿ Mi hoja de dibujo</div>',
        unsafe_allow_html=True
    )

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=st.session_state.brush_size,
        stroke_color=stroke,
        background_image=paper_image,
        height=560,
        width=790,
        drawing_mode="freedraw",
        initial_drawing=st.session_state.saved_drawing,
        update_streamlit=True,
        return_image_data=True,
        key=f"creative_canvas_{st.session_state.canvas_version}"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------
    # GUARDAR DIBUJO
    # -------------------------------------------------

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

    if canvas_result.json_data is not None:
        st.session_state.saved_drawing = canvas_result.json_data

    st.download_button(
        "⬇️ Guardar mi dibujo",
        data=export_png(current_image),
        file_name="creative_notebook.png",
        mime="image/png",
        use_container_width=True
    )


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("""
<div style="text-align:center;color:#A397AA;
font-size:12px;padding-top:18px;">
Creative Notebook · Un espacio para crear a tu manera ✿
</div>
""", unsafe_allow_html=True)
