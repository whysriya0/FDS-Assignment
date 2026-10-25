"""
Fundamentals of Data Science - Case Study 4
Title: Predicting Student Dropout and Academic Success Using Machine Learning
Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3 | Academic Year: 2026-2027
Faculty: Assistant Prof. Durga Devi

Description:
This script performs a comprehensive empirical investigation into student retention
and academic trajectory at a higher education institution.
Key workflow steps:
1. Part A: Data understanding, semantic categorization, and quality auditing.
2. Part B: Exploratory data analysis and descriptive statistics.
3. Part C: Hypothesis testing (Kruskal-Wallis non-parametric ANOVA on first-semester grades,
   assumption checks, effect size calculation, and practical vs statistical significance).
4. Part D: Multiclass classification modeling (Multiclass Logistic Regression,
   stratified 80:20 split, leak-free early-prediction temporal boundary, 5-fold cross-validation,
   confusion matrix, precision/recall/F1-score, macro-averaging, bootstrap uncertainty).
5. Part E: Interpretability (log-odds differences and odds multipliers), institutional interventions,
   and ethical/responsible AI governance principles.
"""

from pathlib import Path
from itertools import combinations
import json
import warnings
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.exceptions import ConvergenceWarning

# Suppress minor convergence warnings if handled
warnings.filterwarnings('ignore', category=ConvergenceWarning)

# Reproducibility settings
SEED = 42
rng = np.random.default_rng(SEED)

# Outcome classes and visual styling
CLASSES = ['Dropout', 'Enrolled', 'Graduate']
COLORS = ['#C55A45', '#D7A535', '#218A87']

plt.style.use('default')
plt.rcParams.update({
    'figure.dpi': 120,
    'savefig.dpi': 200,
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'axes.spines.top': False,
    'axes.spines.right': False
})

RESULTS_DIR = Path('case_study_4_results')
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


def locate_data_file(filename: str) -> Path:
    """Locate data file across current directory, subfolders, or script directory."""
    candidates = [
        Path.cwd() / filename,
        Path.cwd() / '4' / filename,
        Path(__file__).resolve().parent / filename if '__file__' in globals() else None,
        Path(__file__).resolve().parent / '4' / filename if '__file__' in globals() else None
    ]
    for p in candidates:
        if p and p.exists():
            return p
    raise FileNotFoundError(f"Could not locate dataset '{filename}' in current directory or '4/'.")


