import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------
# Download Scan History as CSV
# -----------------------------
def download_csv(df):
    """
    Displays a CSV download button.
    """

    if df.empty:
        st.warning("No scan history available.")
        return

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Scan History",
        data=csv,
        file_name="scan_history.csv",
        mime="text/csv"
    )


# -----------------------------
# Dashboard Metrics
# -----------------------------
def show_metrics(total, qr, barcode):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📊 Total Scans",
            value=total
        )

    with col2:
        st.metric(
            label="🔳 QR Codes",
            value=qr
        )

    with col3:
        st.metric(
            label="🏷️ Barcodes",
            value=barcode
        )


# -----------------------------
# Pie Chart
# -----------------------------
def pie_chart(qr, barcode):

    data = pd.DataFrame(
        {
            "Type": ["QR Code", "Barcode"],
            "Count": [qr, barcode]
        }
    )

    fig = px.pie(
        data,
        names="Type",
        values="Count",
        title="QR Codes vs Barcodes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------
# Bar Chart
# -----------------------------
def bar_chart(df):

    if df.empty:
        st.info("No data available.")
        return

    chart = (
        df.groupby("barcode_type")
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        chart,
        x="barcode_type",
        y="Count",
        color="barcode_type",
        title="Scans by Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------
# Recent Activity
# -----------------------------
def recent_activity(df):

    st.subheader("🕒 Recent Activity")

    if df.empty:
        st.info("No scan history available.")
        return

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True
    )


# -----------------------------
# Search Box
# -----------------------------
def search_box():

    keyword = st.text_input(
        "🔍 Search by QR Code / Barcode"
    )

    return keyword.strip()


# -----------------------------
# Display History
# -----------------------------
def display_history(df):

    if df.empty:
        st.warning("No records found.")
        return

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------
# Dashboard Header
# -----------------------------
def dashboard_title():

    st.title("📷 ScanVibe")

    st.caption(
        "QR & Barcode Scanner using Streamlit"
    )

    st.divider()


# -----------------------------
# Section Header
# -----------------------------
def section(title):

    st.markdown(f"## {title}")


# -----------------------------
# Custom CSS
# -----------------------------
def load_css():

    st.markdown(
        """
        <style>

        .stApp{
            background:#F8FAFC;
        }

        h1{
            color:#1E3A8A;
        }

        h2{
            color:#2563EB;
        }

        .stButton>button{
            width:100%;
            border-radius:10px;
            height:45px;
            font-size:16px;
            font-weight:bold;
        }

        .stDownloadButton>button{
            width:100%;
            border-radius:10px;
            height:45px;
            font-size:16px;
            font-weight:bold;
        }

        div[data-testid="metric-container"]{
            border-radius:15px;
            padding:15px;
            background:#FFFFFF;
            box-shadow:0px 2px 10px rgba(0,0,0,0.1);
        }

        </style>
        """,
        unsafe_allow_html=True
    )
