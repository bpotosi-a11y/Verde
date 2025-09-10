import cv2
import numpy as np
import pandas as pd
import streamlit as st

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
    return porcentaje, mask

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Análisis de Cobertura Verde y Cálculo de Dosis")

# Parámetros del lote
hectareas = st.number_input("Número de hectáreas del lote", min_value=0.1, step=0.1)

altura_maleza = st.checkbox("¿La maleza supera los 50 cm?")

pres_gramineas = st.selectbox("Presencia de gramíneas", ["Ninguna", "Baja", "Media", "Alta"])
pres_hoja_ancha = st.selectbox("Presencia de hoja ancha", ["Ninguna", "Baja", "Media", "Alta"])
pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_ciperaceas = st.checkbox("¿Presencia de ciperáceas?")
pres_mortino = st.checkbox("¿Presencia de mortiño?")
pres_gargantillo = st.checkbox("¿Presencia de gargantillo?")
pres_cuero_sapo = st.checkbox("¿Presencia de cuero de sapo?")
pres_meloso = st.checkbox("¿Presencia de pasto meloso?")

# Subir imágenes
archivos = st.file_uploader("Selecciona tus imágenes", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if archivos and st.button("🔍 Analizar imágenes"):
    porcentajes = []
    for archivo in archivos:
        file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        p, _ = calcular_verde(img)
        porcentajes.append(p)

    promedio = np.mean(porcentajes) if porcentajes else 0
    st.write(f"🌿 **Cobertura verde promedio:** {promedio:.2f}%")

    # ==========================
    # Cálculo de dosis
    # ==========================
    dosis_touch = 0
    dosis_metsulfuron = 0

    # --- GRAMÍNEAS (Touchdown)
    if pres_gramineas != "Ninguna":
        if pres_gramineas == "Alta":
            porc_gram = (4/5) * promedio
        elif pres_gramineas == "Media":
            porc_gram = (1/2) * promedio
        elif pres_gramineas == "Baja":
            porc_gram = (1/3) * promedio

        factor = 3 if promedio < 60 else 3
        dosis_touch = (porc_gram/100) * hectareas * factor
    else:
        dosis_touch = 0  # sin gramíneas → no hay dosis

    # --- HOJA ANCHA (Metsulfurón)
    if pres_hoja_ancha != "Ninguna":
        if pres_hoja_ancha == "Alta":
            porc_hoja = (5/5) * promedio
        elif pres_hoja_ancha == "Media":
            porc_hoja = (1/2) * promedio
        elif pres_hoja_ancha == "Baja":
            porc_hoja = (1/3) * promedio

        dosis_metsulfuron = (porc_hoja/100) * hectareas * 2.6
    else:
        dosis_metsulfuron = 0  # sin hoja ancha → no hay dosis

    # --- Ajustes adicionales
    if pres_ciperaceas:
        dosis_touch += 0.2 * hectareas
    if pres_helechos:
        dosis_metsulfuron += 0.1 * hectareas
    if pres_meloso:
        dosis_touch += 0.3 * hectareas

    # Ajuste combinado: helechos + mortiño + gargantillo + cuero de sapo
    pres_extra = sum([pres_mortino, pres_gargantillo, pres_cuero_sapo])
    if pres_extra == 2:
        dosis_metsulfuron += 0.1 * hectareas
    elif pres_extra == 3:
        dosis_metsulfuron += 0.2 * hectareas

    # --- Ajuste por altura
    if altura_maleza:
        dosis_touch += 0.3 * hectareas
        dosis_metsulfuron += 0.2 * hectareas

    # ==========================
    # Resultados finales
    # ==========================
    st.subheader("📊 Resultados finales")
    st.write(f"Dosis total de **Touchdown** para {hectareas:.1f} ha: {dosis_touch:.3f} L")
    st.write(f"Dosis total de **Metsulfurón** para {hectareas:.1f} ha: {dosis_metsulfuron:.3f} unidades")

    # Guardar resultados
    resultados = pd.DataFrame({
        "Cobertura promedio (%)": [promedio],
        "Hectáreas": [hectareas],
        "Touchdown (L)": [dosis_touch],
        "Metsulfurón (unidades)": [dosis_metsulfuron]
    })
    resultados.to_excel("resultados_cobertura.xlsx", index=False)
    st.success("✅ Resultados guardados en 'resultados_cobertura.xlsx'")
