from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QTabWidget, QScrollArea, QFrame,
                             QToolButton, QMenu, QAction, QButtonGroup, 
                             QRadioButton, QPushButton, QSizePolicy, 
                             QSplitter, QTableWidgetItem)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette


class SmartFilterManager:
    """Manages smart filters for project list with dark theme styling"""
    
    def __init__(self, main_app):
        """Initialize the smart filter manager
        
        Args:
            main_app: The main application instance (ProjectOrganizer)
        """
        self.main_app = main_app
        
        # Define smart filters with enhanced icons
        self.filters = {
            "all": {
                "name": "All Projects",
                "icon": "view-list-icons",
                "function": self.filter_all,
                "category": "general",
                "color": "#3f6fd1"  # Blue
            },
            "due_today": {
                "name": "Due Today",
                "icon": "appointment-soon",
                "function": self.filter_due_today,
                "category": "deadline",
                "color": "#ff4081"  # Pink
            },
            "due_this_week": {
                "name": "Due This Week",
                "icon": "calendar-week",
                "function": self.filter_due_this_week,
                "category": "deadline",
                "color": "#ffa726"  # Orange
            },
            "overdue": {
                "name": "Overdue",
                "icon": "appointment-missed",
                "function": self.filter_overdue,
                "category": "deadline",
                "color": "#ff5252"  # Red
            },
            "high_priority": {
                "name": "High Priority",
                "icon": "emblem-important",
                "function": self.filter_high_priority,
                "category": "general",
                "color": "#ff5252"  # Red
            },
            "recently_updated": {
                "name": "Recently Updated",
                "icon": "document-save",
                "function": self.filter_recently_updated,
                "category": "activity",
                "color": "#64b5f6"  # Light Blue
            },
            "stalled": {
                "name": "Stalled Projects",
                "icon": "media-playback-pause",
                "function": self.filter_stalled,
                "category": "activity",
                "color": "#9575cd"  # Purple
            },
            "nearly_complete": {
                "name": "Nearly Complete",
                "icon": "task-complete",
                "function": self.filter_nearly_complete,
                "category": "progress",
                "color": "#66bb6a"  # Green
            },
            "no_progress": {
                "name": "No Progress",
                "icon": "dialog-error",
                "function": self.filter_no_progress,
                "category": "progress",
                "color": "#ff9100"  # Amber
            },
            "completed": {
                "name": "Completed",
                "icon": "emblem-success",
                "function": self.filter_completed,
                "category": "progress",
                "color": "#66bb6a"  # Green
            }
        }
        
        # Current active filter
        self.active_filter = "all"
        
        # Additional search/filter criteria
        self.search_text = ""
        self.language_filter = "All"
        self.sort_by = "Date Added"
    
    def apply_filter(self, filter_id=None, search_text=None, language_filter=None, sort_by=None):
        """Apply the selected filter and update the project list
        
        Args:
            filter_id: ID of the filter to apply, or None to use the active filter
            search_text: Text to search for, or None to use the existing search
            language_filter: Language to filter by, or None to use the existing filter
            sort_by: Field to sort by, or None to use the existing sort
            
        Returns:
            list: Filtered projects
        """
        # Update active filter and criteria if provided
        if filter_id:
            self.active_filter = filter_id
        if search_text is not None:
            self.search_text = search_text
        if language_filter is not None:
            self.language_filter = language_filter
        if sort_by is not None:
            self.sort_by = sort_by
        
        # Apply the filter function to get the initial filtered list
        filter_func = self.filters[self.active_filter]["function"]
        filtered_projects = filter_func()
        
        # Apply additional filters
        # Apply search filter
        if self.search_text:
            search_text = self.search_text.lower()
            filtered_projects = [p for p in filtered_projects 
                               if search_text in p["name"].lower() or 
                                  search_text in p.get("description", "").lower()]
        
        # Apply language filter
        if self.language_filter != "All":
            filtered_projects = [p for p in filtered_projects 
                               if p["language"] == self.language_filter]
        
        # Sort the results
        if self.sort_by == "Priority":
            priority_order = {"High Priority": 0, "Medium Priority": 1, "Low Priority": 2}
            filtered_projects.sort(key=lambda x: priority_order.get(x["priority"], 3))
        elif self.sort_by == "Deadline":
            # Sort by deadline, putting projects with no deadline at the end
            filtered_projects.sort(key=lambda x: x.get("deadline", "9999-99-99"))
        elif self.sort_by == "Completion":
            filtered_projects.sort(key=lambda x: float(x.get("completion", 0)), reverse=True)
        elif self.sort_by == "Name":
            filtered_projects.sort(key=lambda x: x["name"].lower())
        # Default is Date Added, which is the original order
        
        return filtered_projects
    
    def filter_all(self):
        """Filter: All projects
        
        Returns:
            list: All projects
        """
        return self.main_app.projects
    
    def filter_due_today(self):
        """Filter: Projects due today
        
        Returns:
            list: Projects due today
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return [p for p in self.main_app.projects if p.get("deadline") == today]
    
    def filter_due_this_week(self):
        """Filter: Projects due within the next 7 days
        
        Returns:
            list: Projects due this week
        """
        today = datetime.now().date()
        end_of_week = (today + timedelta(days=7)).strftime("%Y-%m-%d")
        today_str = today.strftime("%Y-%m-%d")
        
        return [p for p in self.main_app.projects 
                if p.get("deadline") and today_str <= p.get("deadline") <= end_of_week]
    
    def filter_overdue(self):
        """Filter: Overdue projects (deadline passed, not complete)
        
        Returns:
            list: Overdue projects
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return [p for p in self.main_app.projects 
                if p.get("deadline") and p.get("deadline") < today and int(p.get("completion", 0)) < 100]
    
    def filter_high_priority(self):
        """Filter: High priority projects
        
        Returns:
            list: High priority projects
        """
        return [p for p in self.main_app.projects if p["priority"] == "High Priority"]
    
    def filter_recently_updated(self):
        """Filter: Projects updated in the last 3 days
        
        Returns:
            list: Recently updated projects
        """
        # Calculate the date 3 days ago
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        
        return [p for p in self.main_app.projects 
                if "last_updated" in p and p["last_updated"][:10] >= three_days_ago]
    
    def filter_stalled(self):
        """Filter: Projects that haven't been updated in over 14 days with < 100% completion
        
        Returns:
            list: Stalled projects
        """
        # Calculate the date 14 days ago
        fourteen_days_ago = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        
        return [p for p in self.main_app.projects 
                if ("last_updated" in p and p["last_updated"][:10] < fourteen_days_ago
                    and int(p.get("completion", 0)) < 100)]
    
    def filter_nearly_complete(self):
        """Filter: Projects that are at least 75% complete but not 100%
        
        Returns:
            list: Nearly complete projects
        """
        return [p for p in self.main_app.projects 
                if 75 <= int(p.get("completion", 0)) < 100]
    
    def filter_no_progress(self):
        """Filter: Projects with 0% completion
        
        Returns:
            list: Projects with no progress
        """
        return [p for p in self.main_app.projects 
                if int(p.get("completion", 0)) == 0]
    
    def filter_completed(self):
        """Filter: Completed projects (100% completion)
        
        Returns:
            list: Completed projects
        """
        return [p for p in self.main_app.projects 
                if int(p.get("completion", 0)) == 100]


