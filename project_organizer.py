import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QSplitter, QTextEdit, QProgressBar, 
                            QFormLayout, QRadioButton, QButtonGroup, QSlider, QFileDialog, 
                            QMessageBox, QDialog, QDialogButtonBox, QTabWidget, QScrollArea,
                            QFrame, QGroupBox, QCheckBox, QSpinBox, QDateEdit, QCalendarWidget)
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QColor, QFont, QPalette, QPixmap


class ProjectOrganizer(QMainWindow):
    """Main application window for the Project Organizer application"""
    
    def __init__(self):
        super().__init__()
        
        # Set up basic window properties
        self.setWindowTitle("Project Organizer")
        self.setMinimumSize(1000, 700)
        
        # Set application icon
        app_icon = QIcon("logopo.png")
        self.setWindowIcon(app_icon)
        
        # Set up the application style
        self.setup_style()
        
        # Data storage
        self.projects = []
        self.data_file = "projects_data.json"
        self.load_data()
        
        # Set up the UI
        self.setup_ui()
        
        # Update the project list
        self.update_project_list()
    
    def setup_style(self):
        """Set up the application style with dark theme colors by default"""
        # Set dark theme color scheme
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
        
        # Set font
        self.font_family = "Segoe UI"
        
        # Create stylesheet with dark theme
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
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
    
    def setup_ui(self):
        """Set up the main user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create header
        self.create_header(main_layout)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        main_layout.addWidget(splitter, 1)  # Stretch to fill available space
        
        # Create project list panel
        list_panel = QWidget()
        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_panel.setMinimumWidth(600)
        
        self.create_project_filters(list_layout)
        self.create_project_table(list_layout)
        
        # Create detail panel
        detail_panel = QWidget()
        detail_layout = QVBoxLayout(detail_panel)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_panel.setMinimumWidth(300)
        
        self.create_detail_view(detail_layout)
        
        # Add panels to splitter
        splitter.addWidget(list_panel)
        splitter.addWidget(detail_panel)
        
        # Set initial sizes
        splitter.setSizes([600, 400])
        
        # Create action buttons
        self.create_action_buttons(main_layout)
    
    def create_header(self, parent_layout):
        """Create the application header"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # App title
        title_label = QLabel("Project Organizer")
        title_label.setFont(QFont(self.font_family, 18, QFont.Bold))
        header_layout.addWidget(title_label)
        
        # Stats display
        self.stats_label = QLabel()
        header_layout.addWidget(self.stats_label, 0, Qt.AlignRight)
        
        parent_layout.addWidget(header_widget)
    
    def create_project_filters(self, parent_layout):
        """Create the project filtering controls"""
        # Title
        filter_title = QLabel("Your Projects")
        filter_title.setFont(QFont(self.font_family, 12, QFont.Bold))
        parent_layout.addWidget(filter_title)
        
        # Filter frame
        filter_widget = QWidget()
        filter_widget.setObjectName("card")
        filter_layout = QVBoxLayout(filter_widget)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search projects...")
        self.search_input.textChanged.connect(self.update_project_list)
        search_layout.addWidget(self.search_input)
        
        search_button = QPushButton("Search")
        search_button.setIcon(QIcon.fromTheme("search"))
        search_button.clicked.connect(self.update_project_list)
        search_layout.addWidget(search_button)
        
        filter_layout.addLayout(search_layout)
        
        # Filter options
        filter_options = QHBoxLayout()
        
        # Priority filter
        filter_options.addWidget(QLabel("Filter by:"))
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All", "High Priority", "Medium Priority", "Low Priority"])
        self.priority_filter.currentIndexChanged.connect(self.update_project_list)
        filter_options.addWidget(self.priority_filter)
        
        # Language filter
        filter_options.addWidget(QLabel("Language:"))
        self.language_filter = QComboBox()
        self.language_filter.addItems(["All", "Python", "C++", "JavaScript", "HTML/CSS", "C#", "Java", "PHP"])
        self.language_filter.currentIndexChanged.connect(self.update_project_list)
        filter_options.addWidget(self.language_filter)
        
        # Sort filter
        filter_options.addWidget(QLabel("Sort by:"))
        self.sort_filter = QComboBox()
        self.sort_filter.addItems(["Date Added", "Priority", "Deadline", "Completion"])
        self.sort_filter.currentIndexChanged.connect(self.update_project_list)
        filter_options.addWidget(self.sort_filter)
        
        filter_layout.addLayout(filter_options)
        
        # Add to parent
        parent_layout.addWidget(filter_widget)
    
    def create_project_table(self, parent_layout):
        """Create the project list table"""
        # Create table widget
        self.project_table = QTableWidget()
        self.project_table.setColumnCount(5)
        self.project_table.setHorizontalHeaderLabels(["Project Name", "Language", "Priority", "Deadline", "Completion"])
        
        # Set table properties
        self.project_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.project_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.project_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.project_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.project_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.project_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.project_table.setSelectionMode(QTableWidget.SingleSelection)
        self.project_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.project_table.verticalHeader().setVisible(False)
        self.project_table.setAlternatingRowColors(True)
        
        # Connect selection signal
        self.project_table.itemSelectionChanged.connect(self.on_project_select)
        
        parent_layout.addWidget(self.project_table, 1)  # Stretch to fill available space
    
    def create_detail_view(self, parent_layout):
        """Create the project detail view"""
        # Title
        detail_title = QLabel("Project Details")
        detail_title.setFont(QFont(self.font_family, 12, QFont.Bold))
        parent_layout.addWidget(detail_title)
        
        # Create a scroll area for details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # The main container for all details
        self.detail_container = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_container)
        
        # Default message
        self.default_message = QLabel("Select a project to view details")
        self.default_message.setAlignment(Qt.AlignCenter)
        self.default_message.setStyleSheet(f"color: {self.colors['text_secondary']};")
        self.detail_layout.addWidget(self.default_message)
        
        # Set the container as the scroll area widget
        scroll_area.setWidget(self.detail_container)
        parent_layout.addWidget(scroll_area, 1)  # Stretch to fill available space
    
    def create_action_buttons(self, parent_layout):
        """Create main action buttons"""
        button_layout = QHBoxLayout()
        
        # Add project button
        add_button = QPushButton("Add New Project")
        add_button.setIcon(QIcon.fromTheme("list-add"))
        add_button.clicked.connect(self.add_project)
        button_layout.addWidget(add_button)
        
        # Spacer
        button_layout.addStretch()
        
        # Export button
        export_button = QPushButton("Export Projects")
        export_button.setObjectName("successButton")
        export_button.setIcon(QIcon.fromTheme("document-save"))
        export_button.clicked.connect(self.export_projects)
        button_layout.addWidget(export_button)
        
        parent_layout.addLayout(button_layout)
    
    def update_project_list(self):
        """Update the project list with filtered and sorted projects"""
        # Get filter values
        search_text = self.search_input.text().lower()
        priority_filter = self.priority_filter.currentText()
        language_filter = self.language_filter.currentText()
        sort_by = self.sort_filter.currentText()
        
        # Filter projects
        filtered_projects = []
        for project in self.projects:
            # Apply filters
            if priority_filter != "All" and project["priority"] != priority_filter:
                continue
                
            if language_filter != "All" and project["language"] != language_filter:
                continue
                
            # Apply search
            if search_text and search_text not in project["name"].lower() and search_text not in project.get("description", "").lower():
                continue
                
            filtered_projects.append(project)
        
        # Sort projects
        if sort_by == "Priority":
            priority_order = {"High Priority": 0, "Medium Priority": 1, "Low Priority": 2}
            filtered_projects.sort(key=lambda x: priority_order.get(x["priority"], 3))
        elif sort_by == "Deadline":
            # Sort by deadline, putting projects with no deadline at the end
            filtered_projects.sort(key=lambda x: x.get("deadline", "9999-99-99"))
        elif sort_by == "Completion":
            filtered_projects.sort(key=lambda x: float(x.get("completion", 0)), reverse=True)
        # Date Added is the default sort order (the order in the list)
        
        # Clear table
        self.project_table.setRowCount(0)
        
        # Add projects to table
        self.project_table.setRowCount(len(filtered_projects))
        
        for row, project in enumerate(filtered_projects):
            # Project name
            name_item = QTableWidgetItem(project["name"])
            name_item.setData(Qt.UserRole, project["name"])  # Store the project name for reference
            self.project_table.setItem(row, 0, name_item)
            
            # Language
            lang_item = QTableWidgetItem(project["language"])
            self.project_table.setItem(row, 1, lang_item)
            
            # Priority
            priority_item = QTableWidgetItem(project["priority"])
            
            # Set background color based on priority
            if project["priority"] == "High Priority":
                priority_item.setBackground(QColor(self.colors['high_priority']))
                name_item.setForeground(QColor("#FF5252"))  # Red text for high priority
                name_item.setFont(QFont(self.font_family, weight=QFont.Bold))
                # Remove this line to maintain dark theme
                # name_item.setBackground(QColor(255, 235, 235)) 
            elif project["priority"] == "Medium Priority":
                priority_item.setBackground(QColor(self.colors['medium_priority']))
                # Remove this line to maintain dark theme
                # name_item.setBackground(QColor(255, 250, 240))
            else:  # Low Priority
                priority_item.setBackground(QColor(self.colors['low_priority']))
            
            self.project_table.setItem(row, 2, priority_item)
            
            # Deadline
            deadline_item = QTableWidgetItem(project.get("deadline", "Not set"))
            self.project_table.setItem(row, 3, deadline_item)
            
            # Completion
            completion = project.get("completion", 0)
            completion_item = QTableWidgetItem(f"{completion}%")
            
            # Change text color based on completion
            if int(completion) == 100:
                completion_item.setForeground(QColor(self.colors['success']))
                completion_item.setFont(QFont(self.font_family, weight=QFont.Bold))
            
            self.project_table.setItem(row, 4, completion_item)
        
        # Update stats
        self.update_stats()
        
        # Update language filter options if needed
        self.update_language_filter()
    
    def update_language_filter(self):
        """Update the language filter dropdown with available languages"""
        # Store current selection
        current_selection = self.language_filter.currentText()
        
        # Get all languages
        languages = set(["All"])
        for project in self.projects:
            languages.add(project["language"])
        
        # Clear and refill
        self.language_filter.blockSignals(True)
        self.language_filter.clear()
        self.language_filter.addItems(sorted(list(languages)))
        
        # Restore selection if possible
        index = self.language_filter.findText(current_selection)
        if index >= 0:
            self.language_filter.setCurrentIndex(index)
        self.language_filter.blockSignals(False)
    
    def update_stats(self):
        """Update the statistics display"""
        total = len(self.projects)
        completed = sum(1 for p in self.projects if int(p.get("completion", 0)) == 100)
        high_priority = sum(1 for p in self.projects if p["priority"] == "High Priority")
        
        stats_text = f"Total: {total} | Completed: {completed} | High Priority: {high_priority}"
        self.stats_label.setText(stats_text)
    
    def on_project_select(self):
        """Handle project selection in the table"""
        selected_items = self.project_table.selectedItems()
        if not selected_items:
            return
        
        # Get the project name from the first column
        row = selected_items[0].row()
        project_name = self.project_table.item(row, 0).data(Qt.UserRole)
        
        # Find the project in the data
        selected_project = None
        for project in self.projects:
            if project["name"] == project_name:
                selected_project = project
                break
        
        if selected_project:
            self.display_project_details(selected_project)
    
    def display_project_details(self, project):
        """Display the details of the selected project"""
        # Clear the current detail view
        self.clear_detail_view()
        
        # Create a card for project details
        detail_card = QFrame()
        detail_card.setObjectName("card")
        detail_layout = QVBoxLayout(detail_card)
        
        # Project name
        name_label = QLabel(project["name"])
        name_label.setFont(QFont(self.font_family, 16, QFont.Bold))
        detail_layout.addWidget(name_label)
        
        # Create a form layout for the details
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Language
        lang_label = QLabel(project["language"])
        form_layout.addRow("Language:", lang_label)
        
        # Priority
        priority_label = QLabel(project["priority"])
        # Set text color based on priority
        if project["priority"] == "High Priority":
            priority_label.setStyleSheet(f"color: {self.colors['high_priority']}; font-weight: bold;")
        elif project["priority"] == "Medium Priority":
            priority_label.setStyleSheet(f"color: {self.colors['medium_priority']}; font-weight: bold;")
        else:  # Low Priority
            priority_label.setStyleSheet(f"color: {self.colors['low_priority']}; font-weight: bold;")
        form_layout.addRow("Priority:", priority_label)
        
        # Deadline
        if "deadline" in project and project["deadline"]:
            deadline_label = QLabel(project["deadline"])
            form_layout.addRow("Deadline:", deadline_label)
        
        # Completion
        completion_layout = QHBoxLayout()
        completion_value = int(project.get("completion", 0))
        
        completion_label = QLabel(f"{completion_value}%")
        completion_layout.addWidget(completion_label)
        
        progress_bar = QProgressBar()
        progress_bar.setMaximum(100)
        progress_bar.setValue(completion_value)
        progress_bar.setTextVisible(False)
        
        # Set progress bar color based on completion
        if completion_value == 100:
            progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.colors['success']}; }}")
        elif completion_value >= 75:
            progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.colors['primary']}; }}")
        elif completion_value >= 25:
            progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.colors['medium_priority']}; }}")
        else:
            progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.colors['high_priority']}; }}")
            
        completion_layout.addWidget(progress_bar, 1)  # Stretch to fill available space
        form_layout.addRow("Completion:", completion_layout)
        
        detail_layout.addLayout(form_layout)
        
        # Description
        if "description" in project and project["description"]:
            description_group = QGroupBox("Description")
            description_layout = QVBoxLayout(description_group)
            
            description_text = QTextEdit()
            description_text.setPlainText(project["description"])
            description_text.setReadOnly(True)
            description_text.setMaximumHeight(100)
            description_layout.addWidget(description_text)
            
            detail_layout.addWidget(description_group)
        
        # Notes
        if "notes" in project and project["notes"]:
            notes_group = QGroupBox("Notes")
            notes_layout = QVBoxLayout(notes_group)
            
            notes_text = QTextEdit()
            notes_text.setPlainText(project["notes"])
            notes_text.setReadOnly(True)
            notes_text.setMaximumHeight(100)
            notes_layout.addWidget(notes_text)
            
            detail_layout.addWidget(notes_group)
        
        # Dependencies
        if "dependencies" in project and project["dependencies"]:
            dependencies_group = QGroupBox("Dependencies")
            dependencies_layout = QVBoxLayout(dependencies_group)
            
            for dependency in project["dependencies"]:
                dep_label = QLabel(f"• {dependency}")
                dependencies_layout.addWidget(dep_label)
            
            detail_layout.addWidget(dependencies_group)
        
        # Last updated
        if "last_updated" in project:
            updated_label = QLabel(f"Last updated: {project['last_updated']}")
            updated_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 9pt;")
            detail_layout.addWidget(updated_label)
        
        # Add action buttons
        button_layout = QHBoxLayout()
        
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_project(project))
        button_layout.addWidget(edit_button)
        
        progress_button = QPushButton("Update Progress")
        progress_button.setObjectName("successButton")
        progress_button.clicked.connect(lambda: self.update_progress(project))
        button_layout.addWidget(progress_button)
        
        delete_button = QPushButton("Delete")
        delete_button.setObjectName("dangerButton")
        delete_button.clicked.connect(lambda: self.delete_project(project))
        button_layout.addWidget(delete_button)
        
        detail_layout.addLayout(button_layout)
        
        # Add the card to the detail layout
        self.detail_layout.addWidget(detail_card)
    
    def clear_detail_view(self):
        """Clear the detail view container"""
        # Remove all widgets from the layout
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def add_project(self):
        """Open dialog to add a new project"""
        dialog = ProjectDialog(self, "Add New Project")
        
        if dialog.exec_() == QDialog.Accepted:
            # Get the new project data
            project_data = dialog.get_project_data()
            
            # Add current date information
            project_data["created_date"] = datetime.now().strftime("%Y-%m-%d")
            project_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to the projects list
            self.projects.append(project_data)
            
            # Save data
            self.save_data()
            
            # Update the project list
            self.update_project_list()
            
            # Show confirmation
            QMessageBox.information(self, "Success", f"Project '{project_data['name']}' has been added successfully!")
    
    def edit_project(self, project):
        """Open dialog to edit an existing project"""
        dialog = ProjectDialog(self, f"Edit Project: {project['name']}", project)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get the updated project data
            updated_data = dialog.get_project_data()
            
            # Find the project index
            project_index = None
            for i, p in enumerate(self.projects):
                if p["name"] == project["name"]:
                    project_index = i
                    break
            
            if project_index is not None:
                # Update last modified time
                updated_data["created_date"] = project.get("created_date", datetime.now().strftime("%Y-%m-%d"))
                updated_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Update the project in the list
                self.projects[project_index] = updated_data
                
                # Save data
                self.save_data()
                
                # Update the project list
                self.update_project_list()
                
                # Show confirmation
                QMessageBox.information(self, "Success", f"Project '{updated_data['name']}' has been updated successfully!")
            else:
                QMessageBox.warning(self, "Error", "Could not find the project to update.")
    
    def update_progress(self, project):
        """Open dialog to update project progress"""
        dialog = ProgressDialog(self, project)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get the new progress value
            new_progress = dialog.get_progress()
            
            # Find and update the project
            for p in self.projects:
                if p["name"] == project["name"]:
                    p["completion"] = new_progress
                    p["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            
            # Save data
            self.save_data()
            
            # Update the project list
            self.update_project_list()
            
            # Update detail view if project is still selected
            selected_items = self.project_table.selectedItems()
            if selected_items:
                row = selected_items[0].row()
                if self.project_table.item(row, 0).data(Qt.UserRole) == project["name"]:
                    self.on_project_select()
            
            # Show completion message if project is now 100% complete
            if int(new_progress) == 100:
                QMessageBox.information(self, "Congratulations!", 
                                       f"Project '{project['name']}' is now complete!")
            else:
                QMessageBox.information(self, "Success", 
                                       f"Progress for '{project['name']}' updated to {new_progress}%")
    
    def delete_project(self, project):
        """Delete a project after confirmation"""
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{project['name']}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Find and remove the project
            for i, p in enumerate(self.projects):
                if p["name"] == project["name"]:
                    del self.projects[i]
                    break
            
            # Save data
            self.save_data()
            
            # Update the project list
            self.update_project_list()
            
            # Clear the detail view
            self.clear_detail_view()
            self.default_message = QLabel("Select a project to view details")
            self.default_message.setAlignment(Qt.AlignCenter)
            self.default_message.setStyleSheet(f"color: {self.colors['text_secondary']};")
            self.detail_layout.addWidget(self.default_message)
            
            # Show confirmation
            QMessageBox.information(self, "Success", f"Project '{project['name']}' has been deleted successfully!")
    
    def export_projects(self):
        """Export projects to a file"""
        # Create export dialog
        dialog = ExportDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            export_format = dialog.get_export_format()
            
            # Create export data based on format
            if export_format == "JSON":
                # JSON format (full data)
                export_data = json.dumps(self.projects, indent=4)
                default_filename = f"project_export_{datetime.now().strftime('%Y%m%d')}.json"
                file_filter = "JSON Files (*.json)"
                default_ext = ".json"
            
            elif export_format == "CSV":
                # CSV format (basic data)
                import csv
                import io
                
                output = io.StringIO()
                fieldnames = ["name", "language", "priority", "deadline", "completion", "description"]
                
                writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                
                for project in self.projects:
                    writer.writerow({field: project.get(field, "") for field in fieldnames})
                
                export_data = output.getvalue()
                default_filename = f"project_export_{datetime.now().strftime('%Y%m%d')}.csv"
                file_filter = "CSV Files (*.csv)"
                default_ext = ".csv"
            
            else:  # Text Report
                # Generate a readable text report
                export_data = f"PROJECT REPORT - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                export_data += "=" * 80 + "\n\n"
                
                # Summary statistics
                total = len(self.projects)
                completed = sum(1 for p in self.projects if int(p.get("completion", 0)) == 100)
                high_priority = sum(1 for p in self.projects if p["priority"] == "High Priority")
                
                export_data += f"SUMMARY\n"
                export_data += f"Total Projects: {total}\n"
                export_data += f"Completed Projects: {completed}\n"
                export_data += f"High Priority Projects: {high_priority}\n"
                export_data += f"Completion Rate: {int(completed/total*100) if total > 0 else 0}%\n\n"
                
                # Project details
                export_data += "PROJECT DETAILS\n"
                
                for i, project in enumerate(sorted(self.projects, 
                                                  key=lambda x: (x["priority"] != "High Priority", 
                                                               x["priority"] != "Medium Priority"))):
                    export_data += "-" * 80 + "\n"
                    export_data += f"{i+1}. {project['name']} ({project['language']})\n"
                    export_data += f"   Priority: {project['priority']}\n"
                    
                    if "deadline" in project:
                        export_data += f"   Deadline: {project['deadline']}\n"
                    
                    export_data += f"   Completion: {project.get('completion', 0)}%\n"
                    
                    if "description" in project and project["description"]:
                        export_data += f"   Description: {project['description']}\n"
                    
                    export_data += "\n"
                
                default_filename = f"project_report_{datetime.now().strftime('%Y%m%d')}.txt"
                file_filter = "Text Files (*.txt)"
                default_ext = ".txt"
            
            # Ask for save location
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Projects", default_filename, file_filter
            )
            
            if file_path:
                # Add extension if not present
                if not file_path.endswith(default_ext):
                    file_path += default_ext
                
                # Save the file
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(export_data)
                    
                    QMessageBox.information(self, "Export Successful", 
                                           f"Projects exported successfully to:\n{file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Export Error", 
                                        f"An error occurred during export:\n{str(e)}")
    
    def load_data(self):
        """Load project data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.projects = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Data Load Error", 
                               f"Error loading saved data:\n{str(e)}")
            self.projects = []
    
    def save_data(self):
        """Save project data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.projects, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Data Save Error", 
                               f"Error saving data:\n{str(e)}")
    
    def get_icon(self, icon_name):
        """Get an icon by name
        
        Args:
            icon_name: Name of the icon
            
        Returns:
            QIcon: The icon
        """
        return QIcon.fromTheme(icon_name, QIcon("logopo.png")) 


