import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import ee
import geemap.foliumap as geemap

def show_home():
    st.markdown("""
    <style>
    html, body, [class*="css"], .main, div, p, h1, h2, h3, h4, h5, h6, span, button, input {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.01em;
    }
    .main-header h2 {
        color: #238b45;
        font-weight: 700;
        margin-bottom: 0.2em;
    }
    .main-header h5 {
        color: #A9A9A9;
        font-weight: 400;
        margin-bottom: 1.2em;
    }
    .info-card {
        background: rgba(35,139,69,0.12);
        border-radius: 16px;
        padding: 1.5em 1.5em 1em 1.5em;
        margin-bottom: 1.5em;
        box-shadow: 0 2px 12px rgba(35,139,69,0.10);
    }
    .stats-col {
        background: #232323;
        border-radius: 14px;
        padding: 1.2em 1em 1em 1em;
        margin-left: 0.5em;
        color: #fff;
        box-shadow: 0 2px 12px rgba(35,139,69,0.10);
    }
    .stats-title {
        color: #A9A9A9;
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 0.7em;
        text-align: center;
    }
    .metric-label {
        font-size: 1.05em;
        color: #A9A9A9;
        margin-bottom: 0.2em;
    }
    .metric-value {
        font-size: 1.3em;
        color: #fff;
        font-weight: 700;
        margin-bottom: 0.7em;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h2 style="margin: 0; text-align: center;">
            Aboveground Biomass Monitoring<br>for Cattien National Park
        </h2>
        <h5 style="margin: 0 0 1rem 0; text-align: center;">
            Harnessing AI & Satellite Data for a Greener Vietnam
        </h5>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2.5, 1])
    with col1:
        st.markdown(
            """
            <style>
            .about-title { color: #238b45; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.7em; }
            .about-desc { color: #fff; font-size: 1.13rem; line-height: 1.7; margin-bottom: 0.7em; }
            .about-note { color: #fff; font-size: 1.13rem; line-height: 1.7; font-style: italic; }
            .about-card { background: rgba(35,139,69,0.12); border-radius: 16px; padding: 1.5em 1.5em 1em 1.5em; margin-bottom: 1.5em; box-shadow: 0 2px 12px rgba(35,139,69,0.10); }
            </style>
            <div class="about-card">
                <div class="about-title">About Biomass2025</div>
                <div class="about-desc">
                    Biomass2025 leverages advanced <b>Random Forest Machine Learning</b> and <b>Google Earth Engine</b> to estimate aboveground biomass density across <b>Cattien National Park</b>.<br><br>
                    Our mission is to empower forest conservation, enable data-driven decisions, and inspire sustainable land management through cutting-edge remote sensing technology.
                </div>
                <div class="about-note">
                    Join us in protecting Vietnam's natural heritage for generations to come.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("""
        <div class="stats-col" style="background: #232323; border-radius: 14px; padding: 1.2em 1em 1em 1em; margin-left: 0.5em; color: #fff; box-shadow: 0 2px 12px rgba(35,139,69,0.10);">
            <div class="stats-title" style="color: #fff; font-size: 1.1em; font-weight: 600; margin-bottom: 0.7em; text-align: center;">Project Highlights</div>
            <div class="metric-label" style="font-size: 1.05em; color: #A9A9A9; margin-bottom: 0.2em;">Area Coverage</div>
            <div class="metric-value" style="font-size: 1.3em; color: #fff; font-weight: 700; margin-bottom: 0.7em;">73,878 ha</div>
            <div class="metric-label" style="font-size: 1.05em; color: #A9A9A9; margin-bottom: 0.2em;">Model Accuracy</div>
            <div class="metric-value" style="font-size: 1.3em; color: #fff; font-weight: 700; margin-bottom: 0.7em;">80%+</div>
            <div class="metric-label" style="font-size: 1.05em; color: #A9A9A9; margin-bottom: 0.2em;">Years Analyzed</div>
            <div class="metric-value" style="font-size: 1.3em; color: #fff; font-weight: 700; margin-bottom: 0.7em;">2021–2024</div>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown("---")
    st.markdown("""
            <h3 style="color: #ffffff"; text-align: center; margin: 0;>
                How it Works</h3>
        """, unsafe_allow_html=True)
    
    steps = [
        ("01", "Data Acquisition", "Collecting Landsat and Sentinel-2 satellite data from Google Earth Engine."),
        ("02", "Data Processing", "Preprocessing and extraction of spectral and textural features."),
        ("03", "Machine Learning", "Training a Random Forest model with ground truth data."),
        ("04", "Prediction & Mapping", "Biomass prediction and visualization of results on an interactive map."),
        ("05", "Analysis & Monitoring", "Temporal analysis and monitoring of biomass trend.")
    ]
    
    cols = st.columns(len(steps))
    for i, (num, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 0;">
                <div style="background-color: rgba(60, 90, 60, 0.25); color: white; border-radius: 50%; 
                           width: 50px; height: 50px; display: flex; align-items: center; 
                           justify-content: center; margin: 1rem auto 1rem auto; font-weight: bold;">
                    {num}
                </div>
                <h5 style="color: #9ACD32; margin: 0;">{title}</h5>
                <p style="font-size: 0.8rem; opacity: 1;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
   
    st.markdown("---")
     # Sample chart
    st.markdown("### Biomass Trend")


    # 1. Chọn năm và load data AGB tương ứng
    years = [2021, 2022, 2023, 2024]
    selected_year = st.selectbox('Select AGB year:', years, index=0)
    agb_layer = load_layer(f'projects/seventh-program-460820-u1/assets/Cattien/agb_{selected_year}')
    agb_trend = load_layer('projects/seventh-program-460820-u1/assets/Cattien/gedi_trend_2021_2024')

    # 2. Parameter visualisasi yang sesuai dengan GEE
    vis_params_agb_2021 = {
    'bands': 'agbd',
    'min': 0,
    'max': 300,
    'palette': px.colors.sequential.Viridis
    }

    vis_params_agb_trend = {
        'bands': 'agbd',
        'min': -20,
        'max': 5,
        'palette': ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60']
    }

    # 3. Buat peta split-panel
    # Lấy geometry Cat Tien từ asset giống script GEE
    cat_tien_geom = ee.FeatureCollection('projects/seventh-program-460820-u1/assets/Cat_tien_ranh_gioi').geometry()
    centroid = cat_tien_geom.centroid().coordinates().getInfo()
    # centroid trả về [lon, lat]
    Map = geemap.Map(center=[centroid[1], centroid[0]], zoom=11)
    
    # Tambahkan layer với parameter visualisasi
    left_layer = geemap.ee_tile_layer(agb_layer, vis_params_agb_2021, f'AGB {selected_year}')
    right_layer = geemap.ee_tile_layer(agb_trend, vis_params_agb_trend, 'Trend AGB')
    
    # Split map
    Map.split_map(left_layer, right_layer)
    
    # Tambahkan legenda
    Map.add_colorbar(vis_params_agb_2021, label=f'AGB {selected_year} (ton/ha)', position='topright')
    Map.add_colorbar(vis_params_agb_trend, label='Trend AGB 2021-2024 (ton/ha/year)', position='bottomright')

    # Buat 3 kolom: kiri, tengah, kanan
    col1, col2, col3 = st.columns([0.5, 5, 0.5])

    with col2:
        Map.to_streamlit(height=950)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; 
                background-color: rgba(60, 90, 60, 0.25); border-radius: 0px;">
        <p style="margin: 0; opacity: 0.7;">
            © 2025 | BIOMASS2025<br>
            Aboveground Biomass Monitoring System — Developed for academic research purposes.<br>
            Authors: Nguyen Van Quy, Dinh Ba Duy, Bui Manh Hung, Vu Manh, Vu Trong Hieu, and Nguyen Hong Hai.
        </p>
    </div>
    """, unsafe_allow_html=True)


def load_layer(asset_id):
    try:
        return ee.Image(asset_id)
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        return None
