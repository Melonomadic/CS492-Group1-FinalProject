import re
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


FLIGHT_NUMBER_PATTERN = re.compile(r"[A-Z0-9]{2}\s*\d{1,4}[A-Z]?", re.IGNORECASE)
AIRPORT_CODE_PATTERN = re.compile(r"[A-Z]{3}", re.IGNORECASE)


class FlightSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Search")
        self.root.resizable(False, False)

        container = ttk.Frame(root, padding=20)
        container.grid()

        ttk.Label(container, text="Find a flight", font=("", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 14)
        )

        self.flight_number = tk.StringVar()
        self.departing_airport = tk.StringVar()
        self.destination_airport = tk.StringVar()
        self.flight_date = tk.StringVar()

        fields = (
            ("Flight number (e.g., UA123)", self.flight_number),
            ("Departing airport (3-letter code)", self.departing_airport),
            ("Destination airport (3-letter code)", self.destination_airport),
            ("Date of flight (YYYY-MM-DD)", self.flight_date),
        )
        for row, (label, variable) in enumerate(fields, start=1):
            ttk.Label(container, text=label).grid(
                row=row, column=0, sticky="w", padx=(0, 12), pady=5
            )
            ttk.Entry(container, textvariable=variable, width=32).grid(
                row=row, column=1, sticky="ew", pady=5
            )

        ttk.Button(container, text="Search flights", command=self.search).grid(
            row=len(fields) + 1, column=0, columnspan=2, sticky="ew", pady=(14, 0)
        )

    def search(self):
        flight_number = self.flight_number.get().strip().upper()
        departing_airport = self.departing_airport.get().strip().upper()
        destination_airport = self.destination_airport.get().strip().upper()
        date_text = self.flight_date.get().strip()

        missing = [
            label
            for label, value in (
                ("Flight number", flight_number),
                ("Departing airport", departing_airport),
                ("Destination airport", destination_airport),
                ("Date of flight", date_text),
            )
            if not value
        ]
        if missing:
            messagebox.showerror(
                "Incomplete search",
                "Complete all fields. Missing: " + ", ".join(missing) + ".",
            )
            return

        if not FLIGHT_NUMBER_PATTERN.fullmatch(flight_number):
            messagebox.showerror(
                "Invalid flight number",
                "Enter a 2-character airline code followed by 1-4 digits "
                "(for example, UA123).",
            )
            return

        for label, airport in (
            ("Departing airport", departing_airport),
            ("Destination airport", destination_airport),
        ):
            if not AIRPORT_CODE_PATTERN.fullmatch(airport):
                messagebox.showerror(
                    "Invalid airport",
                    f"{label} must be 3 letters (for example, DEN).",
                )
                return

        if departing_airport == destination_airport:
            messagebox.showerror(
                "Invalid route", "Departing and destination airports must be different."
            )
            return

        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d")
            if parsed_date.strftime("%Y-%m-%d") != date_text:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid date", "Enter a real date as YYYY-MM-DD (for example, 2026-12-31)."
            )
            return

        criteria = (
            f"Flight number: {flight_number}",
            f"Departing airport: {departing_airport}",
            f"Destination airport: {destination_airport}",
            f"Date of flight: {date_text}",
        )
        messagebox.showinfo(
            "Flight search",
            "Search criteria:\n" + "\n".join(criteria)
            + "\n\nConnect a flight data source to display matching flights.",
        )


def main():
    root = tk.Tk()
    FlightSearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
