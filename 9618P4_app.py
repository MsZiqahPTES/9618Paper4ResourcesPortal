import streamlit as st
import os

# 1. Setup Page Appearance
st.set_page_config(page_title="9618 P4 Practical Portal", layout="wide", page_icon="💻")

# 2. Folder Configuration (Matches your updated PyCharm folders)
FOLDERS = {
    'Question_Paper(9618_s/wYY_4v)': '9618pyp4_qp',
    'Mark_Scheme(9618_s/wYY_4v)': '9618pyp4_ms',
    'TextFiles(9618_s/wYY_4v_TXT)': '9618pyp4_txt',
    'Evidence_Doc(9618_s/wYY_4v_evidence)': '9618pyp4_evi'
}

# 3. Sidebar: Tutor Management Panel
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

# 4. Main Area: Student Download Portal
st.title("📚 PTES 9618 CS Paper 4 Hub")
st.info("Select your exam details below to download the required files.")

# Selection Columns
col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("Examination Year", [2021, 2022, 2023, 2024, 2025])
with col2:
    series = st.selectbox("Series/Session", ["June (s)", "November (w)"])
    s_code = series.split("(")[1][0]  # Extracts 's', 'w', or 'm'
with col3:
    variant = st.selectbox("Variant Number", [41, 42, 43])

st.divider()

# 5. Simplified File Discovery Logic
year_short = str(year)[2:]
# The standard search string, e.g., "9618_s21_42"
search_string = f"9618_{s_code}{year_short}_{variant}"

st.write(f"### Available Resources for {search_string}")

for label, folder_path in FOLDERS.items():
    if os.path.exists(folder_path):
        all_files = os.listdir(folder_path)

        # We look for ANY file in that folder that starts with our search string
        matching_files = [f for f in all_files if f.startswith(search_string)]

        if matching_files:
            for filename in matching_files:
                file_full_path = os.path.join(folder_path, filename)
                with open(file_full_path, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download {label}: {filename}",
                        data=f,
                        file_name=filename,
                        key=f"btn_{label}_{filename}"  # Unique key
                    )
        else:
            st.warning(f"No {label} files found.")