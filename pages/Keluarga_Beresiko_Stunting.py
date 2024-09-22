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
    'data/resiko_stunting.csv', sep=',',
    dtype={'KODE_KEC':'str', 'jumlah':'float'}
)

st.title("Peta Profil Kependudukan Kota Bandung")
st.subheader("", divider='rainbow')

with st.container(border=True):
    kolom1, kolom2, kolom3 = st.columns(3)
    data = data[data['kategori'] == 'BERESIKO STUNTING']
    data = data.sort_values(by='tahun', ascending=False)
    pilihantahun = data['tahun'].unique()
    
    with kolom1:
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
            
    if tahunterpilih:
        st.subheader(f"Sebaran Keluarga Beresiko Stunting di Kota Bandung, Tahun {tahunterpilih} (KK)")
        fig = px.choropleth_mapbox(
            data_frame=data[(data['tahun'] == tahunterpilih)],
            geojson=geojson_data,
            locations="KODE_KEC",
            color="jumlah",
            color_continuous_scale="Viridis_r",
            opacity=0.7,
            featureidkey="properties.KODE_KEC",
            zoom=11,
            center={"lat": -6.914845, "lon": 107.609836},
            mapbox_style="carto-positron",
            hover_name="kemendagri_nama_kecamatan",
            hover_data=['kemendagri_nama_kecamatan', 'tahun', 'jumlah']
        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

kol1,kol2 = st.columns(2)
with kol1:
    st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-keluarga-beresiko-dan-tidak-beresiko-stunting-berdasarkan-kecamatan-di-kota-bandung")
with kol2:
    st.link_button("Sumber Peta", url="https://github.com/Alf-Anas/batas-administrasi-indonesia") 
st.subheader("", divider='rainbow')

with st.container(border=True):
    filter_data = data[(data['tahun'] == tahunterpilih)]
    fig2 = px.sunburst(filter_data, path=['bps_nama_kabupaten_kota', 'kemendagri_nama_kecamatan'],
                      values='jumlah',
                      hover_data='tahun')
    
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.plotly_chart(fig2, use_container_width=True)