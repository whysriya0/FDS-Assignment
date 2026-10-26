# Fundamentals of Data Science (FDS) — Case Studies Dossier

> **Academic Submission for Fundamentals of Data Science (Course Code: 22CSC59)**  
> **Chaitanya Bharathi Institute of Technology (Autonomous), Hyderabad**  
> **Department of Computer Science and Engineering | Academic Year 2026–2027**

---

## 📋 Student & Submission Metadata

| Parameter | Submission Details |
| :--- | :--- |
| **Student Name** | **Sriya Ammanamanchi** |
| **Roll Number** | **160124733156** |
| **Section / Class** | **CSE-3** |
| **Academic Year** | **2026–2027** |
| **Subject Name** | **Fundamentals of Data Science (22CSC59)** |
| **Faculty Mentor** | **Assistant Prof. Durga Devi** |
| **Primary Submission PDF** | [`Combined_Case_Study_Report.pdf`](./Combined_Case_Study_Report.pdf) *(41-page comprehensive academic report)* |
| **Executable Jupyter Notebook** | [`Sriya_Case_Studies_1_and_4.ipynb`](./Sriya_Case_Studies_1_and_4.ipynb) |
| **Standalone Python Programs** | [`case_study_1_retail.py`](./case_study_1_retail.py), [`case_study_4_student_dropout.py`](./case_study_4_student_dropout.py), [`run_all.py`](./run_all.py) |

---

## 🎯 Submission Guidelines Compliance Matrix

This repository strictly fulfills all seven institutional case study submission guidelines:

| # | Prescribed Guideline | Implementation & Verification in Repository |
| :-: | :--- | :--- |
| **1** | **Title Page Format**<br>*(Title, Roll No, Name, Section, Year, Subject, Faculty)* | Complete title page included on Page 1 of [`Combined_Case_Study_Report.pdf`](./Combined_Case_Study_Report.pdf), in [`Sriya_Case_Studies_1_and_4.ipynb`](./Sriya_Case_Studies_1_and_4.ipynb), and documented across all scripts. |
| **2** | **Core Academic Sections**<br>*(Problem statement, methodology, statistical findings, model evaluation, conclusion)* | Rigorously articulated across both case studies in both the PDF report, standalone Python scripts, and notebook. |
| **3** | **Meaningful Visualizations**<br>*(Titles, axis labels, legends, and narrative interpretations)* | Every figure includes descriptive titles, labeled axes, units, legends, and an explicit shaded callout detailing empirical interpretations. No naked graphs. |
| **4** | **Explained Statistical Findings & Model Metrics** | Statistical findings (means, medians, skewness, ANOVA, Kruskal-Wallis $H$, effect sizes $\epsilon^2$, odds multipliers, macro-F1, bootstrap 95% CIs) are thoroughly interpreted. |
| **5** | **Executable Jupyter Notebook (.ipynb)** | [`Sriya_Case_Studies_1_and_4.ipynb`](./Sriya_Case_Studies_1_and_4.ipynb) contains complete executable code, saved execution outputs, markdown explanations, and visualizations. |
| **6** | **Comprehensive PDF Report** | [`Combined_Case_Study_Report.pdf`](./Combined_Case_Study_Report.pdf) is the official, complete 41-page report detailing both studies. |
| **7** | **GitHub Repository Link & Python Code** | Clean, modular Python code provided ([`case_study_1_retail.py`](./case_study_1_retail.py), [`case_study_4_student_dropout.py`](./case_study_4_student_dropout.py), [`run_all.py`](./run_all.py)) and repository initialized for GitHub submission. |

---

## 📂 Repository File Structure

