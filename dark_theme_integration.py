"""
Project Organizer Dark Theme Integration Module

This module integrates all the dark-themed enhancements to the Project Organizer application:
1. Dark mode support (exclusively dark theme)
2. Enhanced dashboard with dark theme styling
3. Smart filters with dark theme styling
4. Backup functionality with dark theme styling
5. Simple notification system for deadlines with dark theme styling
"""

# Import PyQt components needed for final tweaks
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel

# Import enhanced dark mode implementation
from dark_mode_support import add_dark_mode_support

# Import enhanced dashboard implementation
from enhanced_dashboard import add_dashboard

# Import enhanced smart filters implementation
from dark_smart_filters import add_smart_filters

# Import original modules (which will be styled by the dark theme)
from backup_functionality import add_backup_functionality
from deadline_notifications import add_deadline_notifications


def apply_final_tweaks(project_organizer):
    """Apply any final tweaks to ensure consistent dark theme styling
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Enhance table header styling
    project_organizer.project_table.horizontalHeader().setStyleSheet(f"""
        QHeaderView::section {{
            background-color: {project_organizer.colors['card']};
            color: {project_organizer.colors['text']};
            border: 1px solid {project_organizer.colors['border']};
            padding: 8px;
            font-weight: bold;
        }}
    """)
    
    # Add alternating row colors to project table
    project_organizer.project_table.setAlternatingRowColors(True)
    project_organizer.project_table.setStyleSheet(f"""
        QTableWidget {{
            alternate-background-color: {project_organizer.colors['background']};
            background-color: {project_organizer.colors['card']};
            gridline-color: {project_organizer.colors['border']};
            border: 1px solid {project_organizer.colors['border']};
            border-radius: 4px;
            selection-background-color: {project_organizer.colors['primary']};
            selection-color: white;
        }}
    """)
    
    # Enhance search input styling
    project_organizer.search_input.setStyleSheet(f"""
        QLineEdit {{
            background-color: {project_organizer.colors['card']};
            color: {project_organizer.colors['text']};
            border: 1px solid {project_organizer.colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border: 1px solid {project_organizer.colors['primary']};
        }}
    """)
    
    # Enhance combo boxes styling
    combobox_style = f"""
        QComboBox {{
            background-color: {project_organizer.colors['card']};
            color: {project_organizer.colors['text']};
            border: 1px solid {project_organizer.colors['border']};
            border-radius: 4px;
            padding: 4px 8px;
            min-width: 100px;
        }}
        QComboBox:hover {{
            border: 1px solid {project_organizer.colors['primary']};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid {project_organizer.colors['border']};
        }}
        QComboBox QAbstractItemView {{
            background-color: {project_organizer.colors['card']};
            color: {project_organizer.colors['text']};
            border: 1px solid {project_organizer.colors['border']};
            selection-background-color: {project_organizer.colors['primary']};
            selection-color: white;
        }}
    """
    
    project_organizer.priority_filter.setStyleSheet(combobox_style)
    project_organizer.language_filter.setStyleSheet(combobox_style)
    project_organizer.sort_filter.setStyleSheet(combobox_style)
    
    # Enhance buttons
    for i in range(project_organizer.centralWidget().layout().count()):
        item = project_organizer.centralWidget().layout().itemAt(i)
        if isinstance(item, QHBoxLayout):
            # This is likely the action buttons layout
            for j in range(item.count()):
                widget = item.itemAt(j).widget()
                if isinstance(widget, QPushButton):
                    widget.setMinimumHeight(36)
                    widget.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {project_organizer.colors['primary']};
                            color: white;
                            border: none;
                            border-radius: 6px;
                            padding: 8px 16px;
                            font-weight: bold;
                            text-transform: uppercase;
                            font-size: 11px;
                        }}
                        QPushButton:hover {{
                            background-color: {project_organizer.colors['primary_dark']};
                        }}
                        QPushButton:pressed {{
                            background-color: {project_organizer.colors['primary']};
                            border: 1px solid white;
                        }}
                    """)
    
    # Make project name bold in the project table
    for row in range(project_organizer.project_table.rowCount()):
        name_item = project_organizer.project_table.item(row, 0)
        if name_item:
            font = name_item.font()
            font.setBold(True)
            name_item.setFont(font)
    
    # Update the application title style
    for i in range(project_organizer.centralWidget().layout().count()):
        item = project_organizer.centralWidget().layout().itemAt(i)
        if isinstance(item, QHBoxLayout):
            for j in range(item.count()):
                widget = item.itemAt(j).widget()
                if isinstance(widget, QLabel) and widget.text() == "Project Organizer":
                    widget.setStyleSheet(f"""
                        font-size: 24px;
                        font-weight: bold;
                        color: {project_organizer.colors['text']};
                    """)
                    break


def enhance_project_organizer(project_organizer):
    """Apply all dark-themed enhancements to the Project Organizer application
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    print("Applying dark-themed enhancements to Project Organizer...")
    
    # Load all enhancements in proper order
    # 1. First apply dark mode support as it modifies the UI style
    add_dark_mode_support(project_organizer)
    
    # 2. Add backup functionality
    add_backup_functionality(project_organizer)
    
    # 3. Add smart filters
    add_smart_filters(project_organizer)
    
    # 4. Add enhanced project dashboard
    add_dashboard(project_organizer)
    
    # 5. Add deadline notifications (last to ensure UI is fully set up)
    add_deadline_notifications(project_organizer)
    
    # 6. Apply any final dark theme tweaks
    apply_final_tweaks(project_organizer)
    
    print("All dark-themed enhancements applied successfully!")