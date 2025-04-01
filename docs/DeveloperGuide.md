# Project Organizer - Developer Guide

This guide provides technical documentation for developers who want to understand, modify, or extend the Project Organizer application.

## Architecture Overview

Project Organizer follows a modular architecture that separates core functionality from UI enhancements, making it easier to maintain and extend.

### Core Components

1. **Project Organizer Core (`project_organizer.py`):**
   - Implements the base application functionality
   - Defines the `ProjectOrganizer` class which is the main application window
   - Manages project data (loading, saving, CRUD operations)
   - Implements the basic UI with light theme

2. **Dark Theme Integration (`dark_theme_integration.py`):**
   - Central integration point for all dark theme enhancements
   - Applies dark theme components in the correct order
   - Calls individual enhancement modules through their add_* functions

3. **Enhancement Modules:**
   - **Dark Mode Support (`dark_mode_support.py`):** Implements the dark theme styling
   - **Smart Filters (`dark_smart_filters.py`):** Adds advanced project filtering
   - **Dashboard (`enhanced_dashboard.py`):** Implements project analytics
   - **Notifications (`deadline_notifications.py`):** Handles deadline reminders
   - **Backup System (`backup_functionality.py`):** Provides data backup and restore

### Application Flow

1. `dark_main.py` is the entry point for the dark-themed application
2. It creates a `ProjectOrganizer` instance
3. It calls `enhance_project_organizer()` to apply dark theme enhancements
4. Each enhancement module adds its functionality to the base application

## Code Structure

### Class Hierarchy

```
ProjectOrganizer (main window)
├── Theme Management
│   └── DarkThemeManager
├── Project Management
│   ├── ProjectDialog
│   ├── ProgressDialog
│   └── ExportDialog
├── Smart Filters
│   ├── SmartFilterManager
│   ├── FilterButton
│   └── SmartFilterPanel
├── Dashboard
│   ├── DashboardWidget
│   ├── DashboardDialog
│   └── MetricCard
├── Notifications
│   ├── NotificationManager
│   └── NotificationSettingsDialog
└── Backup
    ├── BackupManager
    └── BackupDialog
```

### Key Modules in Detail

#### project_organizer.py

Implements the core application functionality:
- Loading and saving project data
- UI setup and rendering
- Project list and detail views
- CRUD operations for projects

Key classes:
- `ProjectOrganizer`: Main application window
- `ProjectDialog`: Dialog for adding/editing projects
- `ProgressDialog`: Dialog for updating project progress
- `ExportDialog`: Dialog for exporting projects

#### dark_mode_support.py

Applies dark theme styling to the application:
- Sets color schemes
- Styles all UI elements
- Creates a custom application palette
- Adds a menu bar with essential options

Key classes:
- `DarkThemeManager`: Manages the dark theme application
- `AboutDialog`: Shows application information

#### dark_smart_filters.py

Implements the smart filtering system:
- Defines filter criteria and functions
- Renders the filter panel
- Applies filters to the project list

Key classes:
- `SmartFilterManager`: Manages filter definitions and application
- `FilterButton`: Individual filter button with selection state
- `SmartFilterPanel`: Panel containing all filter buttons

#### enhanced_dashboard.py

Implements the project analytics dashboard:
- Renders various chart types
- Calculates metrics from project data
- Displays summaries and statistics

Key classes:
- `DashboardWidget`: Implements the dashboard UI
- `DashboardDialog`: Dialog containing the dashboard
- `MetricCard`: Individual metric display card

#### deadline_notifications.py

Implements the deadline notification system:
- Checks for upcoming deadlines
- Shows system tray notifications
- Provides notification settings

Key classes:
- `NotificationManager`: Manages notifications and timers
- `NotificationSettingsDialog`: Dialog for configuring notifications

#### backup_functionality.py

Implements the backup and restore functionality:
- Creates automated and manual backups
- Provides backup restoration
- Exports backups to external locations

Key classes:
- `BackupManager`: Manages backup operations
- `BackupDialog`: Dialog for backup and restore operations

## Data Model

Projects are stored as a list of dictionaries in a JSON file:

```json
[
  {
    "name": "Project 1",
    "language": "Python",
    "priority": "High Priority",
    "completion": 75,
    "deadline": "2025-05-15",
    "description": "Project description",
    "notes": "Additional notes",
    "dependencies": ["dependency1", "dependency2"],
    "created_date": "2025-04-01",
    "last_updated": "2025-04-01 12:00:00"
  },
  {
    "name": "Project 2",
    ...
  }
]
```

Key properties:
- `name`: String (unique identifier)
- `language`: String (programming language)
- `priority`: String ("High Priority", "Medium Priority", or "Low Priority")
- `completion`: Integer (0-100)
- `deadline`: String (YYYY-MM-DD format, optional)
- `description`: String (optional)
- `notes`: String (optional)
- `dependencies`: List of strings (optional)
- `created_date`: String (YYYY-MM-DD format)
- `last_updated`: String (YYYY-MM-DD HH:MM:SS format)

## Implementation Details

### Adding New Projects

```python
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
```

### Filtering Projects

```python
def apply_filter(self, filter_id=None, search_text=None, language_filter=None, sort_by=None):
    """Apply the selected filter and update the project list"""
    # Update active filter and criteria if provided
    if filter_id:
        self.active_filter = filter_id
        
    # Apply the filter function to get the initial filtered list
    filter_func = self.filters[self.active_filter]["function"]
    filtered_projects = filter_func()
    
    # Apply additional filters
    if self.search_text:
        search_text = self.search_text.lower()
        filtered_projects = [p for p in filtered_projects 
                           if search_text in p["name"].lower() or 
                              search_text in p.get("description", "").lower()]
```

