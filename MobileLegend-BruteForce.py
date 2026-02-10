import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
from PIL import Image
import os
import base64

heroMage = pd.read_excel('data/hero_mage.xlsx')
magicItem = pd.read_excel('data/item_magic.xlsx')

st.subheader('Pilih Hero')
selected_hero = st.selectbox(
    '-',
    heroMage['nama hero']
)

hero = heroMage[heroMage['nama hero'] == selected_hero].iloc[0]

hero_type = hero['type hero'].strip().lower()
hero_attack_type = hero['attack type'].strip().lower()

nama_item = magicItem['nama item'].tolist()
cd_item = magicItem['cooldown reduction'].tolist()
power_item = magicItem['magic power'].tolist()
speed_item = magicItem['attack speed'].tolist()

limitItem = 3

bestItemCount = 0
bestCombo = ["", "", ""]
bestCd = 0
bestPower = 0
bestSpeed = 0

expHP = 3850
limitSpeed = 20

if hero_type == 'burst':
    limitCd = 30
elif hero_type == 'cd':
    limitCd = 25

jumlah_item = len(nama_item)

for i in range(jumlah_item):
    total_cd = cd_item[i]
    total_power = power_item[i]
    total_speed = speed_item[i]

    if hero_attack_type == 'basic attack':
        if (
            total_speed > 0 and
            total_speed <= limitSpeed
        ):
            if (
                bestItemCount < 1 or
                total_speed > bestSpeed or
                (total_speed == bestSpeed and total_power > bestPower)
            ):
                bestItemCount = 1
                bestCd = total_cd
                bestPower = total_power
                bestSpeed = total_speed
                bestCombo[0] = nama_item[i]

    elif (hero_attack_type == 'skill'):
        if (total_speed == 0) and (total_cd <= limitCd):
            if (bestItemCount < 1) or (total_cd > bestCd) or (total_cd == bestCd) and (total_power > bestPower):
                bestItemCount = 1
                bestCd = total_cd
                bestPower = total_power
                bestSpeed = 0
                bestCombo[0] = nama_item[i]
                bestCombo[1] = ""
                bestCombo[2] = ""

for i in range(jumlah_item):
    for j in range(i + 1, jumlah_item):

        total_cd = cd_item[i] + cd_item[j]
        total_power = power_item[i] + power_item[j]

        speed_i = speed_item[i]
        speed_j = speed_item[j]

        if hero_attack_type == 'basic attack':
            if (
                speed_i + speed_j > 0 and
                speed_i + speed_j <= limitSpeed
            ):
                cd_ok = (bestCd < limitCd) and (total_cd <= limitCd)
        
                if (
                    bestItemCount < 2 or
                    (cd_ok and total_cd > bestCd) or
                    (not cd_ok and total_power > bestPower)
                ):
                    bestItemCount = 2
                    bestCd = total_cd if cd_ok else bestCd
                    bestPower = total_power
                    bestSpeed = speed_i
                    bestCombo[0] = nama_item[i]
                    bestCombo[1] = nama_item[j]

        elif (hero_attack_type == 'skill'):
            if (speed_i == 0) and (speed_j == 0) and (total_cd <= limitCd):
                if (bestItemCount < 2) or (total_cd > bestCd) or (total_cd == bestCd) and (total_power > bestPower):
                    bestItemCount = 2
                    bestCd = total_cd
                    bestPower = total_power
                    bestSpeed = 0
                    bestCombo[0] = nama_item[i]
                    bestCombo[1] = nama_item[j]
                    bestCombo[2] = ""

for i in range(jumlah_item):
    for j in range(i + 1, jumlah_item):
        for k in range(j + 1, jumlah_item):

            total_cd = cd_item[i] + cd_item[j] + cd_item[k]
            total_power = power_item[i] + power_item[j] + power_item[k]

            speed_i = speed_item[i]
            speed_j = speed_item[j]
            speed_k = speed_item[k]

            if hero_attack_type == 'basic attack':
                total_speed = speed_i + speed_j + speed_k

                if (
                    total_speed > 0 and
                    total_speed <= limitSpeed
                ):
                    cd_ok = (bestCd < limitCd) and (total_cd <= limitCd)

                    if (
                        bestItemCount < 3 or
                        (cd_ok and total_cd > bestCd) or
                        (not cd_ok and total_power > bestPower)
                    ):
                        bestItemCount = 3
                        bestCd = total_cd if cd_ok else bestCd
                        bestPower = total_power
                        bestSpeed = speed_i
                        bestCombo[0] = nama_item[i]
                        bestCombo[1] = nama_item[j]
                        bestCombo[2] = nama_item[k]

            elif (hero_attack_type == 'skill'):
                if (speed_i == 0) and (speed_j == 0) and (speed_k == 0) and (total_cd <= limitCd) or(cd_item[i] == 0 and cd_item[j] == 0 and cd_item[k] == 0):
                    if (bestItemCount < 3) or (total_cd > bestCd) or (total_cd == bestCd and total_power > bestPower):
                        bestItemCount = 3
                        bestCd = total_cd
                        bestPower = total_power
                        bestSpeed = 0
                        bestCombo[0] = nama_item[i]
                        bestCombo[1] = nama_item[j]
                        bestCombo[2] = nama_item[k]

st.write('Hero :', selected_hero)

hero_filename = selected_hero.lower().replace(" ", "_") + ".png"
hero_image_path = f"img/{hero_filename}"


if os.path.exists(hero_image_path):
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center;">
            <img src="data:image/png;base64,{base64.b64encode(open(hero_image_path, "rb").read()).decode()}" width="145">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Foto hero tidak ditemukan")


st.write('kombinasi item terpilih :')

for item in bestCombo:
    col_img, col_text = st.columns([1, 10])

    item_filename = item.lower().replace(" ", "_") + ".png"
    item_image_path = f"img/items/{item_filename}"

    with col_img:
        if os.path.exists(item_image_path):
            st.image(item_image_path, width=45)
        else:
            st.write("")

    with col_text:
        st.write(item)
