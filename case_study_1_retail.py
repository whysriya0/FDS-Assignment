"""
Fundamentals of Data Science - Case Study 1
Title: Online Retail Market Basket Clustering and Association Analysis
Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3 | Academic Year: 2026-2027
Faculty: Assistant Prof. Durga Devi

Description:
This script performs complete statistical and unsupervised machine learning analysis
on transaction basket records from an online retail dataset.
Key workflow steps:
1. Data loading, verification, cleaning, and basket normalization.
2. Descriptive statistics of transactions and basket sizes.
3. Frequency analysis of individual products.
4. Binary representation (one-hot encoding) and PCA dimensionality reduction.
5. Cluster number selection via Silhouette coefficient and Davies-Bouldin index.
6. Execution and comparison of four clustering algorithms:
   - K-Means
   - Agglomerative Hierarchical Clustering (Ward's linkage)
   - DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
   - Spectral Clustering
7. Hierarchical dendrogram and 2D PCA cluster projection.
8. Qualitative cluster profiling (product prevalence, lift, average basket size) and heatmap.
9. Export of all audit metrics, tables, and high-resolution figures.
"""

from pathlib import Path
from collections import Counter
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score
from scipy.cluster.hierarchy import linkage, dendrogram

# Suppress minor warnings for clean console outputs
warnings.filterwarnings('ignore', category=FutureWarning)

# Reproducibility settings
SEED = 42
rng = np.random.default_rng(SEED)

# Visual styling
sns.set_theme(style='whitegrid', context='notebook')
COLORS = ['#185a7d', '#e07a5f', '#4d908e', '#f2cc8f', '#6d597a', '#999999']
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

ASSET_DIR = Path('case_study_1_results')
ASSET_DIR.mkdir(exist_ok=True, parents=True)


def locate_data_file(filename: str) -> Path:
    """Locate data file across current directory, subfolders, or script directory."""
    candidates = [
        Path.cwd() / filename,
        Path.cwd() / '1' / filename,
        Path(__file__).resolve().parent / filename if '__file__' in globals() else None,
        Path(__file__).resolve().parent / '1' / filename if '__file__' in globals() else None
    ]
    for p in candidates:
        if p and p.exists():
            return p
    raise FileNotFoundError(f"Could not locate dataset '{filename}' in current directory or '1/'.")


def clean_basket(row: pd.Series) -> list:
    """Clean and deduplicate product names within an individual transaction."""
    items = []
    for value in row.dropna().astype(str):
        item = ' '.join(value.strip().lower().split())
        if item and item not in items:
            items.append(item)
    return items


