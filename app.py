
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from io import BytesIO
import numpy as np

# CONFIGURACIÓN
st.set_page_config(
    page_title="Creative Notebook",
    page_icon="🎨",
    layout="wide"
)

# ESTILOS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fffaf5, #f8f1ff, #f2f8ff);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
}

.hero {
    background: linear-gradient(110deg, #f9dce8, #fbe8c8, #e7e4ff);
    border-radius: 25px;
    padding: 25px;
    margin-bottom: 20px;
}

.hero h1 {
    color: #454052;
    font-size: 2.2rem;
    font-weight: 800;
}

.hero p {
    color: #756d7d;
}

.panel {
    background: rgba(255,255,255,0.85);
    border: 1px solid #eee7f0;
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 16px;
    box-shadow: 0 6px 22px rgba(100,80,120,.06);
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 13px;
    background: #ffffff;
    color: #514b5c;
    border: 1px solid #eaddec;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #f8effb;
    border-color: #d7b9e8;
    color: #514b5c;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ESTADOS
if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

if "final_image" not in st.session_state:
    st.session_state.final_image = None

if "selected_color" not in st.session_state:
    st.session_state.selected_color = "#514A7E"


# FUNCIÓN DE COLOR
def hex_to_rgba(color, opacity):
    color = color.lstrip("#")

    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    alpha = opacity / 100

    return f"rgba({r}, {g}, {b}, {alpha:.2f})"


# FUNCIÓN PARA DESCARGAR
def create_png(image_array):
    image = Image.fromarray(
        np.asarray(image_array).astype("uint8")
    ).convert("RGBA")

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return buffer.getvalue()


# CABECERA
st.markdown("""
<div class="hero">
    <h1>✿ Creative Notebook</h1>
    <p>Your little creative space · Un lugar para dibujar, probar y crear.</p>
</div>
""", unsafe_allow_html=True)


# PANTALLA FINAL
if st.session_state.finished:

    st.markdown("## ✨ ¡Tu creación está lista!")

    st.write("Este es el resultado de tu sesión creativa.")

    if st.session_state.final_image is not None:

        st.image(
            st.session_state.final_image,
            use_container_width=True
        )

        st.download_button(
            "⬇️ Descargar mi ilustración",
            data=create_png(st.session_state.final_image),
            file_name="mi_creacion.png",
            mime="image/png",
            use_container_width=True
        )

    if st.button("↩ Volver al cuaderno"):

        st.session_state.finished = False
        st.rerun()


# NOTEBOOK
else:

    # HERRAMIENTAS
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### 🖌️ Herramientas de dibujo")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        tool = st.selectbox(
            "Herramienta",
            [
                "✏️ Lápiz",
                "🖌️ Pincel",
                "🖍️ Marcador",
                "📏 Línea",
                "▭ Rectángulo",
                "⭕ Círculo",
                "⬡ Polígono",
                "⌖ Seleccionar",
                "🧽 Borrador",
                "• Punto"
            ]
        )

    with col2:

        brush_size = st.slider(
            "Grosor",
            1,
            40,
            7
        )

    with col3:

        opacity = st.slider(
            "Opacidad",
            10,
            100,
            100,
            step=5
        )

    with col4:

        background_color = st.color_picker(
            "Fondo del papel",
            "#FFFFFF"
        )

    st.markdown("### 🎨 Paleta de colores")

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

    cols = st.columns(10)

    for i, (name, color) in enumerate(palette.items()):

        with cols[i]:

            if st.button(
                name,
                key=f"color_{name}",
                use_container_width=True
            ):

                st.session_state.selected_color = color
                st.rerun()

    custom_color = st.color_picker(
        "Elige tu propio color",
        st.session_state.selected_color,
        key="custom_color"
    )

    st.session_state.selected_color = custom_color

    st.markdown('</div>', unsafe_allow_html=True)


    # CONFIGURACIÓN DE HERRAMIENTAS
    modes = {
        "✏️ Lápiz": "freedraw",
        "🖌️ Pincel": "freedraw",
        "🖍️ Marcador": "freedraw",
        "📏 Línea": "line",
        "▭ Rectángulo": "rect",
        "⭕ Círculo": "circle",
        "⬡ Polígono": "polygon",
        "⌖ Seleccionar": "transform",
        "🧽 Borrador": "freedraw",
        "• Punto": "point"
    }

    drawing_mode = modes[tool]

    current_color = st.session_state.selected_color

    if tool == "🧽 Borrador":
        current_color = background_color

    if tool == "✏️ Lápiz":
        opacity = min(opacity, 85)

    elif tool == "🖍️ Marcador":
        opacity = min(opacity, 45)
        brush_size = max(brush_size, 12)

    stroke_color = hex_to_rgba(
        current_color,
        opacity
    )


    # LIENZO
    st.markdown("### 📝 Mi espacio de dibujo")

    canvas_result = st_canvas(
        fill_color=hex_to_rgba(
            st.session_state.selected_color,
            22
        ),
        stroke_width=brush_size,
        stroke_color=stroke_color,
        background_color=background_color,
        height=520,
        width=1000,
        drawing_mode=drawing_mode,
        display_toolbar=False,
        update_streamlit=True,
        key=f"canvas_{st.session_state.canvas_version}"
    )

    st.caption(
        "✿ Elige tus herramientas, experimenta con los colores y crea libremente."
    )


    # ACCIONES
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### ✨ Acciones")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🗑️ Limpiar lienzo",
            use_container_width=True
        ):

            st.session_state.canvas_version += 1
            st.rerun()

    with col2:

        if st.button(
            "↻ Nuevo cuaderno",
            use_container_width=True
        ):

            st.session_state.canvas_version += 1
            st.session_state.selected_color = "#514A7E"
            st.rerun()

    with col3:

        if st.button(
            "✨ Terminar creación",
            use_container_width=True
        ):

            if canvas_result.image_data is not None:

                st.session_state.final_image = np.asarray(
                    canvas_result.image_data
                ).astype("uint8")

                st.session_state.finished = True
                st.rerun()

            else:

                st.warning("Primero realiza un dibujo.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.caption("Creative Notebook · Crea a tu manera ✿")
