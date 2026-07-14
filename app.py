import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode

from database import (
    add_scan,
    get_history,
    clear_history,
    search_history,
    statistics,
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
    section,
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="ScanVibe",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()
dashboard_title()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/qr-code.png", width=80)
st.sidebar.title("📷 ScanVibe")
page = st.sidebar.radio("Navigation", ["📷 Scanner", "📜 History", "📊 Dashboard"])
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **ScanVibe**
    QR & Barcode Scanner built using
    ✅ Streamlit
    ✅ SQLite
    ✅ pyzbar
    """
)


def decode_image(image: Image.Image):
    """Decode all QR codes / barcodes found in a PIL image."""
    results = []
    for r in decode(image):
        content = r.data.decode("utf-8", errors="replace")
        symbology = r.type  # e.g. QRCODE, EAN13, CODE128, UPCA...
        category = "QR Code" if symbology == "QRCODE" else "Barcode"
        results.append({"content": content, "category": category, "format": symbology})
    return results


def handle_results(results):
    if not results:
        st.warning("No QR code or barcode detected. Try better lighting, focus, or a closer shot.")
        return
    seen = set()
    for r in results:
        if r["content"] in seen:
            continue
        seen.add(r["content"])
        st.success(f"**{r['category']}** ({r['format']}) detected:")
        st.code(r["content"])
        add_scan(r["content"], r["category"], r["format"])
    st.toast("Saved to history ✅")


# -------------------------------------------------
# Scanner Page
# -------------------------------------------------
if page == "📷 Scanner":
    section("Scan a Code")
    st.caption("Works with QR codes and most 1D barcodes (EAN, UPC, CODE128, etc.)")

    tab1, tab2 = st.tabs(["📸 Use Camera", "🖼️ Upload Image"])

    with tab1:
        img_file = st.camera_input("Take a picture", key="camera")
        if img_file is not None:
            image = Image.open(img_file)
            handle_results(decode_image(image))

    with tab2:
        uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "webp"])
        if uploaded is not None:
            image = Image.open(uploaded)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            handle_results(decode_image(image))

# -------------------------------------------------
# History Page
# -------------------------------------------------
elif page == "📜 History":
    section("Scan History")

    query = search_box()
    history = search_history(query) if query else get_history()

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        download_csv(history)
    with col2:
        if st.button("🧹 Clear All"):
            st.session_state["confirm_clear"] = True

    if st.session_state.get("confirm_clear"):
        st.warning("This will permanently delete all scan history. Are you sure?")
        c1, c2 = st.columns([1, 1])
        if c1.button("✅ Yes, clear it"):
            clear_history()
            st.session_state["confirm_clear"] = False
            st.rerun()
        if c2.button("Cancel"):
            st.session_state["confirm_clear"] = False
            st.rerun()

    st.markdown(f"**{len(history)}** result(s)")
    display_history(history)

# -------------------------------------------------
# Dashboard Page
# -------------------------------------------------
elif page == "📊 Dashboard":
    total_scans, qr_count, barcode_count = statistics()
    history = get_history()

    show_metrics(total_scans, qr_count, barcode_count)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section("Scan Type Breakdown")
        pie_chart(qr_count, barcode_count)
    with col2:
        section("Daily Scan Activity")
        bar_chart(history)

    st.markdown("---")
    recent_activity(history)
