"""
File Manager
Entry point for the application.

Author: <Author Name>
Version: 1.0.0
"""

import sys
from gui import FileManagerApp


def main():
    """Launch the File Manager application."""
    try:
        app = FileManagerApp()
        app.run()

    except KeyboardInterrupt:
        print("\nApplication closed by user.")
        sys.exit(0)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
