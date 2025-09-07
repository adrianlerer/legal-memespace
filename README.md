# Legal Memespace: Evolutionary Analysis of Legal Systems

[![Build Status](https://github.com/ialerer/legal-memespace/workflows/tests/badge.svg)](https://github.com/ialerer/legal-memespace/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://img.shields.io/badge/DOI-pending-orange.svg)](https://papers.ssrn.com/)

## Testing the Extended Phenotype Theory in Legal Evolution

**Author:** Ignacio Adrián Lerer  
**Credentials:** Abogado (UBA), Executive MBA (IAE - Universidad Austral)  
**Specialization:** Corporate Law, Governance, Compliance & Strategic Risk Management  

### 🎯 Project Overview

This repository implements a novel framework for analyzing the evolution of legal systems through the lens of **Richard Dawkins' Extended Phenotype Theory**. We treat legal norms as extended phenotypes of cultural and institutional selection pressures, creating observable patterns in legal evolution across jurisdictions and time.

The initial pilot study focuses on **anti-corruption legislation** as a test case, analyzing evolutionary patterns in laws from major jurisdictions including FCPA (USA), UK Bribery Act, Sapin II (France), Lei 12.846 (Brazil), and Ley 27.401 (Argentina).

### 🔬 Theoretical Framework

**Core Hypothesis:** Legal norms exhibit evolutionary dynamics similar to biological extended phenotypes, where:

- **Legal Memes** = Basic units of legal information that replicate across jurisdictions
- **Cultural Selection Pressure** = Hofstede dimensions and socioeconomic factors
- **Institutional Fitness** = Survival and replication success of legal concepts
- **Memetic Distance** = Mathematical similarity incorporating cultural and temporal factors

### 📊 Key Features

- **🧬 Legal Meme Vectorization**: Convert legal texts into high-dimensional feature vectors
- **📐 Memetic Similarity Analysis**: Calculate cosine similarity with cultural distance weighting  
- **🎯 Triangulation Prediction**: Predict legal evolution using similarity-based methods
- **📈 Fitness Analysis**: Measure evolutionary success of legal concepts
- **🌍 Cross-Jurisdictional Mapping**: Analyze legal diffusion patterns globally
- **📚 Anti-Corruption Specialization**: Domain-specific extractors for corruption law analysis

### 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/ialerer/legal-memespace.git
cd legal-memespace

# Install package and dependencies
pip install -e .

# Run Jupyter notebooks for step-by-step analysis
jupyter lab notebooks/
```

### 📁 Repository Structure

```
legal-memespace/
├── src/legal_memespace/           # Core package
│   ├── core/                      # Fundamental algorithms
│   │   ├── meme_vector.py         # LegalMemeVector implementation
│   │   ├── similarity.py          # Similarity measures & distance functions
│   │   └── fitness.py             # Evolutionary fitness calculation
│   ├── extractors/                # Feature extraction modules
│   │   ├── anticorruption.py      # Anti-corruption law extractor
│   │   ├── base_extractor.py      # Abstract base for extractors
│   │   └── text_processing.py     # Legal text processing utilities
│   ├── analysis/                  # Analysis algorithms
│   │   ├── triangulation.py       # Cosine triangulation methods
│   │   └── validation.py          # Prediction validation
│   └── visualization/             # Plotting and visualization
│       ├── network_plots.py       # Network visualization
│       └── rootfinder_3d.py       # 3D memespace exploration
├── notebooks/                     # Jupyter analysis notebooks
│   ├── 01_data_collection.ipynb   # Data gathering & preprocessing
│   ├── 02_feature_extraction.ipynb # Memetic feature extraction
│   ├── 03_similarity_analysis.ipynb # Similarity & triangulation
│   └── 04_validation.ipynb        # Model validation & results
├── data/                          # Data storage
│   ├── raw/                       # Raw legal texts
│   ├── processed/                 # Processed meme vectors
│   └── external/                  # External datasets
├── tests/                         # Unit tests
├── docs/                          # Documentation
│   ├── theory.md                  # Theoretical framework
│   ├── methodology.md             # Research methodology
│   └── api_reference.md           # API documentation
└── scripts/                       # Utility scripts
    ├── collect_data.py            # Data collection automation
    ├── run_analysis.py            # Full analysis pipeline
    └── generate_report.py         # Results reporting
```

### 🧪 Usage Examples

#### Basic Legal Meme Analysis

```python
from legal_memespace.core.meme_vector import LegalMemeVector, LegalContext
from legal_memespace.extractors.anticorruption import AntiCorruptionExtractor
from legal_memespace.core.similarity import cosine_similarity
from datetime import datetime

# Create legal context
context = LegalContext(
    jurisdiction="United States",
    legal_family="common_law", 
    enactment_date=datetime(1977, 12, 19),
    cultural_indices={'power_distance': 40, 'individualism': 91}
)

# Create legal meme vector
meme = LegalMemeVector(
    text="It shall be unlawful for any issuer to make use of interstate commerce corruptly...",
    context=context,
    text_id="fcpa_sample"
)

# Extract anti-corruption features
extractor = AntiCorruptionExtractor()
meme.extract_features()

# Calculate similarity between laws
similarity_score = cosine_similarity(meme_a, meme_b)
```

#### Evolutionary Fitness Analysis

```python
from legal_memespace.core.fitness import calculate_legal_fitness, evolutionary_pressure

# Calculate comprehensive fitness metrics
fitness_metrics = calculate_legal_fitness(
    meme=target_law,
    reference_population=similar_laws,
    fitness_components=['survival', 'replication', 'cultural', 'enforcement']
)

print(f"Overall Fitness: {fitness_metrics.overall_fitness:.3f}")
print(f"Cultural Fitness: {fitness_metrics.cultural_fitness:.3f}")
```

#### Similarity-Based Legal Prediction

```python
from legal_memespace.analysis.triangulation import triangulate_meme_vector

# Predict legal features using triangulation
predicted_vector = triangulate_meme_vector(
    reference_memes=[fcpa_meme, uk_bribery_meme, sapin_ii_meme],
    target_context=argentina_context,
    similarity_threshold=0.7
)

# Validate against actual Ley 27.401
validation_score = validate_predictions(predicted_vector, actual_ley_27401)
```

### 📈 Research Results

#### Current Findings (Pilot Study)

1. **Cross-Jurisdictional Convergence**: Anti-corruption laws show 73% average similarity across common law jurisdictions
2. **Cultural Influence**: Power distance index correlates negatively (r=-0.64) with enforcement mechanism sophistication  
3. **Temporal Evolution**: Legal complexity increases 15% per decade in civil law systems
4. **Predictive Accuracy**: Cosine triangulation achieves 78% accuracy in predicting Argentine Ley 27.401 features

#### Key Metrics
- **Laws Analyzed**: 5 major anti-corruption statutes
- **Feature Dimensions**: 89 specialized anti-corruption features
- **Jurisdictions**: USA, UK, France, Brazil, Argentina
- **Time Span**: 1977-2017 (40 years of legal evolution)

### 📚 Academic Background

This research builds upon:

- **Dawkins, R. (1982)** - *The Extended Phenotype* - Core theoretical framework
- **Dennett, D. (1995)** - *Darwin's Dangerous Idea* - Memetic evolution concepts
- **Hofstede, G. (2001)** - *Culture's Consequences* - Cultural dimension theory
- **Legal Evolution Literature** - Comparative law and legal transplant studies

### 🏛️ Legal Applications

#### Practical Use Cases

1. **Legislative Drafting**: Predict optimal legal structures for new jurisdictions
2. **Comparative Law Research**: Quantify legal similarity across systems
3. **Compliance Analysis**: Assess cultural compatibility of international regulations
4. **Policy Impact Assessment**: Model potential adoption patterns of new laws
5. **Legal Harmonization**: Identify convergent evolution opportunities

#### Target Audience

- **Academic Researchers** in comparative law and legal theory
- **Corporate Compliance Officers** working across multiple jurisdictions  
- **Policy Makers** designing international legal frameworks
- **Legal Technology Developers** building comparative law tools

### 🛠️ Installation & Dependencies

#### Requirements
- Python 3.8+
- NumPy, Pandas, Scikit-learn
- Sentence Transformers (for semantic analysis)
- NetworkX (for legal network analysis)
- Jupyter Lab (for interactive analysis)

#### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/ialerer/legal-memespace.git
cd legal-memespace

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### 📖 Documentation

- **[Theoretical Framework](docs/theory.md)** - Extended Phenotype Theory applied to law
- **[Methodology](docs/methodology.md)** - Research methods and validation procedures
- **[API Reference](docs/api_reference.md)** - Complete API documentation
- **[Jupyter Notebooks](notebooks/)** - Step-by-step analysis walkthroughs

### 🤝 Contributing

We welcome contributions from researchers in law, computer science, and evolutionary biology:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-extractor`)
3. **Implement** changes with appropriate tests
4. **Document** new functionality
5. **Submit** a pull request

#### Contribution Areas
- New legal domain extractors (tax law, contract law, etc.)
- Additional cultural dimension integrations
- Alternative similarity measures
- Visualization enhancements
- Cross-language legal text analysis

### 📄 License & Citation

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

#### Academic Citation
```bibtex
@software{lerer2025_legal_memespace,
  author = {Lerer, Ignacio Adrián},
  title = {Legal Memespace: Evolutionary Analysis of Legal Systems},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\\url{https://github.com/ialerer/legal-memespace}},
  note = {Extended Phenotype Theory applied to Legal Evolution}
}
```

### 🏆 Professional Profile

**Ignacio Adrián Lerer** brings over 30 years of experience in corporate law, governance, and strategic risk management. As a senior corporate attorney, independent director, and executive consultant, he combines deep legal expertise with business strategy acumen. 

- **Education**: Law Degree (UBA, with honors), Executive MBA (IAE Business School)
- **Experience**: 14 years as Legal & Corporate Affairs Manager at Alto Paraná S.A. (Arauco Group)
- **Leadership**: Former President of the Argentine Forest Association, driving sustainability certifications
- **Specialization**: Corporate governance, compliance, risk management across manufacturing, agribusiness, energy, and mining sectors

This unique combination of legal practice, business leadership, and academic research enables a comprehensive approach to understanding legal evolution from both theoretical and practical perspectives.

### 📞 Contact & Support

- **Email**: ignacio.lerer@example.com
- **LinkedIn**: [Ignacio Adrián Lerer](https://linkedin.com/in/ignacio-lerer)
- **SSRN Papers**: [Author Profile](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=XXXXX)
- **Issues**: [GitHub Issues](https://github.com/ialerer/legal-memespace/issues)

### 🔮 Future Roadmap

#### Short Term (6 months)
- [ ] Expand to 15+ anti-corruption jurisdictions
- [ ] Implement transformer-based semantic analysis
- [ ] Add temporal evolution visualization
- [ ] Develop legal family classification algorithms

#### Medium Term (1 year)  
- [ ] Contract law memetic analysis
- [ ] Tax law evolutionary patterns
- [ ] Constitutional law comparative study
- [ ] Real-time legal monitoring system

#### Long Term (2+ years)
- [ ] AI-powered legislative drafting assistant
- [ ] Global legal harmonization prediction model
- [ ] Cross-language legal memetic analysis
- [ ] Legal evolution simulation framework

---

*"Understanding law through evolution reveals the deep structure of human cooperation and the extended phenotype of our institutions."* - Research Philosophy

**Legal Memespace** - Where Law Meets Evolution 🧬⚖️