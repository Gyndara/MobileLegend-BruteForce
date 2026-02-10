import streamlit as st
import pandas as pd


heroMage = pd.read_excel('data/hero_mage.xlsx')
magicItem = pd.read_excel('data/item_magic.xlsx')

st.subheader('Pilih Hero')
selected_hero = st.selectbox('-', heroMage['nama hero'])

hero = heroMage[heroMage['nama hero'] == selected_hero].iloc[0]

hero_type = hero['type hero'].strip().lower()
hero_attack_type = hero['attack type'].strip().lower()

nama_item = magicItem['nama item'].tolist()
cd_item = magicItem['cooldown reduction'].tolist()
power_item = magicItem['magic power'].tolist()
speed_item = magicItem['attack speed'].tolist()

jumlah_item = len(nama_item)

limitSpeed = 20

if (hero_type == 'burst'):
    limitCd = 30
elif (hero_type == 'cd'):
    limitCd = 25
else:
    limitCd = 25


bestCombo = ["", "", ""]
bestCd = -1
bestPower = -1


if (hero_attack_type == 'basic attack'):

    for i in range(jumlah_item):
        if (
            speed_item[i] > 0 and
            speed_item[i] <= limitSpeed
        ):

            for j in range(jumlah_item):
                if (
                    j != i and
                    speed_item[j] == 0
                ):

                    for k in range(jumlah_item):
                        if (
                            k != i and
                            k != j and
                            speed_item[k] == 0
                        ):

                            total_cd = (
                                cd_item[i] +
                                cd_item[j] +
                                cd_item[k]
                            )

                            total_power = (
                                power_item[i] +
                                power_item[j] +
                                power_item[k]
                            )

                            kondisi_normal = (
                                total_cd <= limitCd
                            )

                            kondisi_power_only = (
                                cd_item[j] == 0 and
                                cd_item[k] == 0
                            )

                            if (kondisi_normal or kondisi_power_only):
                                if (
                                    total_cd > bestCd or
                                    (
                                        total_cd == bestCd and
                                        total_power > bestPower
                                    )
                                ):
                                    bestCd = total_cd
                                    bestPower = total_power
                                    bestCombo[0] = nama_item[i]
                                    bestCombo[1] = nama_item[j]
                                    bestCombo[2] = nama_item[k]


elif (hero_attack_type == 'skill'):

    for i in range(jumlah_item):
        if (speed_item[i] == 0):

            for j in range(jumlah_item):
                if (
                    j != i and
                    speed_item[j] == 0
                ):

                    for k in range(jumlah_item):
                        if (
                            k != i and
                            k != j and
                            speed_item[k] == 0
                        ):

                            total_cd = (
                                cd_item[i] +
                                cd_item[j] +
                                cd_item[k]
                            )

                            total_power = (
                                power_item[i] +
                                power_item[j] +
                                power_item[k]
                            )

                            kondisi_normal = (
                                total_cd <= limitCd
                            )

                            kondisi_power_only = (
                                cd_item[i] == 0 and
                                cd_item[j] == 0 and
                                cd_item[k] == 0
                            )

                            if (kondisi_normal or kondisi_power_only):
                                if (
                                    total_cd > bestCd or
                                    (
                                        total_cd == bestCd and
                                        total_power > bestPower
                                    )
                                ):
                                    bestCd = total_cd
                                    bestPower = total_power
                                    bestCombo[0] = nama_item[i]
                                    bestCombo[1] = nama_item[j]
                                    bestCombo[2] = nama_item[k]

st.write('Hero :', selected_hero)
st.write('Kombinasi item terpilih :')

for item in bestCombo:
    st.write('-', item)
