# Price Auditor Pro 🚀

A lightweight Python-based GUI utility to audit and compare product pricing between website exports and Everest ERP spreadsheets.

## 🛠 Features
* **Automatic Mapping:** Designed to handle "Sku/Price" (Website) and "Code/Sell Price" (Everest) formats.
* **Data Cleaning:** Automatically handles currency symbols (`$`), commas, and preserves leading zeros in part numbers.
* **Smart Filtering:** Flags items existing in both systems with a price discrepancy (ignores $0.00 entries).
* **Precision Check:** Includes a $0.01 tolerance to avoid false positives from rounding.
* **Instant Reports:** Generates a clean `.txt` mismatch report for quick auditing.

---

## 📋 Prerequisites

You will need Python 3.x installed. The application relies on `pandas` and `openpyxl` (for Excel support).

```bash
pip install pandas openpyxl