### Notification System

```python
def check_notifications(self):
    """Check for deadline notifications"""
    if not self.enabled:
        return
    
    # Get current date
    current_date = datetime.now().date()
    
    # Check for project deadline notifications
    projects_to_notify = []
    
    for project in self.main_app.projects:
        # Skip if no deadline or already completed
        if not project.get("deadline") or int(project.get("completion", 0)) == 100:
            continue
        
        try:
            deadline = datetime.strptime(project["deadline"], "%Y-%m-%d").date()
            days_left = (deadline - current_date).days
            
            # Create a unique ID for this notification
            notification_id = f"{project['name']}_{project['deadline']}"
            
            # Check if it's time to notify and we haven't shown this notification yet
            if 0 <= days_left <= self.remind_days_before and notification_id not in self.shown_notifications:
                projects_to_notify.append((project, days_left))
                self.shown_notifications.add(notification_id)
        except ValueError:
            # Skip invalid dates
            continue
```

## Extension Points

### Adding a New Feature

To add a new feature to Project Organizer:

1. Create a new module for your feature (e.g., `my_feature.py`)
2. Implement an integration function:

```python
def add_my_feature(project_organizer):
    """Add your feature to the project organizer
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Your integration code here
    
    # Example: Add a new button to the UI
    for i in range(project_organizer.centralWidget().layout().count()):
        item = project_organizer.centralWidget().layout().itemAt(i)
        if isinstance(item, QHBoxLayout):
            # This is likely the action buttons layout
            my_button = QPushButton("My Feature")
            my_button.clicked.connect(lambda: my_feature_function(project_organizer))
            item.addWidget(my_button)
            break
    
    def my_feature_function(self):
        """Implement your feature functionality"""
        # Your feature code here
        pass
    
    # Add the method to the project_organizer instance
    project_organizer.my_feature_function = my_feature_function.__get__(project_organizer)
```

3. Import and call your integration function in `dark_theme_integration.py`:

```python
from my_feature import add_my_feature

def enhance_project_organizer(project_organizer):
    # Existing code...
    add_my_feature(project_organizer)
    # Existing code...
```

### Modifying the Data Model

To add new fields to the project data model:

1. Modify the `ProjectDialog` class to include new fields
2. Update the `get_project_data` method to include the new fields
3. Add UI elements to display the new fields in the project details panel
4. Update any filters or dashboard components that might use the new fields

### Adding a New Smart Filter

To add a new smart filter:

1. Add a new entry to the `filters` dictionary in `SmartFilterManager.__init__`:

```python
self.filters["my_filter"] = {
    "name": "My Filter",
    "icon": "filter-icon-name",
    "function": self.filter_my_filter,
    "category": "general",
    "color": "#3f6fd1"  # Blue
}
```

2. Implement the filter function:

```python
def filter_my_filter(self):
    """Filter: Description of what this filter does
    
    Returns:
        list: Filtered projects
    """
    return [p for p in self.main_app.projects if your_condition(p)]
```

## Development Environment Setup

1. Install Python 3.6 or higher
2. Install PyQt5:
   ```bash
   pip install PyQt5
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/faridfgx/ProjectOrganizer.git
   cd ProjectOrganizer
   ```
4. Run the application in development mode:
   ```bash
   python dark_main.py
   ```

### Debugging Tips

- Use `print` statements or Python's logging module to trace execution
- Check the application's data file (`projects_data.json`) for data integrity
- Test filters with various project configurations
- Verify backup files after backup operations

## UI Design Guidelines

All UI components should follow the dark theme design language:

- Use the color scheme defined in `colors` dictionary:
  ```python
  colors = {
      'primary': "#3f6fd1",
      'primary_dark': "#2d50a7",
      'accent': "#ff9800",
      'background': "#1e1e1e",
      'card': "#2d2d2d",
      'text': "#e0e0e0",
      'text_secondary': "#a0a0a0",
      'border': "#3d3d3d",
      'success': "#66bb6a",
      'warning': "#ffca28",
      'error': "#ef5350",
      'high_priority': "#f44336",
      'medium_priority': "#ffa726",
      'low_priority': "#66bb6a"
  }
  ```

- Follow consistent spacing:
  - Margins: 10-15px
  - Padding: 8-12px
  - Element spacing: 8-10px
  
- Use rounded corners for UI elements:
  - Border radius: 4-8px

- Add tooltips to complex UI elements to aid usability

## Building and Distribution

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --icon=logopo.png dark_main.py

# The executable will be in the dist/ directory
```

For a more comprehensive build:

```bash
pyinstaller --name="Project Organizer" \
            --onefile \
            --windowed \
            --icon=logopo.png \
            --add-data="logopo.png;." \
            dark_main.py
```

## Testing

When testing new features or modifications:

1. Test with empty state (no projects)
2. Test with a large number of projects
3. Test all filters with various project configurations
4. Test deadline notifications with projects due soon
5. Test backup and restore functionality
6. Verify that dark theme styling is consistent across all UI elements
7. Test on different operating systems if possible

## Version Control

When committing changes:

1. Use descriptive commit messages
2. Group related changes into single commits
3. Test before committing
4. Follow the branching strategy outlined in the CONTRIBUTING.md file