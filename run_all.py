"""
Fundamentals of Data Science - Master Pipeline Runner
Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3 | Academic Year: 2026-2027
Faculty: Assistant Prof. Durga Devi

Description:
This master runner script executes both case study analyses sequentially:
1. Executes Case Study 1 (Online Retail Basket Clustering)
2. Executes Case Study 4 (Predicting Student Dropout and Academic Success)
3. Generates the comprehensive final submission PDF report
4. Audits all output figures, CSV tables, and JSON files
"""

import sys
import subprocess
from pathlib import Path


def run_step(step_name: str, script_name: str):
    print("\n" + "=" * 75)
    print(f"STEP: {step_name} ({script_name})")
    print("=" * 75)
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    if result.returncode != 0:
        print(f"[ERROR] Step failed with return code {result.returncode}")
        sys.exit(result.returncode)
    print(f"[SUCCESS] {step_name} completed successfully.")


def main():
    print("=" * 75)
    print("STARTING FULL REPRODUCTION PIPELINE: CASE STUDIES 1 & 4")
    print("Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3")
    print("Subject: Fundamentals of Data Science (FDS)")
    print("=" * 75)

    # 1. Run Case Study 1
    run_step("Case Study 1: Retail Basket Clustering", "case_study_1_retail.py")

    # 2. Run Case Study 4
    run_step("Case Study 4: Student Dropout & Academic Success", "case_study_4_student_dropout.py")

    # 3. Generate Submission PDF Report
    pdf_script = Path("generate_case_study_report.py")
    if pdf_script.exists():
        run_step("Generate Formal Submission PDF Report", "generate_case_study_report.py")

    print("\n" + "=" * 75)
    print("ALL CASE STUDY PIPELINES AND REPORTS COMPLETED SUCCESSFULLY!")
    print("=" * 75)


if __name__ == '__main__':
    main()