class ProjectDialog(QDialog):
    """Dialog for adding or editing a project"""
    
    def __init__(self, parent=None, title="Project", project=None):
        super().__init__(parent)
        
        self.setWindowTitle(title)
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        # Store the colors from parent
        self.colors = parent.colors if parent else {
            'primary': "#2979ff",
            'error': "#f44336",
            'text_secondary': "#757575"
        }
        
        # Store the project data if editing
        self.project = project
        
        # Set up the dialog layout
        self.setup_ui()
        
        # Fill fields if editing
        if project:
            self.fill_fields(project)
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Create form container
        form_container = QWidget()
        self.form_layout = QVBoxLayout(form_container)
        
        # Project name
        self.name_label = QLabel("Project Name*:")
        self.name_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.form_layout.addWidget(self.name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name")
        self.form_layout.addWidget(self.name_input)
        
        # Language
        self.language_label = QLabel("Programming Language*:")
        self.language_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.form_layout.addWidget(self.language_label)
        
        self.language_input = QComboBox()
        self.language_input.addItems(["Python", "C++", "JavaScript", "HTML/CSS", "C#", "Java", "PHP", "Other"])
        self.language_input.setEditable(True)
        self.form_layout.addWidget(self.language_input)
        
        # Priority
        priority_group = QGroupBox("Priority*")
        priority_layout = QVBoxLayout(priority_group)
        
        self.priority_group = QButtonGroup(self)
        
        self.high_priority = QRadioButton("High Priority")
        self.priority_group.addButton(self.high_priority)
        priority_layout.addWidget(self.high_priority)
        
        self.medium_priority = QRadioButton("Medium Priority")
        self.medium_priority.setChecked(True)  # Default
        self.priority_group.addButton(self.medium_priority)
        priority_layout.addWidget(self.medium_priority)
        
        self.low_priority = QRadioButton("Low Priority")
        self.priority_group.addButton(self.low_priority)
        priority_layout.addWidget(self.low_priority)
        
        self.form_layout.addWidget(priority_group)
        
        # Deadline
        self.deadline_label = QLabel("Deadline:")
        self.deadline_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.form_layout.addWidget(self.deadline_label)
        
        deadline_layout = QHBoxLayout()
        
        self.deadline_input = QDateEdit()
        self.deadline_input.setDisplayFormat("yyyy-MM-dd")
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate())
        deadline_layout.addWidget(self.deadline_input)
        
        self.deadline_checkbox = QCheckBox("Set deadline")
        deadline_layout.addWidget(self.deadline_checkbox)
        
        self.form_layout.addLayout(deadline_layout)
        
        # Completion
        self.completion_label = QLabel("Completion Percentage:")
        self.completion_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.form_layout.addWidget(self.completion_label)
        
        completion_layout = QHBoxLayout()
        
        self.completion_slider = QSlider(Qt.Horizontal)
        self.completion_slider.setMinimum(0)
        self.completion_slider.setMaximum(100)
        self.completion_slider.setValue(0)
        self.completion_slider.setTickPosition(QSlider.TicksBelow)
        self.completion_slider.setTickInterval(10)
        completion_layout.addWidget(self.completion_slider, 1)
        
        self.completion_spin = QSpinBox()
        self.completion_spin.setMinimum(0)
        self.completion_spin.setMaximum(100)
        self.completion_spin.setSuffix("%")
        completion_layout.addWidget(self.completion_spin)
        
        # Connect slider and spinbox
        self.completion_slider.valueChanged.connect(self.completion_spin.setValue)
        self.completion_spin.valueChanged.connect(self.completion_slider.setValue)
        
        self.form_layout.addLayout(completion_layout)
        
        # Description
        self.description_label = QLabel("Description:")
        self.description_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.form_layout.addWidget(self.description_label)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter project description")
        self.description_input.setMaximumHeight(100)
        self.form_layout.addWidget(self.description_input)
        
        # Notes
        self.notes_label = QLabel("Notes:")
        self.notes_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.form_layout.addWidget(self.notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter project notes")
        self.notes_input.setMaximumHeight(100)
        self.form_layout.addWidget(self.notes_input)
        
        # Dependencies
        self.dependencies_label = QLabel("Dependencies (One per line):")
        self.dependencies_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.form_layout.addWidget(self.dependencies_label)
        
        self.dependencies_input = QTextEdit()
        self.dependencies_input.setPlaceholderText("Enter project dependencies (one per line)")
        self.dependencies_input.setMaximumHeight(100)
        self.form_layout.addWidget(self.dependencies_input)
        
        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet(f"color: {self.colors['text_secondary']};")
        self.form_layout.addWidget(required_note)
        
        # Set the scroll widget
        scroll.setWidget(form_container)
        layout.addWidget(scroll)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def fill_fields(self, project):
        """Fill the form fields with project data"""
        self.name_input.setText(project["name"])
        
        # Set language
        index = self.language_input.findText(project["language"])
        if index >= 0:
            self.language_input.setCurrentIndex(index)
        else:
            self.language_input.setEditText(project["language"])
        
        # Set priority
        if project["priority"] == "High Priority":
            self.high_priority.setChecked(True)
        elif project["priority"] == "Medium Priority":
            self.medium_priority.setChecked(True)
        else:
            self.low_priority.setChecked(True)
        
        # Set deadline
        if "deadline" in project and project["deadline"]:
            self.deadline_checkbox.setChecked(True)
            try:
                date = QDate.fromString(project["deadline"], "yyyy-MM-dd")
                self.deadline_input.setDate(date)
            except:
                pass
        
        # Set completion
        self.completion_spin.setValue(int(project.get("completion", 0)))
        
        # Set description
        if "description" in project:
            self.description_input.setPlainText(project["description"])
        
        # Set notes
        if "notes" in project:
            self.notes_input.setPlainText(project["notes"])
        
        # Set dependencies
        if "dependencies" in project and project["dependencies"]:
            self.dependencies_input.setPlainText("\n".join(project["dependencies"]))
    
    def validate_and_accept(self):
        """Validate the form data before accepting"""
        # Check required fields
        name = self.name_input.text().strip()
        language = self.language_input.currentText().strip()
        
        if not name:
            QMessageBox.warning(self, "Validation Error", "Project name is required!")
            return
        
        if not language:
            QMessageBox.warning(self, "Validation Error", "Programming language is required!")
            return
        
        # Check for duplicate name if adding new project
        if not self.project or (self.project and name != self.project["name"]):
            parent = self.parent()
            if any(p["name"] == name for p in parent.projects):
                QMessageBox.warning(self, "Validation Error", 
                                   "A project with this name already exists!")
                return
        
        # If all validations pass, accept the dialog
        self.accept()
    
    def get_project_data(self):
        """Get the project data from the form"""
        # Get priority
        if self.high_priority.isChecked():
            priority = "High Priority"
        elif self.medium_priority.isChecked():
            priority = "Medium Priority"
        else:
            priority = "Low Priority"
        
        # Get deadline
        deadline = None
        if self.deadline_checkbox.isChecked():
            deadline = self.deadline_input.date().toString("yyyy-MM-dd")
        
        # Get dependencies
        dependencies_text = self.dependencies_input.toPlainText().strip()
        dependencies = [dep.strip() for dep in dependencies_text.split("\n") if dep.strip()]
        
        # Create project data dictionary
        project_data = {
            "name": self.name_input.text().strip(),
            "language": self.language_input.currentText().strip(),
            "priority": priority,
            "completion": self.completion_spin.value(),
            "description": self.description_input.toPlainText().strip(),
            "notes": self.notes_input.toPlainText().strip()
        }
        
        if deadline:
            project_data["deadline"] = deadline
        
        if dependencies:
            project_data["dependencies"] = dependencies
        
        return project_data


class ProgressDialog(QDialog):
    """Dialog for updating project progress"""
    
    def __init__(self, parent=None, project=None):
        super().__init__(parent)
        
        self.setWindowTitle(f"Update Progress: {project['name']}")
        self.setFixedSize(400, 200)
        
        # Set up the dialog layout
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(f"Update Progress for '{project['name']}'")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Current progress info
        current_progress = int(project.get("completion", 0))
        current_label = QLabel(f"Current Progress: {current_progress}%")
        current_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(current_label)
        
        # Progress controls
        progress_frame = QFrame()
        progress_layout = QHBoxLayout(progress_frame)
        
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(100)
        self.progress_slider.setValue(current_progress)
        self.progress_slider.setTickPosition(QSlider.TicksBelow)
        self.progress_slider.setTickInterval(10)
        progress_layout.addWidget(self.progress_slider, 1)
        
        self.progress_spin = QSpinBox()
        self.progress_spin.setMinimum(0)
        self.progress_spin.setMaximum(100)
        self.progress_spin.setValue(current_progress)
        self.progress_spin.setSuffix("%")
        progress_layout.addWidget(self.progress_spin)
        
        # Connect slider and spinbox
        self.progress_slider.valueChanged.connect(self.progress_spin.setValue)
        self.progress_spin.valueChanged.connect(self.progress_slider.setValue)
        
        layout.addWidget(progress_frame)
        
        # Add spacer
        layout.addStretch()
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_progress(self):
        """Get the progress value"""
        return self.progress_spin.value()


class ExportDialog(QDialog):
    """Dialog for selecting export format"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Export Projects")
        # Increase the dialog size to give more room for buttons
        self.setMinimumSize(450, 250)
        
        # Set up the dialog layout
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Select Export Format")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Format options
        self.json_radio = QRadioButton("JSON (All data)")
        self.json_radio.setChecked(True)
        self.json_radio.setMinimumHeight(28)  # Increase height
        layout.addWidget(self.json_radio)
        
        json_desc = QLabel("   Exports all project details in a format that can be imported later.")
        json_desc.setStyleSheet("color: gray;")
        layout.addWidget(json_desc)
        
        self.csv_radio = QRadioButton("CSV (Basic data)")
        self.csv_radio.setMinimumHeight(28)  # Increase height
        layout.addWidget(self.csv_radio)
        
        csv_desc = QLabel("   Exports basic project data in a format that can be opened in Excel.")
        csv_desc.setStyleSheet("color: gray;")
        layout.addWidget(csv_desc)
        
        self.text_radio = QRadioButton("Text Report (Readable summary)")
        self.text_radio.setMinimumHeight(28)  # Increase height
        layout.addWidget(self.text_radio)
        
        text_desc = QLabel("   Generates a human-readable report of all projects.")
        text_desc.setStyleSheet("color: gray;")
        layout.addWidget(text_desc)
        
        # Add spacer
        layout.addStretch()
        
        # Dialog buttons - use QPushButton instead of QDialogButtonBox for more control
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.setMinimumSize(100, 30)  # Set minimum button size
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumSize(100, 30)  # Set minimum button size
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_export_format(self):
        """Get the selected export format"""
        if self.json_radio.isChecked():
            return "JSON"
        elif self.csv_radio.isChecked():
            return "CSV"
        else:
            return "Text"


# Main function to run the application
def main():
    app = QApplication(sys.argv)
    
    # Set application icon for all windows
    app_icon = QIcon("logopo.png")
    app.setWindowIcon(app_icon)
    
    window = ProjectOrganizer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()