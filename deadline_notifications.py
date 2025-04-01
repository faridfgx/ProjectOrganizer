from PyQt5.QtWidgets import (QSystemTrayIcon, QMenu, QAction, QDialog, 
                             QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
                             QListWidgetItem, QPushButton, QCheckBox, QGroupBox,
                             QFormLayout, QSpinBox, QTimeEdit, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QSettings, QTime, QDateTime
from PyQt5.QtGui import QIcon, QFont, QColor
from datetime import datetime, timedelta


class NotificationManager:
    """Manages deadline notifications for the Project Organizer"""
    
    def __init__(self, main_app):
        """Initialize the notification manager
        
        Args:
            main_app: The main application instance (ProjectOrganizer)
        """
        self.main_app = main_app
        self.settings = QSettings("ProjectOrganizer", "Notifications")
        
        # Setup system tray icon if supported
        self.setup_tray_icon()
        
        # Load notification settings
        self.enabled = self.settings.value("notifications_enabled", True, type=bool)
        self.remind_days_before = self.settings.value("remind_days_before", 1, type=int)
        self.check_interval = self.settings.value("check_interval", 60, type=int)  # minutes
        self.notify_time = self.settings.value("notify_time", "09:00", type=str)
        self.daily_summary = self.settings.value("daily_summary", True, type=bool)
        
        # Track shown notifications to avoid duplicates
        self.shown_notifications = set()
        
        # Create notification timer
        self.notification_timer = QTimer(main_app)
        self.notification_timer.timeout.connect(self.check_notifications)
        
        # Check if notifications are enabled
        if self.enabled:
            # Start the timer
            self.notification_timer.start(self.check_interval * 60 * 1000)  # Convert to milliseconds
            
            # Perform an initial check
            QTimer.singleShot(5000, self.check_notifications)
    
    def setup_tray_icon(self):
        """Set up the system tray icon if supported"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self.main_app)
            self.tray_icon.setIcon(QIcon.fromTheme("appointment-soon", QIcon("logopo.png")))  # Change from "Porgat.png" to "logopo.png"
            self.tray_icon.setToolTip("Project Organizer")
            
            # Create tray menu
            tray_menu = QMenu()
            
            # Add actions
            open_action = QAction("Open Project Organizer", self.tray_icon)
            open_action.triggered.connect(self.main_app.show)
            tray_menu.addAction(open_action)
            
            tray_menu.addSeparator()
            
            # Add pending deadlines section if notifications are enabled
            self.pending_menu = QMenu("Pending Deadlines")
            self.pending_menu.addAction("No pending deadlines")
            tray_menu.addMenu(self.pending_menu)
            
            tray_menu.addSeparator()
            
            # Notification settings
            settings_action = QAction("Notification Settings", self.tray_icon)
            settings_action.triggered.connect(self.show_notification_settings)
            tray_menu.addAction(settings_action)
            
            # Exit action
            exit_action = QAction("Exit", self.tray_icon)
            exit_action.triggered.connect(self.main_app.close)
            tray_menu.addAction(exit_action)
            
            # Set the menu
            self.tray_icon.setContextMenu(tray_menu)
            
            # Show the icon
            self.tray_icon.show()
            
            # Connect tray icon signals
            self.tray_icon.activated.connect(self.tray_icon_activated)
        else:
            self.tray_icon = None
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation
        
        Args:
            reason: Activation reason
        """
        if reason == QSystemTrayIcon.DoubleClick:
            # Show the main window
            self.main_app.show()
            self.main_app.activateWindow()
    
    def check_notifications(self):
        """Check for deadline notifications"""
        if not self.enabled:
            return
        
        # Get current date
        current_date = datetime.now().date()
        
        # Check if we should show daily summary
        current_time = datetime.now().time()
        notify_time = datetime.strptime(self.notify_time, "%H:%M").time()
        
        if self.daily_summary and current_time.hour == notify_time.hour and current_time.minute == notify_time.minute:
            self.show_daily_summary()
        
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
        
        # Create notifications for each project
        for project, days_left in projects_to_notify:
            self.show_deadline_notification(project, days_left)
        
        # Update tray menu if available
        self.update_tray_menu()
    
    def show_deadline_notification(self, project, days_left):
        """Show a notification for an upcoming deadline
        
        Args:
            project: Project data
            days_left: Days left until deadline
        """
        if not self.tray_icon:
            return
        
        # Create notification message
        if days_left == 0:
            message = f"Project '{project['name']}' is due today!"
            title = "Project Due Today"
        else:
            message = f"Project '{project['name']}' is due in {days_left} day{'s' if days_left > 1 else ''}!"
            title = "Upcoming Project Deadline"
        
        # Add priority information
        if project["priority"] == "High Priority":
            message += "\nThis is a high priority project!"
        
        # Show notification
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Information,
            5000  # Display for 5 seconds
        )
    
    def show_daily_summary(self):
        """Show a daily summary of upcoming deadlines"""
        if not self.tray_icon:
            return
        
        # Get current date
        current_date = datetime.now().date()
        
        # Collect upcoming deadlines
        upcoming_deadlines = []
        
        for project in self.main_app.projects:
            # Skip if no deadline or already completed
            if not project.get("deadline") or int(project.get("completion", 0)) == 100:
                continue
            
            try:
                deadline = datetime.strptime(project["deadline"], "%Y-%m-%d").date()
                days_left = (deadline - current_date).days
                
                # Include deadlines within the next 7 days
                if 0 <= days_left <= 7:
                    upcoming_deadlines.append((project, days_left))
            except ValueError:
                # Skip invalid dates
                continue
        
        # Create notification message
        if not upcoming_deadlines:
            message = "No upcoming deadlines for the next week."
            title = "Daily Project Summary"
        else:
            title = "Upcoming Project Deadlines"
            message = f"You have {len(upcoming_deadlines)} project{'s' if len(upcoming_deadlines) > 1 else ''} due soon:\n\n"
            
            # Sort by days left
            upcoming_deadlines.sort(key=lambda x: x[1])
            
            for project, days_left in upcoming_deadlines:
                if days_left == 0:
                    message += f"• {project['name']} - Due TODAY"
                else:
                    message += f"• {project['name']} - Due in {days_left} day{'s' if days_left > 1 else ''}"
                
                # Add priority information
                if project["priority"] == "High Priority":
                    message += " (High Priority)"
                
                message += "\n"
        
        # Show notification
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Information,
            10000  # Display for 10 seconds
        )
    
    def update_tray_menu(self):
        """Update the tray menu with pending deadlines"""
        if not self.tray_icon:
            return
        
        # Clear the pending menu
        self.pending_menu.clear()
        
        # Get current date
        current_date = datetime.now().date()
        
        # Collect upcoming deadlines
        upcoming_deadlines = []
        
        for project in self.main_app.projects:
            # Skip if no deadline or already completed
            if not project.get("deadline") or int(project.get("completion", 0)) == 100:
                continue
            
            try:
                deadline = datetime.strptime(project["deadline"], "%Y-%m-%d").date()
                days_left = (deadline - current_date).days
                
                # Include deadlines within the next 7 days
                if 0 <= days_left <= 7:
                    upcoming_deadlines.append((project, days_left))
            except ValueError:
                # Skip invalid dates
                continue
        
        # Add deadlines to menu
        if not upcoming_deadlines:
            no_deadlines_action = QAction("No pending deadlines", self.tray_icon)
            no_deadlines_action.setEnabled(False)
            self.pending_menu.addAction(no_deadlines_action)
        else:
            # Sort by days left
            upcoming_deadlines.sort(key=lambda x: x[1])
            
            for project, days_left in upcoming_deadlines:
                if days_left == 0:
                    action_text = f"{project['name']} - Due TODAY"
                else:
                    action_text = f"{project['name']} - Due in {days_left} day{'s' if days_left > 1 else ''}"
                
                # Create action
                action = QAction(action_text, self.tray_icon)
                action.triggered.connect(lambda checked=False, p=project: self.open_project(p))
                
                # Set icon based on priority
                if project["priority"] == "High Priority":
                    action.setIcon(QIcon.fromTheme("emblem-important"))
                
                self.pending_menu.addAction(action)
    
    def open_project(self, project):
        """Open the main window and select the specified project
        
        Args:
            project: Project data
        """
        # Show the main window
        self.main_app.show()
        self.main_app.activateWindow()
        
        # Find and select the project in the table
        for row in range(self.main_app.project_table.rowCount()):
            project_name = self.main_app.project_table.item(row, 0).data(Qt.UserRole)
            if project_name == project["name"]:
                self.main_app.project_table.selectRow(row)
                break
    
    def show_notification_settings(self):
        """Show the notification settings dialog"""
        dialog = NotificationSettingsDialog(self.main_app, self)
        if dialog.exec_() == QDialog.Accepted:
            # Apply new settings
            self.enabled = dialog.enabled_checkbox.isChecked()
            self.remind_days_before = dialog.days_before_spin.value()
            self.check_interval = dialog.interval_spin.value()
            self.notify_time = dialog.notify_time_edit.time().toString("HH:mm")
            self.daily_summary = dialog.daily_summary_checkbox.isChecked()
            
            # Save settings
            self.settings.setValue("notifications_enabled", self.enabled)
            self.settings.setValue("remind_days_before", self.remind_days_before)
            self.settings.setValue("check_interval", self.check_interval)
            self.settings.setValue("notify_time", self.notify_time)
            self.settings.setValue("daily_summary", self.daily_summary)
            
            # Update timer
            if self.enabled:
                self.notification_timer.start(self.check_interval * 60 * 1000)
                # Run initial check
                QTimer.singleShot(1000, self.check_notifications)
            else:
                self.notification_timer.stop()
    
    def reset_notification_state(self):
        """Reset the notification state to show notifications again"""
        self.shown_notifications.clear()


