import streamlit as st
import geemap.foliumap as geemap
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
import ee

def show_map(year, color_palette):

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
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h2 style="margin: 0; text-align: center;">
            Biomass Distribution Map
        </h2>
        <h5 style="margin: 0 0 1rem 0; text-align: center;">
            Visualize, compare, and analyze aboveground biomass across years and color schemes
        </h5>
    </div>
    """, unsafe_allow_html=True)

    # Get feature collections
    try:
        AGBP_per_year_fc = ee.FeatureCollection('projects/seventh-program-460820-u1/assets/Cattien/AGBP_per_year')
        AGBP_Diff_per_year_fc = ee.FeatureCollection('projects/seventh-program-460820-u1/assets/Cattien/AGBP_Diff_per_year')
        RMSE_per_year_fc = ee.FeatureCollection('projects/seventh-program-460820-u1/assets/Cattien/RMSE_per_year')
    except Exception as e:
        st.error(f"Error loading FeatureCollections: {str(e)}")
        return

    # Convert to dataframes
    AGBP_per_year = fc_to_df(AGBP_per_year_fc, ['year', 'total_agb'])
    AGBP_Diff_per_year = fc_to_df(AGBP_Diff_per_year_fc, ['year', 'change'])
    RMSE_per_year = fc_to_df(RMSE_per_year_fc, ['year', 'rmse'])

    # Get palette colors
    palettes = {
        'Greens': ['f7fcf5', 'e5f5e0', 'c7e9c0', 'a1d99b', '74c476', '41ab5d', '238b45', '006d2c', '00441b'],
        'Viridis': px.colors.sequential.Viridis,
        'Plasma': px.colors.sequential.Plasma,
        'Earth': ['#f7f4f0', '#d4c5a9', '#a67c52', '#6b4423', '#3d2817']
    }

    st.markdown("""
    <div class="main-header">
        <h2 style="margin: 0; text-align: left;">
            Aboveground Biomass Distribution
        </h2>
    </div>
    """, unsafe_allow_html=True)


    # Map Visualization Control
    st.markdown("#### Map Visualization Control")
    years = [2021, 2022, 2023, 2024]
    selected_year = st.selectbox('Year', years, index=years.index(year) if year in years else 0, key="map_year_select")
    col1, col2 = st.columns([3.3, 0.7])
    
    with col1:
        # Interactive Map
        display_map(selected_year, palettes[color_palette])
    
    with col2:
        # Top: Statistics
        st.subheader("Statistics")
        st.markdown("""
        <style>
        /* Reduce gap above metric */
        [data-testid="stMetric"] {
            margin-top: -1.5rem !important;
            margin-bottom: rem !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        /* Make st.metric value font smaller */
        [data-testid="stMetricValue"] {
            font-size: 1.7rem !important;  /* Adjust as needed (e.g., 1.2rem, 1rem) */
            font-weight: 600 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        display_stats(selected_year)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Bottom: Model Performance
        st.subheader("Model Performance")
        
        # Load observed vs predicted data for the year
        try:
            obs_pred_df = load_observed_vs_predicted(selected_year)
            rmse_row = RMSE_per_year[RMSE_per_year['year'] == selected_year]
            
            if not rmse_row.empty and not obs_pred_df.empty:
                rmse_val = rmse_row.iloc[0]['rmse']
                mean_obs = obs_pred_df['agbd'].mean()
                error_pct = (rmse_val / mean_obs) * 100 if mean_obs != 0 else 0
        
                # Create donut chart
                donut_chart = make_donut(error_pct)
                st.altair_chart(donut_chart, use_container_width=False)
            else:
                st.info("No RMSE or observed data for this year.")
        except Exception as e:
            st.error(f"Error loading performance data: {str(e)}")

    # Custom CSS untuk tab: aktif tetap, tidak aktif transparan, font besar
    st.markdown("""
    <style>
    /* Semua tab: border di seluruh sisi, font besar, padding lega */
    .stTabs [role="tab"] {
        border: 2.5px solid #b6a89d !important;
        border-bottom: none !important;
        border-radius: 0 !important;
        margin-right: -2.5px; /* agar border tengah tidak double */
        padding: 16px 38px 16px 38px !important;
        background-color: transparent !important;
        position: relative;
        z-index: 2;
        transition: background 0.2s;
    }
    /* Tab tidak aktif: transparan, font besar */
    .stTabs [role="tab"]:not([aria-selected="true"]) {
        background-color: transparent !important;
        color: #b6a89d !important;
        border-radius: 0;
        border: none !important;
        margin-bottom: 4px;
    }
    /* Tab aktif: warna highlight, font besar */
    .stTabs [role="tab"][aria-selected="true"] {
        background: rgba(60, 90, 60, 0.5) !important;
        color: #a04a1a !important;
        border-radius: 0;
        border: none !important;
        margin-bottom: 5px;
    }

    /* Ukuran font tab label */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.6rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: bold !important;
        line-height: 1.4;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Tab navigasi
    tab1, tab2, tab3 = st.tabs(["Total Aboveground Biomass", "Model RMSE", "Biomass Distribution"])

    with tab1:
        st.subheader("Total Aboveground Biomass 2021 - 2024", help= "The total mass of living vegetation above the ground surface within Cattien National Park area")
        col1, col2 = st.columns([1,1])
        with col1:
            if not AGBP_per_year.empty:
                fig1 = px.line(
                    AGBP_per_year.sort_values('year'),
                    x='year', y='total_agb', markers=True,
                    labels={'total_agb': 'AGB (ton)', 'year': 'Year'},
                    title=' '
                )
                fig1.update_traces(line=dict(color='#9ACD32', width=3), marker=dict(size=8))
                fig1.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=18),
                    title=dict(font=dict(size=24)),
                    xaxis=dict(
                        type='category', 
                        showgrid=False, 
                        tickfont=dict(size=16),
                        title=dict(font=dict(size=18))  # Perbaikan: gunakan title=dict(font=dict())
                    ),
                    yaxis=dict(
                        showgrid=False, 
                        tickfont=dict(size=16),
                        title=dict(font=dict(size=18))  # Perbaikan: gunakan title=dict(font=dict())
                    ),
                    height=350,
                    margin=dict(l=30, r=30, t=40, b=30)
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.warning("Data Total Aboveground Biomass tidak tersedia.")

    with tab3:
        st.subheader("Aboveground Biomass Distribution", help="Histogram of AGB (ton/ha) values for all pixels in Cát Tiên region")
        try:
            agb_img = ee.Image(f'projects/seventh-program-460820-u1/assets/Cattien/agb_{selected_year}').select('agbd')
            geometry = ee.FeatureCollection('projects/seventh-program-460820-u1/assets/Cat_tien_ranh_gioi').geometry()
            # Lấy giá trị pixel về dưới dạng list (giới hạn 5000 pixel để tránh timeout)
            values = agb_img.sample(region=geometry, scale=100, geometries=False, numPixels=5000).aggregate_array('agbd').getInfo()
            import numpy as np
            import plotly.figure_factory as ff
            if values and len(values) > 0:
                values = [v for v in values if v is not None]
                hist_fig = ff.create_distplot([values], group_labels=["AGB (ton/ha)"], bin_size=10, show_rug=False)
                hist_fig.update_layout(
                    title=f"AGB Distribution (Histogram) {selected_year}",
                    xaxis_title="AGB (ton/ha)",
                    yaxis_title="Pixel Count",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=16),
                    height=350
                )
                st.plotly_chart(hist_fig, use_container_width=True)
            else:
                st.warning("Không có dữ liệu AGB để hiển thị histogram.")
        except Exception as e:
            st.error(f"Không thể hiển thị histogram: {str(e)}")

    with tab2:
        st.subheader("Model RMSE 2021 - 2024",
                     help= "Predictive accuracy measure that calculates the average difference between predicted and actual values.")
        col1, col2 = st.columns([1,1])
        with col1:
            if not RMSE_per_year.empty:
                fig2 = px.line(
                    RMSE_per_year.sort_values('year'),
                    x='year', y='rmse', markers=True,
                    labels={'rmse': 'RMSE (ton/Ha)', 'year': 'Year'},
                    title=' '
                )
                fig2.update_traces(line=dict(color='#9ACD32', width=3), marker=dict(size=8))
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=18),
                    title=dict(font=dict(size=24)),
                    xaxis=dict(
                        type='category', 
                        showgrid=False, 
                        tickfont=dict(size=16),
                        title=dict(font=dict(size=18))  # Perbaikan: gunakan title=dict(font=dict())
                    ),
                    yaxis=dict(
                        showgrid=False, 
                        tickfont=dict(size=16),
                        title=dict(font=dict(size=18))  # Perbaikan: gunakan title=dict(font=dict())
                    ),
                    height=350,
                    margin=dict(l=30, r=30, t=40, b=30)
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Data RMSE tidak tersedia.")

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
    
# --- FeatureCollection to DataFrame ---
@st.cache_data
def fc_to_df(_feature_collection, properties):
    try:
        features = _feature_collection.getInfo()['features']
        data = [{prop: f['properties'].get(prop, None) for prop in properties} for f in features]
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Error converting FeatureCollection to DataFrame: {str(e)}")
        return pd.DataFrame()

# --- Year-specific FeatureCollections ---
@st.cache_data
def load_agb(year: int):
    try:
        asset_id = f'projects/seventh-program-460820-u1/assets/Cattien/agb_{year}'
        return ee.Image(asset_id).select('agbd')
    except Exception as e:
        st.error(f"Error loading AGB data for year {year}: {str(e)}")
        return None

@st.cache_data
def load_observed_vs_predicted(year):
    try:
        # Định nghĩa asset_id cho từng năm, cần đúng tên asset đã export trên GEE
        asset_id = f'projects/seventh-program-460820-u1/assets/Cattien/Observed_vs_Predicted_{year}'
        fc = ee.FeatureCollection(asset_id)
        return fc_to_df(fc, ['agbd', 'agbd_predicted'])
    except Exception as e:
        st.error(f"Error loading observed vs predicted data for year {year}: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def get_tanjung_puting_geometry():
    # Lấy geometry từ asset Cat_tien_ranh_gioi giống script GEE
    return ee.FeatureCollection('projects/seventh-program-460820-u1/assets/Cat_tien_ranh_gioi').geometry()

def display_map(year, palette):
    try:
        agb_layer = load_agb(year)
        if agb_layer is None:
            st.error(f"AGB data for {year} not available")
            return
            
        # Lấy geometry Cat Tien từ asset giống script GEE
        cat_tien_geom = ee.FeatureCollection('projects/seventh-program-460820-u1/assets/Cat_tien_ranh_gioi').geometry()
        centroid = cat_tien_geom.centroid().coordinates().getInfo()
        # centroid trả về [lon, lat]
        vis_params = {
            'min': 0,
            'max': 300,
            'palette': palette,
            'bands': ['agbd']
        }
        Map = geemap.Map(center=[centroid[1], centroid[0]], zoom=11)
        Map.addLayer(agb_layer, vis_params, f'AGB {year}')
        Map.add_colorbar(vis_params, label="AGB (ton/Ha)")
        Map.to_streamlit(height=750)
        
    except Exception as e:
        st.error(f"Error displaying map: {str(e)}")

def display_stats(year):
    """Display statistics for selected year"""
    try:
        agb_layer = load_agb(year)
        if agb_layer is None:
            st.error(f"AGB data for {year} not available")
            return
            
        geometry = get_tanjung_puting_geometry()
        
        stats = agb_layer.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                ee.Reducer.min(), '', True
            ).combine(
                ee.Reducer.max(), '', True
            ),
            geometry=geometry,
            scale=100,
            maxPixels=1e10
        ).getInfo()
        
        agb_mean = stats.get('agbd_mean', 0)
        if agb_mean is None:
            agb_mean = 0
        st.metric(label=f"Average AGB {year}", 
                  value=f"{agb_mean:.1f} ton/ha",
                  help="Average aboveground biomass value per hectare (Density)")
        
    except Exception as e:
        st.error(f"Error calculating stats: {str(e)}")

def make_donut(error_pct):
    source = pd.DataFrame({
        "category": ['Error', 'Accuracy'],
        "value": [error_pct, 100 - error_pct],
        "color": ['#E74C3C', '#4CAF50']
    })
    
    # Chart tanpa .configure() di level individual
    chart = alt.Chart(source).mark_arc(
        innerRadius=40,
        outerRadius=70
    ).encode(
        theta=alt.Theta('value:Q'),
        color=alt.Color(
            'category:N',
            scale=alt.Scale(
                domain=['Error', 'Accuracy'],
                range=['#E74C3C', '#4CAF50']
            ),
            legend=None
        )
    )
    
    text = alt.Chart(pd.DataFrame({'text': [f'{100-error_pct:.1f}%']})).mark_text(
        align='center',
        baseline='middle',
        fontSize=20,
        fontWeight='bold',
        color='#ffffff'
    ).encode(text='text:N')
    
    # Gabungkan chart dan konfigurasi di level LayerChart
    combined_chart = (chart + text).resolve_scale(color='independent')
    
    # Konfigurasi background transparan di level akhir
    return combined_chart.configure(
        background='transparent',
        view={'stroke': None}  # Hilangkan border
    ).properties(
        width=140,
        height=160
    )

    
