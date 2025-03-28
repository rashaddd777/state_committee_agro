All data in this repository is derived from The State Statistical Committee of the Republic of Azerbaijan.

Overview
This project focuses on analyzing agricultural data for multiple crops (including onions, potatoes, tomatoes, and cucumbers). It contains:

Data Files: Cleaned CSV files from official statistics and additional feature files (*_features.csv) that include derived metrics such as:

first5_sum, last5_sum

growth

std_dev

cagr (compound annual growth rate)

Notebooks: Jupyter notebooks for yield, sown area, and production EDA, as well as advanced analyses (clustering, regression, risk vs. reward plots, etc.).

Feature Generation: Python scripts that melt wide-format CSV data into long format and compute the derived metrics listed above.

Data Sources
The State Statistical Committee of the Republic of Azerbaijan
All CSV data originates from this source, covering sown area, yield, and production metrics for various crops across different regions and years.

Notebooks
EDA: Yield – Explores trends, distributions, correlations, and advanced analytics for yield data.

EDA: Sown Area – Analyzes how much land is allocated for each crop, plus derived insights like growth and volatility.

EDA: Production – Examines production quantities, identifying top regions, and applying clustering or regression models for deeper insights.

Contact
For questions or contributions, please open an issue or contact the rkerimov17619@ada.edu.az. Ensure compliance with any usage restrictions from stat.gov.az when using this data.
