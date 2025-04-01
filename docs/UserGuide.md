# Project Organizer - User Guide

## Introduction

Project Organizer is a desktop application designed to help you manage your programming projects efficiently. With its intuitive interface and powerful features, you can track project progress, set priorities, manage deadlines, and keep all your project information organized in one place.

## Getting Started

### Installation

1. Download the latest release from the [releases page](https://github.com/faridfgx/ProjectOrganizer/releases)
2. Run the installer and follow the on-screen instructions
3. Launch Project Organizer from your applications menu or desktop shortcut

### Main Interface

![Main Interface](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/main.png)

The Project Organizer interface is divided into several key areas:

- **Project List** (center): Shows all your projects with basic information
- **Project Details** (right): Displays comprehensive information about the selected project
- **Smart Filters** (left): Quick filters to find specific types of projects
- **Action Buttons** (bottom): Buttons for common actions like adding projects, opening the dashboard, etc.

## Managing Projects

### Adding a New Project

1. Click the "Add New Project" button at the bottom of the window
2. Fill in the project details:

![New Project](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/newprj.png)

   - **Name**: A unique identifier for your project
   - **Programming Language**: The primary language used
   - **Priority**: High, Medium, or Low priority
   - **Deadline**: Optional due date for the project
   - **Completion**: Current progress percentage
   - **Description**: Brief overview of the project
   - **Notes**: Additional information or comments
   - **Dependencies**: Other projects or resources this project depends on

3. Click "Save" to add the project to your list

### Editing Projects

1. Select a project from the list
2. Click the "Edit" button in the project details panel
3. Modify any information as needed
4. Click "Save" to update the project

### Updating Progress

1. Select a project from the list
2. Click the "Update Progress" button
3. Adjust the completion percentage using the slider or spin box
4. Click "Save" to update the progress

### Deleting Projects

1. Select a project from the list
2. Click the "Delete" button in the project details panel
3. Confirm the deletion when prompted

## Using Smart Filters

![Smart Filters](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/filters.png)

Smart filters help you quickly find specific projects:

- **All Projects**: Shows all projects in your list
- **Due Today**: Shows projects due today
- **Due This Week**: Shows projects due within the next 7 days
- **Overdue**: Shows projects past their deadline
- **High Priority**: Shows only high-priority projects
- **Recently Updated**: Shows projects updated in the last 3 days
- **Stalled Projects**: Shows projects with no updates in the last 14 days
- **Nearly Complete**: Shows projects between 75% and 99% complete
- **No Progress**: Shows projects with 0% completion
- **Completed**: Shows 100% completed projects

Click on any filter to instantly see matching projects.

## Project Dashboard

![Dashboard](https://github.com/faridfgx/ProjectOrganizer/raw/main/screenshots/dashboard.png)

The dashboard provides visual analytics of your projects:

1. Click the "Dashboard" button to open it
2. View summary metrics showing project counts by category
3. Explore charts showing:
   - Project distribution by priority
   - Project completion statistics
   - Language distribution
   - Project timeline
4. See recently updated projects and upcoming deadlines
5. Click "Refresh Dashboard" to update the information

## Backup and Restore

### Creating Backups

1. Click "Backup & Restore" button
2. Click "Create Manual Backup" to make a backup of your project data
3. Configure automatic backups if desired:
   - Enable automatic backups
   - Set backup frequency
   - Choose how many backups to keep

### Restoring From Backup

1. Click "Backup & Restore" button
2. Select a backup from the list
3. Click "Restore Selected Backup"
4. Confirm the restoration

### Exporting Backups

1. Click "Backup & Restore" button
2. Select a backup from the list
3. Click "Export Backup"
4. Choose a destination to save the backup file

## Notifications

Project Organizer can remind you about upcoming deadlines:

1. Click the "Notifications" button
2. Enable deadline notifications
3. Configure notification settings:
   - How many days before a deadline to remind you
   - How often to check for deadlines
   - When to show the daily summary
4. Use "Test Notification" to verify your system supports notifications

## Exporting Projects

You can export your projects for reporting or sharing:

1. Click "Export Projects" button
2. Choose an export format:
   - **JSON**: Complete data (can be imported later)
   - **CSV**: Basic data (compatible with spreadsheets)
   - **Text Report**: Human-readable summary
3. Choose where to save the exported file

## Searching and Filtering

In addition to smart filters, you can use the search bar and dropdown filters:

1. Use the search bar to find projects by name or description
2. Use the "Filter by" dropdown to filter by priority
3. Use the "Language" dropdown to filter by programming language
4. Use the "Sort by" dropdown to change the order of projects

## Additional Tips

- **Priority Color Coding**: Projects are color-coded by priority (red for high, orange for medium, green for low)
- **Deadline Highlighting**: Approaching and overdue deadlines are highlighted
- **Completion Progress**: The completion percentage is shown with a visual progress bar

## Troubleshooting

### Data Not Saving

- Check that you have write permissions for the application folder
- Try running the application as administrator
- Verify there's enough disk space

### Notifications Not Working

- Check if system tray is supported by your desktop environment
- Ensure your OS allows notifications from applications
- Try the "Test Notification" button in notification settings

### UI Display Issues

- Make sure your display scaling is set to 100%
- Try resizing the window if some elements are cut off
- Verify you're using the latest version of the application

## Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the [GitHub Issues](https://github.com/faridfgx/ProjectOrganizer/issues) for known problems
2. Submit a new issue if your problem hasn't been reported
3. Include detailed information about your system and the problem you're experiencing