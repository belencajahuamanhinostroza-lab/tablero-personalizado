        "Menta": "#A8DCC5",
        "Celeste": "#9CCFE5",
        "Lavanda": "#BDB0E8",
        "Lila": "#D9A9D8",
        "Coral": "#E98282",
        "Carbón": "#454052",
        "Blanco": "#FFFFFF",
    }

    palette_cols = st.columns(len(palette) + 1)
    for index, (name, color) in enumerate(palette.items()):
        with palette_cols[index]:
            is_selected = st.session_state.selected_color == color
            button_label = ("✓ " if is_selected else "") + name
            if st.button(
                button_label,
                key=f"palette_{name}",
                help=f"Elegir {name.lower()}",
                use_container_width=True
            ):
                st.session_state.selected_color = color
                st.rerun()

    with palette_cols[-1]:
        custom_color = st.color_picker(
            "Personalizado",
            value=st.session_state.selected_color,
            key="custom_color_picker"
        )
        if custom_color != st.session_state.selected_color:
            st.session_state.selected_color = custom_color

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # CONFIGURACIÓN SEGÚN HERRAMIENTA
    # -----------------------------------------------------
    drawing_modes = {
        "✏️ Lápiz": "freedraw",
        "🖌️ Pincel": "freedraw",
        "🖍️ Marcador": "freedraw",
        "📏 Línea": "line",
        "▭ Rectángulo": "rect",
        "⭕ Círculo": "circle",
        "⬡ Polígono": "polygon",
        "⌖ Seleccionar / mover": "transform",
        "🧽 Borrador": "freedraw",
        "• Punto": "point",
    }

    drawing_mode = drawing_modes[tool_label]
    current_color = background_color if tool_label == "🧽 Borrador" else st.session_state.selected_color

    # Diferencia visual entre lápiz, pincel y marcador mediante tamaño/opacidad.
    effective_opacity = opacity
    if tool_label == "✏️ Lápiz":
        effective_opacity = min(opacity, 85)
    elif tool_label == "🖍️ Marcador":
        effective_opacity = min(opacity, 45)

    stroke_color = hex_to_rgba(current_color, effective_opacity)
    effective_width = brush_size
    if tool_label == "🖍️ Marcador":
        effective_width = max(brush_size, 12)

    # -----------------------------------------------------
    # LIENZO
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-label">03 · Mi espacio de dibujo</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="canvas-shell">', unsafe_allow_html=True)

    canvas_result = st_canvas(
        fill_color=hex_to_rgba(st.session_state.selected_color, 22),
        stroke_width=effective_width,
        stroke_color=stroke_color,
        background_color=background_color,
        height=520,
        width=1000,
        drawing_mode=drawing_mode,
        display_toolbar=False,
        update_streamlit=True,
        key=f"creative_canvas_{st.session_state.canvas_version}",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Consejo: elige una herramienta y un color, y dibuja directamente sobre el papel.")

    # -----------------------------------------------------
    # ACCIONES
    # -----------------------------------------------------
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">04 · Acciones</div>', unsafe_allow_html=True)

    action_left, action_middle, action_right = st.columns([1, 1, 1.3])

    with action_left:
        if st.button("🗑️ Limpiar lienzo", use_container_width=True):
            st.session_state.canvas_version += 1
            st.rerun()

    with action_middle:
        if st.button("↻ Nuevo cuaderno", use_container_width=True):
            st.session_state.canvas_version += 1
            st.session_state.selected_color = "#514A7E"
            st.rerun()

    with action_right:
        if st.button("✨ Terminar creación", type="primary", use_container_width=True):
            if canvas_result.image_data is not None:
                st.session_state.final_image = np.asarray(
                    canvas_result.image_data
                ).astype("uint8")
                st.session_state.finished = True
                st.rerun()
            else:
                st.info("Primero realiza un dibujo en tu lienzo.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Creative Notebook · Crea a tu manera ✿")
