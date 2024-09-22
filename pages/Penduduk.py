import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import requests

st.set_page_config(layout='wide')

geojson_data = requests.get(
    "https://raw.githubusercontent.com/firmanh3200/batas-administrasi-indonesia/refs/heads/master/Kel_Desa/desa3273.json"
).json()

data = pd.read_csv(
    'data/jumlah_penduduk.csv', sep=',',
    dtype={'KODE_KD':'str', 'jumlah_penduduk':'float'}
)

datapenduduk = data.groupby(['kemendagri_nama_kecamatan', 'kemendagri_nama_desa_kelurahan', 'KODE_KD', 'tahun', 'semester'])['jumlah_penduduk'].sum().reset_index()

st.title("Peta Profil Kependudukan Kota Bandung")
st.subheader("", divider='rainbow')

with st.container(border=True):
    kolom1, kolom2, kolom3 = st.columns(3)
    datapenduduk = datapenduduk.sort_values(by=['tahun', 'semester'], ascending=[False, True])
    pilihantahun = datapenduduk['tahun'].unique()
    pilihansem = datapenduduk['semester'].unique()
    
    with kolom1:
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
    
    with kolom2:
        semterpilih = st.selectbox("Filter Semester", pilihansem)
            
    if tahunterpilih and semterpilih:
        st.subheader(f"Sebaran Penduduk di Kota Bandung, :blue[Semester {semterpilih} Tahun {tahunterpilih}]")

        fig = px.choropleth_mapbox(
            data_frame=datapenduduk[(datapenduduk['tahun'] == tahunterpilih) & (datapenduduk['semester'] == semterpilih)],
            geojson=geojson_data,
            locations="KODE_KD",
            color="jumlah_penduduk",
            color_continuous_scale="Viridis_r",
            opacity=0.7,
            featureidkey="properties.KODE_KD",
            zoom=11,
            center={"lat": -6.914845, "lon": 107.609836},
            mapbox_style="carto-positron",
            hover_name="kemendagri_nama_desa_kelurahan",
            hover_data=['kemendagri_nama_kecamatan', 'kemendagri_nama_desa_kelurahan', 'tahun', 'semester', 'jumlah_penduduk']
        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

    kol1, kol2, kol3 = st.columns(3)
    with kol1:
        st.warning("Referensi")
    with kol2:
        st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-penduduk-kota-bandung-berdasarkan-jenis-kelamin-2")
    with kol3:
        st.link_button("Sumber Peta", url="https://github.com/Alf-Anas/batas-administrasi-indonesia") 

st.subheader("", divider='rainbow')