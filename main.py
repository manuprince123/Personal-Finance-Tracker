import sys
import os

# Ensure the project root is always on the path, regardless of how the script is invoked
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from src.gui.app import FinanceTrackerApp
    app = FinanceTrackerApp()
    app.mainloop()