```text
FDS_Sriya/
├── Combined_Case_Study_Report.pdf   # Official 41-page case study submission report
├── Sriya_Case_Studies_1_and_4.ipynb # Complete executable Jupyter notebook with outputs
├── case_study_1_retail.py          # Standalone Python program for Case Study 1
├── case_study_4_student_dropout.py # Standalone Python program for Case Study 4
├── run_all.py                      # Master pipeline runner script (executes full workflow)
├── requirements.txt                # Pinned dependencies for reproducible execution
├── .gitignore                      # Standard Python, Jupyter, and OS ignore rules
├── README.md                       # Comprehensive repository documentation
│
├── 1/                              # Case Study 1 directory
│   ├── Case Study.docx             # Official problem statement specification
│   ├── Online retail_new.csv       # Primary transaction records (7,501 baskets)
│   └── Online retail.xlsx          # Companion workbook for validation
│
├── 4/                              # Case Study 4 directory
│   ├── student performance.docx    # Official problem statement specification
│   └── Studentdata.csv             # Higher education dataset (4,424 records, 37 attributes)
│
├── case_study_1_results/           # Exported assets for Case Study 1
│   ├── fig1_product_frequency.png  # Top 20 product bar chart
│   ├── fig2_basket_size.png        # Basket size histogram (mean & median)
│   ├── fig3_pca_variance.png       # Scree plot (cumulative & individual variance)
│   ├── fig4_k_selection.png        # Silhouette & Davies-Bouldin vs K diagnostic
│   ├── fig5_dendrogram.png         # Ward hierarchical clustering tree (250 sample)
│   ├── fig6_pca_clusters.png       # 2D PCA projection of K-Means clusters
│   ├── fig7_cluster_heatmap.png    # Product prevalence heatmap across clusters
│   └── results.json                # Summary metrics and profile dictionary
│
└── case_study_4_results/           # Exported assets for Case Study 4
    ├── data_dictionary.csv         # Semantic taxonomy of 37 features
    ├── descriptive_statistics.csv  # Descriptive statistics for numerical variables
    ├── outcome_statistics.csv      # Metrics partitioned by target category
    ├── first_semester_statistics.csv # 1st sem grade metrics and zero frequencies
    ├── split_manifest.csv          # Audit manifest of stratified train/test split
    ├── model_comparison.csv        # Baseline vs Admission-only vs Semester-1 model
    ├── classification_report.csv   # Precision, recall, F1 per class + macro averages
    ├── bootstrap_intervals.csv     # 1,000-resample 95% confidence intervals
    ├── all_coefficients.csv        # Fitted log-odds and odds multipliers
    ├── analysis_summary.json       # Hypothesis test and pipeline summary audit
    ├── fig1_target_distribution.png # Outcome class distribution bar chart
    ├── fig2_numerical_distributions.png # Histograms of Age and Admission grade
    ├── fig3_admission_grade_distribution.png # Admission grade box plot by outcome
    ├── fig4_first_semester_grade_distribution.png # 1st sem grade box plot by outcome
    ├── fig5_outcome_by_age_band.png # Outcome stacked bar chart across age cohorts
    └── fig6_confusion_matrix.png   # Held-out test set confusion matrix
```

---

## 🔍 Analytical Overview: Case Study 1
### Online Retail Market Basket Clustering and Association Analysis

- **Problem Statement:** Segment 7,501 retail transactions across 119 catalog products to identify latent shopping basket archetypes and item affinities.
- **Preprocessing:** Sanitized text tokens, lowercased product names, eliminated intra-basket duplicate items, and validated 100% equivalence with the companion Excel workbook.
- **Descriptive Statistics:**
  - Average basket size: **3.91 items** (std = 2.91, median = 3.0 items, max = 20 items).
  - Singletons (1 item): **23.4%** of transactions; small baskets ($\le 2$ items): **40.5%**.
  - Top items: *Mineral water* (23.8% of baskets), *Eggs* (18.0%), *Spaghetti* (17.4%), and *French fries* (17.1%).
- **Dimensionality Reduction:** Formulated a $7501 \times 119$ binary indicator matrix (density = 3.29%). PCA compressed the space to 20 principal components, preserving **54.9% of cumulative variance** (first 2 PCs retain 11.2%).
- **Clustering Benchmarking:**
  - **K-Means ($k=5$):** Selected champion model. Silhouette = **0.1572**, Davies-Bouldin = **2.0894**, 100% coverage.
  - **Ward Hierarchical ($k=5$):** Silhouette = 0.0368, Davies-Bouldin = 3.5260 (exhibits Euclidean chaining).
  - **DBSCAN ($\epsilon=3.5$, MinPts=15):** Silhouette = 0.2304, but discards 17.2% of transactions as noise.
  - **Spectral Clustering ($k=5$):** Silhouette = -0.1436 (manifold overlap in graph Laplacian space).
