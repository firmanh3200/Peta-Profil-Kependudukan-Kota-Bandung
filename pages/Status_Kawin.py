import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import requests

st.set_page_config(layout='wide')

geojson_data = requests.get(
    "https://raw.githubusercontent.com/firmanh3200/batas-administrasi-indonesia/refs/heads/master/Kecamatan/kecamatan3273.json"
).json()

data = pd.read_csv(
    'data/status_kawin.csv', sep=',',
    dtype={'KODE_KEC':'str', 'jumlah_penduduk':'float'}
)
#data = data.rename(columns={'KODE_KD':'kodedesa'})

#filter_data = data.query("bps_nama_kecamatan == 'CIBEUNYING KIDUL' and tahun == 2023 and semester == 1")

st.title("Peta Profil Kependudukan Kota Bandung")
kol1,kol2 = st.columns(2)
with kol1:
    st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-penduduk-kota-bandung-berdasarkan-status-kawin")
with kol2:
    st.link_button("Sumber Peta", url="https://github.com/Alf-Anas/batas-administrasi-indonesia") 
st.subheader("", divider='rainbow')

with st.container(border=True):
    kolom1, kolom2, kolom3 = st.columns(3)
    data = data.sort_values(by=['tahun', 'semester'], ascending=[False, True])
    pilihantahun = data['tahun'].unique()
    pilihansem = data['semester'].unique()
    
    with kolom1:
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
    
    with kolom2:
        semterpilih = st.selectbox("Filter Semester", pilihansem)
        
    with kolom3:
        pilihanjenis = data[(data['tahun'] == tahunterpilih) & (data['semester'] == semterpilih)]['status_kawin'].unique()
        jenisterpilih = st.selectbox("Filter Status", pilihanjenis)
        
    if tahunterpilih and semterpilih and jenisterpilih:
        st.subheader(f"Sebaran Penduduk :green[ Berstatus {jenisterpilih}] di Kota Bandung, :blue[Semester {semterpilih} Tahun {tahunterpilih}]")

        fig = px.choropleth_mapbox(
            data_frame=data[(data['tahun'] == tahunterpilih) & (data['semester'] == semterpilih) & (data['status_kawin'] == jenisterpilih)],
            geojson=geojson_data,
            locations="KODE_KEC",
            color="jumlah_penduduk",
            color_continuous_scale="Viridis_r",
            opacity=0.7,
            featureidkey="properties.KODE_KEC",
            zoom=11,
            center={"lat": -6.914845, "lon": 107.609836},
            mapbox_style="carto-positron",
            hover_name="kemendagri_nama_kecamatan",
            hover_data=['kemendagri_nama_kecamatan', 'tahun', 'semester', 'status_kawin', 'jumlah_penduduk']
        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

st.subheader("", divider='rainbow')

with st.container(border=True):
    filter_data = data[(data['tahun'] == tahunterpilih) & (data['semester'] == semterpilih) & (data['status_kawin'] == jenisterpilih)]
    fig2 = px.sunburst(filter_data, path=['bps_nama_kabupaten_kota', 'kemendagri_nama_kecamatan'],
                      values='jumlah_penduduk',
                      hover_name='status_kawin')
    
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.plotly_chart(fig2, use_container_width=True)

