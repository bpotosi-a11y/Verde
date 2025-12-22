import pandas as pd
import streamlit as st

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Cálculo de Dosis y Eficacia de Aplicación")

# -------------------------------
# Parámetros del lote
# -------------------------------
hectareas = st.number_input(
    "Número de hectáreas del lote",
    min_value=0.1,
    step=0.1
)

# -------------------------------
# Cobertura
# -------------------------------
cobertura_pastos = st.number_input(
    "Cobertura de pastos (%)",
    min_value=0.0, max_value=100.0, step=1.0
)

cobertura_hojas = st.number_input(
    "Cobertura de hojas anchas (%)",
    min_value=0.0, max_value=100.0, step=1.0
)

# -------------------------------
# Alturas y operación
# -------------------------------
altura_maleza = st.number_input(
    "Altura promedio de la maleza (cm)",
    min_value=5.0, step=5.0
)

velocidad = st.number_input(
    "Velocidad de aplicación (m/min)",
    value=40.0, step=1.0
)

st.caption("👉 Velocidad óptima recomendada: **40 m/min**")

# -------------------------------
# Presencias
# -------------------------------
floracion = st.checkbox("¿Pastos en floración?")
pasto_resistente = st.checkbox("¿Presencia de pastos resistentes?")
pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_ciperaceas = st.checkbox("¿Presencia de ciperáceas?")
pres_meloso = st.checkbox("¿Presencia de pasto meloso?")

# ================================
# Función: nivel de resistencia
# ================================
def nivel_resistencia(porc):
    if porc < 30:
        return "Bajo"
    elif porc < 60:
        return "Medio"
    else:
        return "Alto"

# ================================
# Botón principal
# ================================
if st.button("📐 Calcular dosis y eficacia"):

    # -------------------------------
    # Nivel de resistencia
    # -------------------------------
    nivel_pastos = nivel_resistencia(cobertura_pastos)

    # -------------------------------
    # Dosis base por fumigadora (cm³)
    # -------------------------------
    if nivel_pastos == "Bajo":
        dosis_touch_fumi = 350
    elif nivel_pastos == "Medio":
        dosis_touch_fumi = 400
    else:
        dosis_touch_fumi = 550

    # Ajustes
    if pres_ciperaceas:
        dosis_touch_fumi += 50
    if pres_meloso:
        dosis_touch_fumi += 50

    # -------------------------------
    # Conversión a DHT (L/ha)
    # Supuesto técnico: 20 fumigadoras/ha
    # -------------------------------
    DHT = (dosis_touch_fumi * 20) / 1000

    # -------------------------------
    # MODELO DE REGRESIÓN (RES)
    # -------------------------------
    RES = (
        0.306
        - 0.0279 * cobertura_pastos
        + 0.1265 * altura_maleza
        + 0.0546 * velocidad
        - 0.0075 * DHT
        - 0.0099 * int(floracion)
        + 0.0629 * int(pasto_resistente)
    )

    RES = max(0, min(RES * 100, 100))  # % y acotado

    # -------------------------------
    # Ajuste final de dosis según RES
    # -------------------------------
    factor_ajuste = 1.0
    if RES > 40:
        factor_ajuste = 1.20
    elif RES > 30:
        factor_ajuste = 1.10

    dosis_final_fumi = dosis_touch_fumi * factor_ajuste

    # -------------------------------
    # Resultados
    # -------------------------------
    st.subheader("📊 Resultados técnicos")

    st.write(f"**Nivel de resistencia:** {nivel_pastos}")
    st.write(f"**Dosis base Touchdown:** {dosis_touch_fumi:.0f} cm³/fumigadora")
    st.write(f"**Dosis final ajustada:** {dosis_final_fumi:.0f} cm³/fumigadora")
    st.write(f"**Dosis Touchdown (DHT):** {DHT:.2f} L/ha")

    st.subheader("🎯 Eficacia esperada")
    st.write(f"**Maleza residual estimada (RES):** {RES:.1f} %")

    if RES < 25:
        st.success("✔ Alta eficacia esperada")
    elif RES < 40:
        st.warning("⚠ Eficacia media, monitorear rebrote")
    else:
        st.error("❌ Eficacia baja, ajuste obligatorio")

    st.subheader("🚶 Recomendación operativa")
    st.write("Velocidad óptima sugerida: **40 m/min**")