- **Cluster Archetypes & Lift Insights:**
  - *Cluster 0 (15.9%, avg size 4.96):* **Water & Pantry Staples** (Mineral water 100%, lift 4.20).
  - *Cluster 1 (12.1%, avg size 4.21):* **Breakfast & Protein** (Eggs 100%, lift 5.56; burgers, lift 1.84).
  - *Cluster 2 (12.0%, avg size 4.24):* **Quick Snacks & Fried Foods** (French fries 100%, lift 5.85).
  - *Cluster 3 (15.5%, avg size 6.45):* **Dinner / Pasta Feast** (Spaghetti 100%, lift 5.73; ground beef, lift 2.59).
  - *Cluster 4 (44.5%, avg size 2.49):* **General Convenience** (Small casual baskets).

---

## 🎓 Analytical Overview: Case Study 4
### Predicting Student Dropout and Academic Success via Machine Learning

- **Problem Statement:** Forecast eventual academic trajectory (**Dropout**, **Enrolled**, or **Graduate**) for 4,424 university students using admission, demographic, socioeconomic, and 1st-semester academic records.
- **Data Quality & Taxonomy:** Verified 0 missing values and 0 duplicates across 37 attributes. Categorized into 9 Nominal features, 8 Binary indicators, 1 Ordinal feature, and 18 Numerical predictors.
- **Class Imbalance:** **Graduate: 49.93%** (2,209), **Dropout: 32.12%** (1,421), **Enrolled: 17.95%** (794). A naive majority baseline achieves 49.9% accuracy but a dismal macro-F1 of 0.222.
- **Inferential Hypothesis Testing:**
  - $H_0$: 1st-semester grade distributions are identical across Dropout, Enrolled, and Graduate.
  - $H_1$: 1st-semester grade distributions differ significantly across outcome categories.
  - *Assumption Audit:* Brown-Forsythe test rejected variance homogeneity ($F = 549.87, p = 5.47 \times 10^{-214}$). Non-parametric test required.
  - *Kruskal-Wallis Omnibus Test:* **$H = 1094.19, df = 2, p = 2.51 \times 10^{-238}$** $\rightarrow$ **Decisively Reject $H_0$**.
  - *Effect Size:* Epsilon-squared **$\epsilon^2 = 0.2470$** confirms a **large practical effect size** ($\epsilon^2 > 0.14$), explaining 24.7% of outcome variance.
- **Leak-Free Supervised Classification:**
  - Enforced a strict early-warning boundary: excluded 2nd-semester and end-of-program variables to prevent target leakage.
  - Stratified 80:20 train-test partition (Train: 3,539; Test: 885).
  - Preprocessing pipeline: `SimpleImputer` + `StandardScaler` (numeric) + `OneHotEncoder(drop='first')` (nominal).
  - Final Multiclass Logistic Regression model achieved:
    - **Test Accuracy: 70.73%** (95% CI: $[67.57\%, 73.56\%]$ via 1,000 bootstrap resamples).
    - **Macro Precision: 66.62%**, **Macro Recall: 66.87%**, **Macro F1: 0.6623** (95% CI: $[0.6259, 0.6933]$).
    - Class-level F1: **Graduate = 0.8106**, **Dropout = 0.7070**, **Enrolled = 0.4693**.
- **Model Interpretability (Odds Multipliers):**
  - *Top Protective Factor:* 1st-semester approved units (odds multiplier **$0.041\times$**, cutting dropout odds by 95.9% per SD).
  - *Top Risk Factor:* 1st-semester enrolled units without approval (odds multiplier **$3.791\times$**).
  - *Demographic Factor:* Age at enrollment (odds multiplier **$1.408\times$** per SD, reflecting adult learner competing responsibilities).
- **Responsible AI Governance:** Institutional predictions must strictly guide proactive academic support (early tutoring, fee payment installment counseling), never punitive disciplinary action or algorithmic exclusion.

---

## 🚀 Reproduction and Execution Guide

### 1. Environment Setup

Clone or download the repository, then install dependencies:

```bash
# Verify Python version (Python 3.10 or 3.11 recommended)
python --version

# Install required Python packages
pip install -r requirements.txt
```

### 2. Run the Full Reproduction Pipeline

To execute both case study models, export all figures and metrics, and re-verify everything in one command:

```bash
python run_all.py
```

### 3. Run Individual Case Studies

You can also run each case study independently:

```bash
# Execute Case Study 1 (Online Retail Basket Clustering)
python case_study_1_retail.py

# Execute Case Study 4 (Student Dropout Prediction)
python case_study_4_student_dropout.py
```




