# Importiert den Playwright-Typ der Browserseite für die Typangabe im Konstruktor.
from playwright.sync_api import Page


# Bündelt Aktionen rund um die TodoMVC-Seite in einem Page-Object.
class TodoPage:
    # Übernimmt die vom Test bereitgestellte Browserseite.
    def __init__(self, page: Page):
        # Speichert die Seite, damit die Methoden damit interagieren können.
        self.page = page
        # Merkt sich das Eingabefeld anhand seiner stabilen Test-ID.
        self.input_field = page.get_by_test_id("text-input")

    # Öffnet die TodoMVC-Demo im Browser.
    def goto(self):
        self.page.goto("https://todomvc.com/examples/react/dist/")

    # Fügt ein neues Todo mit dem angegebenen Text hinzu.
    def input_todo(self, todo_text: str):
        # Trägt den Todo-Text in das Eingabefeld ein.
        self.input_field.fill(todo_text)
        # Bestätigt die Eingabe mit Enter.
        self.input_field.press("Enter")

    # Schaltet das Todo mit dem angegebenen Text zwischen offen und erledigt um.
    def todo_item_toggle(self, todo_text: str):
        # Sucht das Listenelement mit passendem Text und klickt dessen Statusfeld.
        self.page.get_by_role("listitem").filter(
            has_text=todo_text
        ).get_by_test_id("todo-item-toggle").click()

    # Zeigt nur noch nicht erledigte Todos an.
    def active_link(self):
        self.page.get_by_role("link", name="Active").click()

    # Zeigt nur erledigte Todos an.
    def completed_link(self):
        self.page.get_by_role("link", name="Completed").click()

    # Entfernt alle erledigten Todos aus der Liste.
    def clear_completed(self):
        self.page.get_by_role("button", name="Clear completed").click()