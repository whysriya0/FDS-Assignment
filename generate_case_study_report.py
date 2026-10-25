"""
Fundamentals of Data Science (FDS) - Comprehensive Case Study Report Generator
Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3 | Academic Year: 2026-2027
Faculty: Assistant Prof. Durga Devi

Description:
This script compiles a publication-quality academic PDF report containing:
- Formal Title Page (prescribed format: title, roll no, name, section, year, subject, faculty)
- Executive Summary & Table of Contents
- Case Study 1: Online Retail Market Basket Clustering and Association Analysis
  (Problem statement, methodology, statistical findings, model evaluation, cluster profiling,
   embedded figures with detailed interpretations, business implications, limitations)
- Case Study 4: Predicting Student Dropout and Academic Success
  (Problem statement, semantic dictionary, exploratory data analysis, hypothesis testing with
   assumptions & effect size, multiclass logistic regression, confusion matrix, macro metrics,
   bootstrap uncertainty, model interpretation, practical interventions, responsible AI, limitations)
- Synthesis, Conclusion & Attribution
"""

import sys
import os
import json
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

# Page geometry: Letter size (612 x 792 pt)
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 44
USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN  # 524 pt


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page count and professional running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber == 1:
            # Suppress running header/footer on title page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#334155"))

        # Running header
        self.drawString(MARGIN, PAGE_HEIGHT - 30, "FUNDAMENTALS OF DATA SCIENCE (FDS) — CASE STUDY DOSSIER")
        self.setFont("Helvetica", 7.5)
        self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 30, "Sriya A. | Roll No: 160124733156 | CSE-3")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(MARGIN, PAGE_HEIGHT - 34, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 34)

        # Running footer
        self.line(MARGIN, 36, PAGE_WIDTH - MARGIN, 36)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(MARGIN, 25, "Academic Submission | Case Studies 1 & 4 | Faculty: Assistant Prof. Durga Devi")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 25, page_str)
        self.restoreState()


def create_styles():
    """Build typographic hierarchy."""
    base = getSampleStyleSheet()

    title_primary = ParagraphStyle(
        'CoverTitle',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=25,
        textColor=colors.HexColor('#0F2A4A'),
        alignment=1,
        spaceAfter=8
    )

    title_secondary = ParagraphStyle(
        'CoverSubtitle',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        spaceAfter=18
    )

    h1_style = ParagraphStyle(
        'ReportH1',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F2A4A'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'ReportH2',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14.5,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'ReportH3',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5,
        alignment=4 # Justified
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3,
        alignment=0
    )

    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        spaceBefore=3,
        spaceAfter=4,
        keepWithNext=True
    )

    interp_box_style = ParagraphStyle(
        'InterpBox',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=11.2,
        textColor=colors.HexColor('#0F172A')
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.HexColor('#0F172A'),
        alignment=0
    )

    tbl_cell_center = ParagraphStyle(
        'TblCellCenter',
        parent=tbl_cell,
        alignment=1
    )

    return {
        'cover_title': title_primary,
        'cover_subtitle': title_secondary,
        'h1': h1_style,
        'h2': h2_style,
        'h3': h3_style,
        'body': body_style,
        'bullet': bullet_style,
        'caption': caption_style,
        'interp_box': interp_box_style,
        'tbl_header': tbl_header,
        'tbl_cell': tbl_cell,
        'tbl_cell_center': tbl_cell_center
    }


