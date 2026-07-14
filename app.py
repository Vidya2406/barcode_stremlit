import streamlit as st
import cv2
import numpy as np
import pandas as pd

from database import (
    add_scan,
    get_history,
    delete_scan,
    clear_history,
    search_history,
    statistics
)

from utils import (
    dashboard_title,
    load_css,
    show_metrics,
    pie_chart,
    bar_chart,
    recent_activity,
    display_history,
    download_csv,
    search_box,
    section
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="ScanVibe",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

dashboard_title()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.image(
    "https://img.icons8.com/color/96/qr-code.png",
    width=80
)

st.sidebar.title("📷 ScanVibe")

page = st.sidebar.radio(
    "Navigation",
    [
        "📷 Scanner",
        "📜 History",
        "📊 Dashboard"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **ScanVibe**

    QR Scanner built using

    ✅ Streamlit

    ✅ SQLite

    ✅ OpenCV
    """
)

# -------------------------------------------------
# Dashboard Statistics
# -------------------------------------------------

total_scans, qr_count, barcode_count = statistics()
