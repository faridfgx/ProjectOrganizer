import os
import shutil
import json
from datetime import datetime
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QFileDialog, QListWidget, 
                            QDialogButtonBox, QCheckBox, QGroupBox, QFormLayout,
                            QSpinBox, QComboBox, QListWidgetItem)
from PyQt5.QtCore import QTimer, QSettings
from PyQt5.QtGui import QFont


class BackupManager:
    """Manages backup operations for the Project Organizer application"""
    
    def __init__(self, main_app):
        """Initialize the backup manager
        
        Args:
            main_app: The main application instance (ProjectOrganizer)
        """
        self.main_app = main_app
        self.data_file = main_app.data_file
        self.backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
        self.settings = QSettings("ProjectOrganizer", "Backup")
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        # Set up automatic backup timer if enabled
        self.setup_auto_backup()
    
    def setup_auto_backup(self):
        """Set up the automatic backup timer based on settings"""
        # Load settings with defaults
        auto_backup_enabled = self.settings.value("auto_backup_enabled", False, type=bool)
        backup_interval = self.settings.value("backup_interval", 60, type=int)  # minutes
        
        if hasattr(self, 'backup_timer'):
            # Stop existing timer if it exists
            self.backup_timer.stop()
        
        if auto_backup_enabled:
            # Create and start timer for automatic backups
            self.backup_timer = QTimer(self.main_app)
            self.backup_timer.timeout.connect(self.create_auto_backup)
            # Convert minutes to milliseconds
            self.backup_timer.start(backup_interval * 60 * 1000)
    
    def create_backup(self, manual=True):
        """Create a backup of the project data
        
        Args:
            manual: Whether this is a manual backup (user-initiated)
            
        Returns:
            tuple: (success, message)
        """
        try:
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_type = "manual" if manual else "auto"
            backup_filename = f"projectdata_backup_{backup_type}_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Check if data file exists
            if not os.path.exists(self.data_file):
                return False, "No data file found to backup."
            
            # Copy the data file
            shutil.copy2(self.data_file, backup_path)
            
            # Clean up old backups if needed
            self.cleanup_old_backups()
            
            return True, f"Backup created successfully: {backup_filename}"
            
        except Exception as e:
            return False, f"Backup failed: {str(e)}"
    
    def create_auto_backup(self):
        """Create an automatic backup (called by timer)"""
        success, message = self.create_backup(manual=False)
        
        # Log the result but don't show message to user
        print(f"Auto backup: {message}")
    
    def restore_backup(self, backup_file):
        """Restore from a backup file
        
        Args:
            backup_file: Path to the backup file
            
        Returns:
            tuple: (success, message)
        """
        try:
            # Verify the backup file is valid JSON
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            # Create backup of current data before restoring
            current_backup_success, _ = self.create_backup(manual=False)
            if not current_backup_success:
                return False, "Could not create safety backup of current data."
            
            # Copy the backup file to the main data file
            shutil.copy2(backup_file, self.data_file)
            
            return True, "Backup restored successfully."
            
        except json.JSONDecodeError:
            return False, "Invalid backup file format."
        except Exception as e:
            return False, f"Restore failed: {str(e)}"
    
    def cleanup_old_backups(self):
        """Remove old backups based on retention settings"""
        max_backups = self.settings.value("max_backups", 10, type=int)
        
        # Get all backup files
        backup_files = []
        for filename in os.listdir(self.backup_dir):
            if filename.startswith("projectdata_backup_"):
                file_path = os.path.join(self.backup_dir, filename)
                backup_files.append((file_path, os.path.getmtime(file_path)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Delete older backups beyond the limit
        if len(backup_files) > max_backups:
            for file_path, _ in backup_files[max_backups:]:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting old backup {file_path}: {e}")
    
    def export_backup(self, backup_file, destination):
        """Export a backup file to an external location
        
        Args:
            backup_file: Path to the backup file
            destination: Destination path
            
        Returns:
            tuple: (success, message)
        """
        try:
            shutil.copy2(backup_file, destination)
            return True, f"Backup exported to {destination}"
        except Exception as e:
            return False, f"Export failed: {str(e)}"


class BackupDialog(QDialog):
    """Dialog for backup and restore operations"""
    
    def __init__(self, parent, backup_manager):
        super().__init__(parent)
        self.parent = parent
        self.backup_manager = backup_manager
        self.settings = backup_manager.settings
        
        self.setWindowTitle("Backup and Restore")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.setup_ui()
        self.load_backups()
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Backup and Restore Projects")
        title.setFont(QFont(self.parent.font_family, 14, QFont.Bold))
        layout.addWidget(title)
        
        # Backup control group
        backup_group = QGroupBox("Backup")
        backup_layout = QVBoxLayout(backup_group)
        
        # Manual backup button
        backup_button = QPushButton("Create Manual Backup")
        backup_button.setIcon(self.parent.get_icon("backup"))
        backup_button.clicked.connect(self.create_backup)
        backup_layout.addWidget(backup_button)
        
        # Auto backup settings
        auto_backup_group = QGroupBox("Automatic Backup Settings")
        auto_backup_layout = QFormLayout(auto_backup_group)
        
        self.auto_backup_checkbox = QCheckBox("Enable automatic backups")
        auto_backup_enabled = self.settings.value("auto_backup_enabled", False, type=bool)
        self.auto_backup_checkbox.setChecked(auto_backup_enabled)
        self.auto_backup_checkbox.stateChanged.connect(self.save_backup_settings)
        auto_backup_layout.addRow(self.auto_backup_checkbox)
        
        # Interval setting
        interval_layout = QHBoxLayout()
        backup_interval = self.settings.value("backup_interval", 60, type=int)
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(5)
        self.interval_spin.setMaximum(1440)  # 24 hours in minutes
        self.interval_spin.setValue(backup_interval)
        self.interval_spin.valueChanged.connect(self.save_backup_settings)
        interval_layout.addWidget(self.interval_spin)
        
        interval_label = QLabel("minutes")
        interval_layout.addWidget(interval_label)
        interval_layout.addStretch()
        
        auto_backup_layout.addRow("Backup every:", interval_layout)
        
        # Retention setting
        max_backups = self.settings.value("max_backups", 10, type=int)
        self.retention_spin = QSpinBox()
        self.retention_spin.setMinimum(1)
        self.retention_spin.setMaximum(100)
        self.retention_spin.setValue(max_backups)
        self.retention_spin.valueChanged.connect(self.save_backup_settings)
        auto_backup_layout.addRow("Keep last:", self.retention_spin)
        
        backup_layout.addWidget(auto_backup_group)
        layout.addWidget(backup_group)
        
        # Available backups group
        restore_group = QGroupBox("Available Backups")
        restore_layout = QVBoxLayout(restore_group)
        
        # Backup list
        self.backup_list = QListWidget()
        self.backup_list.setAlternatingRowColors(True)
        restore_layout.addWidget(self.backup_list)
        
        # Restore controls
        restore_controls = QHBoxLayout()
        
        restore_button = QPushButton("Restore Selected Backup")
        restore_button.setIcon(self.parent.get_icon("restore"))
        restore_button.clicked.connect(self.restore_backup)
        restore_controls.addWidget(restore_button)
        
        export_button = QPushButton("Export Backup")
        export_button.setIcon(self.parent.get_icon("export"))
        export_button.clicked.connect(self.export_backup)
        restore_controls.addWidget(export_button)
        
        delete_button = QPushButton("Delete Backup")
        delete_button.setIcon(self.parent.get_icon("delete"))
        delete_button.clicked.connect(self.delete_backup)
        restore_controls.addWidget(delete_button)
        
        restore_layout.addLayout(restore_controls)
        layout.addWidget(restore_group)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_backups(self):
        """Load and display available backups"""
        self.backup_list.clear()
        
        # Get all backup files
        backup_files = []
        for filename in os.listdir(self.backup_manager.backup_dir):
            if filename.startswith("projectdata_backup_"):
                file_path = os.path.join(self.backup_manager.backup_dir, filename)
                backup_files.append((filename, file_path, os.path.getmtime(file_path)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[2], reverse=True)
        
        # Add to list
        for filename, file_path, mtime in backup_files:
            # Format the date
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            # Determine if auto or manual backup
            backup_type = "Auto" if "auto" in filename else "Manual"
            
            # Format display text
            display_text = f"{date_str} ({backup_type})"
            
            item = QListWidgetItem(display_text)
            item.setData(100, file_path)  # Store file path as data
            self.backup_list.addItem(item)
    
    def create_backup(self):
        """Create a manual backup"""
        success, message = self.backup_manager.create_backup()
        
        if success:
            QMessageBox.information(self, "Backup", message)
            self.load_backups()
        else:
            QMessageBox.warning(self, "Backup Failed", message)
    
    def restore_backup(self):
        """Restore the selected backup"""
        selected_items = self.backup_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Restore", "Please select a backup to restore.")
            return
        
        backup_file = selected_items[0].data(100)
        display_text = selected_items[0].text()
        
        # Confirm restore
        confirm = QMessageBox.question(
            self, "Confirm Restore",
            f"Are you sure you want to restore the backup from {display_text}?\n\n"
            "This will replace your current project data.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            success, message = self.backup_manager.restore_backup(backup_file)
            
            if success:
                QMessageBox.information(self, "Restore Successful", message)
                # Reload data in the main application
                self.parent.load_data()
                self.parent.update_project_list()
                self.accept()  # Close dialog
            else:
                QMessageBox.warning(self, "Restore Failed", message)
    
    def export_backup(self):
        """Export the selected backup to an external location"""
        selected_items = self.backup_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Export", "Please select a backup to export.")
            return
        
        backup_file = selected_items[0].data(100)
        backup_filename = os.path.basename(backup_file)
        
        # Get destination path
        destination, _ = QFileDialog.getSaveFileName(
            self, "Export Backup", backup_filename, "JSON Files (*.json)"
        )
        
        if destination:
            success, message = self.backup_manager.export_backup(backup_file, destination)
            
            if success:
                QMessageBox.information(self, "Export Successful", message)
            else:
                QMessageBox.warning(self, "Export Failed", message)
    
    def delete_backup(self):
        """Delete the selected backup"""
        selected_items = self.backup_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Delete", "Please select a backup to delete.")
            return
        
        backup_file = selected_items[0].data(100)
        display_text = selected_items[0].text()
        
        # Confirm delete
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the backup from {display_text}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                os.remove(backup_file)
                QMessageBox.information(self, "Delete Successful", "Backup deleted successfully.")
                self.load_backups()
            except Exception as e:
                QMessageBox.warning(self, "Delete Failed", f"Error deleting backup: {str(e)}")
    
    def save_backup_settings(self):
        """Save backup settings to QSettings"""
        auto_backup_enabled = self.auto_backup_checkbox.isChecked()
        backup_interval = self.interval_spin.value()
        max_backups = self.retention_spin.value()
        
        self.settings.setValue("auto_backup_enabled", auto_backup_enabled)
        self.settings.setValue("backup_interval", backup_interval)
        self.settings.setValue("max_backups", max_backups)
        
        # Update backup timer
        self.backup_manager.setup_auto_backup()


# Integration with main application
def add_backup_functionality(project_organizer):
    """Add backup functionality to the project organizer
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Add backup manager to the main application
    project_organizer.backup_manager = BackupManager(project_organizer)
    
    # Add an icon accessor method if not already present
    if not hasattr(project_organizer, 'get_icon'):
        def get_icon(self, icon_name):
            """Get an icon by name
            
            Args:
                icon_name: Name of the icon
                
            Returns:
                QIcon: The icon
            """
            from PyQt5.QtGui import QIcon
            return QIcon.fromTheme(icon_name)
        
        project_organizer.get_icon = get_icon.__get__(project_organizer)
    
    # Add font attributes if not already present
    if not hasattr(project_organizer, 'font_large'):
        from PyQt5.QtGui import QFont
        project_organizer.font_large = QFont(project_organizer.font_family, 12, QFont.Bold)
    
    # Add backup action to the menu or toolbar
    def open_backup_dialog(self):
        """Open the backup dialog"""
        dialog = BackupDialog(self, self.backup_manager)
        dialog.exec_()
    
    project_organizer.open_backup_dialog = open_backup_dialog.__get__(project_organizer)
    
    # Add to action buttons layout
    export_button_index = None
    for i in range(project_organizer.centralWidget().layout().count()):
        item = project_organizer.centralWidget().layout().itemAt(i)
        if isinstance(item, QHBoxLayout):
            # This is likely the action buttons layout
            backup_button = QPushButton("Backup & Restore")
            backup_button.setIcon(project_organizer.get_icon("drive-harddisk"))
            backup_button.clicked.connect(project_organizer.open_backup_dialog)
            
            # Insert before the Export button if found
            for j in range(item.count()):
                widget = item.itemAt(j).widget()
                if isinstance(widget, QPushButton) and widget.text() == "Export Projects":
                    export_button_index = j
                    break
            
            if export_button_index is not None:
                item.insertWidget(export_button_index, backup_button)
            else:
                # Add after spacer if export button not found
                item.addWidget(backup_button)
            
            break
    
    # Modify save_data to create auto backup when data changes
    # Store the original save_data function
    original_save_data = project_organizer.save_data

    # Create a new save_data function that calls the original and adds backup functionality
    def save_data_with_backup():
        """Save data and create automatic backup if needed"""
        # Call original save method
        original_save_data()
        
        # Create auto backup if enabled
        if project_organizer.backup_manager.settings.value("auto_backup_enabled", False, type=bool):
            # Only backup on significant changes (determined by number of projects change)
            project_count_key = "last_project_count"
            last_count = project_organizer.backup_manager.settings.value(project_count_key, 0, type=int)
            current_count = len(project_organizer.projects)
            
            if current_count != last_count:
                project_organizer.backup_manager.create_auto_backup()
                project_organizer.backup_manager.settings.setValue(project_count_key, current_count)

    # Assign the new function to the project_organizer instance
    project_organizer.save_data = save_data_with_backup