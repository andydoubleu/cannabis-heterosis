# Atlas Lab: Cannabis Heterosis Predictor

!Atlas Lab Logo.png

Welcome to the **Atlas Lab Cannabis Heterosis Predictor** — a user-friendly Streamlit application that helps you analyze the potential heterosis (hybrid vigor) between two cannabis strains using their genome sequencing data.

> Upload parent strain genome CSV files, get instant predictions, visual insights, and export results ✨

---

## Features

- 📂 **Upload Parent Strain CSVs**
- 🤷 Automatic prediction of heterosis in progeny
- 📊 Visualizations:
  - Pie chart of heterozygosity vs. homozygosity
  - Bar chart: marker distribution per chromosome
- 🌐 Strain name inputs for custom reporting
- 🔗 Export results as a timestamped CSV with full metadata
- 🌱 Atlas Lab clean branding and UI

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/andydoubleu/cannabis-heterosis-predictor.git
cd cannabis-heterosis-predictor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser:**
Streamlit will automatically provide a local URL (usually `http://localhost:8501/`).

---

## Usage

1. Enter the names of your two parent strains.
2. Upload your genome sequencing CSV files for both parents.
3. Review the heterosis predictions and interactive charts.
4. Download the detailed prediction results as a CSV!

**CSV File Requirements:**
- Columns required: `Marker ID`, `Chromosome`, `Position`, `Reference Allele`, `Alternate Allele`, `Genotype`

---

## Deploy to Streamlit Cloud

Want to share your app with the world? Streamlit Cloud makes it easy!

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)

1. Push your app to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository and deploy. Done!

---

## Roadmap

- [ ] Add multi-page support (e.g., About, Results, Settings)
- [ ] Advanced marker filtering (chromosome or trait-specific)
- [ ] Custom themes: light/dark mode toggle
- [ ] Optional user manual integration

---

## Credits

Made with ❤️ by [Atlas Lab](https://github.com/andydoubleu)

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

> _Atlas Lab: By farmers, for farmers._ 🌿
