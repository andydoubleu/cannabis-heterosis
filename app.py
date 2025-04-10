import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime

# === App Setup ===
st.set_page_config(page_title="Atlas Lab | Cannabis Heterosis Predictor", layout="wide")

# === Atlas Lab Custom Styling ===
custom_css = """
<style>
/* Background and text */
body {
    background-color: #f9f9f9;
    color: #333333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Headers */
h1, h2, h3, h4 {
    color: #4b6043;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Footer */
footer {
    visibility: hidden;
}

/* Expander styling */
.streamlit-expanderHeader {
    font-weight: bold;
    color: #4b6043;
}

/* Buttons */
button[kind="primary"] {
    background-color: #76c893;
    color: white;
    border-radius: 8px;
}

/* Charts */
.css-1r6slb0 e1tzin5v2 {
    background-color: white;
    border-radius: 12px;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Atlas Lab logo
st.image("atlas seed logo.png", width=120)

st.title("Atlas Lab: Cannabis Heterosis Predictor")
st.markdown("""
Welcome to **Atlas Lab**!

Upload genome CSV files for two parent strains to predict the potential level of heterosis in their progeny.

**File format requirements:**
- Must contain columns: `Marker ID`, `Reference Allele`, `Alternate Allele`, `Genotype`
""")

# === Strain name inputs ===
strain_col1, strain_col2 = st.columns(2)
with strain_col1:
    strain1_name = st.text_input("Enter Parent 1 Strain Name", value="Parent 1")
with strain_col2:
    strain2_name = st.text_input("Enter Parent 2 Strain Name", value="Parent 2")

# === File uploader ===
col1, col2 = st.columns(2)
with col1:
    parent1_file = st.file_uploader("Upload Parent 1 Genome CSV", type="csv", key="p1")
with col2:
    parent2_file = st.file_uploader("Upload Parent 2 Genome CSV", type="csv", key="p2")

# === Helper function ===
def parse_genotype(geno):
    if pd.isna(geno):
        return []
    return geno.split("/")

# === Main logic ===
if parent1_file and parent2_file:
    df1 = pd.read_csv(parent1_file)
    df2 = pd.read_csv(parent2_file)

    merged = pd.merge(df1, df2, on="Marker ID", suffixes=("_" + strain1_name, "_" + strain2_name))

    def predict_progeny(row):
        alleles_p1 = set(parse_genotype(row[f'Genotype_{strain1_name}']))
        alleles_p2 = set(parse_genotype(row[f'Genotype_{strain2_name}']))
        shared_alleles = alleles_p1.intersection(alleles_p2)

        if not shared_alleles:
            return "Heterozygous"
        elif len(alleles_p1.union(alleles_p2)) > 1:
            return "Heterozygous"
        else:
            return "Homozygous"

    merged['Predicted Progeny'] = merged.apply(predict_progeny, axis=1)

    # Add generation metadata
    merged.insert(0, "Generated By", "Atlas Lab")
    merged.insert(1, "Parent 1 Strain", strain1_name)
    merged.insert(2, "Parent 2 Strain", strain2_name)
    merged.insert(3, "Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    total_markers = len(merged)
    hetero_count = (merged['Predicted Progeny'] == "Heterozygous").sum()
    homo_count = (merged['Predicted Progeny'] == "Homozygous").sum()

    hetero_percent = (hetero_count / total_markers) * 100
    homo_percent = (homo_count / total_markers) * 100

    if hetero_percent > 75:
        heterosis_score = "High"
    elif hetero_percent > 40:
        heterosis_score = "Medium"
    else:
        heterosis_score = "Low"

    st.subheader(f"🔄 Prediction Summary for {strain1_name} × {strain2_name}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Markers Analyzed", total_markers)
    col2.metric("Heterozygous Markers", f"{hetero_count} ({hetero_percent:.1f}%)")
    col3.metric("Homozygous Markers", f"{homo_count} ({homo_percent:.1f}%)")
    col4.metric("Heterosis Score", heterosis_score)

    # Pie chart visualization
    st.subheader(f":bar_chart: Marker Heterozygosity Distribution for {strain1_name} × {strain2_name}")
    fig, ax = plt.subplots()
    ax.pie([hetero_count, homo_count], labels=['Heterozygous', 'Homozygous'], autopct='%1.1f%%', startangle=90, colors=['#76c893', '#f4a261'])
    ax.axis('equal')
    st.pyplot(fig)

    # Bar chart per chromosome
    st.subheader(f":dna: Marker Distribution per Chromosome for {strain1_name} × {strain2_name}")
    chrom_data = merged.groupby([f'Chromosome_{strain1_name}', 'Predicted Progeny']).size().unstack(fill_value=0)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    chrom_data.plot(kind='bar', stacked=True, ax=ax2, color=['#76c893', '#f4a261'])
    ax2.set_xlabel("Chromosome")
    ax2.set_ylabel("Number of Markers")
    ax2.set_title(f"Homozygous vs. Heterozygous Markers per Chromosome\n{strain1_name} × {strain2_name}")
    st.pyplot(fig2)

    # Detailed data table
    with st.expander("🔗 See detailed marker comparison"):
        st.dataframe(merged)

    # CSV export with timestamp in filename
    csv_buffer = io.StringIO()
    merged.to_csv(csv_buffer, index=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📥 Download Predictions as CSV",
        data=csv_buffer.getvalue(),
        file_name=f"{strain1_name}_{strain2_name}_heterosis_predictions_{timestamp}.csv",
        mime='text/csv'
    )

    st.success("Analysis complete! Check the visualizations, table, and download your results above.")

else:
    st.info("Please upload both genome CSV files to begin the analysis.")

# === Footer ===
st.markdown("""
---
<p style='text-align: center;'>Made with ❤️ by <a href='https://github.com/andydoubleu' target='_blank'>Atlas Lab</a></p>
""", unsafe_allow_html=True)