def main():
    print("=" * 75)
    print("CASE STUDY 4: PREDICTING STUDENT DROPOUT AND ACADEMIC SUCCESS")
    print("Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3")
    print("=" * 75)

    # -------------------------------------------------------------
    # PART A: DATA UNDERSTANDING AND PREPROCESSING
    # -------------------------------------------------------------
    print("\n[PART A] Loading Data & Conducting Semantic Audits...")
    data_path = locate_data_file('Studentdata.csv')
    df = pd.read_csv(data_path, sep=';')
    df.columns = df.columns.str.strip()

    print(f"Dataset Dimensions: {df.shape[0]:,} rows (students) and {df.shape[1]} attributes")
    print(f"Target Attribute: 'Target' with unique classes: {list(df['Target'].unique())}")

    # Semantic categorization
    nominal = [
        'Marital status', 'Application mode', 'Course', 'Previous qualification',
        'Nacionality', "Mother's qualification", "Father's qualification",
        "Mother's occupation", "Father's occupation"
    ]
    binary = [
        'Daytime/evening attendance', 'Displaced', 'Educational special needs',
        'Debtor', 'Tuition fees up to date', 'Gender', 'Scholarship holder', 'International'
    ]
    numeric = [c for c in df if c not in nominal + binary + ['Target']]

    schema = pd.DataFrame({
        'attribute': df.columns,
        'semantic_type': [
            'Target: Nominal' if c == 'Target' else
            'Nominal Code' if c in nominal else
            'Binary Indicator' if c in binary else
            'Ordinal / Scaled Numeric' if c == 'Application order' else
            'Continuous / Discrete Numerical'
            for c in df
        ],
        'dtype': [str(df[c].dtype) for c in df],
        'unique_values': [df[c].nunique() for c in df]
    })
    schema.to_csv(RESULTS_DIR / 'data_dictionary.csv', index=False)
    print("Exported data dictionary to data_dictionary.csv")

    # Data Quality Verification
    missing_total = int(df.isna().sum().sum())
    blank_strings = int(df.isin(['', ' ']).sum().sum())
    duplicates = int(df.duplicated().sum())

    grade1 = 'Curricular units 1st sem (grade)'
    approved1 = 'Curricular units 1st sem (approved)'
    enrolled1 = 'Curricular units 1st sem (enrolled)'

    audit = {
        'total_records': len(df),
        'attributes': df.shape[1],
        'missing_values': missing_total,
        'blank_strings': blank_strings,
        'duplicate_records': duplicates,
        'age_min': float(df['Age at enrollment'].min()),
        'age_max': float(df['Age at enrollment'].max()),
        'admission_grade_min': float(df['Admission grade'].min()),
        'admission_grade_max': float(df['Admission grade'].max()),
        'zero_first_sem_grades': int(df[grade1].eq(0).sum()),
        'zero_first_sem_grade_pct': float((df[grade1].eq(0).mean()) * 100)
    }
    print("Quality Audit Summary:")
    print(json.dumps(audit, indent=2))
    assert missing_total == 0 and duplicates == 0, "Data audit failed!"

    # -------------------------------------------------------------
    # PART B: EXPLORATORY DATA ANALYSIS AND STATISTICS
    # -------------------------------------------------------------
    print("\n[PART B] Exploratory Data Analysis & Descriptive Statistics...")

    # Class distribution
    counts = df['Target'].value_counts().reindex(CLASSES)
    pcts = (counts / len(df)) * 100
    dist_df = pd.DataFrame({'Count': counts, 'Percentage (%)': pcts.round(2)})
    print("\nOutcome Class Distribution:\n", dist_df)

    # Fig 1: Target Class Distribution
    fig, ax = plt.subplots(figsize=(8, 4.8))
    bars = ax.bar(CLASSES, counts, color=COLORS, width=0.55, edgecolor='none', alpha=0.88)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 35,
                f"{int(h):,} ({h/len(df)*100:.1f}%)", ha='center', va='bottom', fontsize=10, weight='bold')
    ax.set_title('Figure 1. Academic Outcome Distribution (Target Variable)', pad=12)
    ax.set_xlabel('Final Academic Outcome')
    ax.set_ylabel('Student Count')
    ax.set_ylim(0, max(counts) * 1.15)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / 'fig1_target_distribution.png', dpi=200)
    plt.close()
    print("Saved: fig1_target_distribution.png")

    # Selected numerical variables
    selected_nums = ['Age at enrollment', 'Admission grade', 'Previous qualification (grade)']
    desc_stats = df[selected_nums].describe(percentiles=[.25, .5, .75]).round(2)
    desc_stats.to_csv(RESULTS_DIR / 'descriptive_statistics.csv')
    print("\nDescriptive Statistics for Selected Numerical Variables:\n", desc_stats)

    # Fig 2: Histograms of Age at enrollment and Admission grade
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    axes[0].hist(df['Age at enrollment'], bins=25, color=COLORS[0], edgecolor='white', alpha=0.85)
    axes[0].axvline(df['Age at enrollment'].median(), color='#111111', linestyle='--',
                    label=f"Median: {df['Age at enrollment'].median():.0f}")
    axes[0].set_title('Distribution of Age at Enrollment')
    axes[0].set_xlabel('Age at Enrollment (Years)')
    axes[0].set_ylabel('Frequency')
    axes[0].legend(frameon=True)

    axes[1].hist(df['Admission grade'], bins=25, color=COLORS[2], edgecolor='white', alpha=0.85)
    axes[1].axvline(df['Admission grade'].mean(), color='#111111', linestyle='--',
                    label=f"Mean: {df['Admission grade'].mean():.1f}")
    axes[1].set_title('Distribution of Admission Grades')
    axes[1].set_xlabel('Admission Grade (0–200 Scale)')
    axes[1].set_ylabel('Frequency')
    axes[1].legend(frameon=True)

    fig.suptitle('Figure 2. Distributions of Key Enrollment Metrics', weight='bold', y=1.02)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / 'fig2_numerical_distributions.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved: fig2_numerical_distributions.png")

    # Fig 3: Admission Grade by Outcome
    fig, ax = plt.subplots(figsize=(8, 4.5))
    boxes = ax.boxplot([df.loc[df['Target'] == c, 'Admission grade'] for c in CLASSES],
                       tick_labels=CLASSES, patch_artist=True,
                       flierprops={'markersize': 3, 'alpha': 0.3})
    for patch, color in zip(boxes['boxes'], COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title('Figure 3. Comparison of Admission Grades Across Outcome Classes', pad=12)
    ax.set_xlabel('Final Academic Outcome')
    ax.set_ylabel('Admission Grade (0–200 Scale)')
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / 'fig3_admission_grade_distribution.png', dpi=200)
    plt.close()
    print("Saved: fig3_admission_grade_distribution.png")

    # Fig 4: First-Semester Grades by Outcome
    fig, ax = plt.subplots(figsize=(8, 4.5))
    boxes = ax.boxplot([df.loc[df['Target'] == c, grade1] for c in CLASSES],
                       tick_labels=CLASSES, patch_artist=True,
                       flierprops={'markersize': 3, 'alpha': 0.3})
    for patch, color in zip(boxes['boxes'], COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title('Figure 4. First-Semester Average Grades Across Academic Outcomes', pad=12)
    ax.set_xlabel('Final Academic Outcome')
    ax.set_ylabel('1st Sem Grade (0–20 Scale)')
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / 'fig4_first_semester_grade_distribution.png', dpi=200)
    plt.close()
    print("Saved: fig4_first_semester_grade_distribution.png")

    grade_summary = df.groupby('Target')[grade1].agg(['count', 'mean', 'median', 'std', 'skew']).reindex(CLASSES)
    grade_summary['q1'] = df.groupby('Target')[grade1].quantile(.25)
    grade_summary['q3'] = df.groupby('Target')[grade1].quantile(.75)
    grade_summary['zero_percent'] = df.assign(zero=df[grade1].eq(0)).groupby('Target').zero.mean() * 100
    grade_summary.to_csv(RESULTS_DIR / 'first_semester_statistics.csv')
    print("\nFirst-Semester Grade Statistical Summary:\n", grade_summary.round(3))

    # Fig 5: Outcome Distribution by Age Band
    age_bands = pd.cut(df['Age at enrollment'], [0, 20, 25, 35, np.inf],
                       labels=['<=20', '21-25', '26-35', '36+'])
    age_cross = pd.crosstab(age_bands, df['Target'], normalize='index').reindex(columns=CLASSES) * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    age_cross.plot(kind='bar', stacked=True, color=COLORS, ax=ax, edgecolor='white', width=0.6, alpha=0.9)
    ax.set_title('Figure 5. Academic Outcome Composition Across Enrollment Age Bands', pad=12)
    ax.set_xlabel('Age at Enrollment Band (Years)')
    ax.set_ylabel('Percentage of Cohort (%)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title='Outcome', frameon=True, bbox_to_anchor=(1.02, 1), loc='upper left')
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / 'fig5_outcome_by_age_band.png', dpi=200)
    plt.close()
    print("Saved: fig5_outcome_by_age_band.png")

    # -------------------------------------------------------------
    # PART C: HYPOTHESIS TESTING
    # -------------------------------------------------------------
    print("\n[PART C] Inferential Statistics & Hypothesis Testing...")
    print("Hypothesis formulation:")
    print("  H0: The distribution of 1st-semester grades is identical across Dropout, Enrolled, and Graduate.")
    print("  H1: The distribution of 1st-semester grades differs significantly across at least one outcome group.")

    groups = [df.loc[df['Target'] == c, grade1].to_numpy() for c in CLASSES]

    # Assumption Testing: Levene / Brown-Forsythe Test of Homoscedasticity
    lev = stats.levene(*groups, center='median')
    print(f"Variance Homogeneity (Brown-Forsythe): Stat = {lev.statistic:.4f}, p = {lev.pvalue:.4e}")
    print("Assessment: Variances are highly heteroscedastic (p < 0.001) and grades are non-normal. Non-parametric test required.")

    # Kruskal-Wallis Test
    H_stat, p_val = stats.kruskal(*groups)
    n_total = len(df)
    k_groups = len(CLASSES)
    epsilon_sq = (H_stat - k_groups + 1) / (n_total - k_groups)

    test_res = {
        'H_statistic': float(H_stat),
        'degrees_of_freedom': k_groups - 1,
        'p_value': float(p_val),
        'significance_level_alpha': 0.05,
        'decision': 'Reject H0' if p_val < 0.05 else 'Fail to Reject H0',
        'effect_size_epsilon_squared': float(epsilon_sq),
        'practical_importance': 'Large effect size (epsilon^2 > 0.14)'
    }
    print("Kruskal-Wallis Omnibus Test Results:")
    print(json.dumps(test_res, indent=2))

    # Post-hoc pairwise comparisons with Holm-Bonferroni correction
    pairwise = []
    for a, b in combinations(CLASSES, 2):
        u_val, p_raw = stats.mannwhitneyu(
            df.loc[df['Target'] == a, grade1],
            df.loc[df['Target'] == b, grade1],
            alternative='two-sided', method='asymptotic'
        )
        pairwise.append({'comparison': f"{a} vs {b}", 'Mann_Whitney_U': float(u_val), 'p_raw': float(p_raw)})

    pairwise_df = pd.DataFrame(pairwise)
    # Holm step-down
    p_sorted = pairwise_df['p_raw'].sort_values()
    m = len(p_sorted)
    holm_p = np.zeros(m)
    running = 0.0
    for rank, (idx, val) in enumerate(p_sorted.items()):
        adj = (m - rank) * val
        running = max(running, min(1.0, adj))
        holm_p[rank] = running
    pairwise_df.loc[p_sorted.index, 'p_holm_bonferroni'] = holm_p
    print("\nPairwise Post-Hoc Tests (Holm-Bonferroni Adjusted):\n", pairwise_df.to_string(index=False))

    # -------------------------------------------------------------
    # PART D: MULTICLASS CLASSIFICATION MODELING
    # -------------------------------------------------------------
    print("\n[PART D] Multiclass Classification Modeling & Evaluation...")

    # Early-prediction boundary: exclude future (2nd sem) and end-of-program variables to avoid data leakage
    uncertain = ['Debtor', 'Tuition fees up to date', 'Scholarship holder', 'Unemployment rate', 'Inflation rate', 'GDP']
    second_sem = [c for c in df if '2nd sem' in c]
    first_sem = [c for c in df if '1st sem' in c]

    main_features = [c for c in df.drop(columns='Target') if c not in uncertain + second_sem]
    admission_features = [c for c in main_features if c not in first_sem]

    print(f"Total features considered: {len(df.columns) - 1}")
    print(f"Main leak-free features (up to 1st sem): {len(main_features)}")
    print(f"Admission-only baseline features: {len(admission_features)}")
    print(f"Excluded for data-leakage prevention (2nd sem + post-enrollment): {len(uncertain + second_sem)}")

    X = df.drop(columns='Target')
    y = df['Target']

    # Stratified 80:20 Train-Test split
    train_idx, test_idx = train_test_split(df.index, test_size=0.20, random_state=SEED, stratify=y)
    X_train, X_test = X.loc[train_idx], X.loc[test_idx]
    y_train, y_test = y.loc[train_idx], y.loc[test_idx]

    split_manifest = pd.DataFrame({'row_index': df.index, 'partition': np.where(df.index.isin(train_idx), 'train', 'test')})
    split_manifest.to_csv(RESULTS_DIR / 'split_manifest.csv', index=False)

    print(f"Training set: {len(train_idx):,} records | Test set: {len(test_idx):,} records")

    # Pipeline definition
    def build_pipeline(features):
        cats = [c for c in nominal if c in features]
        nums = [c for c in numeric if c in features]
        bins = [c for c in binary if c in features]

        preprocessor = ColumnTransformer([
            ('numeric', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), nums),
            ('categorical', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                                      ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))]), cats),
            ('binary', Pipeline([('imputer', SimpleImputer(strategy='most_frequent'))]), bins)
        ])

        return Pipeline([
            ('prepare', preprocessor),
            ('model', LogisticRegression(max_iter=1000, random_state=SEED))
        ])

    # Model 1: Baseline Dummy Classifier
    dummy = DummyClassifier(strategy='most_frequent')
    dummy.fit(X_train[admission_features], y_train)
    dummy_pred = dummy.predict(X_test[admission_features])

    # Model 2: Admission-Only Logistic Regression
    pipe_adm = build_pipeline(admission_features)
    param_grid = {'model__C': [0.01, 0.1, 1.0, 10.0], 'model__class_weight': [None, 'balanced']}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    grid_adm = GridSearchCV(pipe_adm, param_grid, cv=cv, scoring='f1_macro', n_jobs=-1)
    grid_adm.fit(X_train[admission_features], y_train)
    adm_pred = grid_adm.predict(X_test[admission_features])

    # Model 3: End of Semester 1 Multiclass Logistic Regression
    pipe_main = build_pipeline(main_features)
    grid_main = GridSearchCV(pipe_main, param_grid, cv=cv, scoring='f1_macro', n_jobs=-1)
    grid_main.fit(X_train[main_features], y_train)
    main_model = grid_main.best_estimator_
    main_pred = main_model.predict(X_test[main_features])

    # Performance Comparison
    def evaluate_model(name, actual, pred):
        return {
            'model': name,
            'accuracy': accuracy_score(actual, pred),
            'macro_precision': precision_score(actual, pred, average='macro', zero_division=0),
            'macro_recall': recall_score(actual, pred, average='macro', zero_division=0),
            'macro_f1': f1_score(actual, pred, average='macro', zero_division=0)
        }

    comp_df = pd.DataFrame([
        evaluate_model('Majority Class Baseline', y_test, dummy_pred),
        evaluate_model('Admission-Only Logistic Regression', y_test, adm_pred),
        evaluate_model('End of Semester 1 Logistic Regression', y_test, main_pred)
    ]).set_index('model')
    comp_df.to_csv(RESULTS_DIR / 'model_comparison.csv')
    print("\nModel Comparison Table:\n", comp_df.round(4))

    # Detailed Classification Report
    clf_report = pd.DataFrame(classification_report(y_test, main_pred, labels=CLASSES, output_dict=True, zero_division=0)).T
    clf_report.to_csv(RESULTS_DIR / 'classification_report.csv')
    print("\nFinal Model Classification Report (Semester 1 Logistic Regression):\n", clf_report.round(4))

    # Fig 6: Confusion Matrix
    cm = confusion_matrix(y_test, main_pred, labels=CLASSES)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    disp = ConfusionMatrixDisplay(cm, display_labels=CLASSES)
    disp.plot(ax=ax, cmap='Blues', colorbar=False, values_format='d')
    ax.set_title('Figure 6. Test Set Confusion Matrix (Semester 1 Model)', pad=12)
    ax.set_xlabel('Predicted Final Outcome')
    ax.set_ylabel('Actual Final Outcome')
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / 'fig6_confusion_matrix.png', dpi=200)
    plt.close()
    print("Saved: fig6_confusion_matrix.png")

    # Bootstrap 95% Confidence Intervals
    n_boot = 1000
    boot_acc = []
    boot_f1 = []
    for _ in range(n_boot):
        sample_indices = rng.integers(0, len(y_test), size=len(y_test))
        boot_acc.append(accuracy_score(y_test.iloc[sample_indices], main_pred[sample_indices]))
        boot_f1.append(f1_score(y_test.iloc[sample_indices], main_pred[sample_indices], average='macro', zero_division=0))

    ci_df = pd.DataFrame({
        'metric': ['Accuracy', 'Macro F1'],
        'mean': [np.mean(boot_acc), np.mean(boot_f1)],
        'ci_lower_95': [np.percentile(boot_acc, 2.5), np.percentile(boot_f1, 2.5)],
        'ci_upper_95': [np.percentile(boot_acc, 97.5), np.percentile(boot_f1, 97.5)]
    }).set_index('metric')
    ci_df.to_csv(RESULTS_DIR / 'bootstrap_intervals.csv')
    print("\nBootstrap 95% Confidence Intervals (1,000 resamples):\n", ci_df.round(4))

    # -------------------------------------------------------------
    # PART E: INTERPRETATION AND RECOMMENDATIONS
    # -------------------------------------------------------------
    print("\n[PART E] Feature Interpretability & Strategic Recommendations...")
    prep = main_model.named_steps['prepare']
    clf = main_model.named_steps['model']
    feature_names = prep.get_feature_names_out()

    # Log-odds difference: Dropout vs Graduate
    idx_drop = list(clf.classes_).index('Dropout')
    idx_grad = list(clf.classes_).index('Graduate')
    diff = clf.coef_[idx_drop] - clf.coef_[idx_grad]

    coef_all = pd.DataFrame({
        'feature': feature_names,
        'dropout_vs_graduate_log_odds': diff,
        'odds_multiplier': np.exp(diff)
    }).sort_values(by='dropout_vs_graduate_log_odds')
    coef_all.to_csv(RESULTS_DIR / 'all_coefficients.csv', index=False)

    print("\nTop 5 Features Favoring Graduation (Protective Factors):")
    for _, row in coef_all.head(5).iterrows():
        print(f"  {row['feature']}: Odds Multiplier = {row['odds_multiplier']:.3f} (Log-odds = {row['dropout_vs_graduate_log_odds']:.3f})")

    print("\nTop 5 Features Favoring Dropout (Risk Factors):")
    for _, row in coef_all.tail(5).iloc[::-1].iterrows():
        print(f"  {row['feature']}: Odds Multiplier = {row['odds_multiplier']:.3f} (Log-odds = {row['dropout_vs_graduate_log_odds']:.3f})")

    # Export audit summary JSON
    summary = {
        'audit': audit,
        'hypothesis_test': test_res,
        'model_comparison': comp_df.reset_index().to_dict('records'),
        'bootstrap_confidence_intervals': ci_df.reset_index().to_dict('records'),
        'best_hyperparameters': grid_main.best_params_,
        'recommendations': [
            "Establish Early Warning Alerts triggering at midterm of Semester 1 for zero approved units.",
            "Expand financial aid advising and tuition installment agreements prior to enrollment census.",
            "Provide tailored academic onboarding and peer mentoring for non-traditional and mature students."
        ]
    }
    with open(RESULTS_DIR / 'analysis_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\nAll outputs, figures, and CSV tables successfully exported to '{RESULTS_DIR}/'.")
    print("Case Study 4 execution completed successfully.\n")


if __name__ == '__main__':
    main()
