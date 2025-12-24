from database import FinanceDAO
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, DataTable, Static, Input, Label
from textual.containers import Container, Vertical
from textual.screen import ModalScreen

class AddTickerModal(ModalScreen):
    CSS = """
    AddTickerModal {
        align: center middle;
    }
    #dialog {
        padding: 0 1;
        width: 60;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Enter Stock Ticker:", classes="question")
            yield Input(placeholder="e.g. NVDA")
            yield Label("Press Enter to add. Esc to cancel.", classes="help")

    def on_input_submitted(self, message: Input.Submitted) -> None:
        if message.value:
            dao = FinanceDAO()
            dao.add_watched_ticker(message.value)
            self.app.notify(f"Added {message.value} to watchlist")
        self.dismiss()

class RemoveTickerModal(ModalScreen):
    CSS = """
    AddTickerModal {
        align: center middle;
    }
    #dialog {
        padding: 0 1;
        width: 60;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Enter Stock Ticker to Remove:", classes="question")
            yield Input(placeholder="e.g. NVDA")
            yield Label("Press Enter to remove. Esc to cancel.", classes="help")

    def on_input_submitted(self, message: Input.Submitted) -> None:
        if message.value:
            dao = FinanceDAO()
            dao.remove_watched_ticker(message.value)
            self.app.notify(f"Removed {message.value} from watchlist")
        self.dismiss()

class FinanceTUI(App):
    CSS = """
    DataTable { height: 1fr; border: round $primary; }
    #stats-panel { height: 3; background: $accent; color: white; text-align: center; }
    """

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
        Binding(key="a", action="add_ticker", description="Add Ticker"),
        Binding(key="r", action="remove_ticker", description="Remove Ticker")
    ]

    def action_add_ticker(self) -> None:
        self.push_screen(AddTickerModal())

    def action_remove_ticker(self) -> None:
        self.push_screen(RemoveTickerModal())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Live Market Monitor (SQL Powered)", id="stats-panel")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        # Set up the table columns
        table = self.query_one(DataTable)
        table.add_columns("Ticker", "Price", "5m Avg", "Change")
        
        # Update the data every 5 seconds
        self.set_interval(5, self.update_dashboard)

    def update_dashboard(self) -> None:
        # 1. Fetch from SQL via our DAO
        dao = FinanceDAO()
        df = dao.get_latest_metrics()
        
        # 2. Clear and Update the Table
        table = self.query_one(DataTable)
        table.clear()
        for _, row in df.iterrows():
            table.add_row(
                row['ticker'], 
                f"${row['price']:.2f}", 
                f"${row['mavg_5min']:.2f}",
                row['price_change']
            )

if __name__ == "__main__":
    app = FinanceTUI()
    app.run()
