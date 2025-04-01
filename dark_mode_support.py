from PyQt5.QtWidgets import (QAction, QMenuBar, QMenu, QApplication, 
                             QHBoxLayout, QPushButton, QDialog, QVBoxLayout,
                             QLabel, QDialogButtonBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont


class DarkThemeManager:
    """Applies a dark theme to the Project Organizer application"""
    
    def __init__(self, main_app):
        """Initialize the dark theme manager
        
        Args:
            main_app: The main application instance (ProjectOrganizer)
        """
        self.main_app = main_app
        
        # Define the dark theme colors
        self.colors = {
            'primary': "#3f6fd1",           # Rich blue
            'primary_dark': "#2d50a7",      # Darker blue
            'accent': "#ff9800",            # Orange
            'background': "#1e1e1e",        # Dark gray background
            'card': "#2d2d2d",              # Slightly lighter card background
            'text': "#e0e0e0",              # Light gray text
            'text_secondary': "#a0a0a0",    # Lighter secondary text
            'border': "#3d3d3d",            # Subtle border color
            'success': "#66bb6a",           # Green
            'warning': "#ffca28",           # Yellow
            'error': "#ef5350",             # Red
            'high_priority': "#f44336",     # Bright red for high priority
            'medium_priority': "#ffa726",   # Orange for medium priority
            'low_priority': "#66bb6a"       # Green for low priority
        }
        
        # Apply the dark theme immediately
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the dark theme to the application"""
        # Update main app colors
        self.main_app.colors = self.colors
        
        # Update the application style
        self.update_application_style()
    
    def update_application_style(self):
        """Update the application style for dark theme"""
        # Call the main app's setup_style method
        self.main_app.setup_style()
        
        # Update the application palette
        self.update_application_palette()
        
        # Force update of all widgets
        self.main_app.style().unpolish(self.main_app)
        self.main_app.style().polish(self.main_app)
        self.main_app.update()
    
    def update_application_palette(self):
        """Update the application palette for dark theme"""
        colors = self.main_app.colors
        palette = QPalette()
        
        # Set standard colors
        palette.setColor(QPalette.Window, QColor(colors['background']))
        palette.setColor(QPalette.WindowText, QColor(colors['text']))
        palette.setColor(QPalette.Base, QColor(colors['card']))
        palette.setColor(QPalette.AlternateBase, QColor(colors['background']))
        palette.setColor(QPalette.ToolTipBase, QColor(colors['card']))
        palette.setColor(QPalette.ToolTipText, QColor(colors['text']))
        palette.setColor(QPalette.Text, QColor(colors['text']))
        palette.setColor(QPalette.Button, QColor(colors['background']))
        palette.setColor(QPalette.ButtonText, QColor(colors['text']))
        palette.setColor(QPalette.Link, QColor(colors['primary']))
        palette.setColor(QPalette.Highlight, QColor(colors['primary']))
        palette.setColor(QPalette.HighlightedText, QColor('#ffffff'))
        
        # Set disabled colors
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(colors['text_secondary']))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(colors['text_secondary']))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(colors['text_secondary']))
        
        # Apply the palette
        QApplication.setPalette(palette)


class AboutDialog(QDialog):
    """Dialog showing information about the application"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.setWindowTitle("About Project Organizer")
        self.setFixedSize(500, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout(self)
        
        # App title
        title = QLabel("Project Organizer")
        title.setFont(QFont(self.parent.font_family, 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Version
        version = QLabel("Version 1.1.0 - Dark Edition")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        # Description
        description = QLabel(
            "Project Organizer is a tool for managing your programming projects.\n\n"
            "Features include project tracking, priority management, deadline monitoring, "
            "progress tracking, and more."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        
        # Add spacer
        layout.addSpacing(20)
        
        # Developer Info
        developer_frame = QFrame()
        developer_frame.setObjectName("card")
        developer_layout = QVBoxLayout(developer_frame)
        
        dev_title = QLabel("Developer Information")
        dev_title.setFont(QFont(self.parent.font_family, 12, QFont.Bold))
        dev_title.setAlignment(Qt.AlignCenter)
        developer_layout.addWidget(dev_title)
        
        dev_info = QLabel(
            "Farid Mezane\n"
            "Computer Science Teacher & Software Developer\n\n"
            "With over 10 years of experience in education and software development, "
            "I specialize in creating educational software solutions and applications "
            "that enhance learning experiences. My background spans education, software "
            "development, and technical support.\n\n"
            "Programming: Java, Python, HTML, CSS, JavaScript, C, C++, PHP"
        )
        dev_info.setWordWrap(True)
        dev_info.setAlignment(Qt.AlignLeft)
        developer_layout.addWidget(dev_info)
        
        layout.addWidget(developer_frame)
        
        # Add spacer
        layout.addSpacing(10)
        
        # Add copyright
        copyright = QLabel("© 2025 Farid Mezane. All rights reserved.")
        copyright.setAlignment(Qt.AlignCenter)
        copyright.setStyleSheet(f"color: {self.parent.colors['text_secondary']};")
        layout.addWidget(copyright)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


# Integration with main application
def add_dark_mode_support(project_organizer):
    """Add dark mode support to the project organizer
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Add dark theme manager to the main application
    project_organizer.theme_manager = DarkThemeManager(project_organizer)
    
    # Modify the setup_style method to support the dark theme
    original_setup_style = project_organizer.setup_style
    
    def setup_style_with_dark_theme(self):
        """Set up the application style with dark theme"""
        # Create the stylesheet with dark theme colors
        self.setStyleSheet(f"""
            QMainWindow, QDialog {{
                background-color: {self.colors['background']};
            }}
            QWidget {{
                font-family: {self.font_family};
                color: {self.colors['text']};
            }}
            QLabel {{
                color: {self.colors['text']};
            }}
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.colors['primary_dark']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['primary']};
                border: 1px solid #ddd;
            }}
            QPushButton#accentButton {{
                background-color: {self.colors['accent']};
            }}
            QPushButton#accentButton:hover {{
                background-color: #e67700;
            }}
            QPushButton#dangerButton {{
                background-color: {self.colors['error']};
            }}
            QPushButton#dangerButton:hover {{
                background-color: #c62828;
            }}
            QPushButton#successButton {{
                background-color: {self.colors['success']};
            }}
            QPushButton#successButton:hover {{
                background-color: #388e3c;
            }}
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 8px;
                background-color: {self.colors['card']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 1px solid {self.colors['primary']};
            }}
            QTableWidget {{
                border: 1px solid {self.colors['border']};
                background-color: {self.colors['card']};
                gridline-color: {self.colors['border']};
                color: {self.colors['text']};
            }}
            QHeaderView::section {{
                background-color: {self.colors['primary_dark']};
                padding: 8px;
                border: 1px solid {self.colors['border']};
                font-weight: bold;
                color: white;
            }}
            QFrame#card {{
                background-color: {self.colors['card']};
                border-radius: 8px;
                border: 1px solid {self.colors['border']};
            }}
            QProgressBar {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                text-align: center;
                background-color: {self.colors['background']};
                color: white;
            }}
            QProgressBar::chunk {{
                background-color: {self.colors['primary']};
                width: 10px;
            }}
            QSlider::groove:horizontal {{
                border: 1px solid {self.colors['border']};
                height: 8px;
                background: {self.colors['card']};
                margin: 2px 0;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {self.colors['primary']};
                border: 1px solid {self.colors['primary']};
                width: 18px;
                margin: -8px 0;
                border-radius: 9px;
            }}
            QGroupBox {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                margin-top: 20px;
                font-weight: bold;
                color: {self.colors['text']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: {self.colors['text']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {self.colors['background']};
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.colors['border']};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.colors['primary']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {self.colors['background']};
                height: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.colors['border']};
                min-width: 20px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {self.colors['primary']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
                width: 0px;
            }}
            QTabWidget::pane {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                background-color: {self.colors['card']};
            }}
            QTabBar::tab {{
                background-color: {self.colors['background']};
                border: 1px solid {self.colors['border']};
                border-bottom-color: {self.colors['border']};
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                color: {self.colors['text']};
            }}
            QTabBar::tab:selected {{
                background-color: {self.colors['primary']};
                color: white;
                border-bottom-color: {self.colors['primary']};
            }}
            QMenuBar {{
                background-color: {self.colors['background']};
                color: {self.colors['text']};
                border-bottom: 1px solid {self.colors['border']};
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 4px 10px;
            }}
            QMenuBar::item:selected {{
                background-color: {self.colors['primary']};
                color: white;
            }}
            QMenu {{
                background-color: {self.colors['card']};
                border: 1px solid {self.colors['border']};
            }}
            QMenu::item {{
                padding: 6px 25px 6px 25px;
                color: {self.colors['text']};
            }}
            QMenu::item:selected {{
                background-color: {self.colors['primary']};
                color: white;
            }}
            QListWidget {{
                background-color: {self.colors['card']};
                border: 1px solid {self.colors['border']};
                color: {self.colors['text']};
                alternate-background-color: {self.colors['background']};
            }}
            QListWidget::item:selected {{
                background-color: {self.colors['primary']};
                color: white;
            }}
            QRadioButton, QCheckBox {{
                color: {self.colors['text']};
            }}
            QRadioButton::indicator, QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QRadioButton::indicator::unchecked, QCheckBox::indicator::unchecked {{
                border: 2px solid {self.colors['border']};
                background-color: {self.colors['card']};
                border-radius: 4px;
            }}
            QRadioButton::indicator::checked, QCheckBox::indicator::checked {{
                border: 2px solid {self.colors['primary']};
                background-color: {self.colors['primary']};
                border-radius: 4px;
            }}
            QCalendarWidget {{
                background-color: {self.colors['card']};
                color: {self.colors['text']};
            }}
            QCalendarWidget QToolButton {{
                background-color: {self.colors['primary']};
                color: white;
                border-radius: 2px;
            }}
            QCalendarWidget QMenu {{
                background-color: {self.colors['card']};
                color: {self.colors['text']};
            }}
            QCalendarWidget QSpinBox {{
                background-color: {self.colors['card']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
                selection-color: white;
            }}
            QCalendarWidget QTableView {{
                background-color: {self.colors['card']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
                selection-color: white;
            }}
            QToolTip {{
                background-color: {self.colors['card']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                padding: 4px;
            }}
            QSplitter::handle {{
                background-color: {self.colors['border']};
            }}
            QSplitter::handle:horizontal {{
                width: 2px;
            }}
            QSplitter::handle:vertical {{
                height: 2px;
            }}
            QSplitter::handle:hover {{
                background-color: {self.colors['primary']};
            }}
        """)
    
    # Replace the original method
    project_organizer.setup_style = setup_style_with_dark_theme.__get__(project_organizer)
    
    # Add a simple menu bar with only essential options
    def add_menu_bar():
        """Add a menu bar with minimal options"""
        menu_bar = QMenuBar(project_organizer)
        project_organizer.setMenuBar(menu_bar)
        
        # File menu
        file_menu = QMenu("&File", project_organizer)
        menu_bar.addMenu(file_menu)
        
        # Add export action
        export_action = QAction("&Export Projects", project_organizer)
        export_action.triggered.connect(project_organizer.export_projects)
        file_menu.addAction(export_action)
        
        # Add backup action if the backup functionality is implemented
        if hasattr(project_organizer, 'open_backup_dialog'):
            backup_action = QAction("&Backup && Restore", project_organizer)
            backup_action.triggered.connect(project_organizer.open_backup_dialog)
            file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        # Add exit action
        exit_action = QAction("E&xit", project_organizer)
        exit_action.triggered.connect(project_organizer.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = QMenu("&View", project_organizer)
        menu_bar.addMenu(view_menu)
        
        # Add dashboard action if the dashboard functionality is implemented
        if hasattr(project_organizer, 'open_dashboard'):
            dashboard_action = QAction("&Dashboard", project_organizer)
            dashboard_action.triggered.connect(project_organizer.open_dashboard)
            view_menu.addAction(dashboard_action)
        
        # Help menu
        help_menu = QMenu("&Help", project_organizer)
        menu_bar.addMenu(help_menu)
        
        # Add about action
        about_action = QAction("&About", project_organizer)
        about_action.triggered.connect(lambda: AboutDialog(project_organizer).exec_())
        help_menu.addAction(about_action)
    
    add_menu_bar()