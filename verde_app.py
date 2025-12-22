import streamlit as st

# ================================
# 🌱 Interfaz con Streamlit
# ================================
st.title("🌱 Cálculo de dosis de control de malezas")

# ----------------
# Parámetros del lote
# ----------------
hectareas = st.number_input("Número de hectáreas del lote", min_value=0.1, step=0.1)

porc_pastos = st.number_input(
    "Cobertura de PASTOS (%)", min_value=0.0, max_value=100.0, step=1.0
)

porc_hojas = st.number_input(
    "Cobertura de HOJAS ANCHAS (%)", min_value=0.0, max_value=100.0, step=1.0
)

altura_maleza = st.checkbox("¿La maleza supera los 50 cm?")

altura_plantacion = st.number_input(
    "Altura de la plantación (m)", min_value=0.1, step=0.1
)

pres_helechos = st.checkbox("¿Presencia de helechos?")
pres_ciperaceas = st.checkbox("¿Presencia de ciperáceas?")
pres_mortino = st.checkbox("¿Presencia de mortiño?")
pres_gargantillo = st.checkbox("¿Presencia de gargantillo?")
pres_cuero_sapo = st.checkbox("¿Presencia de cuero de sapo?")
pres_meloso = st.checkbox("¿Presencia de pasto meloso?")

# ================================
# Clasificación por porcentaje
# ================================
def clasificar(porc):
    if porc <= 33:
        return "Baja"
    elif porc <= 66:
        return "Media"
    else:
        return "Alta"

nivel_pastos = clasificar(porc_pastos)
nivel_hojas = clasificar(porc_hojas)

# ================================
# CÁLCULO DE DOSIS POR HECTÁREA
# (LÓGICA ORIGINAL)
# ================================
dosis_touch = 0
dosis_metsulfuron = 0

# --- GRAMÍNEAS (Touchdown)
if porc_pastos > 0:
    if nivel_pastos == "Alta":
        porc_gram = (4/5) * porc_pastos
    elif nivel_pastos == "Media":
        porc_gram = (1/2) * porc_pastos
    else:
        porc_gram = (1/3) * porc_pastos

    factor = 2.9
    dosis_touch = (porc_gram / 100) * hectareas * factor

# --- HOJA ANCHA (Metsulfurón)
if porc_hojas > 0:
    if nivel_hojas == "Alta":
        porc_hoja = (5/5) * porc_hojas
    elif nivel_hojas == "Media":
        porc_hoja = (1/2) * porc_hojas
    else:
        porc_hoja = (1/3) * porc_hojas

    dosis_metsulfuron = (porc_hoja / 100) * hectareas * 2.6

# --- Ajustes adicionales (ORIGINALES)
if pres_ciperaceas:
    dosis_touch += 0.2 * hectareas
if pres_helechos:
    dosis_metsulfuron += 0.1 * hectareas
if pres_meloso:
    dosis_touch += 0.2 * hectareas

pres_extra = sum([pres_mortino, pres_gargantillo, pres_cuero_sapo])
if pres_extra == 2:
    dosis_metsulfuron += 0.1 * hectareas
elif pres_extra == 3:
    dosis_metsulfuron += 0.2 * hectareas

if altura_maleza:
    dosis_touch += 0.3 * hectareas
    dosis_metsulfuron += 0.2 * hectareas

if porc_hojas == 0 and not pres_helechos:
    dosis_metsulfuron = 0

# ================================
# DOSIS POR FUMIGADORA (TABLA)
# ================================
touch_fumi = {
    "Baja": "400 cm³",
    "Media": "480 cm³",
    "Alta": "650 cm³"
}

metsul_fumi = {
    "Baja": "4 g",
    "Media": "6 g",
    "Alta": "10 g"
}

# ================================
# BOQUILLA
# ================================
if altura_plantacion <= 1.5:
    boquilla = "Boquilla marcadora"
    descarga = "320 cc/min"
elif altura_plantacion <= 3:
    boquilla = "110015 ASJ o AI 110015"
    descarga = "300 cc/min"
else:
    boquilla = "8001 TeeJet"
    descarga = "hasta 270 cc/min"

# ================================
# RESULTADOS
# ================================
st.subheader("📊 Resultados finales")

st.write("### 🌱 Pastos – Touchdown")
st.write(f"Nivel: **{nivel_pastos}**")
st.write(f"Dosis por hectárea: **{dosis_touch:.2f} L/ha**")
st.write(f"Dosis por fumigadora: **{touch_fumi[nivel_pastos]}**")

st.write("### 🌿 Hojas anchas – Metsulfurón")
st.write(f"Nivel: **{nivel_hojas}**")
st.write(f"Dosis por hectárea: **{dosis_metsulfuron:.2f} unidades/ha**")
st.write(f"Dosis por fumigadora: **{metsul_fumi[nivel_hojas]}**")

st.write("### 🔧 Boquilla recomendada")
st.write(f"{boquilla} – descarga {descarga}")

