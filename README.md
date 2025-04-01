# Project Organizer

A PyQt5-based desktop application for managing programming projects with a sleek dark theme.

![Project Organizer Dark Theme](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/main.png)

## Overview

Project Organizer is a comprehensive tool designed to help developers track and manage multiple programming projects. The application features a modern dark-themed UI with robust project tracking, smart filtering, analytics dashboard, deadline notifications, and automatic backup functionality.

## Features

- **Project Management**: Create, edit, and track programming projects
- **Smart Filters**: Quickly find projects by status, priority, or deadline
- **Analytics Dashboard**: Visual overview of project status and distribution
- **Dark Theme**: Modern dark UI theme optimized for extended use
- **Deadline Notifications**: System tray notifications for upcoming deadlines
- **Backup System**: Automated and manual backup/restore functionality
- **Export Options**: Export project data in JSON, CSV, or text formats

## Screenshots

### Main Interface
![Main Interface](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/main.png)

### Project Dashboard
![Dashboard](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/dashboard.png)

### Smart Filters
![Smart Filters](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/filters.png)

### Add/Edit Project
![New Project](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/newprj.png)

## Project Structure

```
ProjectOrganizer/
├── dark_main.py               # Main entry point for dark-themed app
├── project_organizer.py       # Core application code
├── dark_theme_integration.py  # Integration of all dark theme components
├── dark_mode_support.py       # Dark mode implementation and app styling
├── dark_smart_filters.py      # Smart filters implementation with dark styling
├── enhanced_dashboard.py      # Dashboard UI and charts implementation
├── deadline_notifications.py  # Notification system for upcoming deadlines
├── backup_functionality.py    # Backup and restore functionality
├── logopo.png                 # Application icon
└── projects_data.json         # Data storage file
```

## Technical Details

### Requirements

- Python 3.6+
- PyQt5 5.12+
- Additional Python packages:
  - datetime
  - json
  - os
  - shutil
  - sys

### Installation

1. Clone the repository:
```bash
git clone https://github.com/faridfgx/ProjectOrganizer.git
cd ProjectOrganizer
```

2. Make sure you have PyQt5 installed:
```bash
pip install PyQt5
```

### Running the Application

To run the dark-themed version of the application:
```bash
python dark_main.py
```

To run the standard version:
```bash
python project_organizer.py
```

### Building an Executable

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --icon=logopo.png dark_main.py

# The executable will be in the dist/ directory
```

## Architecture

The application follows a modular architecture:

1. `project_organizer.py` - Core functionality and base UI
2. Dark theme modules:
   - `dark_mode_support.py` - Implements dark theme styling
   - `dark_smart_filters.py` - Adds smart filtering capability
   - `enhanced_dashboard.py` - Implements project analytics dashboard
3. Support modules:
   - `deadline_notifications.py` - Handles deadline notifications
   - `backup_functionality.py` - Manages data backup/restore

Each module is designed to be relatively independent, with clear integration points through the `dark_theme_integration.py` module.

## Data Management

- Project data is stored in JSON format in `projects_data.json`
- Backups are stored in a `backups/` directory as timestamped JSON files
- Data schema for projects:
  ```json
  {
    "name": "Project Name",
    "language": "Python",
    "priority": "High Priority",
    "completion": 75,
    "deadline": "2025-05-15",
    "description": "Project description text",
    "notes": "Additional notes",
    "dependencies": ["dependency1", "dependency2"],
    "created_date": "2025-04-01",
    "last_updated": "2025-04-01 12:00:00"
  }
  ```

## Extending the Application

### Adding a New Feature

1. Create a new module for your feature (e.g., `my_feature.py`)
2. Implement an integration function:
   ```python
   def add_my_feature(project_organizer):
       """Add your feature to the project organizer
       
       Args:
           project_organizer: The ProjectOrganizer instance
       """
       # Your integration code here
   ```
3. Import and call your integration function in `dark_theme_integration.py`:
   ```python
   from my_feature import add_my_feature
   
   def enhance_project_organizer(project_organizer):
       # Existing code...
       add_my_feature(project_organizer)
       # Existing code...
   ```

### UI Design Guidelines

All UI components follow a consistent dark theme design language:

- Use the color scheme defined in `colors` dictionary from `ProjectOrganizer.setup_style()`
- Text colors:
  - Primary text: `colors['text']` (#e0e0e0)
  - Secondary text: `colors['text_secondary']` (#a0a0a0)
- Background colors:
  - Main background: `colors['background']` (#1e1e1e)
  - Cards/widgets: `colors['card']` (#2d2d2d)
- Accent colors:
  - Primary: `colors['primary']` (#3f6fd1)
  - Success: `colors['success']` (#66bb6a)
  - Warning: `colors['warning']` (#ffca28)
  - Error: `colors['error']` (#ef5350)
- Border radius: 4-8px for most elements
- Spacing:
  - Margins: 10-15px
  - Padding: 8-12px
  - Element spacing: 8-10px

## Documentation

For more detailed information, check out these resources in the `docs` folder:

- [User Guide](docs/UserGuide.md) - Complete guide for users
- [Developer Guide](docs/DeveloperGuide.md) - Technical documentation for developers
- [Contributing](docs/CONTRIBUTING.md) - Guidelines for contributors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Farid Mezane** - Educational Software Developer

## Acknowledgments

- PyQt5 team for the excellent GUI framework
- Icons from various open-source icon sets
- All contributors to the project
