import customtkinter
from src.browser_chromium import browser_chromium

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

window = customtkinter.CTk()
window.geometry("500x300")

def scraped_google_maps():
    search_name = search_in_google_maps.get()
    total = total_leads.get()
    to_csv = checkbox_to_csv.get()
    to_excel = checkbox_to_excel.get()

    if search_name != None and total != None:
        browser_chromium(
            search_google_maps=str(search_name),
            total_data=int(total),
            is_excel=to_excel,
            is_csv=to_csv
        )


_title: str = 'Extractor Leads'
_search: str = 'Search in google maps the business with location'
_total: str = 'Total Leads'
_to_excel: str = 'Download to Excel'
_to_csv: str = 'Download to CSV'

window.title(_title)

search_in_google_maps = customtkinter.CTkEntry(window, placeholder_text=_search, width=300)
search_in_google_maps.pack(padx=10, pady=10)

total_leads = customtkinter.CTkEntry(window, placeholder_text=_total, width=300)
total_leads.pack(padx=10, pady=10)

checkbox_to_excel = customtkinter.CTkCheckBox(window, text=_to_excel)
checkbox_to_excel.pack(padx=10, pady=10)

checkbox_to_csv = customtkinter.CTkCheckBox(window, text=_to_csv)
checkbox_to_csv.pack(padx=10, pady=10)

button_search = customtkinter.CTkButton(window, text="Search", command=scraped_google_maps, width=120)
button_search.pack(padx=10, pady=10)

window.mainloop()