class FilterButton(QWidget):
    """Custom button for smart filters with dark theme styling"""
    
    def __init__(self, parent, filter_id, filter_info, on_click):
        super().__init__(parent)
        self.filter_id = filter_id
        self.filter_info = filter_info
        self.on_click = on_click
        self.is_selected = False
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the button UI with enhanced styling for dark theme"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(12)
        
        # Icon with color tint based on filter
        self.icon_label = QLabel()
        icon = QIcon.fromTheme(self.filter_info["icon"])
        self.icon_label.setPixmap(icon.pixmap(18, 18))
        layout.addWidget(self.icon_label)
        
        # Name with custom font
        self.name_label = QLabel(self.filter_info["name"])
        self.name_label.setStyleSheet(f"color: {self.filter_info.get('color', '#ffffff')};")
        layout.addWidget(self.name_label, 1)  # Stretch
        
        # Count label with pill shape
        self.count_label = QLabel("0")
        self.count_label.setStyleSheet(f"""
            background-color: {self.parent().parent.colors['card']};
            color: {self.parent().parent.colors['text_secondary']};
            border-radius: 10px;
            padding: 2px 8px;
            min-width: 16px;
            text-align: center;
        """)
        layout.addWidget(self.count_label)
        
        # Set the cursor to a pointing hand
        self.setCursor(Qt.PointingHandCursor)
        
        # Set dark theme appearance
        self.setStyleSheet(f"""
            FilterButton {{
                background-color: transparent;
                border-radius: 6px;
                padding: 2px;
            }}
            FilterButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """)
        
        # Set min height
        self.setMinimumHeight(36)
    
    def update_count(self, count):
        """Update the count label
        
        Args:
            count: The new count
        """
        self.count_label.setText(str(count))
        
        # If count is zero, make it less visible
        if count == 0:
            self.count_label.setStyleSheet(f"""
                background-color: {self.parent().parent.colors['background']};
                color: {self.parent().parent.colors['text_secondary']};
                border-radius: 10px;
                padding: 2px 8px;
                min-width: 16px;
                text-align: center;
            """)
        else:
            # Use filter color for non-zero counts
            color = self.filter_info.get('color', self.parent().parent.colors['primary'])
            self.count_label.setStyleSheet(f"""
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 2px 8px;
                min-width: 16px;
                font-weight: bold;
                text-align: center;
            """)
    
    def set_selected(self, selected):
        """Set whether this filter is selected with enhanced visual feedback
        
        Args:
            selected: True if selected, False otherwise
        """
        self.is_selected = selected
        
        if selected:
            # Update appearance for selected state
            color = self.filter_info.get('color', self.parent().parent.colors['primary'])
            self.setStyleSheet(f"""
                FilterButton {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 6px;
                    border-left: 3px solid {color};
                    padding: 2px;
                }}
                FilterButton:hover {{
                    background-color: rgba(255, 255, 255, 0.15);
                }}
            """)
            # Make text bold
            font = self.name_label.font()
            font.setBold(True)
            self.name_label.setFont(font)
            # Make icon brighter
            icon = QIcon.fromTheme(self.filter_info["icon"])
            self.icon_label.setPixmap(icon.pixmap(18, 18))
        else:
            # Reset appearance
            self.setStyleSheet(f"""
                FilterButton {{
                    background-color: transparent;
                    border-radius: 6px;
                    padding: 2px;
                }}
                FilterButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}
            """)
            # Reset text weight
            font = self.name_label.font()
            font.setBold(False)
            self.name_label.setFont(font)
            # Reset icon
            icon = QIcon.fromTheme(self.filter_info["icon"])
            self.icon_label.setPixmap(icon.pixmap(18, 18))
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        if event.button() == Qt.LeftButton:
            self.on_click(self.filter_id)
        super().mousePressEvent(event)


