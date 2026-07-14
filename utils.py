import streamlit as st
import pandas as pd
import altair as alt


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #0f0f1a 0%, #16213e 100%);
        }
        h1, h2, h3, h4 {
            font-family: 'Segoe UI', sans-serif;
        }
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 12px 8px;
        }
        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 14px;
        }
        code {
            word-break: break-all;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def dashboard_title():
    st.markdown(
        "<h1 style='text-align:center; margin-bottom:0;'>📷 ScanVibe</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:gray; margin-top:0;'>Smart QR & Barcode Scanner</p>",
        unsafe_allow_html=True,
    )


def section(title: str):
    st.markdown(f"### {title}")


def show_metrics(total, qr_count, barcode_count):
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scans", total)
    col2.metric("QR Codes", qr_count)
    col3.metric("Barcodes", barcode_count)


def pie_chart(qr_count, barcode_count):
    if qr_count + barcode_count == 0:
        st.info("No scans yet — pie chart will appear once you scan something.")
        return
    df = pd.DataFrame({"Type": ["QR Code", "Barcode"], "Count": [qr_count, barcode_count]})
    chart = (
        alt.Chart(df)
        .mark_arc(innerRadius=70)
        .encode(
            theta=alt.Theta("Count:Q"),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(domain=["QR Code", "Barcode"], range=["#6C5CE7", "#00CEC9"]),
                legend=alt.Legend(title=None),
            ),
            tooltip=["Type", "Count"],
        )
        .properties(height=300)
    )
    st.altair_chart(chart, use_container_width=True)


def bar_chart(history):
    if not history:
        st.info("No scan activity yet.")
        return
    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    daily = df.groupby("date").size().reset_index(name="scans")
    chart = (
        alt.Chart(daily)
        .mark_bar(color="#6C5CE7", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("scans:Q", title="Scans"),
            tooltip=["date", "scans"],
        )
        .properties(height=300)
    )
    st.altair_chart(chart, use_container_width=True)


def recent_activity(history, limit=5):
    section("🕓 Recent Activity")
    if not history:
        st.info("No scans yet.")
        return
    for item in history[:limit]:
        st.markdown(f"**{item['type']}** — `{item['content']}`")
        st.caption(item["timestamp"])
        st.divider()


def display_history(history):
    from database import delete_scan

    if not history:
        st.info("No history to show.")
        return
    for item in history:
        with st.container(border=True):
            c1, c2 = st.columns([6, 1])
            with c1:
                label = item["type"]
                if item.get("format"):
                    label += f" · {item['format']}"
                st.markdown(f"**{label}**")
                st.code(item["content"])
                st.caption(item["timestamp"])
            with c2:
                if st.button("🗑️", key=f"del_{item['id']}"):
                    delete_scan(item["id"])
                    st.rerun()


def download_csv(history):
    if not history:
        st.button("⬇️ Download CSV", disabled=True)
        return
    df = pd.DataFrame(history)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "scan_history.csv", "text/csv")


def search_box():
    return st.text_input("🔍 Search history", placeholder="Search by content, type, or format...")
