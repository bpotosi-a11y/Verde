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
# Coberturas
# -------------------------------
CPT = st.number_input(
    "Cobertura de pastos (%)",
    min_value=0.0, max_value=100.0, step=1.0
)

CHA = st.number_input(
    "Cobertura de hojas anchas (%)",
    min_value=0.0, max_value=100.0, step=1.0
)

# -------------------------------
# Altura y operación
# -------------------------------
AL = st.number_input(
    "Altura promedio de la maleza (cm)",
    min_value=5.0, step=5.0
)

VEL = st.number_input(
    "Velocidad de aplicación (m/min)",
    value=40.0, step=1.0
)

st.caption("Velocidad óptima recomendada: **40 m/min**")

# -------------------------------
# Presencias
# -------------------------------
FL = st.checkbox("¿Presencia de floración?")
PM = st.checkbox("¿Presencia de pastos resistentes?")
pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_mortino = st.checkbox("¿Presencia de mortiño?")
pres_gargantillo = st.checkbox("¿Presencia de gargantillo?")
pres_cuero_sapo = st.checkbox("¿Presencia de cuero de sapo?")
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

    # =====================================================
    # TOUCHDOWN – cálculo base (NO se cambia)
    # =====================================================
    nivel_pastos = nivel_resistencia(CPT)

    if nivel_pastos == "Bajo":
        dosis_touch_fumi = 350
    elif nivel_pastos == "Medio":
        dosis_touch_fumi = 400
    else:
        dosis_touch_fumi = 550

    if pres_ciperaceas:
        dosis_touch_fumi += 50
    if pres_meloso:
        dosis_touch_fumi += 50

    # Conversión a DHT (supuesto operativo constante)
    DHT = (dosis_touch_fumi * 20) / 1000  # L/ha

    # -------- MODELO TOUCHDOWN --------
    RES_touch = (
        0.306
        - 0.0279 * CPT
        + 0.1265 * AL
        + 0.0546 * VEL
        - 0.0075 * DHT
        - 0.0099 * int(FL)
        + 0.0629 * int(PM)
    ) * 100

    # Ajuste de dosis según RES
    factor_touch = 1.0
    if RES_touch > 40:
        factor_touch = 1.20
    elif RES_touch > 30:
        factor_touch = 1.10

    dosis_touch_final = dosis_touch_fumi * factor_touch

    # =====================================================
    # METSULFURÓN – cálculo base (NO se cambia)
    # =====================================================
    nivel_hojas = nivel_resistencia(CHA)

    if nivel_hojas == "Bajo":
        dosis_mets_fumi = 4
    elif nivel_hojas == "Medio":
        dosis_mets_fumi = 6
    else:
        dosis_mets_fumi = 8

    # Conversión a DHM (unidades técnicas)
    DHM = dosis_mets_fumi

    # -------- MODELO METSULFURÓN --------
    RES_mets = (
        0.3095
        + 0.0378 * CHA
        + 0.0038 * DHM
        + 0.1234 * AL
        + 0.0532 * VEL
        - 0.0166 * int(FL)
        + 0.0601 * int(PM)
    ) * 100

    # Evaluación de viabilidad
    problematicas = sum([
        pres_helechos,
        pres_mortino,
        pres_gargantillo,
        pres_cuero_sapo
    ])

    mets_viable = True
    if RES_mets > 45 or AL > 80 or problematicas >= 2:
        mets_viable = False

    # =====================================================
    # RESULTADOS
    # =====================================================
    st.subheader("📊 Resultados técnicos")

    st.write("### 🌾 Touchdown (Pastos)")
    st.write(f"Dosis base: **{dosis_touch_fumi:.0f} cm³/fumigadora**")
    st.write(f"Dosis final ajustada: **{dosis_touch_final:.0f} cm³/fumigadora**")
    st.write(f"Maleza residual esperada (RES): **{RES_touch:.1f} %**")

    st.write("### 🌿 Metsulfurón (Hojas anchas)")
    if mets_viable:
        st.write(f"Dosis recomendada: **{dosis_mets_fumi} g/fumigadora**")
        st.write(f"Maleza residual esperada (RES): **{RES_mets:.1f} %**")
    else:
        st.error(
            "❌ Aplicación química NO viable.\n\n"
            "**Recomendación:** realizar control mecanizado "
            "y reevaluar aplicación química."
        )

    st.subheader("🚶 Recomendación operativa")
    st.write("Velocidad óptima de aplicación: **40 m/min**")