class SmartFilterPanel(QWidget):
    """Panel for displaying and selecting smart filters with dark theme styling"""
    
    def __init__(self, parent, filter_manager):
        super().__init__(parent)
        self.parent = parent
        self.filter_manager = filter_manager
        self.filter_buttons = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the panel UI with dark theme styling"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Title with larger font
        title_label = QLabel("Smart Filters")
        title_label.setFont(QFont(self.parent.font_family, 16, QFont.Bold))
        title_label.setStyleSheet(f"color: {self.parent.colors['text']};")
        title_label.setContentsMargins(10, 8, 10, 8)
        layout.addWidget(title_label)
        
        # Create scrollable area for filters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {self.parent.colors['background']};
                border: none;
            }}
            QScrollBar:vertical {{
                background: {self.parent.colors['background']};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.parent.colors['border']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Container for filter categories
        filter_container = QWidget()
        filter_container.setStyleSheet(f"background-color: {self.parent.colors['background']};")
        filter_layout = QVBoxLayout(filter_container)
        filter_layout.setContentsMargins(10, 5, 5, 10)
        filter_layout.setSpacing(8)
        
        # Create filter categories with modern styling
        categories = {
            "general": "General",
            "deadline": "Deadlines",
            "activity": "Activity",
            "progress": "Progress"
        }
        
        for category_id, category_name in categories.items():
            # Category label with subtle divider
            category_label = QLabel(category_name.upper())
            category_label.setStyleSheet(f"""
                font-weight: bold;
                font-size: 11px;
                color: {self.parent.colors['text_secondary']};
                padding-top: 8px;
                padding-bottom: 4px;
            """)
            category_label.setContentsMargins(8, 8, 8, 4)
            filter_layout.addWidget(category_label)
            
            # Add filters for this category
            category_filters = [f_id for f_id, f_info in self.filter_manager.filters.items() 
                               if f_info["category"] == category_id]
            
            for filter_id in category_filters:
                filter_info = self.filter_manager.filters[filter_id]
                
                # Create filter button
                filter_button = FilterButton(self, filter_id, filter_info, self.apply_filter)
                
                # Set selected state if this is the active filter
                if filter_id == self.filter_manager.active_filter:
                    filter_button.set_selected(True)
                
                # Add to layout
                filter_layout.addWidget(filter_button)
                
                # Store the button for later reference
                self.filter_buttons[filter_id] = filter_button
        
        # Add spacer at the bottom
        filter_layout.addStretch()
        
        # Set the container as the scroll area widget
        scroll_area.setWidget(filter_container)
        layout.addWidget(scroll_area)
    
    def apply_filter(self, filter_id):
        """Apply the selected filter
        
        Args:
            filter_id: ID of the filter to apply
        """
        # Update button selection
        for btn_id, button in self.filter_buttons.items():
            button.set_selected(btn_id == filter_id)
        
        # Apply the filter
        filtered_projects = self.filter_manager.apply_filter(filter_id)
        
        # Update the main app with filtered projects
        self.parent.display_filtered_projects(filtered_projects)
    
    def update_counts(self):
        """Update the count label for each filter button"""
        for filter_id, button in self.filter_buttons.items():
            # Get the count for this filter
            filter_func = self.filter_manager.filters[filter_id]["function"]
            count = len(filter_func())
            
            # Update the button
            button.update_count(count)


# Integration with main application
# Fix for dark_smart_filters.py
# The problem is in the add_smart_filters function
# We need to define the display_filtered_projects method before calling update_project_list

def add_smart_filters(project_organizer):
    """Add smart filters to the project organizer
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Add smart filter manager to the main application
    project_organizer.filter_manager = SmartFilterManager(project_organizer)
    
    # Store the original update_project_list method
    original_update_project_list = project_organizer.update_project_list
    
    # Override the update_project_list method
    def update_project_list_with_filters(self):
        """Update the project list with smart filters applied"""
        # Get filter criteria from UI
        search_text = self.search_input.text()
        language_filter = self.language_filter.currentText()
        sort_by = self.sort_filter.currentText()
        
        # Apply filters with additional criteria
        filtered_projects = self.filter_manager.apply_filter(
            filter_id=None,
            search_text=search_text,
            language_filter=language_filter,
            sort_by=sort_by
        )
        
        # Display filtered projects
        self.display_filtered_projects(filtered_projects)
        
        # Update filter counts
        if hasattr(self, 'filter_panel'):
            self.filter_panel.update_counts()
    
    # Add method to display filtered projects
    def display_filtered_projects(self, filtered_projects):
        """Display the filtered projects in the table
        
        Args:
            filtered_projects: List of projects to display
        """
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
                # Remove light background for dark theme consistency
                # name_item.setBackground(QColor(255, 235, 235))
            elif project["priority"] == "Medium Priority":
                priority_item.setBackground(QColor(self.colors['medium_priority']))
                # Remove light background for dark theme consistency
                # name_item.setBackground(QColor(255, 250, 240))
            else:  # Low Priority
                priority_item.setBackground(QColor(self.colors['low_priority']))
            
            self.project_table.setItem(row, 2, priority_item)
            
            # Deadline
            deadline_item = QTableWidgetItem(project.get("deadline", "Not set"))
            # Colorize based on urgency
            if project.get("deadline"):
                try:
                    deadline_date = datetime.strptime(project["deadline"], "%Y-%m-%d").date()
                    today = datetime.now().date()
                    days_left = (deadline_date - today).days
                    
                    if days_left < 0:  # Overdue
                        deadline_item.setForeground(QColor("#FF5252"))  # Red
                    elif days_left <= 2:  # Due soon
                        deadline_item.setForeground(QColor("#FFA726"))  # Orange
                except ValueError:
                    pass
                    
            self.project_table.setItem(row, 3, deadline_item)
            
            # Completion
            completion = project.get("completion", 0)
            completion_item = QTableWidgetItem(f"{completion}%")
            
            # Change text color based on completion
            if int(completion) == 100:
                completion_item.setForeground(QColor(self.colors['success']))
                completion_item.setFont(QFont(self.font_family, weight=QFont.Bold))
            elif int(completion) >= 75:
                completion_item.setForeground(QColor("#64B5F6"))  # Light blue
            
            self.project_table.setItem(row, 4, completion_item)
        
        # Update stats
        self.update_stats()
        
        # Update language filter options if needed
        self.update_language_filter()
    
    # First, add the display_filtered_projects method to the project_organizer
    project_organizer.display_filtered_projects = display_filtered_projects.__get__(project_organizer)
    
    # Then update the update_project_list method
    project_organizer.update_project_list = update_project_list_with_filters.__get__(project_organizer)
    
    # Modify the UI to add the filter panel
    def add_filter_panel():
        """Add the smart filter panel to the UI"""
        # Find the list panel
        list_panel = None
        for i in range(project_organizer.centralWidget().layout().count()):
            item = project_organizer.centralWidget().layout().itemAt(i)
            if isinstance(item, QSplitter):
                splitter = item.widget()
                if splitter.count() > 0:
                    list_panel = splitter.widget(0)
                    break
        
        if list_panel:
            # Create a splitter for the list panel
            list_splitter = QSplitter(Qt.Horizontal)
            list_splitter.setStyleSheet(f"""
                QSplitter::handle {{
                    background-color: {project_organizer.colors['border']};
                    width: 1px;
                }}
            """)
            
            # Create the filter panel
            filter_panel = SmartFilterPanel(project_organizer, project_organizer.filter_manager)
            project_organizer.filter_panel = filter_panel
            
            # Create a new container for the existing list content
            list_content = QWidget()
            list_content_layout = QVBoxLayout(list_content)
            list_content_layout.setContentsMargins(5, 0, 0, 0)
            
            # Move existing content to the new container
            while list_panel.layout().count():
                item = list_panel.layout().takeAt(0)
                if item.widget():
                    list_content_layout.addWidget(item.widget())
                elif item.layout():
                    list_content_layout.addLayout(item.layout())
            
            # Add the filter panel and list content to the splitter
            list_splitter.addWidget(filter_panel)
            list_splitter.addWidget(list_content)
            
            # Set sizes to give filter panel about 1/4 of the width
            list_splitter.setSizes([200, 400])
            
            # Add the splitter to the list panel
            list_panel.layout().addWidget(list_splitter)
    
    # Call the function to add the filter panel
    add_filter_panel()
    
    # Update project list to apply initial filter
    project_organizer.update_project_list()