from datetime import date, datetime

import tkinter as tk
from tkinter import messagebox


def validate_search_fields(fields: dict[str, tk.Entry]) -> bool:
	"""Return whether all named search entries contain complete, valid input."""
	for name, entry in fields.items():
		value = entry.get().strip()
		if not value:
			messagebox.showerror("Incomplete search", f"Enter a value for {name}.")
			entry.focus_set()
			return False
		if "date" in name.casefold():
			try:
				search_date = datetime.strptime(value, "%Y-%m-%d").date()
			except ValueError:
				messagebox.showerror("Invalid date", f"Enter a valid {name} in YYYY-MM-DD format.")
				entry.focus_set()
				return False
			if search_date < date.today():
				messagebox.showerror("Invalid date", f"The {name} cannot be in the past.")
				entry.focus_set()
				return False
		if any(ord(char) < 32 for char in value):
			messagebox.showerror("Invalid search", f"The {name} field contains invalid characters.")
			entry.focus_set()
			return False
	return True