class NotificationSettingsDialog(QDialog):
    """Dialog for notification settings"""
    
    def __init__(self, parent, notification_manager):
        super().__init__(parent)
        self.parent = parent
        self.notification_manager = notification_manager
        
        self.setWindowTitle("Notification Settings")
        self.setMinimumWidth(400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Enable notifications checkbox
        self.enabled_checkbox = QCheckBox("Enable deadline notifications")
        self.enabled_checkbox.setChecked(self.notification_manager.enabled)
        self.enabled_checkbox.stateChanged.connect(self.toggle_notification_settings)
        layout.addWidget(self.enabled_checkbox)
        
        # Settings group
        self.settings_group = QGroupBox("Notification Settings")
        self.settings_layout = QFormLayout(self.settings_group)
        
        # Days before deadline
        self.days_before_spin = QSpinBox()
        self.days_before_spin.setMinimum(0)
        self.days_before_spin.setMaximum(14)
        self.days_before_spin.setValue(self.notification_manager.remind_days_before)
        self.days_before_spin.setSuffix(" day(s)")
        self.settings_layout.addRow("Remind me", self.days_before_spin)
        
        # Check interval
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(15)
        self.interval_spin.setMaximum(1440)  # 24 hours in minutes
        self.interval_spin.setValue(self.notification_manager.check_interval)
        self.interval_spin.setSuffix(" minutes")
        self.settings_layout.addRow("Check every", self.interval_spin)
        
        # Daily notification time
        self.notify_time_edit = QTimeEdit()
        self.notify_time_edit.setDisplayFormat("HH:mm")
        self.notify_time_edit.setTime(QTime.fromString(self.notification_manager.notify_time, "HH:mm"))
        self.settings_layout.addRow("Daily notification time", self.notify_time_edit)
        
        # Daily summary
        self.daily_summary_checkbox = QCheckBox("Show daily summary of upcoming deadlines")
        self.daily_summary_checkbox.setChecked(self.notification_manager.daily_summary)
        self.settings_layout.addRow("", self.daily_summary_checkbox)
        
        layout.addWidget(self.settings_group)
        
        # Test notification button
        test_button = QPushButton("Test Notification")
        test_button.clicked.connect(self.test_notification)
        layout.addWidget(test_button)
        
        # Dialog buttons
        button_box = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_box.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(cancel_button)
        
        reset_button = QPushButton("Reset Notification State")
        reset_button.clicked.connect(self.reset_notification_state)
        button_box.addWidget(reset_button)
        
        layout.addLayout(button_box)
        
        # Initialize UI state
        self.toggle_notification_settings(self.enabled_checkbox.isChecked())
    
    def toggle_notification_settings(self, state):
        """Toggle notification settings based on enabled state
        
        Args:
            state: Qt.Checked or Qt.Unchecked
        """
        self.settings_group.setEnabled(state == Qt.Checked)
    
    def test_notification(self):
        """Send a test notification"""
        if QSystemTrayIcon.isSystemTrayAvailable() and self.notification_manager.tray_icon:
            self.notification_manager.tray_icon.showMessage(
                "Test Notification",
                "This is a test notification from Project Organizer.",
                QSystemTrayIcon.Information,
                3000  # Display for 3 seconds
            )
        else:
            QMessageBox.information(
                self,
                "System Tray Not Available",
                "The system tray is not available on your system. Notifications cannot be shown."
            )
    
    def reset_notification_state(self):
        """Reset the notification state to show notifications again"""
        self.notification_manager.reset_notification_state()
        QMessageBox.information(
            self,
            "Notification State Reset",
            "The notification state has been reset. Notifications will be shown again for current deadlines."
        )


# Integration with main application
def add_deadline_notifications(project_organizer):
    """Add deadline notifications to the project organizer
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Add notification manager to the main application
    project_organizer.notification_manager = NotificationManager(project_organizer)
    
    # Add notification settings to the menu bar if it exists
    if hasattr(project_organizer, 'menuBar') and project_organizer.menuBar():
        menu_bar = project_organizer.menuBar()
        
        # Find the View menu
        view_menu = None
        for action in menu_bar.actions():
            if action.text() == "&View":
                view_menu = action.menu()
                break
        
        # Add notification settings action to the View menu
        if view_menu:
            view_menu.addSeparator()
            notification_action = QAction("&Notification Settings", project_organizer)
            notification_action.triggered.connect(project_organizer.notification_manager.show_notification_settings)
            view_menu.addAction(notification_action)
    
    # Add notification settings button to UI
    for i in range(project_organizer.centralWidget().layout().count()):
        item = project_organizer.centralWidget().layout().itemAt(i)
        if isinstance(item, QHBoxLayout):
            # This is likely the action buttons layout
            notification_button = QPushButton("Notifications")
            notification_button.setIcon(QIcon.fromTheme("appointment-soon"))
            notification_button.clicked.connect(project_organizer.notification_manager.show_notification_settings)
            
            # Add button at the end
            item.addWidget(notification_button)
            break