"""
Project Organizer - Dark Theme Main Entry Point

This is the main entry point for the Project Organizer application with
dark theme enhancements applied.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from project_organizer import ProjectOrganizer
from dark_theme_integration import enhance_project_organizer

def main():
    """Main entry point for the application"""
    # Create QApplication instance
    app = QApplication(sys.argv)
    
    # Set application icon for all windows
    app_icon = QIcon("logopo.png")
    app.setWindowIcon(app_icon)
    
    # Set fusion style for better dark theme support
    app.setStyle("Fusion")
    
    # Create the main application window
    window = ProjectOrganizer()
    
    # Apply all dark theme enhancements
    enhance_project_organizer(window)
    
    # Show the window
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()