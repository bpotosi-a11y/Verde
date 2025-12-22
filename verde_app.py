import streamlit as st

# ================================
# 🌱 TÍTULO PRINCIPAL
# ================================
st.markdown("<h1 style='text-align: center;'>🌱 Cálculo de dosis para control de malezas</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ================================
# 📌 PARÁMETROS DEL LOTE
# ================================
st.markdown("<h3 style='text-align: center;'>📌 Parámetros del lote</h3>", unsafe_allow_html=True)

hectareas = st.number_input(
    "Número de hectáreas del lote",
    min_value=0.1,
    step=0.1
)

st.markdown("---")

# ================================
# 🌿 COBERTURA DE MALEZAS
# ================================
st.markdown("<h3 style='text-align: center;'>🌿 Cobertura de malezas (%)</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    porc_pastos = st.number_input("Cobertura de pastos (%)", 0.0, 100.0, 1.0)
with col2:
    porc_hojas = st.number_input("Cobertura de hojas anchas (%)", 0.0, 100.0, 1.0)

st.markdown("---")

# ================================
# 🌱 CONDICIONES DEL LOTE
# ================================
st.markdown("<h3 style='text-align: center;'>🌱 Condiciones del lote</h3>", unsafe_allow_html=True)

altura_maleza = st.checkbox("La maleza supera los 50 cm")
altura_plantacion = st.number_input(
    "Altura de la plantación (m)",
    min_value=0.1,
    step=0.1
)

st.markdown("---")

# ================================
# 🌾 PRESENCIA DE MALEZAS ESPECÍFICAS
# ================================
st.markdown("<h3 style='text-align: center;'>🌾 Presencia de malezas específicas</h3>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    pres_helechos = st.checkbox("Helechos")
    pres_ciperaceas = st.checkbox("Ciperáceas")
    pres_meloso = st.checkbox("Pasto meloso")
with col4:
    pres_mortino = st.checkbox("Mortiño")
    pres_gargantillo = st.checkbox("Gargantillo")
    pres_cuero_sapo = st.checkbox("Cuero de sapo")

st.markdown("<hr>", unsafe_allow_html=True)

# ================================
# 🔢 CLASIFICACIÓN DE COBERTURA
# ================================
def clasificar(p):
    if p <= 33:
        return "Baja"
    elif p <= 66:
        return "Media"
    else:
        return "Alta"

nivel_pastos = clasificar(porc_pastos)
nivel_hojas = clasificar(porc_hojas)

# ================================
# 🧮 CÁLCULO DE DOSIS TOTAL (ORIGINAL)
# ================================
dosis_touch_total = 0
dosis_mets_total = 0

# --- Pastos (Touchdown)
if porc_pastos > 0:
    if nivel_pastos == "Alta":
        porc_gram = (4/5) * porc_pastos
    elif nivel_pastos == "Media":
        porc_gram = (1/2) * porc_pastos
    else:
        porc_gram = (1/3) * porc_pastos

    factor = 2.9
    dosis_touch_total = (porc_gram / 100) * hectareas * factor

# --- Hojas anchas (Metsulfurón)
if porc_hojas > 0:
    if nivel_hojas == "Alta":
        porc_hoja = (5/5) * porc_hojas
    elif nivel_hojas == "Media":
        porc_hoja = (1/2) * porc_hojas
    else:
        porc_hoja = (1/3) * porc_hojas

    dosis_mets_total = (porc_hoja / 100) * hectareas * 2.6

# --- Ajustes adicionales (SIN MODIFICAR)
if pres_ciperaceas:
    dosis_touch_total += 0.2 * hectareas
if pres_helechos:
    dosis_mets_total += 0.1 * hectareas
if pres_meloso:
    dosis_touch_total += 0.2 * hectareas

pres_extra = sum([pres_mortino, pres_gargantillo, pres_cuero_sapo])
if pres_extra == 2:
    dosis_mets_total += 0.1 * hectareas
elif pres_extra == 3:
    dosis_mets_total += 0.2 * hectareas

if altura_maleza:
    dosis_touch_total += 0.3 * hectareas
    dosis_mets_total += 0.2 * hectareas

if porc_hojas == 0 and not pres_helechos:
    dosis_mets_total = 0

# ================================
# 📐 DOSIS DERIVADAS
# ================================
dosis_touch_ha = dosis_touch_total / hectareas
dosis_mets_ha = dosis_mets_total / hectareas

# ================================
# 🚜 DOSIS POR FUMIGADORA (TABLA)
# ================================
touch_fumi = {"Baja": "350 cm³", "Media": "400 cm³", "Alta": "550 cm³"}
mets_fumi = {"Baja": "4 g", "Media": "6 g", "Alta": "7–8 g"}

# ================================
# 🔧 BOQUILLA RECOMENDADA
# ================================
if altura_plantacion <= 1.5:
    boquilla = "Boquilla marcadora"
    descarga = "320 cm³/min"
elif altura_plantacion <= 3:
    boquilla = "110015 ASJ o AI 110015"
    descarga = "300 cm³/min"
else:
    boquilla = "8001 TeeJet"
    descarga = "hasta 270 cm³/min"

# ================================
# 📊 RESULTADOS FINALES
# ================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>📊 Resultados</h2>", unsafe_allow_html=True)

st.markdown("### 🌱 Pastos – Touchdown")
st.write(f"**Nivel de cobertura:** {nivel_pastos}")
st.write(f"**Dosis total del lote:** {dosis_touch_total:.2f} L")
st.write(f"**Dosis equivalente:** {dosis_touch_ha:.2f} L/ha")
st.write(f"**Dosis por fumigadora:** {touch_fumi[nivel_pastos]}")

st.markdown("---")

st.markdown("### 🌿 Hojas anchas – Metsulfurón")
st.write(f"**Nivel de cobertura:** {nivel_hojas}")
st.write(f"**Dosis total del lote:** {dosis_mets_total:.2f} unidades")
st.write(f"**Dosis equivalente:** {dosis_mets_ha:.2f} unidades/ha")
st.write(f"**Dosis por fumigadora:** {mets_fumi[nivel_hojas]}")

st.markdown("---")

st.markdown("### 🔧 Boquilla recomendada")
st.write(f"**Tipo:** {boquilla}")
st.write(f"**Descarga:** {descarga}")



