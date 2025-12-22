import cv2
import numpy as np
import streamlit as st

# ================================
# Función diagnóstico visual (NO decisoria)
# ================================
def calcular_verde(img):
    gamma = 1.2
    look_up_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
                              for i in np.arange(0, 256)]).astype("uint8")
    img = cv2.LUT(img, look_up_table)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    porcentaje = (np.sum(mask > 0) / mask.size) * 100
    return porcentaje

# ================================
# 🌱 Interfaz Streamlit
# ================================
st.title("🌱 Diagnóstico visual y cálculo técnico de dosis")

hectareas = st.number_input("Número de hectáreas del lote", min_value=0.1, step=0.1)

altura_plantacion = st.selectbox(
    "Altura promedio de la plantación",
    ["≤ 50 cm", "50–100 cm", "> 100 cm"]
)

altura_maleza = st.checkbox("¿La maleza supera la altura de la plantación?")

pres_gramineas = st.selectbox("Presencia de gramíneas", ["Ninguna", "Baja", "Media", "Alta"])
pres_hoja_ancha = st.selectbox("Presencia de hoja ancha", ["Ninguna", "Baja", "Media", "Alta"])

pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_ciperaceas = st.checkbox("¿Presencia de ciperáceas?")
pres_mortino = st.checkbox("¿Presencia de mortiño?")
pres_gargantillo = st.checkbox("¿Presencia de gargantillo?")
pres_cuero_sapo = st.checkbox("¿Presencia de cuero de sapo?")
pres_meloso = st.checkbox("¿Presencia de pasto meloso?")

# ================================
# Carga de imágenes (solo diagnóstico)
# ================================
archivos = st.file_uploader(
    "Cargar imágenes (diagnóstico visual, no decisorio)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if archivos:
    porcentajes = []
    for archivo in archivos:
        file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        porcentajes.append(calcular_verde(img))

    st.info(f"Cobertura verde promedio (diagnóstico): {np.mean(porcentajes):.1f}%")

# ================================
# 📐 Cálculo técnico de dosis
# ================================
if st.button("📐 Calcular dosis"):

    # --- Definición por altura de plantación
    if altura_plantacion == "≤ 50 cm":
        boquilla = "XR 11002"
        dosis_touch_ha = 2.0
        dosis_mets_ha = 4
    elif altura_plantacion == "50–100 cm":
        boquilla = "XR 11003"
        dosis_touch_ha = 2.8
        dosis_mets_ha = 6
    else:
        boquilla = "XR 11004"
        dosis_touch_ha = 3.5
        dosis_mets_ha = 8

    # --- Ajustes por composición florística
    if pres_gramineas == "Ninguna":
        dosis_touch_ha = 0

    if pres_hoja_ancha == "Ninguna" and not pres_helechos:
        dosis_mets_ha = 0

    if pres_ciperaceas:
        dosis_touch_ha += 0.3

    if pres_meloso:
        dosis_touch_ha += 0.4

    if pres_helechos:
        dosis_mets_ha += 1

    especies_dificiles = sum([pres_mortino, pres_gargantillo, pres_cuero_sapo])
    if especies_dificiles == 2:
        dosis_mets_ha += 1
    elif especies_dificiles == 3:
        dosis_mets_ha += 2

    # --- Ajuste por dominancia vertical
    if altura_maleza:
        dosis_touch_ha += 0.4
        dosis_mets_ha += 1

    # ================================
    # Resultados
    # ================================
    st.subheader("📊 Recomendación técnica final")

    st.write(f"🔹 **Boquilla recomendada:** {boquilla}")
    st.write(f"🔹 **Touchdown:** {dosis_touch_ha:.2f} L/ha → Total: {dosis_touch_ha * hectareas:.2f} L")
    st.write(f"🔹 **Metsulfurón:** {dosis_mets_ha:.1f} g/ha → Total: {dosis_mets_ha * hectareas:.1f} g")

    st.caption(
        "La cobertura verde obtenida por imágenes se utiliza únicamente "
        "como diagnóstico visual, no interviene en el cálculo de dosis."
    )