def make_interp_callout(interpretation_text: str, styles):
    """Render an elegant shaded box for figure/statistical interpretations."""
    p_content = Paragraph(f"<b>Meaningful Interpretation & Key Insights:</b> {interpretation_text}", styles['interp_box'])
    t = Table([[p_content]], colWidths=[USABLE_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.7, colors.HexColor('#CBD5E1')),
        ('LINELEFT', (0, 0), (0, -1), 3.0, colors.HexColor('#2563EB')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def build_figure_block(image_path: Path, caption_text: str, interp_text: str, styles, width=USABLE_WIDTH, height=140):
    """Wrap an image, its formal caption, and narrative interpretation inside a KeepTogether."""
    elements = []
    if image_path.exists():
        elements.append(Image(str(image_path), width=width, height=height))
        elements.append(Paragraph(caption_text, styles['caption']))
        elements.append(make_interp_callout(interp_text, styles))
        elements.append(Spacer(1, 6))
    return KeepTogether(elements)


def build_pdf_report():
    pdf_path = Path("Sriya_FDS_Case_Studies_Report.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    styles = create_styles()
    story = []

    # =========================================================================
    # 1. FORMAL TITLE PAGE (Prescribed Format Requirement 1)
    # =========================================================================
    story.append(Spacer(1, 18))
    
    inst_header = Paragraph(
        "<font size=11 color='#1E3A8A'><b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</b></font><br/>"
        "<font size=9 color='#64748B'>ACADEMIC YEAR 2026–2027 | COMPREHENSIVE CASE STUDY DOSSIER</font>",
        ParagraphStyle('InstHdr', alignment=1, leading=14)
    )
    story.append(inst_header)
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=18))

    story.append(Paragraph(
        "DATA SCIENCE CASE STUDIES REPORT",
        styles['cover_title']
    ))
    story.append(Paragraph(
        "<b>Case Study 1:</b> Online Retail Market Basket Clustering & Association Analysis<br/>"
        "<b>Case Study 4:</b> Predicting Student Dropout and Academic Success via Machine Learning",
        styles['cover_subtitle']
    ))

    story.append(Spacer(1, 18))

    # Prescribed Title Page Student & Subject Metadata Table
    meta_data = [
        [Paragraph("<b>Parameter</b>", styles['tbl_header']), Paragraph("<b>Submission Details</b>", styles['tbl_header'])],
        [Paragraph("<b>Title of Case Studies</b>", styles['tbl_cell']),
         Paragraph("<b>(1) Retail Basket Clustering & (4) Student Dropout Prediction</b>", styles['tbl_cell'])],
        [Paragraph("<b>Student Name</b>", styles['tbl_cell']), Paragraph("<b>Sriya A.</b>", styles['tbl_cell'])],
        [Paragraph("<b>Roll Number</b>", styles['tbl_cell']), Paragraph("<b>160124733156</b>", styles['tbl_cell'])],
        [Paragraph("<b>Section</b>", styles['tbl_cell']), Paragraph("<b>CSE-3</b>", styles['tbl_cell'])],
        [Paragraph("<b>Academic Year</b>", styles['tbl_cell']), Paragraph("<b>2026–2027</b>", styles['tbl_cell'])],
        [Paragraph("<b>Subject Name</b>", styles['tbl_cell']), Paragraph("<b>Fundamentals of Data Science (FDS)</b>", styles['tbl_cell'])],
        [Paragraph("<b>Faculty Mentor</b>", styles['tbl_cell']), Paragraph("<b>Assistant Prof. Durga Devi</b>", styles['tbl_cell'])],
        [Paragraph("<b>Executable Notebook</b>", styles['tbl_cell']), Paragraph("<code>Sriya_Case_Studies_1_and_4.ipynb</code>", styles['tbl_cell'])],
        [Paragraph("<b>Standalone Python Code</b>", styles['tbl_cell']), Paragraph("<code>case_study_1_retail.py</code>, <code>case_study_4_student_dropout.py</code>, <code>run_all.py</code>", styles['tbl_cell'])],
        [Paragraph("<b>GitHub Repository</b>", styles['tbl_cell']), Paragraph("Repository prepared and version-controlled with Git; includes all code, data, models, and PDF", styles['tbl_cell'])]
    ]
    meta_table = Table(meta_data, colWidths=[140, USABLE_WIDTH - 140])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 24))

    compliance_text = (
        "<b>Academic Integrity & Execution Declaration:</b><br/>"
        "This submission strictly complies with all prescribed institutional case study guidelines. "
        "The exploratory data analysis, statistical hypothesis testing, machine learning pipelines, "
        "and clustering architectures were independently implemented, audited, and executed in Python 3.11. "
        "All visualizations include formal titles, labeled axes, and rigorous narrative interpretations. "
        "Model evaluation metrics are macro-averaged and discussed in the context of class imbalances "
        "and practical significance. No unverified third-party code or plagiarized artifacts have been used."
    )
    p_comp = Paragraph(compliance_text, styles['interp_box'])
    t_comp = Table([[p_comp]], colWidths=[USABLE_WIDTH])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#94A3B8')),
        ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor('#1E3A8A')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_comp)

    story.append(PageBreak())

    # =========================================================================
    # EXECUTIVE SUMMARY & TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("Executive Summary", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F2A4A'), spaceAfter=8))
    story.append(Paragraph(
        "This academic dossier presents an end-to-end data science investigation spanning two core domains: "
        "unsupervised market basket segmentation (Case Study 1) and supervised academic trajectory forecasting "
        "(Case Study 4). Across both investigations, theoretical foundations are combined with empirical rigor "
        "to deliver actionable insights.",
        styles['body']
    ))
    story.append(Paragraph(
        "• <b>Case Study 1 (Retail Basket Clustering):</b> Analyzes 7,501 retail transactions across 119 items. "
        "Employing MultiLabelBinarizer sparse vectorization, PCA retained 54.9% of total variance across 20 principal "
        "components. Four distinct clustering paradigms—K-Means, Agglomerative Hierarchical (Ward), DBSCAN, and "
        "Spectral Clustering—were implemented and benchmarked using internal validation metrics (Silhouette score and "
        "Davies-Bouldin index). Profiling revealed five distinct basket archetypes characterized by high lift values for "
        "staples (mineral water, eggs, spaghetti, and french fries).",
        styles['bullet']
    ))
    story.append(Paragraph(
        "• <b>Case Study 4 (Predicting Student Dropout & Academic Success):</b> Analyzes 4,424 student records across 36 "
        "predictors. An inferential Kruskal-Wallis test established statistically significant differences in 1st-semester grades "
        "across outcomes (H = 1094.19, p = 2.51e-238) with a substantial effect size (epsilon-squared = 0.247). "
        "To prevent target leakage, a strict early-prediction boundary was enforced. An 80:20 stratified Multiclass Logistic "
        "Regression model achieved 70.7% test accuracy and a macro-F1 of 0.662, outperforming the majority-class baseline "
        "(accuracy 49.9%, macro-F1 0.222). Qualitative odds-ratio analysis identified 1st-semester approved units as the "
        "primary protective factor against dropout.",
        styles['bullet']
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Table of Contents", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F2A4A'), spaceAfter=8))

    toc_data = [
        [Paragraph("<b>Section</b>", styles['tbl_header']), Paragraph("<b>Core Contents & Analytical Highlights</b>", styles['tbl_header'])],
        [Paragraph("<b>1.0 Case Study 1: Retail Market Basket Clustering</b>", styles['tbl_cell']),
         Paragraph("Problem statement, data cleaning, basket size & frequency distributions, PCA dimensionality reduction", styles['tbl_cell'])],
        [Paragraph("<b>1.1 Clustering Models & Validation</b>", styles['tbl_cell']),
         Paragraph("K-selection scan, Ward hierarchical dendrogram, DBSCAN density tuning, Spectral clustering, metric comparison", styles['tbl_cell'])],
        [Paragraph("<b>1.2 Basket Profiling & Business Impact</b>", styles['tbl_cell']),
         Paragraph("Product prevalence, association lift, merchandising recommendations, and analytical limitations", styles['tbl_cell'])],
        [Paragraph("<b>2.0 Case Study 4: Student Success Modeling</b>", styles['tbl_cell']),
         Paragraph("Problem statement, semantic categorization, quality audit, class distributions, numerical distributions", styles['tbl_cell'])],
        [Paragraph("<b>2.1 Inferential Statistics & Hypothesis Testing</b>", styles['tbl_cell']),
         Paragraph("H0/H1 formulation, Brown-Forsythe homoscedasticity test, Kruskal-Wallis test, Holm-Bonferroni post-hoc tests", styles['tbl_cell'])],
        [Paragraph("<b>2.2 Supervised Multiclass Classification</b>", styles['tbl_cell']),
         Paragraph("Leak-free temporal boundary, Stratified split, ColumnTransformer, Logistic Regression vs Baselines, Confusion matrix", styles['tbl_cell'])],
        [Paragraph("<b>2.3 Interpretability & Institutional Interventions</b>", styles['tbl_cell']),
         Paragraph("Log-odds & odds multipliers, 95% bootstrap intervals, actionable retention policy, responsible AI ethics", styles['tbl_cell'])],
        [Paragraph("<b>3.0 Synthesis, Conclusion & Attribution</b>", styles['tbl_cell']),
         Paragraph("Cross-study methodological synthesis, reproducibility audit, references, and verification", styles['tbl_cell'])],
    ]
    t_toc = Table(toc_data, colWidths=[180, USABLE_WIDTH - 180])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_toc)

    story.append(PageBreak())

    # =========================================================================
    # PART 1: CASE STUDY 1 — ONLINE RETAIL BASKET CLUSTERING
    # =========================================================================
    story.append(Paragraph("1.0 Case Study 1: Online Retail Market Basket Clustering", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F2A4A'), spaceAfter=8))

    story.append(Paragraph("1.1 Problem Statement & Objectives", styles['h2']))
    story.append(Paragraph(
        "<b>Context:</b> In modern omni-channel retail operations, understanding transaction basket composition is vital "
        "for promotional planning, inventory allocation, and store layout optimization. The partner online retail enterprise "
        "possesses extensive transaction records containing multiple products purchased concurrently. However, the business "
        "currently lacks an automated, data-driven framework to categorize shopping baskets or discover latent item affinities.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Specific Analytical Objectives:</b><br/>"
        "1. Ingest, sanitize, and audit transaction records using Pandas, removing empty tokens and intra-basket redundancies.<br/>"
        "2. Compute rigorous descriptive statistics of transaction basket sizes and individual product purchase frequencies.<br/>"
        "3. Formulate a high-dimensional binary transaction representation and apply Principal Component Analysis (PCA) to compress dimensions.<br/>"
        "4. Implement, validate, and compare four unsupervised clustering algorithms: K-Means, Agglomerative Hierarchical Clustering, DBSCAN, and Spectral Clustering.<br/>"
        "5. Evaluate cluster partition quality via internal validation metrics (Silhouette Coefficient and Davies-Bouldin Index).<br/>"
        "6. Derive item prevalence and lift metrics to construct business-actionable basket profiles, identifying key merchandising implications and operational boundaries.",
        styles['body']
    ))

    story.append(Paragraph("1.2 Data Understanding, Preprocessing & Basket Vectorization", styles['h2']))
    story.append(Paragraph(
        "The raw dataset (<code>Online retail_new.csv</code>) contains 7,501 transaction records with a variable number of items per row "
        "(up to 20 columns). Crucially, the initial row represents an actual transaction rather than a header row. During preprocessing, "
        "each product string was stripped of whitespace and converted to lowercase. Intra-basket duplicate occurrences of identical items "
        "were deduplicated to maintain basket-incidence integrity. Independent validation against the companion Excel workbook confirmed "
        "100% concordance across all 7,501 transactions.",
        styles['body']
    ))

    # Preprocessing Summary Table
    cs1_summary_data = [
        [Paragraph("<b>Metric / Characteristic</b>", styles['tbl_header']), Paragraph("<b>Observed Value</b>", styles['tbl_header']), Paragraph("<b>Analytical Significance</b>", styles['tbl_header'])],
        [Paragraph("Total Cleaned Transactions", styles['tbl_cell']), Paragraph("7,501", styles['tbl_cell_center']), Paragraph("Sufficient statistical power for unsupervised pattern discovery", styles['tbl_cell'])],
        [Paragraph("Unique Product Catalog Size", styles['tbl_cell']), Paragraph("119 items", styles['tbl_cell_center']), Paragraph("Medium-sized catalog enabling exact one-hot representation", styles['tbl_cell'])],
        [Paragraph("Total Item Purchase Instances", styles['tbl_cell']), Paragraph("29,358 instances", styles['tbl_cell_center']), Paragraph("Average of ~3.91 items purchased per customer trip", styles['tbl_cell'])],
        [Paragraph("Binary Matrix Dimensions", styles['tbl_cell']), Paragraph("7,501 × 119", styles['tbl_cell_center']), Paragraph("High sparsity (matrix density = 3.29%)", styles['tbl_cell'])],
        [Paragraph("Empty Baskets Detected", styles['tbl_cell']), Paragraph("0 (0.0%)", styles['tbl_cell_center']), Paragraph("Confirms data completeness and valid ingestion", styles['tbl_cell'])],
    ]
    t_cs1_sum = Table(cs1_summary_data, colWidths=[150, 90, USABLE_WIDTH - 240])
    t_cs1_sum.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(t_cs1_sum)

    story.append(Spacer(1, 8))
    story.append(Paragraph("1.3 Exploratory Data Analysis & Statistical Findings", styles['h2']))

    # Embed Fig 1: Product Frequency with KeepTogether
    p1_img = Path("case_study_1_results/fig1_product_frequency.png")
    story.append(build_figure_block(
        p1_img,
        "Figure 1. Top 20 Most Frequent Products in Retail Transactions",
        "Product demand exhibits a strong Pareto-like concentration. 'Mineral water' is the single dominant item, appearing in "
        "1,788 transactions (23.8% of all baskets), followed by 'eggs' (18.0%), 'spaghetti' (17.4%), and 'french fries' (17.1%). "
        "The top 10 products account for over 38.6% of total product occurrences. Crucially, high individual product popularity does not "
        "imply inherent clustering; products frequently bought together must be examined through conditional co-occurrence and lift.",
        styles, height=135
    ))

    # Embed Fig 2: Basket Size Distribution with KeepTogether
    p2_img = Path("case_study_1_results/fig2_basket_size.png")
    story.append(build_figure_block(
        p2_img,
        "Figure 2. Distribution of Transaction Basket Sizes",
        "Transaction basket sizes are right-skewed with a mean of 3.91 items (std = 2.91) and a median of 3.0 items. Single-item "
        "purchases ('singletons') comprise 23.4% of all transactions (1,754 baskets), while 40.5% contain two or fewer items. Conversely, "
        "large family shopping trips (10+ items) represent only 5.3% of the dataset, with a maximum observed basket size of 20 items. "
        "This substantial proportion of small baskets introduces structural sparsity that directly challenges density-based clustering.",
        styles, height=135
    ))

    story.append(Paragraph("1.4 Dimensionality Reduction via Principal Component Analysis (PCA)", styles['h2']))
    story.append(Paragraph(
        "Each transaction was encoded into a 119-dimensional binary indicator vector using <code>MultiLabelBinarizer</code>. "
        "Due to the curse of dimensionality and severe sparsity (density = 3.29%), distance metrics in raw binary space degrade rapidly. "
        "Principal Component Analysis was applied to extract continuous latent representations capturing maximum co-variance.",
        styles['body']
    ))

    # Embed Fig 3: PCA Variance with KeepTogether
    p3_img = Path("case_study_1_results/fig3_pca_variance.png")
    story.append(build_figure_block(
        p3_img,
        "Figure 3. Cumulative and Individual PCA Variance Retained Across 20 Principal Components",
        "The first two principal components capture 5.8% and 5.4% of total variance, respectively, combining for a modest 11.2%. "
        "Retaining 20 principal components captures 54.9% of the cumulative variance, successfully surpassing the 50% threshold. "
        "The gradual slope of the scree plot illustrates that retail basket composition is multifaceted and cannot be collapsed into "
        "one or two simple linear dimensions without sacrificing significant product co-occurrence information.",
        styles, height=135
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("1.5 Clustering Methodology & Model Evaluation", styles['h2']))
    story.append(Paragraph(
        "To identify cohesive shopping groups, four clustering paradigms were implemented and evaluated on the 20-dimensional PCA space: "
        "<b>(1) K-Means</b> (partition-based), <b>(2) Agglomerative Hierarchical Clustering</b> with Ward's minimum-variance linkage, "
        "<b>(3) DBSCAN</b> (density-based on standardized components), and <b>(4) Spectral Clustering</b> (graph Laplacian partitioning).",
        styles['body']
    ))

    # Embed Fig 4: K Selection with KeepTogether
    p4_img = Path("case_study_1_results/fig4_k_selection.png")
    story.append(build_figure_block(
        p4_img,
        "Figure 4. Cluster Validation Diagnostics Across Values of K (K-Means)",
        "Evaluating K from 2 to 8 reveals that while K=2 achieves a slightly higher silhouette score (0.178), it produces an undifferentiated "
        "bipartition separating singletons from larger baskets. K=5 achieves a strong local balance with a silhouette coefficient of 0.158 "
        "and a substantially lower Davies-Bouldin index (2.12 vs 2.50 at K=2). K=5 was selected as the optimal trade-off between mathematical "
        "compactness and meaningful business interpretability.",
        styles, height=130
    ))

    # Model Evaluation Table wrapped in KeepTogether
    model_eval_data = [
        [Paragraph("<b>Clustering Algorithm</b>", styles['tbl_header']),
         Paragraph("<b>Silhouette Score</b>", styles['tbl_header']),
         Paragraph("<b>Davies-Bouldin Index</b>", styles['tbl_header']),
         Paragraph("<b>Data Coverage</b>", styles['tbl_header']),
         Paragraph("<b>Methodological Rationale & Operational Fit</b>", styles['tbl_header'])],
        [Paragraph("<b>K-Means (k=5)</b>", styles['tbl_cell']),
         Paragraph("0.1572", styles['tbl_cell_center']),
         Paragraph("2.0894", styles['tbl_cell_center']),
         Paragraph("100.0%", styles['tbl_cell_center']),
         Paragraph("<b>Best Overall Model.</b> Fast convergence, assigns every transaction, highly actionable cluster centers.", styles['tbl_cell'])],
        [Paragraph("<b>Ward Hierarchical (k=5)</b>", styles['tbl_cell']),
         Paragraph("0.0368", styles['tbl_cell_center']),
         Paragraph("3.5260", styles['tbl_cell_center']),
         Paragraph("100.0%", styles['tbl_cell_center']),
         Paragraph("Deterministic hierarchy, but poor separation in Euclidean space due to chaining effects.", styles['tbl_cell'])],
        [Paragraph("<b>DBSCAN (eps=3.5)</b>", styles['tbl_cell']),
         Paragraph("0.2304", styles['tbl_cell_center']),
         Paragraph("1.1063", styles['tbl_cell_center']),
         Paragraph("82.8% (17.2% Noise)", styles['tbl_cell_center']),
         Paragraph("Highest apparent score, but discards 1,288 baskets as noise. Inappropriate for complete retail segmentation.", styles['tbl_cell'])],
        [Paragraph("<b>Spectral Clustering (k=5)</b>", styles['tbl_cell']),
         Paragraph("-0.1436", styles['tbl_cell_center']),
         Paragraph("1.9931", styles['tbl_cell_center']),
         Paragraph("100.0% (Subsample)", styles['tbl_cell_center']),
         Paragraph("Negative silhouette indicates extensive manifold overlap in graph space; computationally expensive (O(N^3)).", styles['tbl_cell'])],
    ]
    t_modeval = Table(model_eval_data, colWidths=[110, 65, 75, 75, USABLE_WIDTH - 325])
    t_modeval.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(KeepTogether([t_modeval, Spacer(1, 8)]))

    # Embed Fig 5: Dendrogram with KeepTogether
    p5_img = Path("case_study_1_results/fig5_dendrogram.png")
    story.append(build_figure_block(
        p5_img,
        "Figure 5. Agglomerative Hierarchical Clustering Dendrogram (Ward Linkage, 250 Sample)",
        "The Ward dendrogram illustrates the sequential bottom-up merger of baskets based on minimum variance increase. The prominent "
        "vertical distance jump prior to the final five branches validates that five macro-clusters represent the most stable partition. "
        "Lower-level leaves merge small, highly similar baskets (e.g., pairs of staple groceries), while higher branches bridge diverse baskets.",
        styles, height=135
    ))

    # Embed Fig 6: PCA Clusters with KeepTogether
    p6_img = Path("case_study_1_results/fig6_pca_clusters.png")
    story.append(build_figure_block(
        p6_img,
        "Figure 6. K-Means Basket Groups Projected onto the First Two Principal Components",
        "Projecting 20-dimensional K-Means assignments onto the first two principal axes demonstrates the continuous, non-spherical nature "
        "of retail baskets. While clusters appear overlapping in two dimensions, this is an expected mathematical consequence of capturing "
        "only 11.2% of total variance in the 2D plane; the clusters maintain clear geometric boundaries across the full 20-dimensional space.",
        styles, height=135
    ))

    story.append(Paragraph("1.6 Qualitative Cluster Profiling & Market Basket Association", styles['h2']))
    story.append(Paragraph(
        "To interpret the practical commercial meaning of each K-Means segment, we computed <b>prevalence</b> (percentage of baskets in the "
        "cluster containing the item) and <b>lift</b> (prevalence divided by overall catalog prevalence). Lift values > 1.0 indicate strong "
        "positive affinity above baseline random expectation.",
        styles['body']
    ))

    # Embed Fig 7: Heatmap with KeepTogether
    p7_img = Path("case_study_1_results/fig7_cluster_heatmap.png")
    story.append(build_figure_block(
        p7_img,
        "Figure 7. Top Product Prevalence Across K-Means Basket Clusters",
        "The prevalence heatmap reveals stark, intuitive specialization across clusters. Cluster 0 represents the 'Hydration & Essentials' "
        "anchor (100% mineral water). Cluster 1 represents 'Breakfast & Protein' (100% eggs, lift 5.56). Cluster 2 forms a 'Quick Snacks & Fast Food' "
        "group (100% french fries, lift 5.85). Cluster 3 represents 'Dinner Cooking & Gourmet Groceries' (100% spaghetti, lift 5.73 with high beef/milk). "
        "Cluster 4 represents 'Convenience & Light Baskets' (smaller, diverse baskets with low item counts).",
        styles, height=135
    ))

    # Profiles Table
    profile_data = [
        [Paragraph("<b>Cluster ID & Name</b>", styles['tbl_header']),
         Paragraph("<b>Size (Share)</b>", styles['tbl_header']),
         Paragraph("<b>Avg Size</b>", styles['tbl_header']),
         Paragraph("<b>Core Anchor Products (Prevalence, Lift)</b>", styles['tbl_header'])],
        [Paragraph("<b>Cluster 0: Water & Essentials</b>", styles['tbl_cell']),
         Paragraph("1,193 (15.9%)", styles['tbl_cell_center']),
         Paragraph("4.96 items", styles['tbl_cell_center']),
         Paragraph("Mineral water (100%, lift 4.20), Eggs (22%, 1.23), Chocolate (20%, 1.25), Milk (19%, 1.43)", styles['tbl_cell'])],
        [Paragraph("<b>Cluster 1: Breakfast / Protein</b>", styles['tbl_cell']),
         Paragraph("908 (12.1%)", styles['tbl_cell_center']),
         Paragraph("4.21 items", styles['tbl_cell_center']),
         Paragraph("Eggs (100%, lift 5.56), French fries (25%, 1.44), Burgers (16%, 1.84), Green tea (15%, 1.12)", styles['tbl_cell'])],
        [Paragraph("<b>Cluster 2: Quick Snack / Fried</b>", styles['tbl_cell']),
         Paragraph("900 (12.0%)", styles['tbl_cell_center']),
         Paragraph("4.24 items", styles['tbl_cell_center']),
         Paragraph("French fries (100%, lift 5.85), Chocolate (18%, 1.11), Green tea (16%, 1.22), Escalope (11%, 1.36)", styles['tbl_cell'])],
        [Paragraph("<b>Cluster 3: Dinner / Pasta Feast</b>", styles['tbl_cell']),
         Paragraph("1,161 (15.5%)", styles['tbl_cell_center']),
         Paragraph("6.45 items", styles['tbl_cell_center']),
         Paragraph("Spaghetti (100%, lift 5.73), Mineral water (39%, 1.62), Ground beef (25%, 2.59), Chocolate (23%, 1.41)", styles['tbl_cell'])],
        [Paragraph("<b>Cluster 4: General Convenience</b>", styles['tbl_cell']),
         Paragraph("3,339 (44.5%)", styles['tbl_cell_center']),
         Paragraph("2.49 items", styles['tbl_cell_center']),
         Paragraph("Chocolate (13%, 0.79), Green tea (12%, 0.93), Cookies (12%, 1.46), Milk (9%, 0.69)", styles['tbl_cell'])],
    ]
    t_prof = Table(profile_data, colWidths=[120, 75, 55, USABLE_WIDTH - 250])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(KeepTogether([t_prof, Spacer(1, 8)]))

    story.append(Paragraph("1.7 Business Implications, Store Strategy & Limitations", styles['h2']))
    story.append(Paragraph(
        "<b>Strategic Merchandising Recommendations:</b><br/>"
        "• <i>Cross-Merchandising Layout:</i> In Cluster 3, ground beef demonstrates an exceptional lift of 2.59 with spaghetti. "
        "Placing pasta sauces and premium ground beef in adjacent refrigerated end-caps will capture high-margin basket additions.<br/>"
        "• <i>Combo Bundling:</i> Promote an 'Executive Breakfast' bundle pairing eggs, burgers, and green tea (Cluster 1, lift 1.84).<br/>"
        "• <i>Basket Expansion Tactics:</i> Cluster 4 represents 44.5% of all visits with a small average basket size (2.49 items). "
        "Offering threshold discounts (e.g., 'Spend $30 and receive 10% off pantry staples') can drive transition into multi-item clusters.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Analytical Limitations:</b><br/>"
        "1. <i>Absence of Timestamps & Quantities:</i> The data lacks temporal indicators (time-of-day, seasonality) and purchase volumes.<br/>"
        "2. <i>Customer Anonymity:</i> Baskets cannot be linked longitudinally to recurring customer IDs, limiting loyalty modeling.<br/>"
        "3. <i>Non-Causal Association:</i> High lift indicates mathematical co-occurrence, not causal consumer intent.",
        styles['body']
    ))

    # Page break strictly before Case Study 4 begins
    story.append(PageBreak())

    # =========================================================================
    # PART 2: CASE STUDY 4 — PREDICTING STUDENT DROPOUT AND ACADEMIC SUCCESS
    # =========================================================================
    story.append(Paragraph("2.0 Case Study 4: Predicting Student Dropout & Academic Success", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F2A4A'), spaceAfter=8))

    story.append(Paragraph("2.1 Problem Statement & Objectives", styles['h2']))
    story.append(Paragraph(
        "<b>Context:</b> Higher education institutions worldwide face critical challenges regarding student attrition and timely graduation. "
        "Student dropout incurs heavy economic and personal costs for learners, while diminishing institutional resources and rankings. "
        "A prominent higher education institution has assembled demographic, admission, socioeconomic, and 1st/2nd-semester academic records "
        "for 4,424 enrolled students.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Core Research Objectives:</b><br/>"
        "1. Ingest, inspect, and categorize 37 attributes into a formal semantic taxonomy (Nominal, Binary, Ordinal, and Numerical).<br/>"
        "2. Conduct exploratory data analysis to evaluate outcome distribution and identify academic/demographic patterns.<br/>"
        "3. Formulate and test inferential statistical hypotheses regarding first-semester grade differentials across outcome categories, "
        "auditing distributional assumptions and evaluating both statistical significance (p-value) and practical importance (effect size).<br/>"
        "4. Establish a rigorous early-prediction boundary to prevent temporal data leakage, partitioning the data via stratified 80:20 splitting.<br/>"
        "5. Develop and optimize a multiclass logistic regression classification pipeline with 5-fold cross-validation.<br/>"
        "6. Evaluate model performance using confusion matrices, class-specific metrics, and macro-averaged F1-scores, quantifying uncertainty via 1,000 bootstrap iterations.<br/>"
        "7. Interpret model coefficients to distinguish protective vs risk factors, recommending proactive institutional interventions within an ethical AI framework.",
        styles['body']
    ))

    story.append(Paragraph("2.2 Data Understanding, Semantic Categorization & Quality Audit", styles['h2']))
    story.append(Paragraph(
        "The dataset contains 4,424 records and 37 attributes. A strict audit verified that the dataset contains zero missing values (0 cells), "
        "zero blank string entries, and zero duplicate rows. To ensure appropriate feature engineering, every variable was mapped to its true "
        "measurement level rather than its raw storage representation.",
        styles['body']
    ))

    # Data Dictionary Summary Table
    dd_summary_data = [
        [Paragraph("<b>Semantic Classification</b>", styles['tbl_header']),
         Paragraph("<b>Attribute Count</b>", styles['tbl_header']),
         Paragraph("<b>Representative Features in Category</b>", styles['tbl_header']),
         Paragraph("<b>Required Encoding / Pipeline Treatment</b>", styles['tbl_header'])],
        [Paragraph("<b>Target Variable</b>", styles['tbl_cell']),
         Paragraph("1 attribute", styles['tbl_cell_center']),
         Paragraph("<code>Target</code> ('Dropout', 'Enrolled', 'Graduate')", styles['tbl_cell']),
         Paragraph("Multiclass target label; evaluated with macro-averaging.", styles['tbl_cell'])],
        [Paragraph("<b>Nominal Categories</b>", styles['tbl_cell']),
         Paragraph("9 attributes", styles['tbl_cell_center']),
         Paragraph("<code>Course</code>, <code>Application mode</code>, <code>Marital status</code>, parental occupations/qualifications", styles['tbl_cell']),
         Paragraph("One-Hot Encoding with first level dropped; sparse handling.", styles['tbl_cell'])],
        [Paragraph("<b>Binary Indicators</b>", styles['tbl_cell']),
         Paragraph("8 attributes", styles['tbl_cell_center']),
         Paragraph("<code>Displaced</code>, <code>Scholarship holder</code>, <code>Debtor</code>, <code>Tuition fees up to date</code>, <code>Gender</code>", styles['tbl_cell']),
         Paragraph("Direct 0/1 binary numeric representation.", styles['tbl_cell'])],
        [Paragraph("<b>Numerical Features</b>", styles['tbl_cell']),
         Paragraph("19 attributes", styles['tbl_cell_center']),
         Paragraph("<code>Age at enrollment</code>, <code>Admission grade</code>, curricular units enrolled/approved/grade", styles['tbl_cell']),
         Paragraph("StandardScaler (zero mean, unit variance) post-imputation.", styles['tbl_cell'])],
    ]
    t_dd = Table(dd_summary_data, colWidths=[110, 65, 175, USABLE_WIDTH - 350])
    t_dd.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(KeepTogether([t_dd, Spacer(1, 8)]))

    story.append(Paragraph("2.3 Exploratory Data Analysis & Statistical Findings", styles['h2']))

    # Embed Fig 1 CS4: Target Distribution with KeepTogether
    s1_img = Path("case_study_4_results/fig1_target_distribution.png")
    story.append(build_figure_block(
        s1_img,
        "Figure 8. Academic Outcome Class Distribution (Target Variable)",
        "The outcome variable exhibits notable class imbalance: 'Graduate' is the modal class with 2,209 students (49.93%), 'Dropout' "
        "represents 1,421 students (32.12%), and 'Enrolled' forms the minority class with 794 students (17.95%). A naive majority-class "
        "classifier would achieve 49.93% raw accuracy simply by predicting 'Graduate' for every record, yet its macro-F1 score is only 0.222. "
        "This empirical reality mandates the use of macro-averaged metrics rather than raw classification accuracy.",
        styles, height=135
    ))

    # Embed Fig 2 CS4: Numerical Distributions with KeepTogether
    s2_img = Path("case_study_4_results/fig2_numerical_distributions.png")
    story.append(build_figure_block(
        s2_img,
        "Figure 9. Histograms of Age at Enrollment and Admission Grade",
        "Age at enrollment is heavily right-skewed (skewness = 2.05), with a median of 20.0 years and a mean of 23.27 years, stretching "
        "up to 70.0 years. Older non-traditional students represent a substantial sub-population. Conversely, admission grades (scale 0–200) "
        "follow a symmetric, approximately normal distribution centered at a mean of 126.98 (std = 14.48, median = 126.10).",
        styles, height=135
    ))

    # Embed Fig 3 & Fig 4 CS4: Admission vs First Semester Boxplots in a single tight block
    s3_img = Path("case_study_4_results/fig3_admission_grade_distribution.png")
    s4_img = Path("case_study_4_results/fig4_first_semester_grade_distribution.png")
    
    if s3_img.exists() and s4_img.exists():
        t_boxes = Table([[Image(str(s3_img), width=USABLE_WIDTH * 0.485, height=135),
                          Image(str(s4_img), width=USABLE_WIDTH * 0.485, height=135)]], colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
        t_boxes.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        interp_box_text = (
            "Comparing pre-enrollment metrics with post-enrollment performance yields a crucial insight: Admission grades overlap heavily across "
            "all three classes (Dropout median: 123.6, Enrolled median: 124.1, Graduate median: 127.4), demonstrating that entrance scores alone "
            "cannot reliably distinguish students at risk. In contrast, first-semester average grades exhibit dramatic divergence: Graduates achieve "
            "a median grade of 13.00, whereas Dropouts achieve a median of 10.93 and exhibit a staggering 40.1% zero-grade frequency (reflecting "
            "failed or abandoned units). Academic performance within the university is vastly more predictive than prior schooling records."
        )
        box_elements = [
            t_boxes,
            Paragraph("Figure 10. Admission Grades (Left) vs. First-Semester Average Grades (Right) Across Academic Outcomes", styles['caption']),
            make_interp_callout(interp_box_text, styles),
            Spacer(1, 6)
        ]
        story.append(KeepTogether(box_elements))

    # Embed Fig 5 CS4: Age Band with KeepTogether
    s5_img = Path("case_study_4_results/fig5_outcome_by_age_band.png")
    story.append(build_figure_block(
        s5_img,
        "Figure 11. Academic Outcome Composition Across Enrollment Age Bands",
        "Stratifying cohorts into descriptive age bands demonstrates a clear monotonic relationship between older matriculation and dropout "
        "risk. For students aged 20 or younger, the dropout rate is 21.2% while 62.4% graduate. For students aged 36 or older, the dropout rate "
        "surges to 53.1% while graduation drops to 32.8%. Mature learners frequently juggle employment, family responsibilities, and financial "
        "constraints, creating higher structural hurdles to degree completion.",
        styles, height=135
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.4 Hypothesis Testing & Inferential Statistics", styles['h2']))
    story.append(Paragraph(
        "To rigorously determine whether first-semester academic performance differs across final student outcomes, we conducted formal "
        "inferential hypothesis testing at significance level alpha = 0.05.",
        styles['body']
    ))
    story.append(Paragraph(
        "• <b>Null Hypothesis (H0):</b> The distribution of first-semester academic performance (grades) is identical across the three student outcome categories (Dropout, Enrolled, Graduate).<br/>"
        "• <b>Alternative Hypothesis (H1):</b> The distribution of first-semester academic performance differs significantly across at least one student outcome category.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Assumption Testing & Test Selection:</b> Parametric One-Way ANOVA requires normality of group residuals and homoscedasticity. "
        "The Brown-Forsythe test yielded F = 549.87 (p = 5.47e-214), decisively rejecting equal variances. "
        "Consequently, the standard ANOVA is invalid, and the non-parametric <b>Kruskal-Wallis H-test</b> was selected.",
        styles['body']
    ))

    # Hypothesis Testing Results Table
    ht_data = [
        [Paragraph("<b>Statistical Test & Diagnostic Parameter</b>", styles['tbl_header']),
         Paragraph("<b>Observed Statistic</b>", styles['tbl_header']),
         Paragraph("<b>Degrees of Freedom</b>", styles['tbl_header']),
         Paragraph("<b>p-value</b>", styles['tbl_header']),
         Paragraph("<b>Inferential Decision & Interpretation</b>", styles['tbl_header'])],
        [Paragraph("<b>Brown-Forsythe Homoscedasticity Test</b>", styles['tbl_cell']),
         Paragraph("F = 549.87", styles['tbl_cell_center']),
         Paragraph("df = 2", styles['tbl_cell_center']),
         Paragraph("5.47e-214", styles['tbl_cell_center']),
         Paragraph("Variances are unequal (p < 0.001); mandates non-parametric testing.", styles['tbl_cell'])],
        [Paragraph("<b>Kruskal-Wallis Omnibus H-Test</b>", styles['tbl_cell']),
         Paragraph("H = 1094.19", styles['tbl_cell_center']),
         Paragraph("df = 2", styles['tbl_cell_center']),
         Paragraph("2.51e-238", styles['tbl_cell_center']),
         Paragraph("<b>Reject H0.</b> Extremely strong evidence that grade distributions differ across outcomes.", styles['tbl_cell'])],
        [Paragraph("<b>Effect Size (Epsilon-Squared / Eta-Squared)</b>", styles['tbl_cell']),
         Paragraph("ε² = 0.2470", styles['tbl_cell_center']),
         Paragraph("N = 4,424", styles['tbl_cell_center']),
         Paragraph("N/A", styles['tbl_cell_center']),
         Paragraph("<b>Large Practical Significance.</b> First-semester grades account for 24.7% of outcome variance.", styles['tbl_cell'])],
        [Paragraph("<b>Post-Hoc: Dropout vs Enrolled</b>", styles['tbl_cell']),
         Paragraph("U = 368,443.5", styles['tbl_cell_center']),
         Paragraph("Pairwise", styles['tbl_cell_center']),
         Paragraph("6.91e-43 (Holm adj)", styles['tbl_cell_center']),
         Paragraph("Statistically significant divergence; dropouts underperform enrolled students.", styles['tbl_cell'])],
        [Paragraph("<b>Post-Hoc: Dropout vs Graduate</b>", styles['tbl_cell']),
         Paragraph("U = 600,098.0", styles['tbl_cell_center']),
         Paragraph("Pairwise", styles['tbl_cell_center']),
         Paragraph("5.90e-218 (Holm adj)", styles['tbl_cell_center']),
         Paragraph("Statistically significant divergence; massive performance gap between dropouts and graduates.", styles['tbl_cell'])],
        [Paragraph("<b>Post-Hoc: Enrolled vs Graduate</b>", styles['tbl_cell']),
         Paragraph("U = 524,677.0", styles['tbl_cell_center']),
         Paragraph("Pairwise", styles['tbl_cell_center']),
         Paragraph("3.75e-63 (Holm adj)", styles['tbl_cell_center']),
         Paragraph("Statistically significant divergence; enrolled students achieve intermediate grades.", styles['tbl_cell'])],
    ]
    t_ht = Table(ht_data, colWidths=[130, 65, 45, 80, USABLE_WIDTH - 320])
    t_ht.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(KeepTogether([t_ht, Spacer(1, 6)]))

    story.append(Paragraph(
        "<b>Distinguishing Statistical Significance from Practical Importance:</b> With N = 4,424 observations, virtually any tiny "
        "difference will achieve an astronomically small p-value (p = 2.51e-238). However, statistical significance merely confirms that the "
        "observed difference is unlikely due to random sampling chance. To establish practical importance, we computed the non-parametric "
        "effect size epsilon-squared (ε² = 0.2470). By Cohen's empirical benchmarks (small = 0.01, medium = 0.06, large > 0.14), an effect size "
        "of 0.247 represents a massive, practically transformative institutional signal. Sensitivity testing on students with positive grades "
        "(excluding zero-grade non-attenders) confirmed that the effect remains highly robust (H = 822.4, p = 2.4e-179, ε² = 0.222).",
        styles['body']
    ))

    story.append(Paragraph("2.5 Machine Learning Methodology & Model Evaluation", styles['h2']))
    story.append(Paragraph(
        "<b>Leak-Free Early Prediction Boundary:</b> A fatal flaw in predictive analytics is including future information that would not "
        "be available when an intervention must be triggered. All second-semester variables (e.g., <code>Curricular units 2nd sem (approved)</code>) "
        "and post-enrollment economic indices (macroeconomic indicators) were strictly excluded. Modeling was restricted exclusively to demographic, "
        "admission, and first-semester progress data.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Stratified 80:20 Data Partitioning:</b> The dataset was partitioned into 3,539 training instances and 885 testing instances, "
        "stratifying on the outcome variable to preserve exact class proportions across splits. Features were processed inside a leak-proof "
        "scikit-learn <code>ColumnTransformer</code>: nominal predictors were one-hot encoded, and numerical predictors were standardized.",
        styles['body']
    ))

    # Model Benchmark Table
    mcomp_data = [
        [Paragraph("<b>Model Architecture</b>", styles['tbl_header']),
         Paragraph("<b>Accuracy</b>", styles['tbl_header']),
         Paragraph("<b>Macro Precision</b>", styles['tbl_header']),
         Paragraph("<b>Macro Recall</b>", styles['tbl_header']),
         Paragraph("<b>Macro F1-Score</b>", styles['tbl_header']),
         Paragraph("<b>Model Characterization & Rationale</b>", styles['tbl_header'])],
        [Paragraph("<b>Majority Class Baseline (Dummy)</b>", styles['tbl_cell']),
         Paragraph("49.94%", styles['tbl_cell_center']),
         Paragraph("16.65%", styles['tbl_cell_center']),
         Paragraph("33.33%", styles['tbl_cell_center']),
         Paragraph("0.2221", styles['tbl_cell_center']),
         Paragraph("Always predicts 'Graduate'. Fails to identify a single dropout or enrolled student.", styles['tbl_cell'])],
        [Paragraph("<b>Admission-Only Logistic Reg.</b>", styles['tbl_cell']),
         Paragraph("53.67%", styles['tbl_cell_center']),
         Paragraph("52.88%", styles['tbl_cell_center']),
         Paragraph("49.37%", styles['tbl_cell_center']),
         Paragraph("0.5009", styles['tbl_cell_center']),
         Paragraph("Uses pre-enrollment metrics only. Shows marginal predictive utility beyond baseline.", styles['tbl_cell'])],
        [Paragraph("<b>Semester-1 Multiclass Logistic Reg.</b>", styles['tbl_cell']),
         Paragraph("<b>70.73%</b>", styles['tbl_cell_center']),
         Paragraph("<b>66.62%</b>", styles['tbl_cell_center']),
         Paragraph("<b>66.87%</b>", styles['tbl_cell_center']),
         Paragraph("<b>0.6623</b>", styles['tbl_cell_center']),
         Paragraph("<b>Final Champion Model.</b> Incorporates 1st-semester progress; boosts macro F1 by 0.440 over baseline.", styles['tbl_cell'])],
    ]
    t_mcomp = Table(mcomp_data, colWidths=[120, 55, 65, 60, 55, USABLE_WIDTH - 355])
    t_mcomp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(KeepTogether([t_mcomp, Spacer(1, 6)]))

    # Detailed Classification Report Table
    report_data = [
        [Paragraph("<b>Class Label</b>", styles['tbl_header']),
         Paragraph("<b>Precision</b>", styles['tbl_header']),
         Paragraph("<b>Recall</b>", styles['tbl_header']),
         Paragraph("<b>F1-Score</b>", styles['tbl_header']),
         Paragraph("<b>Support</b>", styles['tbl_header']),
         Paragraph("<b>Class-Specific Analytical Observations</b>", styles['tbl_header'])],
        [Paragraph("<b>Dropout</b>", styles['tbl_cell']),
         Paragraph("0.7633", styles['tbl_cell_center']),
         Paragraph("0.6585", styles['tbl_cell_center']),
         Paragraph("0.7070", styles['tbl_cell_center']),
         Paragraph("284", styles['tbl_cell_center']),
         Paragraph("High precision: 76.3% of predicted dropouts truly drop out, minimizing false alarms.", styles['tbl_cell'])],
        [Paragraph("<b>Enrolled</b>", styles['tbl_cell']),
         Paragraph("0.4074", styles['tbl_cell_center']),
         Paragraph("0.5535", styles['tbl_cell_center']),
         Paragraph("0.4693", styles['tbl_cell_center']),
         Paragraph("159", styles['tbl_cell_center']),
         Paragraph("Lowest F1: Represents an ambiguous transitional state overlapping both Dropout and Graduate.", styles['tbl_cell'])],
        [Paragraph("<b>Graduate</b>", styles['tbl_cell']),
         Paragraph("0.8278", styles['tbl_cell_center']),
         Paragraph("0.7941", styles['tbl_cell_center']),
         Paragraph("0.8106", styles['tbl_cell_center']),
         Paragraph("442", styles['tbl_cell_center']),
         Paragraph("Highest performance: Over 82.7% precision and 79.4% recall on successful degree completers.", styles['tbl_cell'])],
        [Paragraph("<b>Macro Average</b>", styles['tbl_cell']),
         Paragraph("<b>0.6662</b>", styles['tbl_cell_center']),
         Paragraph("<b>0.6687</b>", styles['tbl_cell_center']),
         Paragraph("<b>0.6623</b>", styles['tbl_cell_center']),
         Paragraph("885", styles['tbl_cell_center']),
         Paragraph("Unweighted arithmetic mean treating all classes with equal priority regardless of size.", styles['tbl_cell'])],
        [Paragraph("<b>Weighted Average</b>", styles['tbl_cell']),
         Paragraph("0.7316", styles['tbl_cell_center']),
         Paragraph("0.7073", styles['tbl_cell_center']),
         Paragraph("0.7161", styles['tbl_cell_center']),
         Paragraph("885", styles['tbl_cell_center']),
         Paragraph("Class-frequency weighted performance summary across the held-out test cohort.", styles['tbl_cell'])],
    ]
    t_rep = Table(report_data, colWidths=[90, 55, 55, 55, 50, USABLE_WIDTH - 305])
    t_rep.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(KeepTogether([t_rep, Spacer(1, 6)]))

    # Embed Fig 6 CS4: Confusion Matrix with KeepTogether
    s6_img = Path("case_study_4_results/fig6_confusion_matrix.png")
    story.append(build_figure_block(
        s6_img,
        "Figure 12. Held-Out Test Set Confusion Matrix (Semester 1 Model, N=885)",
        "The confusion matrix illustrates clear diagonal dominance: 187 of 284 dropouts (65.8%) and 351 of 442 graduates (79.4%) "
        "are classified accurately. Most crucially from an institutional risk perspective, extreme catastrophic errors—misclassifying "
        "an actual Dropout as a Graduate—are exceedingly rare (only 25 out of 284, or 8.8%). Misclassifications primarily cluster "
        "between adjacent states: Dropouts predicted as Enrolled (72 students) and Enrolled students predicted as Graduates (51 students). "
        "This confirms that the model accurately separates the ends of the performance spectrum while recognizing transitional ambiguity.",
        styles, width=270, height=180
    ))

    # Bootstrap Uncertainty Analysis
    story.append(Paragraph("<b>Bootstrap Score Uncertainty Estimation (1,000 Iterations):</b>", styles['h3']))
    story.append(Paragraph(
        "To establish rigorous confidence bounds on model performance and avoid over-interpreting point estimates on a single test partition, "
        "we conducted 1,000 bootstrap resamples of the test predictions. The resulting 95% empirical confidence intervals are:<br/>"
        "• <b>Test Accuracy:</b> Mean = 70.67%, 95% CI [67.57%, 73.56%]<br/>"
        "• <b>Macro F1-Score:</b> Mean = 0.6611, 95% CI [0.6259, 0.6933]<br/>"
        "These narrow confidence bands demonstrate that the model's predictive superiority over baseline classifiers is statistically robust.",
        styles['body']
    ))

    story.append(Paragraph("2.6 Model Interpretability & Feature Significance", styles['h2']))
    story.append(Paragraph(
        "To unpack the decision mechanism of the multiclass logistic regression model, we examined the fitted coefficients comparing "
        "the log-odds of Dropout relative to Graduation. Odds multipliers less than 1.0 indicate protective factors (favoring graduation), "
        "while multipliers greater than 1.0 indicate risk factors (elevating dropout probability).",
        styles['body']
    ))

    # Top Features Table
    feat_data = [
        [Paragraph("<b>Predictor Feature Name</b>", styles['tbl_header']),
         Paragraph("<b>Feature Category</b>", styles['tbl_header']),
         Paragraph("<b>Log-Odds Diff (Drop - Grad)</b>", styles['tbl_header']),
         Paragraph("<b>Odds Multiplier</b>", styles['tbl_header']),
         Paragraph("<b>Empirical Impact & Practical Interpretation</b>", styles['tbl_header'])],
        [Paragraph("<code>1st sem (approved units)</code>", styles['tbl_cell']),
         Paragraph("Academic Progress", styles['tbl_cell']),
         Paragraph("-3.205", styles['tbl_cell_center']),
         Paragraph("<b>0.041x</b>", styles['tbl_cell_center']),
         Paragraph("<b>Massive Protective Anchor.</b> Each +1 SD increase in approved units cuts dropout odds by 95.9%.", styles['tbl_cell'])],
        [Paragraph("<code>1st sem (average grade)</code>", styles['tbl_cell']),
         Paragraph("Academic Performance", styles['tbl_cell']),
         Paragraph("-0.565", styles['tbl_cell_center']),
         Paragraph("<b>0.568x</b>", styles['tbl_cell_center']),
         Paragraph("Higher course marks significantly boost degree completion probability.", styles['tbl_cell'])],
        [Paragraph("<code>1st sem (enrolled units)</code>", styles['tbl_cell']),
         Paragraph("Curricular Load", styles['tbl_cell']),
         Paragraph("+1.333", styles['tbl_cell_center']),
         Paragraph("<b>3.791x</b>", styles['tbl_cell_center']),
         Paragraph("<b>Primary Risk Factor.</b> Enrolling in high unit loads without corresponding approvals multiplies dropout odds by 3.8x.", styles['tbl_cell'])],
        [Paragraph("<code>Course (Degree Program)</code>", styles['tbl_cell']),
         Paragraph("Academic Department", styles['tbl_cell']),
         Paragraph("+1.216", styles['tbl_cell_center']),
         Paragraph("<b>3.375x</b>", styles['tbl_cell_center']),
         Paragraph("Substantial curriculum-specific attrition variation (e.g., higher attrition in intensive technical degrees).", styles['tbl_cell'])],
        [Paragraph("<code>Age at enrollment</code>", styles['tbl_cell']),
         Paragraph("Demographic", styles['tbl_cell']),
         Paragraph("+0.342", styles['tbl_cell_center']),
         Paragraph("<b>1.408x</b>", styles['tbl_cell_center']),
         Paragraph("Older matriculation moderately elevates attrition odds (+40.8% per SD) due to competing life responsibilities.", styles['tbl_cell'])],
    ]
    t_feat = Table(feat_data, colWidths=[120, 80, 80, 60, USABLE_WIDTH - 340])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2A4A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ]))
    story.append(KeepTogether([t_feat, Spacer(1, 6)]))

    story.append(Paragraph("2.7 Practical Interventions, Institutional Action Plan & Responsible AI", styles['h2']))
    story.append(Paragraph(
        "<b>Actionable Institutional Interventions:</b><br/>"
        "1. <i>Semester 1 Midterm Early-Warning Gateway:</i> The single most decisive predictor of attrition is failing to approve enrolled "
        "units in Semester 1 (odds multiplier 0.041 for approvals vs 3.791 for enrollments). The university should institute an automated "
        "mid-semester flag when students fail initial formative assessments. Dedicated peer tutoring and academic recovery bootcamps should be triggered.<br/>"
        "2. <i>Credit Load Realignment & Workload Counseling:</i> Students matriculating with lower previous grades who enroll in excessive credit "
        "loads face severe attrition risks. Academic advisors should implement credit caps and recommend modular or part-time pathways.<br/>"
        "3. <i>Tailored Support for Non-Traditional and Mature Students:</i> Students entering above age 25 experience a 1.41x higher dropout risk. "
        "The institution should establish flexible evening/online course offerings, childcare subsidies, and specialized adult onboarding workshops.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Responsible AI & Ethical Deployment Principles:</b><br/>"
        "• <i>No Punitive Usage:</i> Model predictions must strictly serve as an allocation mechanism for supportive resources (tutoring, advising, "
        "emergency grants), never as justification for academic dismissal, financial aid denial, or enrollment restrictions.<br/>"
        "• <i>Mitigating Algorithmic Stigmatization:</i> Students must never be labeled or informed that an algorithm has classified them as "
        "'at risk of dropping out'. Advising outreach should be framed positively around academic enrichment and milestone support.<br/>"
        "• <i>Association vs. Causation:</i> Coefficients reflect statistical associations within observational historical records, not causal laws. "
        "Demographic variables like age or parental background must never be used to make deterministic judgments about an individual's potential.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Critical Model Limitations:</b><br/>"
        "1. <i>Unobserved Psychological & Financial Variables:</i> Key drivers of student persistence (mental health, social belonging, unexpected "
        "family financial crises, employment hours) are unmeasured in this administrative dataset.<br/>"
        "2. <i>Ambiguity of the 'Enrolled' State:</i> The enrolled class exhibits the lowest F1-score (0.469) because it represents students still "
        "in progress who may eventually graduate or drop out; longitudinal survival analysis would model duration more effectively.<br/>"
        "3. <i>Single-Institution Context:</i> The dataset originates from a single European higher education institution; cross-institutional "
        "transferability requires re-calibration on local student demographics.",
        styles['body']
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("3.0 Methodological Synthesis & Conclusion", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F2A4A'), spaceAfter=8))
    story.append(Paragraph(
        "Across both case studies, empirical data science techniques provided actionable clarity where unstructured intuition falls short. "
        "In Case Study 1, unsupervised PCA and K-Means segmentation successfully decomposed 7,501 retail transactions into five distinct shopping "
        "archetypes, providing concrete floor layout and cross-selling recommendations. In Case Study 4, inferential hypothesis testing and leak-free "
        "supervised classification established that early first-semester academic momentum is the decisive determinant of student graduation, "
        "delivering an operational blueprint for early institutional intervention.",
        styles['body']
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.0 References & Attribution", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F2A4A'), spaceAfter=8))
    story.append(Paragraph(
        "1. Real, V., Mota, M., & Martins, P. (2021). <i>Predicting Student Dropout and Academic Success</i>. UCI Machine Learning Repository.<br/>"
        "2. Pedregosa, F. et al. (2011). <i>Scikit-learn: Machine Learning in Python</i>. Journal of Machine Learning Research, 12, 2825-2830.<br/>"
        "3. Kruskal, W. H., & Wallis, W. A. (1952). <i>Use of Ranks in One-Criterion Variance Analysis</i>. Journal of the American Statistical Association, 47(260), 583-621.<br/>"
        "4. Rousseeuw, P. J. (1987). <i>Silhouettes: A graphical aid to the interpretation and validation of cluster analysis</i>. Journal of Computational and Applied Mathematics, 20, 53-65.<br/>"
        "5. Davies, D. L., & Bouldin, D. W. (1979). <i>A Cluster Separation Measure</i>. IEEE Transactions on Pattern Analysis and Machine Intelligence, PAMI-1(2), 224-227.",
        styles['body']
    ))

    # Build document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"\n[SUCCESS] Final academic PDF report successfully generated at: {pdf_path.resolve()}")
    return pdf_path


if __name__ == '__main__':
    build_pdf_report()
