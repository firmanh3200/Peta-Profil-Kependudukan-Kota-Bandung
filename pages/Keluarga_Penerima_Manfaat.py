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
    'data/kpm_bansos.csv', sep=',',
    dtype={'KODE_KEC':'str', 
           #'usia_tahun':'str', 
           'jumlah_kpm':'float'}
)

st.title("Peta Profil Kependudukan Kota Bandung")
kol1,kol2 = st.columns(2)
with kol1:
    st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-keluarga-penerima-manfaat-kpm-bansos-di-kota-bandung-2")
with kol2:
    st.link_button("Sumber Peta", url="https://github.com/Alf-Anas/batas-administrasi-indonesia") 
st.subheader("", divider='rainbow')

with st.container(border=True):
    kolom1, kolom2, kolom3 = st.columns(3)
    data = data.sort_values(by=['tahun', 'jenis_bansos'], ascending=[False, True])
    pilihantahun = data['tahun'].unique()
    
    with kolom1:
        st.warning("Silakan melakukan Filter Data")
    
    with kolom2:
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
    
    with kolom3:
        pilihanjenis = data[(data['tahun'] == tahunterpilih)]['jenis_bansos'].unique()
        jenisterpilih = st.selectbox("Filter Jenis Bantuan Sosial", pilihanjenis)
        
    if tahunterpilih and jenisterpilih:
        st.subheader(f"Sebaran Keluarga :green[ Penerima {jenisterpilih}] di Kota Bandung, :blue[Tahun {tahunterpilih}] (KK)")

        fig = px.choropleth_mapbox(
            data_frame=data[(data['tahun'] == tahunterpilih) &  (data['jenis_bansos'] == jenisterpilih)],
            geojson=geojson_data,
            locations="KODE_KEC",
            color="jumlah_kpm",
            color_continuous_scale="Viridis_r",
            opacity=0.7,
            featureidkey="properties.KODE_KEC",
            zoom=11,
            center={"lat": -6.914845, "lon": 107.609836},
            mapbox_style="carto-positron",
            hover_name="kemendagri_nama_kecamatan",
            hover_data=['kemendagri_nama_kecamatan', 'tahun', 'jenis_bansos', 'jumlah_kpm']
        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

st.subheader("", divider='rainbow')

with st.container(border=True):
    filter_data = data[(data['tahun'] == tahunterpilih) & (data['jenis_bansos'] == jenisterpilih)]
    fig2 = px.sunburst(filter_data, path=['bps_nama_kabupaten_kota', 'kemendagri_nama_kecamatan'],
                      values='jumlah_kpm',
                      hover_name='jenis_bansos')
    
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.subheader(f"Sebaran Keluarga :green[ Penerima {jenisterpilih}] di Kota Bandung, :blue[Tahun {tahunterpilih}] (KK)")
    st.plotly_chart(fig2, use_container_width=True)