# Importiert den Playwright-Seitentyp sowie Hilfsfunktionen für verständliche Assertions.
from playwright.sync_api import Page, expect
# Importiert das Page-Object mit den Aktionen für TodoMVC.
from pages.todos_page import TodoPage


# Prüft das Hinzufügen, Filtern und Löschen von Todos.
def test_todo(page: Page) -> None:
    # Erstellt das Page-Object für die vom Fixture bereitgestellte Browserseite.
    todos = TodoPage(page)
    # Öffnet die TodoMVC-Anwendung.
    todos.goto()
    # Legt drei Todos an.
    todos.input_todo("groceries")
    todos.input_todo("sport")
    todos.input_todo("drinks")

    # Markiert zwei Todos als erledigt.
    todos.todo_item_toggle("groceries")
    todos.todo_item_toggle("drinks")

    # Wechselt zur Ansicht der noch aktiven Todos.
    todos.active_link()
    # Das nicht erledigte Todo muss sichtbar sein.
    expect(page.get_by_role("listitem").filter(has_text="sport")).to_be_visible()
    # Erledigte Todos dürfen in der aktiven Ansicht nicht erscheinen.
    expect(page.get_by_role("listitem").filter(has_text="groceries")).to_have_count(0)

    # Wechselt zur Ansicht der erledigten Todos.
    todos.completed_link()
    # Beide als erledigt markierten Todos müssen sichtbar sein.
    expect(page.get_by_role("listitem").filter(has_text="groceries")).to_be_visible()
    expect(page.get_by_role("listitem").filter(has_text="drinks")).to_be_visible()
    # Das aktive Todo darf in der erledigten Ansicht nicht erscheinen.
    expect(page.get_by_role("listitem").filter(has_text="sport")).to_have_count(0)

    # Löscht die erledigten Todos.
    todos.clear_completed()
    # Wechselt zurück zu den aktiven Todos, da das verbleibende Todo nicht erledigt ist.
    todos.active_link()
    # Danach soll genau ein Todo übrig sein.
    expect(page.locator(".todo-list").get_by_role("listitem")).to_have_count(1)
    # Das übrig gebliebene Todo muss das aktive Todo sein.
    expect(page.get_by_role("listitem").filter(has_text="sport")).to_be_visible()
