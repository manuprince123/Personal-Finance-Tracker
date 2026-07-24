import csv
import os

def export_to_csv(transactions, filename="report.csv"):
    """
    Exports a list of transaction dictionaries to a CSV file.
    """
    try:
        # Determine paths
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        export_path = os.path.join(base_dir, filename)

        with open(export_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write Header
            writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])

            # Write Data
            for t in transactions:
                writer.writerow([t['date'], t['type'], t['category'], t['amount'], t['description']])
        return True, f"Successfully exported to {export_path}"
    except Exception as e:
        return False, f"Failed to export: {str(e)}"
