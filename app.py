import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cannabis Hybrid Vigor Predictor", layout="wide")

st.title("🌱 Cannabis Hybrid Vigor (Heterosis) Predictor")
st.markdown("""
Upload genome CSV files for two parent strains to predict the potential level of hybrid vigor in their progeny.

**File format requirements:**
- Must contain columns: `Marker ID`, `Reference Allele`, `Alternate Allele`, `Genotype`
""")

# File uploader
col1, col2 = st.columns(2)
with col1:
    parent1_file = st.file_uploader("Upload Parent 1 Genome CSV", type="csv", key="p1")
with col2:
    parent2_file = st.file_uploader("Upload Parent 2 Genome CSV", type="csv", key="p2")

def parse_genotype(geno):
    if pd.isna(geno):
        return []
    return geno.split("/")

if parent1_file and parent2_file:
    # Read the data
    df1 = pd.read_csv(parent1_file)
    df2 = pd.read_csv(parent2_file)

    # Merge on Marker ID
    merged = pd.merge(df1, df2, on="Marker ID", suffixes=("_p1", "_p2"))

    # Predict progeny heterozygosity
    def predict_progeny(row):
        alleles_p1 = set(parse_genotype(row['Genotype_p1']))
        alleles_p2 = set(parse_genotype(row['Genotype_p2']))
        shared_alleles = alleles_p1.intersection(alleles_p2)

        if not shared_alleles:
            return "Heterozygous"  # completely different alleles
        elif len(alleles_p1.union(alleles_p2)) > 1:
            return "Heterozygous"
        else:
            return "Homozygous"

    merged['Predicted Progeny'] = merged.apply(predict_progeny, axis=1)

    # Summary statistics
    total_markers = len(merged)
    hetero_count = (merged['Predicted Progeny'] == "Heterozygous").sum()
    homo_count = (merged['Predicted Progeny'] == "Homozygous").sum()

    hetero_percent = (hetero_count / total_markers) * 100
    homo_percent = (homo_count / total_markers) * 100

    # Real-time heterosis scoring
    if hetero_percent > 75:
        vigor_score = "High"
    elif hetero_percent > 40:
        vigor_score = "Medium"
    else:
        vigor_score = "Low"

    st.subheader("Prediction Summary")
    st.metric("Total Markers Analyzed", total_markers)
    st.metric("Predicted Heterozygous Markers", f"{hetero_count} ({hetero_percent:.1f}%)")
    st.metric("Predicted Homozygous Markers", f"{homo_count} ({homo_percent:.1f}%)")
    st.metric("Hybrid Vigor Score", vigor_score)

    # Pie chart visualization
    fig, ax = plt.subplots()
    ax.pie([hetero_count, homo_count], labels=['Heterozygous', 'Homozygous'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Bar chart per chromosome
    st.subheader("Marker Distribution per Chromosome")
    chrom_data = merged.groupby(['Chromosome_p1', 'Predicted Progeny']).size().unstack(fill_value=0)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    chrom_data.plot(kind='bar', stacked=True, ax=ax2)
    ax2.set_xlabel("Chromosome")
    ax2.set_ylabel("Number of Markers")
    ax2.set_title("Homozygous vs. Heterozygous Markers per Chromosome")
    st.pyplot(fig2)

    # Show merged table
    with st.expander("See detailed marker comparison"):
        st.dataframe(merged)

    st.success("Analysis complete! Check the visualizations and table above.")

else:
    st.info("Please upload both genome CSV files to begin the analysis.")
