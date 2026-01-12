"""
Primary operating programme
"""
from GUI.main_window import StorageTracker
from Core import add_item_sql

class Main:
    """
    The main class programme loop is initialised here.
    """
    def __init__(self):
        """
        Primary service logic
        Args:
            StorageTracer (str, optional): For structuring the main page programme
            setup_database(): Used to initialise the SQLite database;
                if the SQL database already exists in the file, no new creation is required.

        Return：
            None No return
        """
        # Correct instantiation StorageTracker
        self.app = StorageTracker()

        # Generate SQLite
        add_item_sql.setup_database()

    def Main_run(self):
        """
        The main operating programme runs here.
        Args:
            run(): Call the instance's run method

        Return：
            None No return
        """
        self.app.run()



# Create and run the application
if __name__ == "__main__":
    app = Main()
    app.Main_run()