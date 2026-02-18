import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def load_and_map(file_path, is_everest=True):
    """Loads file, extracts specific columns, and renames them."""
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.csv':
            # dtype=str preserves leading zeros like 05301
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
        else:
            # keep_default_na=False prevents empty cells from breaking
            df = pd.read_excel(file_path, dtype=str, keep_default_na=False)
    except Exception as e:
        raise ValueError(f"Could not read file: {e}")

    # Column Mapping Logic
    if is_everest:
        cols = {'Code': 'part_number', 'Sell Price': 'price'}
    else:
        cols = {'Sku': 'part_number', 'Price': 'price'}

    # Verify columns exist
    for original_col in cols.keys():
        if original_col not in df.columns:
            raise ValueError(f"Missing column: '{original_col}' in {os.path.basename(file_path)}")

    # Filter to only necessary columns and rename
    df = df[list(cols.keys())].rename(columns=cols)
    
    # Clean Price: Remove $, commas, and convert to numbers
    df['price'] = pd.to_numeric(df['price'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    # Clean Part Numbers: Uppercase and strip spaces (STAYS AS STRING)
    df['part_number'] = df['part_number'].astype(str).str.strip().str.upper()
    
    return df

def run_comparison():
    file_web = entry_web.get()
    file_ev = entry_ev.get()

    if not file_web or not file_ev:
        messagebox.showerror("Error", "Please select both files first.")
        return

    try:
        # 1. Load and Format
        df_web = load_and_map(file_web, is_everest=False)
        df_ev = load_and_map(file_ev, is_everest=True)

        # 2. Merge (Inner join as per your original)
        merged_df = pd.merge(df_web, df_ev, on='part_number', suffixes=('_website', '_everest'))

        # 3. Identify price mismatches
        mismatches = merged_df[
            (merged_df['price_website'] != merged_df['price_everest']) &
            (merged_df['price_website'] > 0) &
            (merged_df['price_everest'] > 0)
        ]

        # 4. Save File Dialog
        if not mismatches.empty:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                initialfile="price_mismatches.txt",
                title="Save Mismatch Report"
            )
            
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(f"PRICE MISMATCH REPORT (Website vs Everest)\n" + "="*45 + "\n\n")
                    for _, row in mismatches.iterrows():
                        f.write(f"Part Number: {row['part_number']}\n")
                        f.write(f"  Website Price: ${row['price_website']:,.2f}\n")
                        f.write(f"  Everest Price: ${row['price_everest']:,.2f}\n")
                        f.write("-" * 45 + "\n")
                messagebox.showinfo("Success", f"Found {len(mismatches)} mismatches.\nReport saved to: {save_path}")
        else:
            messagebox.showinfo("No Mismatches", "All prices match perfectly!")

    except Exception as e:
        messagebox.showerror("Processing Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("Price Auditor Pro")
root.geometry("500x400") # Slightly taller to ensure buttons show

def browse(entry_field):
    fn = filedialog.askopenfilename(filetypes=[("All Data Files", "*.xlsx *.xls *.csv")])
    if fn:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, fn)

# UI Elements (Added 'expand=True' to ensure they don't vanish)
tk.Label(root, text="Website Spreadsheet", font=('Arial', 10, 'bold')).pack(pady=(20,0))
tk.Label(root, text="(Needs 'Sku' and 'Price' columns)", font=('Arial', 8, 'italic')).pack()
entry_web = tk.Entry(root, width=50)
entry_web.pack(pady=5)
tk.Button(root, text="Browse Website File", command=lambda: browse(entry_web)).pack(pady=5)

tk.Label(root, text="Everest Spreadsheet", font=('Arial', 10, 'bold')).pack(pady=(20,0))
tk.Label(root, text="(Needs 'Code' and 'Sell Price' columns)", font=('Arial', 8, 'italic')).pack()
entry_ev = tk.Entry(root, width=50)
entry_ev.pack(pady=5)
tk.Button(root, text="Browse Everest File", command=lambda: browse(entry_ev)).pack(pady=5)

tk.Button(root, text="RUN COMPARISON", command=run_comparison, 
          bg="#2ecc71", fg="white", font=('Arial', 12, 'bold'), height=2).pack(pady=25, fill='x', padx=50)

root.mainloop()