def main():
    print("=" * 70)
    print("CASE STUDY 1: ONLINE RETAIL BASKET CLUSTERING & ANALYSIS")
    print("Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3")
    print("=" * 70)

    # 1. Load Data
    csv_path = locate_data_file('Online retail_new.csv')
    print(f"\n[1/7] Loading dataset from: {csv_path}")
    raw = pd.read_csv(csv_path, header=None)
    print(f"Raw dataset shape: {raw.shape} (rows: transactions, columns: maximum item slots)")

    # 2. Preprocess & Clean Baskets
    baskets = [clean_basket(row) for _, row in raw.iterrows()]
    basket_sizes = np.array([len(b) for b in baskets])
    item_counts = Counter(item for basket in baskets for item in set(basket))

    print(f"Cleaned transactions count: {len(baskets):,}")
    print(f"Unique products cataloged: {len(item_counts)}")
    print(f"Empty baskets detected: {int((basket_sizes == 0).sum())}")
    
    # Optional companion workbook cross-validation
    try:
        xlsx_path = locate_data_file('Online retail.xlsx')
        workbook = pd.read_excel(xlsx_path, header=None).dropna(how='all')
        excel_baskets = [clean_basket(pd.Series(str(row.iloc[0]).split(','))) for _, row in workbook.iterrows()]
        print(f"Companion workbook validation: {len(excel_baskets)} baskets | Match CSV: {excel_baskets == baskets}")
    except Exception as e:
        print(f"Companion workbook validation note: {e}")

    # 3. Descriptive Statistics
    print("\n[2/7] Calculating Descriptive Statistics...")
    size_stats = pd.Series(basket_sizes).describe(percentiles=[.25, .5, .75, .9, .95]).round(3)
    frequency = pd.Series(item_counts).sort_values(ascending=False)

    summary = {
        'transactions': len(baskets),
        'products': len(item_counts),
        'total_item_occurrences': int(basket_sizes.sum()),
        'mean_size': float(basket_sizes.mean()),
        'median_size': float(np.median(basket_sizes)),
        'std_size': float(basket_sizes.std()),
        'max_size': int(basket_sizes.max()),
        'singleton_share': float((basket_sizes == 1).mean()),
        'small_share_le_2': float((basket_sizes <= 2).mean()),
        'large_share_ge_10': float((basket_sizes >= 10).mean()),
        'top10_occurrence_share': float(frequency.head(10).sum() / frequency.sum())
    }
    print("Basket Size Summary:\n", size_stats)
    print("\nTop 10 Most Frequently Purchased Items:\n", frequency.head(10))

    # 4. Generate Visualizations for EDA
    print("\n[3/7] Generating EDA Visualizations...")

    # Fig 1: Top 20 Popular Products
    fig, ax = plt.subplots(figsize=(11, 6))
    top20 = frequency.head(20)
    bars = ax.barh(top20.index[::-1], top20.values[::-1], color=COLORS[0], edgecolor='none', alpha=0.85)
    for bar in bars:
        w = bar.get_width()
        pct = (w / len(baskets)) * 100
        ax.text(w + 15, bar.get_y() + bar.get_height() / 2, f"{int(w)} ({pct:.1f}%)",
                va='center', ha='left', fontsize=9, color='#333333')
    ax.set_title('Top 20 Most Frequent Products in Retail Transactions', pad=12)
    ax.set_xlabel('Number of Baskets Containing Product')
    ax.set_ylabel('Product Name')
    ax.set_xlim(0, max(top20.values) * 1.15)
    fig.tight_layout()
    fig.savefig(ASSET_DIR / 'fig1_product_frequency.png', dpi=200)
    plt.close()
    print("Saved: fig1_product_frequency.png")

    # Fig 2: Basket Size Distribution
    fig, ax = plt.subplots(figsize=(11, 6))
    max_b = min(int(basket_sizes.max()), 25)
    bins = np.arange(0.5, max_b + 1.5, 1)
    ax.hist(basket_sizes, bins=bins, color=COLORS[1], edgecolor='white', alpha=0.85, rwidth=0.85)
    ax.axvline(basket_sizes.mean(), color='#185a7d', linestyle='--', linewidth=2,
               label=f"Mean: {basket_sizes.mean():.2f}")
    ax.axvline(np.median(basket_sizes), color='#4d908e', linestyle='-', linewidth=2,
               label=f"Median: {np.median(basket_sizes):.1f}")
    ax.set_title('Distribution of Transaction Basket Sizes', pad=12)
    ax.set_xlabel('Number of Unique Items per Transaction (Basket Size)')
    ax.set_ylabel('Number of Transactions')
    ax.set_xticks(range(1, max_b + 1))
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(ASSET_DIR / 'fig2_basket_size.png', dpi=200)
    plt.close()
    print("Saved: fig2_basket_size.png")

    # 5. One-Hot Encoding and PCA
    print("\n[4/7] One-Hot Encoding & Dimensionality Reduction (PCA)...")
    encoder = MultiLabelBinarizer()
    X = encoder.fit_transform(baskets).astype(np.float32)
    products = np.array(encoder.classes_)
    print(f"One-hot binary feature matrix shape: {X.shape} | Matrix Density: {X.mean():.4f}")

    n_pcs = 20
    pca = PCA(n_components=n_pcs, random_state=SEED)
    Z = pca.fit_transform(X)
    Z_standardized = StandardScaler().fit_transform(Z)
    explained = pca.explained_variance_ratio_
    cum_var = np.cumsum(explained)

    print(f"Variance explained by first 2 PCs: {cum_var[1]:.2%}")
    print(f"Cumulative variance retained by {n_pcs} PCs: {cum_var[-1]:.2%}")

    # Fig 3: PCA Variance Scree Plot
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(range(1, n_pcs + 1), cum_var * 100, marker='o', color=COLORS[0], linewidth=2.2, label='Cumulative Variance')
    ax.bar(range(1, n_pcs + 1), explained * 100, alpha=0.6, color=COLORS[2], label='Individual PC Variance')
    ax.axhline(50, color='#888888', linestyle=':', label='50% Threshold')
    ax.set_title('Cumulative and Individual PCA Variance Retained Across 20 Principal Components', pad=12)
    ax.set_xlabel('Principal Component Index')
    ax.set_ylabel('Explained Variance (%)')
    ax.set_xticks(range(1, n_pcs + 1))
    ax.set_ylim(0, 65)
    ax.legend(frameon=True, loc='center right')
    fig.tight_layout()
    fig.savefig(ASSET_DIR / 'fig3_pca_variance.png', dpi=200)
    plt.close()
    print("Saved: fig3_pca_variance.png")

    # 6. Cluster Diagnostics: K Selection (Silhouette & Davies-Bouldin)
    print("\n[5/7] Evaluating Optimal K for K-Means Clustering...")
    k_rows = []
    for k in range(2, 9):
        labels_k = KMeans(n_clusters=k, n_init=20, random_state=SEED).fit_predict(Z)
        k_rows.append({
            'k': k,
            'silhouette': silhouette_score(Z, labels_k, sample_size=3000, random_state=SEED),
            'davies_bouldin': davies_bouldin_score(Z, labels_k)
        })
    k_scan = pd.DataFrame(k_rows).set_index('k')
    print("K Selection Scan Table:\n", k_scan.round(4))

    # Fig 4: K-Selection Diagnostic
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(k_scan.index, k_scan.silhouette, marker='o', color=COLORS[0], linewidth=2)
    axes[0].set_title('Silhouette Score by K (Higher is Better)')
    axes[0].set_xlabel('Number of Clusters (K)')
    axes[0].set_ylabel('Silhouette Coefficient')
    axes[0].set_xticks(k_scan.index)

    axes[1].plot(k_scan.index, k_scan.davies_bouldin, marker='s', color=COLORS[1], linewidth=2)
    axes[1].set_title('Davies-Bouldin Index by K (Lower is Better)')
    axes[1].set_xlabel('Number of Clusters (K)')
    axes[1].set_ylabel('Davies-Bouldin Index')
    axes[1].set_xticks(k_scan.index)

    fig.suptitle('Figure 4. Cluster Validation Diagnostics Across Values of K', weight='bold', y=1.02)
    fig.tight_layout()
    fig.savefig(ASSET_DIR / 'fig4_k_selection.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved: fig4_k_selection.png")

    # 7. Multi-Algorithm Clustering Comparison
    print("\n[6/7] Fitting 4 Clustering Algorithms: K-Means, Hierarchical, DBSCAN, Spectral...")
    eval_idx = rng.choice(len(Z), size=2000, replace=False)
    Z_eval = Z[eval_idx]

    # Model 1: K-Means (k=5)
    kmeans = KMeans(n_clusters=5, n_init=20, random_state=SEED)
    labels_kmeans = kmeans.fit_predict(Z)

    # Model 2: Agglomerative Hierarchical (Ward, k=5)
    hier = AgglomerativeClustering(n_clusters=5, linkage='ward')
    labels_hier = hier.fit_predict(Z)

    # Model 3: DBSCAN
    dbscan = DBSCAN(eps=3.5, min_samples=15, n_jobs=-1)
    labels_dbscan = dbscan.fit_predict(Z_standardized)

    # Model 4: Spectral Clustering on evaluation sample
    spectral = SpectralClustering(n_clusters=5, affinity='nearest_neighbors', n_neighbors=20,
                                  assign_labels='kmeans', n_init=10, random_state=SEED)
    labels_spectral_eval = spectral.fit_predict(Z_eval)

    def partition_metrics(space, labels, coverage=1.0, note=''):
        if not 2 <= len(np.unique(labels)) < len(labels):
            return {'silhouette': np.nan, 'davies_bouldin': np.nan,
                    'coverage': coverage, 'note': note + '; fewer than two valid clusters'}
        return {
            'silhouette': silhouette_score(space, labels),
            'davies_bouldin': davies_bouldin_score(space, labels),
            'coverage': coverage,
            'note': note
        }

    metric_rows = {}
    metric_rows['K-means'] = partition_metrics(Z_eval, labels_kmeans[eval_idx], 1.0, 'Full-data fit; 5 clusters')
    metric_rows['Ward hierarchical'] = partition_metrics(Z_eval, labels_hier[eval_idx], 1.0, 'Full-data fit; 5 clusters')
    nonnoise_eval = labels_dbscan[eval_idx] >= 0
    metric_rows['DBSCAN (non-noise)'] = partition_metrics(
        Z_standardized[eval_idx][nonnoise_eval],
        labels_dbscan[eval_idx][nonnoise_eval],
        float(nonnoise_eval.mean()),
        'Noise excluded; standardized PC space'
    )
    metric_rows['Spectral (sample fit)'] = partition_metrics(Z_eval, labels_spectral_eval, 1.0, 'Fit only on evaluation sample')

    metrics = pd.DataFrame(metric_rows).T
    metrics.insert(0, 'model', metrics.index)
    metrics = metrics.reset_index(drop=True)
    print("\nClustering Model Comparison Table:\n", metrics.to_string())

    # Fig 5: Dendrogram (250 Sample)
    dendro_idx = rng.choice(len(Z), size=250, replace=False)
    Z_sample = Z[dendro_idx]
    link_mat = linkage(Z_sample, method='ward')
    fig, ax = plt.subplots(figsize=(12, 6))
    dendrogram(link_mat, truncate_mode='lastp', p=30, ax=ax,
               color_threshold=link_mat[-4, 2], above_threshold_color='#777777')
    ax.set_title('Figure 5. Agglomerative Hierarchical Clustering Dendrogram (Ward Linkage)', pad=12)
    ax.set_xlabel('Sample Basket Index or Merged Cluster Size')
    ax.set_ylabel('Ward Euclidean Distance')
    fig.tight_layout()
    fig.savefig(ASSET_DIR / 'fig5_dendrogram.png', dpi=200)
    plt.close()
    print("Saved: fig5_dendrogram.png")

    # Fig 6: K-Means 2D PCA Clusters
    fig, ax = plt.subplots(figsize=(11, 7))
    for c in range(5):
        c_indices = np.where(labels_kmeans == c)[0]
        sample_size = min(450, len(c_indices))
        sample_subset = rng.choice(c_indices, size=sample_size, replace=False)
        ax.scatter(Z[sample_subset, 0], Z[sample_subset, 1], s=14, alpha=0.55,
                   color=COLORS[c], label=f'Cluster {c} (n={len(c_indices):,})')
    ax.set_title('Figure 6. K-Means Basket Groups in First Two Principal Components (k=5)', pad=12)
    ax.set_xlabel(f'Principal Component 1 ({explained[0]:.1%} variance)')
    ax.set_ylabel(f'Principal Component 2 ({explained[1]:.1%} variance)')
    ax.legend(markerscale=2.5, frameon=True, title='Clusters')
    fig.tight_layout()
    fig.savefig(ASSET_DIR / 'fig6_pca_clusters.png', dpi=200)
    plt.close()
    print("Saved: fig6_pca_clusters.png")

    # 8. Cluster Profiling and Interpretation
    print("\n[7/7] Profiling K-Means Clusters & Computing Association Lift...")
    profile_rows = []
    overall_prev = X.mean(axis=0)
    for c in range(5):
        mask = (labels_kmeans == c)
        prev = X[mask].mean(axis=0)
        lift = prev / (overall_prev + 1e-12)
        for rank, idx in enumerate(np.argsort(-prev)[:6], 1):
            profile_rows.append({
                'cluster': c,
                'baskets': int(mask.sum()),
                'mean_size': float(basket_sizes[mask].mean()),
                'rank': rank,
                'product': products[idx],
                'prevalence': float(prev[idx]),
                'lift': float(lift[idx])
            })
    profiles = pd.DataFrame(profile_rows)

    print("\nCluster Key Characteristics:")
    for c in range(5):
        p = profiles[profiles.cluster == c]
        top_items = ', '.join([f"{r.product} ({r.prevalence:.0%}, lift: {r.lift:.2f})" for r in p.itertuples()])
        print(f"Cluster {c} (n={p.baskets.iloc[0]}, avg size={p.mean_size.iloc[0]:.2f}): {top_items}")

    # Fig 7: Cluster Heatmap
    top_products = list(frequency.head(12).index)
    heat = np.array([[X[labels_kmeans == c][:, list(products).index(p)].mean() for p in top_products] for c in range(5)])
    fig, ax = plt.subplots(figsize=(13, 6))
    sns.heatmap(heat, annot=True, fmt='.2f', cmap='YlGnBu', xticklabels=top_products,
                yticklabels=[f'Cluster {c}' for c in range(5)],
                cbar_kws={'label': 'Within-Cluster Product Prevalence'}, ax=ax)
    ax.set_title('Figure 7. Top Product Prevalence Across 5 K-Means Basket Clusters', pad=12)
    ax.set_xlabel('Product Name')
    ax.set_ylabel('Cluster ID')
    ax.tick_params(axis='x', rotation=35)
    fig.tight_layout()
    fig.savefig(ASSET_DIR / 'fig7_cluster_heatmap.png', dpi=200)
    plt.close()
    print("Saved: fig7_cluster_heatmap.png")

    # Save summary results
    results = {
        'summary': summary,
        'pca_variance_20': float(explained.sum()),
        'pca_variance_2': float(explained[:2].sum()),
        'k_scan': k_scan.reset_index().to_dict('records'),
        'metrics': metrics.to_dict('records'),
        'dbscan_noise_share': float((labels_dbscan == -1).mean()),
        'kmeans_sizes': np.bincount(labels_kmeans).tolist(),
        'profiles': profiles.to_dict('records')
    }
    with open(ASSET_DIR / 'results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\nAll outputs, figures, and summary JSON successfully saved to '{ASSET_DIR}/'.")
    print("Case Study 1 execution completed successfully.\n")


if __name__ == '__main__':
    main()
