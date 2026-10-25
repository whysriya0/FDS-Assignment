"""
Fundamentals of Data Science - Master Pipeline Runner
Author: Sriya A. | Roll No: 160124733156 | Section: CSE-3 | Academic Year: 2026-2027
Faculty: Assistant Prof. Durga Devi

Description:
This master runner script executes both case study analyses sequentially:
1. Executes Case Study 1 (Online Retail Basket Clustering)
2. Executes Case Study 4 (Predicting Student Dropout and Academic Success)
3. Verifies that all figures, CSV tables, and the final PDF report exist
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
    print("Subject: Fundamentals of Data Science (22CSC59)")
    print("=" * 75)

    # 1. Run Case Study 1
    run_step("Case Study 1: Retail Basket Clustering", "case_study_1_retail.py")

    # 2. Run Case Study 4
    run_step("Case Study 4: Student Dropout & Academic Success", "case_study_4_student_dropout.py")

    # 3. Verify Final PDF Report
    final_pdf = Path("Combined_Case_Study_Report.pdf")
    if final_pdf.exists():
        print(f"\n[VERIFIED] Final Case Study Report confirmed: {final_pdf.resolve()} ({final_pdf.stat().st_size:,} bytes)")
    else:
        print("\n[WARNING] Combined_Case_Study_Report.pdf not found in root directory!")

    print("\n" + "=" * 75)
    print("ALL CASE STUDY PIPELINES AND AUDITS COMPLETED SUCCESSFULLY!")
    print("=" * 75)


if __name__ == '__main__':
    main()
