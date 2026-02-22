import streamlit as st
import os
import pdfplumber  # Make sure you clicked "Install Requirement" in PyCharm!

# 1. Setup Page Appearance
st.set_page_config(page_title="9618 P4 Practical Portal", layout="wide", page_icon="💻")

# 2. Folder Configuration
FOLDERS = {
    'Question_Paper': '9618pyp4_qp',
    'Mark_Scheme': '9618pyp4_ms',
    'TextFiles': '9618pyp4_txt',
    'Evidence_Doc': '9618pyp4_evi'
}


# --- NEW: SEARCH LOGIC ---
@st.cache_data  # This prevents the app from being slow every time someone searches
def search_inside_pdfs(keyword, folder_path):
    matches = []
    if not os.path.exists(folder_path):
        return matches

    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    for filename in files:
        path = os.path.join(folder_path, filename)
        try:
            with pdfplumber.open(path) as pdf:
                # Scans every page for the keyword
                for page in pdf.pages:
                    text = page.extract_text()
                    if text and keyword.lower() in text.lower():
                        matches.append(filename)
                        break
        except:
            continue
    return matches


# 3. Sidebar: Tutor Management Panel (Same as yours)
with st.sidebar:
    st.header("👩‍🏫 Tutor Control Panel")
    if st.text_input("Enter Admin Password", type="password") == "PTES9618":
        st.subheader("Upload New Paper")
        uploaded_file = st.file_uploader("Select file")
        target_folder = st.selectbox("Upload to category:", list(FOLDERS.keys()))

        if st.button("Save to Server"):
            if uploaded_file:
                save_path = os.path.join(FOLDERS[target_folder], uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Saved: {uploaded_file.name}")

# 4. Main Area
st.title("📚 PTES 9618 CS Paper 4 Hub")

# --- NEW: TOPIC SEARCH SECTION ---
st.subheader("🔍 Search by Topic (Content Search)")
st.info("This scans INSIDE all Question Papers (2021-2025) for your keyword.")
query = st.text_input("Enter a topic (e.g., Recursion, Linked List, Stack, Binary Tree)")

if query:
    with st.spinner(f"Reading papers to find '{query}'..."):
        results = search_inside_pdfs(query, FOLDERS['Question_Paper'])

    if results:
        st.success(f"Topic found in {len(results)} Question Papers:")
        for qp_file in results:
            with open(os.path.join(FOLDERS['Question_Paper'], qp_file), "rb") as f:
                st.download_button(f"⬇️ Get Paper: {qp_file}", f, file_name=qp_file, key=f"search_{qp_file}")
    else:
        st.warning("Keyword not found in any PDF content.")

st.divider()

# 5. Your Original Selection Logic (Still works!)
st.subheader("📅 Browse by Session")
col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("Examination Year", [2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
with col2:
    series = st.selectbox("Series/Session", ["June (s)", "November (w)"])
    s_code = series.split("(")[1][0]
with col3:
    variant = st.selectbox("Variant Number", [41, 42, 43])

year_short = str(year)[2:]
search_string = f"9618_{s_code}{year_short}_{variant}"
st.write(f"### Manual Selection: {search_string}")

for label, folder_path in FOLDERS.items():
    if os.path.exists(folder_path):
        all_files = os.listdir(folder_path)
        matching_files = [f for f in all_files if f.startswith(search_string)]

        if matching_files:
            for filename in matching_files:
                file_full_path = os.path.join(folder_path, filename)
                with open(file_full_path, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download {label}: {filename}",
                        data=f,
                        file_name=filename,
                        key=f"btn_{label}_{filename}"
                    )
        else:
            st.warning(f"No {label} files found.")
######################################################################
# --- FOOTER & VISITOR COUNTER ---
st.markdown("---")
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.write("✨ **PTES 9618 Resource Portal Tracking** ✨")

    # Custom HITS Badge with PTES Blue and PTES Green number
    st.markdown(
        "![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?"
        "url=https%3A%2F%2F9618-paper4-resources-bank.streamlit.app&"
        "count_bg=%234CAF50&"  # This is your PTES Green!
        "title_bg=%23003366&"  # This is your PTES Blue!
        "icon=&icon_color=%23E7E7E7&"
        "title=Total+Portal+Hits&"
        "edge_flat=false)"
    )

    # Adding Green to the colored text row
    st.markdown(
        "<div style='text-align: center; font-weight: bold; font-size: 18px;'>"
        "<span style='color: red;'>🔴 Academic Excellence</span> | "
        "<span style='color: #FFD700;'>🟡 Digital Integrity</span> | "
        "<span style='color: #0047AB;'>🔵 Future Readiness</span> | "
        "<span style='color: #2E8B57;'>🟢 Holistic Growth</span>"
        "</div>",
        unsafe_allow_html=True
    )

    st.caption("Proudly serving the students of Pusat Tingkatan Enam")
######################################################################


