#Data Discrepancy Analysis

#Project Overview

This project analyzes discrepancies in backend datasets related to a recurring allowance scheduling system. These discrepancies were caused by backend issues, resulting in inconsistencies in the next_payment_day and payment_date fields. The objective is to align the backend data with the event logs (allowance_events), which are considered the source of truth.

#What the Code Does
The script data_discrepancy_analysis.py performs the following tasks:

Load Data:

Reads the provided datasets: allowance_events.json, allowance_backend_table.csv, and payment_schedule_backend_table.csv.
Data Processing:

Cleans and preprocesses the allowance_events dataset to extract user details, allowance frequency, and payment days.
Discrepancy Analysis:

Calculates the expected next_payment_day based on the event logs.
Compares the calculated values with the backend records (allowance_backend_table) to identify discrepancies.
Classification of Discrepancies:

Categorizes discrepancies into:
Missing Calculation: When the calculated next_payment_day cannot be determined.
Mismatched Values: When backend next_payment_day does not align with the calculated value.
Other: Discrepancies that do not fit into the above categories.
Export Results:

Outputs two CSV files:
comparison_results.csv: Detailed comparison of backend data and calculated values.
discrepancy_summary.csv: Summary of discrepancies by type and count.


#Files Included
- allowance_backend_table.csv: Backend records of allowances.
- allowance_events.json: Event logs, considered the source of truth.
- payment_schedule_backend_table.csv: Backend payment schedules.
- data_discrepancy_analysis.py: Python script that performs the analysis.
- comparison_results.csv: Detailed results of the comparison between backend and calculated values.
- discrepancy_summary.csv: Summary of discrepancy types and counts.
- README.md: Documentation of the project.

#How to Run the Code
Prerequisites
Python 3.7 or higher installed.
Required libraries: pandas, numpy.


Clone this repository:
git clone https://github.com/your-username/data-discrepancy-analysis.git
cd data-discrepancy-analysis

(Optional) Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\\Scripts\\activate   # For Windows

pip install pandas numpy
python data_discrepancy_analysis.py


#How to Analyze the Results
comparison_results.csv:

Contains detailed comparisons between backend next_payment_day and calculated values.
Each row represents a record with metadata and whether discrepancies exist.
discrepancy_summary.csv:

Provides a summary of discrepancies by type and count.
Useful for understanding the overall scope of issues.


