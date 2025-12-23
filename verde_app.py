import streamlit as st

# ============================================================
# 🌱 INTERFAZ GENERAL
# ============================================================
st.set_page_config(page_title="Cálculo de dosis de malezas", layout="centered")
st.title("🌱 Cálculo de dosis para control de malezas")

st.markdown("---")

# ============================================================
# 📐 PARÁMETROS DEL LOTE
# ============================================================
st.header("📐 Parámetros del lote")

hectareas = st.number_input(
    "Número de hectáreas del lote",
    min_value=0.1,
    step=0.1
)

altura_plantacion = st.number_input(
    "Altura de la plantación (m)",
    min_value=0.1,
    step=0.1
)

st.markdown("---")

# ============================================================
# 🌿 COBERTURA DE MALEZAS
# ============================================================
st.header("🌿 Cobertura de malezas")

porc_pastos = st.number_input(
    "Cobertura de PASTOS (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)

porc_hojas = st.number_input(
    "Cobertura de HOJAS ANCHAS (%)",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)

altura_maleza = st.checkbox("¿La maleza supera los 50 cm?")

st.markdown("---")

# ============================================================
# 🌱 ESPECIES PROBLEMA
# ============================================================
st.header("🌱 Presencia de especies problema")

pres_helechos = st.checkbox("Helechos")
pres_ciperaceas = st.checkbox("Ciperáceas")
pres_mortino = st.checkbox("Mortiño")
pres_gargantillo = st.checkbox("Gargantillo")
pres_cuero_sapo = st.checkbox("Cuero de sapo")
pres_meloso = st.checkbox("Pasto meloso")

# ============================================================
# 🔢 CLASIFICACIÓN DE COBERTURA (ORIGINAL)
# ============================================================
def clasificar(p):
    if p <= 33:
        return "Baja"
    elif p <= 66:
        return "Media"
    else:
        return "Alta"

nivel_pastos = clasificar(porc_pastos)
nivel_hojas = clasificar(porc_hojas)

# ============================================================
# 🧮 CÁLCULO DE DOSIS TOTAL (ORIGINAL – NO TOCAR)
# ============================================================
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

# --- Ajustes originales
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

# ============================================================
# 📊 DOSIS POR HECTÁREA (DERIVADA – ORIGINAL)
# ============================================================
dosis_touch_ha = dosis_touch_total / hectareas
dosis_mets_ha = dosis_mets_total / hectareas

# ============================================================
# 🚿 DOSIS POR FUMIGADORA (SOLO INFORMATIVA – NO CALCULA)
# ============================================================
def dosis_fumigadora_touchdown(p):
    if p <= 20:
        return "350 cc por fumigadora (Baja)"
    elif p <= 40:
        return "420 cc por fumigadora (Media baja)"
    elif p <= 70:
        return "530 cc por fumigadora (Media alta)"
    else:
        return "650 cc por fumigadora (Alta)"

touch_fumi = dosis_fumigadora_touchdown(porc_pastos)

mets_fumi = {
    "Baja": "4 g por fumigadora",
    "Media": "6 g por fumigadora",
    "Alta": "7–8 g por fumigadora"
}

# ============================================================
# 🔧 BOQUILLA RECOMENDADA
# ============================================================
if altura_plantacion <= 1.5:
    boquilla = "Boquilla marcadora"
    descarga = "320 cc/min"
elif altura_plantacion <= 3:
    boquilla = "110015 ASJ o AI 110015"
    descarga = "300 cc/min"
else:
    boquilla = "8001 TeeJet"
    descarga = "hasta 270 cc/min"

# ============================================================
# 📈 RESULTADOS
# ============================================================
st.markdown("---")
st.header("📈 Resultados")

st.subheader("🌱 Pastos – Touchdown")
st.write(f"**Dosis total del lote:** {dosis_touch_total:.2f} L")
st.write(f"**Dosis equivalente:** {dosis_touch_ha:.2f} L/ha")
st.write(f"**Dosis por fumigadora:** {touch_fumi}")

st.subheader("🌿 Hojas anchas – Metsulfurón")
st.write(f"**Dosis total del lote:** {dosis_mets_total:.2f} unidades")
st.write(f"**Dosis equivalente:** {dosis_mets_ha:.2f} unidades/ha")
st.write(f"**Dosis por fumigadora:** {mets_fumi[nivel_hojas]}")

st.subheader("🔧 Boquilla recomendada")
st.write(f"{boquilla} – descarga {descarga}")
