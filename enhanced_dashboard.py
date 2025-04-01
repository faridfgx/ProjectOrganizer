from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTabWidget, QSplitter, QFrame, QScrollArea,
                             QPushButton, QDialog, QListWidget, QGridLayout,
                             QSizePolicy, QSpacerItem, QListWidgetItem)
from PyQt5.QtCore import Qt, QSize, QDate, QRectF, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter, QPen, QBrush, QPainterPath
from PyQt5.QtChart import (QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, 
                          QBarSet, QBarCategoryAxis, QValueAxis, QLineSeries)
import math
from datetime import datetime, timedelta
import collections


class MetricCard(QFrame):
    """Card displaying a single metric optimized for dark theme"""
    
    def __init__(self, parent, title, icon_name, color, data_func):
        super().__init__(parent)
        self.parent = parent
        self.title = title
        self.icon_name = icon_name
        self.color = color
        self.data_func = data_func
        
        self.setup_ui()
        self.update_value()
    
    def setup_ui(self):
        """Set up the card UI"""
        # Set frame properties
        self.setObjectName("card")
        self.setMinimumHeight(110)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Add subtle glow effect with brighter borders
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {self.parent.parent.colors['card']};
                border: 1px solid {self.color};
                border-radius: 8px;
            }}
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        
        # Title
        title_layout = QHBoxLayout()
        
        icon = QIcon.fromTheme(self.icon_name)
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(20, 20))
        title_layout.addWidget(icon_label)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"color: {self.color}; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        layout.addLayout(title_layout)
        
        # Value
        self.value_label = QLabel("0")
        self.value_label.setFont(QFont(self.parent.parent.font_family, 28, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(f"color: {self.color};")
        layout.addWidget(self.value_label)
    
    def update_value(self):
        """Update the metric value"""
        value = self.data_func()
        self.value_label.setText(str(value))


class DashboardWidget(QWidget):
    """Widget for displaying project statistics and charts optimized for dark theme"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Title
        title_layout = QHBoxLayout()
        title = QLabel("Project Dashboard")
        title.setFont(QFont(self.parent.font_family, 18, QFont.Bold))
        title.setStyleSheet(f"color: {self.parent.colors['text']};")
        title_layout.addWidget(title)
        
        # Refresh button
        refresh_button = QPushButton("Refresh Dashboard")
        refresh_button.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_button.clicked.connect(self.refresh_dashboard)
        refresh_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.parent.colors['primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.parent.colors['primary_dark']};
            }}
        """)
        title_layout.addWidget(refresh_button, 0, Qt.AlignRight)
        
        layout.addLayout(title_layout)
        
        # Scrollable area for dashboard content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Create dashboard content
        dashboard_content = QWidget()
        self.dashboard_layout = QVBoxLayout(dashboard_content)
        self.dashboard_layout.setSpacing(20)
        
        # Create dashboard sections
        self.create_summary_section()
        self.create_charts_section()
        self.create_status_section()
        
        # Add empty QLabel to provide padding at bottom
        padding = QLabel()
        padding.setMinimumHeight(20)
        self.dashboard_layout.addWidget(padding)
        
        # Set the dashboard content as the scroll area widget
        scroll_area.setWidget(dashboard_content)
        layout.addWidget(scroll_area)
    
    def create_summary_section(self):
        """Create the summary section with key metrics"""
        # Section title
        section_title = QLabel("Summary")
        section_title.setFont(QFont(self.parent.font_family, 16, QFont.Bold))
        self.dashboard_layout.addWidget(section_title)
        
        # Summary cards layout
        summary_layout = QGridLayout()
        summary_layout.setSpacing(16)
        
        # Create metric cards with enhanced colors for dark theme
        metrics = [
            {"title": "Total Projects", "icon": "folder", "color": "#2196F3", "data_func": self.get_total_projects},
            {"title": "Completed", "icon": "task-complete", "color": "#66BB6A", "data_func": self.get_completed_projects},
            {"title": "High Priority", "icon": "emblem-important", "color": "#FF5252", "data_func": self.get_high_priority_projects},
            {"title": "Due This Week", "icon": "appointment-soon", "color": "#FFA726", "data_func": self.get_due_this_week},
            {"title": "Overdue", "icon": "appointment-missed", "color": "#FF4081", "data_func": self.get_overdue_projects},
            {"title": "Stalled", "icon": "media-playback-pause", "color": "#9575CD", "data_func": self.get_stalled_projects}
        ]
        
        # Add metric cards to the grid (3 columns)
        for i, metric in enumerate(metrics):
            card = MetricCard(self, metric["title"], metric["icon"], metric["color"], metric["data_func"])
            summary_layout.addWidget(card, i // 3, i % 3)
        
        self.dashboard_layout.addLayout(summary_layout)
    
    def create_charts_section(self):
        """Create the charts section"""
        # Section title
        section_title = QLabel("Charts")
        section_title.setFont(QFont(self.parent.font_family, 16, QFont.Bold))
        self.dashboard_layout.addWidget(section_title)
        
        # Create tabs for different charts
        charts_tabs = QTabWidget()
        charts_tabs.setDocumentMode(True)
        
        # Set tab style for dark theme
        charts_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {self.parent.colors['border']};
                border-radius: 8px;
                background-color: {self.parent.colors['card']};
            }}
            QTabBar::tab {{
                background-color: {self.parent.colors['background']};
                border: 1px solid {self.parent.colors['border']};
                border-bottom-color: {self.parent.colors['border']};
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                color: {self.parent.colors['text']};
                min-width: 80px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.parent.colors['primary']};
                color: white;
                border-bottom-color: {self.parent.colors['primary']};
            }}
        """)
        
        # Create chart views
        self.distribution_chart = self.create_distribution_chart()
        self.progress_chart = self.create_progress_chart()
        self.languages_chart = self.create_languages_chart()
        self.timeline_chart = self.create_timeline_chart()
        
        # Add charts to tabs
        charts_tabs.addTab(self.distribution_chart, "Project Distribution")
        charts_tabs.addTab(self.progress_chart, "Progress")
        charts_tabs.addTab(self.languages_chart, "Languages")
        charts_tabs.addTab(self.timeline_chart, "Timeline")
        
        # Set a fixed height for the charts section
        charts_tabs.setFixedHeight(350)
        
        self.dashboard_layout.addWidget(charts_tabs)
    
    def create_status_section(self):
        """Create the status section"""
        # Section title
        section_title = QLabel("Project Status")
        section_title.setFont(QFont(self.parent.font_family, 16, QFont.Bold))
        self.dashboard_layout.addWidget(section_title)
        
        # Status layout
        status_layout = QHBoxLayout()
        
        # Recent projects
        recent_card = QFrame()
        recent_card.setObjectName("card")
        recent_card.setMinimumWidth(300)
        recent_card.setStyleSheet(f"""
            QFrame#card {{
                background-color: {self.parent.colors['card']};
                border: 1px solid {self.parent.colors['border']};
                border-radius: 8px;
            }}
        """)
        recent_layout = QVBoxLayout(recent_card)
        
        recent_title = QLabel("Recently Updated")
        recent_title.setFont(QFont(self.parent.font_family, 14, QFont.Bold))
        recent_layout.addWidget(recent_title)
        
        self.recent_list = QListWidget()
        self.recent_list.setAlternatingRowColors(True)
        self.recent_list.setMaximumHeight(200)
        self.recent_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {self.parent.colors['card']};
                border: 1px solid {self.parent.colors['border']};
                color: {self.parent.colors['text']};
                alternate-background-color: {self.parent.colors['background']};
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {self.parent.colors['primary']};
                color: white;
            }}
        """)
        recent_layout.addWidget(self.recent_list)
        
        status_layout.addWidget(recent_card)
        
        # Upcoming deadlines
        deadline_card = QFrame()
        deadline_card.setObjectName("card")
        deadline_card.setMinimumWidth(300)
        deadline_card.setStyleSheet(f"""
            QFrame#card {{
                background-color: {self.parent.colors['card']};
                border: 1px solid {self.parent.colors['border']};
                border-radius: 8px;
            }}
        """)
        deadline_layout = QVBoxLayout(deadline_card)
        
        deadline_title = QLabel("Upcoming Deadlines")
        deadline_title.setFont(QFont(self.parent.font_family, 14, QFont.Bold))
        deadline_layout.addWidget(deadline_title)
        
        self.deadline_list = QListWidget()
        self.deadline_list.setAlternatingRowColors(True)
        self.deadline_list.setMaximumHeight(200)
        self.deadline_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {self.parent.colors['card']};
                border: 1px solid {self.parent.colors['border']};
                color: {self.parent.colors['text']};
                alternate-background-color: {self.parent.colors['background']};
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {self.parent.colors['primary']};
                color: white;
            }}
        """)
        deadline_layout.addWidget(self.deadline_list)
        
        status_layout.addWidget(deadline_card)
        
        self.dashboard_layout.addLayout(status_layout)
    
    def create_distribution_chart(self):
        """Create a pie chart showing project distribution by priority"""
        # Create the chart with dark theme styling
        chart = QChart()
        chart.setTitle("Projects by Priority")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Configure chart for dark theme
        chart.setBackgroundVisible(False)
        chart.setBackgroundBrush(QBrush(QColor(self.parent.colors['card'])))
        chart.setTitleBrush(QBrush(QColor(self.parent.colors['text'])))
        chart.setTitleFont(QFont(self.parent.font_family, 12, QFont.Bold))
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet(f"background-color: {self.parent.colors['card']};")
        
        return chart_view

    def create_progress_chart(self):
        """Create a chart showing project completion progress"""
        # Create the chart with dark theme styling
        chart = QChart()
        chart.setTitle("Project Completion")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Configure chart for dark theme
        chart.setBackgroundVisible(False)
        chart.setBackgroundBrush(QBrush(QColor(self.parent.colors['card'])))
        chart.setTitleBrush(QBrush(QColor(self.parent.colors['text'])))
        chart.setTitleFont(QFont(self.parent.font_family, 12, QFont.Bold))
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet(f"background-color: {self.parent.colors['card']};")
        
        return chart_view

    def create_languages_chart(self):
        """Create a chart showing project distribution by language"""
        # Create the chart with dark theme styling
        chart = QChart()
        chart.setTitle("Projects by Language")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Configure chart for dark theme
        chart.setBackgroundVisible(False)
        chart.setBackgroundBrush(QBrush(QColor(self.parent.colors['card'])))
        chart.setTitleBrush(QBrush(QColor(self.parent.colors['text'])))
        chart.setTitleFont(QFont(self.parent.font_family, 12, QFont.Bold))
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet(f"background-color: {self.parent.colors['card']};")
        
        return chart_view

    def create_timeline_chart(self):
        """Create a timeline chart showing project deadlines"""
        # Create the chart with dark theme styling
        chart = QChart()
        chart.setTitle("Project Timeline")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Configure chart for dark theme
        chart.setBackgroundVisible(False)
        chart.setBackgroundBrush(QBrush(QColor(self.parent.colors['card'])))
        chart.setTitleBrush(QBrush(QColor(self.parent.colors['text'])))
        chart.setTitleFont(QFont(self.parent.font_family, 12, QFont.Bold))
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet(f"background-color: {self.parent.colors['card']};")
        
        return chart_view
    
    def refresh_dashboard(self):
        """Refresh all dashboard data and charts"""
        # Update summary section
        for i in range(self.dashboard_layout.count()):
            item = self.dashboard_layout.itemAt(i)
            if isinstance(item, QGridLayout):
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if isinstance(widget, MetricCard):
                        widget.update_value()
        
        # Completely recreate all charts instead of just updating them
        self.recreate_all_charts()
        
        # Update status section
        self.update_recent_list()
        self.update_deadline_list()

    def recreate_all_charts(self):
        """Recreate all chart views from scratch to prevent stacking"""
        # Get the charts tabs widget
        charts_tabs = None
        for i in range(self.dashboard_layout.count()):
            item = self.dashboard_layout.itemAt(i)
            if isinstance(item.widget(), QTabWidget):
                charts_tabs = item.widget()
                break
        
        if not charts_tabs:
            return
        
        # Store the current tab index
        current_tab = charts_tabs.currentIndex()
        
        # Remove all existing tabs
        while charts_tabs.count() > 0:
            charts_tabs.removeTab(0)
        
        # Create new chart views
        self.distribution_chart = self.create_distribution_chart()
        self.progress_chart = self.create_progress_chart()
        self.languages_chart = self.create_languages_chart()
        self.timeline_chart = self.create_timeline_chart()
        
        # Add charts to tabs
        charts_tabs.addTab(self.distribution_chart, "Project Distribution")
        charts_tabs.addTab(self.progress_chart, "Progress")
        charts_tabs.addTab(self.languages_chart, "Languages")
        charts_tabs.addTab(self.timeline_chart, "Timeline")
        
        # Update each chart with data
        self.update_distribution_chart()
        self.update_progress_chart()
        self.update_languages_chart()
        self.update_timeline_chart()
        
        # Restore the previously selected tab
        if current_tab < charts_tabs.count():
            charts_tabs.setCurrentIndex(current_tab)
        
    def update_distribution_chart(self):
        """Update the distribution chart with current data"""
        # Get priority distribution
        priority_counts = collections.Counter()
        for project in self.parent.projects:
            priority_counts[project["priority"]] += 1
        
        # Check if we have any data
        if not priority_counts:
            # No data, just clear the chart
            chart = self.distribution_chart.chart()
            chart.removeAllSeries()
            return
        
        # Create series
        series = QPieSeries()
        
        # Add slices with colors optimized for dark theme
        colors = {
            "High Priority": QColor("#FF5252"),  # Bright red
            "Medium Priority": QColor("#FFA726"),  # Orange
            "Low Priority": QColor("#66BB6A")     # Green
        }
        
        for priority, count in priority_counts.items():
            slice = series.append(priority, count)
            slice.setBrush(colors.get(priority, QColor("#9E9E9E")))
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor(self.parent.colors['text']))
            # Use LabelOutside position
            slice.setLabelPosition(QPieSlice.LabelOutside)
        
        # Get the chart and update it
        chart = self.distribution_chart.chart()
        chart.removeAllSeries()  # This is important to prevent stacking
        chart.addSeries(series)
        
        # Configure legend for dark theme
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setLabelColor(QColor(self.parent.colors['text']))
        chart.legend().setFont(QFont(self.parent.font_family, 10))
    
    # Fix for update_progress_chart to handle empty data case

    def update_progress_chart(self):
        """Update the progress chart with current data"""
        # Make sure we have projects
        if not self.parent.projects:
            # No data, just clear the chart
            chart = self.progress_chart.chart()
            chart.removeAllSeries()
            return
            
        # Group projects by completion percentage ranges
        completion_ranges = {
            "0%": 0,
            "1-25%": 0,
            "26-50%": 0,
            "51-75%": 0,
            "76-99%": 0,
            "100%": 0
        }
        
        for project in self.parent.projects:
            completion = int(project.get("completion", 0))
            if completion == 0:
                completion_ranges["0%"] += 1
            elif completion <= 25:
                completion_ranges["1-25%"] += 1
            elif completion <= 50:
                completion_ranges["26-50%"] += 1
            elif completion <= 75:
                completion_ranges["51-75%"] += 1
            elif completion < 100:
                completion_ranges["76-99%"] += 1
            else:
                completion_ranges["100%"] += 1
        
        # Create bar set with colors optimized for dark theme
        bar_set = QBarSet("Projects")
        bar_set.setColor(QColor(self.parent.colors['primary']))
        bar_set.setBorderColor(QColor(self.parent.colors['text']))
        bar_set.append([count for count in completion_ranges.values()])
        
        # Create bar series
        series = QBarSeries()
        series.append(bar_set)
        
        # Create axes
        axis_x = QBarCategoryAxis()
        axis_x.append(list(completion_ranges.keys()))
        axis_x.setLabelsColor(QColor(self.parent.colors['text']))
        
        axis_y = QValueAxis()
        axis_y.setRange(0, max(max(completion_ranges.values()), 1))  # Ensure at least 1 
        axis_y.setTickCount(min(max(max(completion_ranges.values()), 1) + 1, 10))
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(QColor(self.parent.colors['text']))
        axis_y.setGridLineColor(QColor(self.parent.colors['border']))
        
        # Get the chart and update it
        chart = self.progress_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(series)
        chart.setAxisX(axis_x, series)
        chart.setAxisY(axis_y, series)
        chart.legend().setVisible(False)
    
    def update_languages_chart(self):
        """Update the languages chart with current data"""
        # Count projects by language
        language_counts = collections.Counter()
        for project in self.parent.projects:
            language_counts[project["language"]] += 1
        
        # Check if we have any data
        if not language_counts:
            # No data, just clear the chart
            chart = self.languages_chart.chart()
            chart.removeAllSeries()
            return
        
        # Sort languages by count (descending)
        sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Limit to top 8 languages for readability
        if len(sorted_languages) > 8:
            other_count = sum(count for lang, count in sorted_languages[7:])
            sorted_languages = sorted_languages[:7] + [("Other", other_count)]
        
        # Create bar set with vibrant colors
        bar_set = QBarSet("Languages")
        bar_set.setColor(QColor("#5C6BC0"))  # Indigo color
        bar_set.setBorderColor(QColor(self.parent.colors['text']))
        bar_set.append([count for _, count in sorted_languages])
        
        # Create bar series
        series = QBarSeries()
        series.append(bar_set)
        
        # Create axes
        axis_x = QBarCategoryAxis()
        axis_x.append([lang for lang, _ in sorted_languages])
        axis_x.setLabelsColor(QColor(self.parent.colors['text']))
        
        axis_y = QValueAxis()
        axis_y.setRange(0, max(language_counts.values()) + 1)
        axis_y.setTickCount(min(max(language_counts.values()) + 1, 10))
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(QColor(self.parent.colors['text']))
        axis_y.setGridLineColor(QColor(self.parent.colors['border']))
        
        # Get the chart and update it
        chart = self.languages_chart.chart()
        chart.removeAllSeries()
        chart.addSeries(series)
        chart.setAxisX(axis_x, series)
        chart.setAxisY(axis_y, series)
        chart.legend().setVisible(False)
    
    # Similar potential issue exists in update_timeline_chart function

    def update_timeline_chart(self):
        """Update the timeline chart with current data"""
        # Get projects with deadlines
        projects_with_deadlines = [p for p in self.parent.projects if p.get("deadline")]
        
        if not projects_with_deadlines:
            # No projects with deadlines
            chart = self.timeline_chart.chart()
            chart.removeAllSeries()
            return
        
        # Sort projects by deadline
        projects_with_deadlines.sort(key=lambda x: x.get("deadline", "9999-99-99"))
        
        # Get date range
        today = datetime.now().date()
        first_deadline = datetime.strptime(projects_with_deadlines[0]["deadline"], "%Y-%m-%d").date()
        last_deadline = datetime.strptime(projects_with_deadlines[-1]["deadline"], "%Y-%m-%d").date()
        
        # Ensure range includes today
        start_date = min(today, first_deadline)
        end_date = max(today, last_deadline)
        
        # Extend range by a few days for readability
        start_date = start_date - timedelta(days=3)
        end_date = end_date + timedelta(days=3)
        
        # Create series for each priority level with dark theme optimized colors
        high_series = QLineSeries()
        high_series.setName("High Priority")
        high_series.setColor(QColor("#FF5252"))  # Bright red
        high_series.setPen(QPen(QColor("#FF5252"), 3))
        
        medium_series = QLineSeries()
        medium_series.setName("Medium Priority")
        medium_series.setColor(QColor("#FFA726"))  # Orange
        medium_series.setPen(QPen(QColor("#FFA726"), 3))
        
        low_series = QLineSeries()
        low_series.setName("Low Priority")
        low_series.setColor(QColor("#66BB6A"))  # Green
        low_series.setPen(QPen(QColor("#66BB6A"), 3))
        
        # Count projects by date and priority
        date_range = (end_date - start_date).days + 1
        
        high_counts = [0] * date_range
        medium_counts = [0] * date_range
        low_counts = [0] * date_range
        
        for project in projects_with_deadlines:
            deadline = datetime.strptime(project["deadline"], "%Y-%m-%d").date()
            day_index = (deadline - start_date).days
            
            if day_index < 0 or day_index >= date_range:
                continue
                
            if project["priority"] == "High Priority":
                high_counts[day_index] += 1
            elif project["priority"] == "Medium Priority":
                medium_counts[day_index] += 1
            else:
                low_counts[day_index] += 1
        
        # Add points to series
        for i in range(date_range):
            high_series.append(i, high_counts[i])
            medium_series.append(i, medium_counts[i])
            low_series.append(i, low_counts[i])
        
        # Create axes optimized for dark theme
        axis_x = QValueAxis()
        axis_x.setRange(0, date_range - 1)
        axis_x.setTickCount(min(date_range, 10))
        
        # Use setLabelFormat instead of setTickLabelFormat
        # Set label format to show nothing for tick marks - we'll create custom labels below
        axis_x.setLabelFormat("")
        axis_x.setLabelsColor(QColor(self.parent.colors['text']))
        axis_x.setGridLineColor(QColor(self.parent.colors['border']))
        
        # Create custom labels for x-axis (dates) using alternative approach
        # We can't use setTickLabelFormat as it doesn't exist
        # Instead we'll add text annotations at specific points
        chart = self.timeline_chart.chart()
        
        # Calculate max count and ensure it's at least 1 to avoid issues with empty data
        max_count = max(max(high_counts or [0]), max(medium_counts or [0]), max(low_counts or [0]), 1)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, max_count + 1)
        axis_y.setTickCount(min(max_count + 1, 10))
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(QColor(self.parent.colors['text']))
        axis_y.setGridLineColor(QColor(self.parent.colors['border']))
        
        # Clear and update the chart
        chart.removeAllSeries()
        
        chart.addSeries(high_series)
        chart.addSeries(medium_series)
        chart.addSeries(low_series)
        
        chart.setAxisX(axis_x, high_series)
        chart.setAxisY(axis_y, high_series)
        chart.setAxisX(axis_x, medium_series)
        chart.setAxisY(axis_y, medium_series)
        chart.setAxisX(axis_x, low_series)
        chart.setAxisY(axis_y, low_series)
        
        # Configure legend for dark theme
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setLabelColor(QColor(self.parent.colors['text']))
        chart.legend().setFont(QFont(self.parent.font_family, 10))
        
        # Add a line for today with modern styling
        today_index = (today - start_date).days
        if 0 <= today_index < date_range:
            today_line = QLineSeries()
            today_line.setName("Today")
            today_line.append(today_index, 0)
            today_line.append(today_index, max_count + 1)
            
            pen = QPen(QColor("#FF4081"))  # Pink
            pen.setWidth(2)
            pen.setStyle(Qt.DashLine)
            today_line.setPen(pen)
            
            chart.addSeries(today_line)
            chart.setAxisX(axis_x, today_line)
            chart.setAxisY(axis_y, today_line)
    
    def update_recent_list(self):
        """Update the recently updated projects list with improved styling"""
        self.recent_list.clear()
        
        # Sort projects by last updated date (newest first)
        sorted_projects = sorted(
            [p for p in self.parent.projects if "last_updated" in p],
            key=lambda x: x["last_updated"],
            reverse=True
        )
        
        # Show top 5 recently updated projects
        for i, project in enumerate(sorted_projects[:5]):
            date_str = project["last_updated"][:10]
            item = QListWidgetItem(f"{project['name']} - {date_str}")
            
            # Set icon based on priority
            if project["priority"] == "High Priority":
                item.setIcon(QIcon.fromTheme("emblem-important"))
            elif project["priority"] == "Medium Priority":
                item.setIcon(QIcon.fromTheme("emblem-default"))
            else:
                item.setIcon(QIcon.fromTheme("emblem-symbolic-link"))
            
            # Set text color based on priority
            if project["priority"] == "High Priority":
                item.setForeground(QColor("#FF5252"))
            elif project["priority"] == "Medium Priority":
                item.setForeground(QColor("#FFA726"))
            
            self.recent_list.addItem(item)
    
    def update_deadline_list(self):
        """Update the upcoming deadlines list with improved styling"""
        self.deadline_list.clear()
        
        # Get today's date
        today = datetime.now().date()
        
        # Get projects with deadlines in the future
        future_deadlines = []
        for project in self.parent.projects:
            if not project.get("deadline"):
                continue
                
            try:
                deadline = datetime.strptime(project["deadline"], "%Y-%m-%d").date()
                if deadline >= today and int(project.get("completion", 0)) < 100:
                    future_deadlines.append((project, deadline))
            except ValueError:
                # Skip invalid dates
                continue
        
        # Sort by deadline (nearest first)
        future_deadlines.sort(key=lambda x: x[1])
        
        # Show top 5 upcoming deadlines
        for project, deadline in future_deadlines[:5]:
            days_left = (deadline - today).days
            
            if days_left == 0:
                days_text = "Today"
            elif days_left == 1:
                days_text = "Tomorrow"
            else:
                days_text = f"{days_left} days left"
            
            item = QListWidgetItem(f"{project['name']} - {days_text}")
            
            # Set icon and style based on urgency
            if days_left <= 1:
                item.setIcon(QIcon.fromTheme("appointment-missed"))
                item.setForeground(QColor("#FF5252"))  # Red for urgent
            elif days_left <= 3:
                item.setIcon(QIcon.fromTheme("appointment-soon"))
                item.setForeground(QColor("#FFA726"))  # Orange for soon
            else:
                item.setIcon(QIcon.fromTheme("appointment-new"))
            
            self.deadline_list.addItem(item)
    
    # Data functions for metric cards
    def get_total_projects(self):
        """Get the total number of projects"""
        return len(self.parent.projects)
    
    def get_completed_projects(self):
        """Get the number of completed projects"""
        return sum(1 for p in self.parent.projects if int(p.get("completion", 0)) == 100)
    
    def get_high_priority_projects(self):
        """Get the number of high priority projects"""
        return sum(1 for p in self.parent.projects if p["priority"] == "High Priority")
    
    def get_due_this_week(self):
        """Get the number of projects due this week"""
        today = datetime.now().date()
        end_of_week = (today + timedelta(days=7)).strftime("%Y-%m-%d")
        today_str = today.strftime("%Y-%m-%d")
        
        return sum(1 for p in self.parent.projects 
                  if p.get("deadline") and today_str <= p.get("deadline") <= end_of_week
                  and int(p.get("completion", 0)) < 100)
    
    def get_overdue_projects(self):
        """Get the number of overdue projects"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        return sum(1 for p in self.parent.projects 
                  if p.get("deadline") and p.get("deadline") < today 
                  and int(p.get("completion", 0)) < 100)
    
    def get_stalled_projects(self):
        """Get the number of stalled projects"""
        fourteen_days_ago = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        
        return sum(1 for p in self.parent.projects 
                  if ("last_updated" in p and p["last_updated"][:10] < fourteen_days_ago
                      and int(p.get("completion", 0)) < 100))


class DashboardDialog(QDialog):
    """Dialog for displaying the project dashboard"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.setWindowTitle("Project Dashboard")
        self.setMinimumSize(900, 700)
        
        # Set dark theme styling
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.parent.colors['background']};
            }}
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create dashboard widget - fresh instance each time
        self.dashboard = DashboardWidget(parent)
        layout.addWidget(self.dashboard)
        
        # Don't auto-refresh here; we'll do it in showEvent
    
    def showEvent(self, event):
        """Override showEvent to refresh dashboard when dialog is shown"""
        super().showEvent(event)
        # Refresh the dashboard when the dialog is shown
        # Using QTimer.singleShot to ensure the UI is fully visible first
        QTimer.singleShot(100, self.refreshDashboard)
    
    def refreshDashboard(self):
        """Refresh the dashboard safely"""
        if hasattr(self, 'dashboard') and self.dashboard:
            self.dashboard.refresh_dashboard()

# Integration with main application
# Update the add_dashboard function to ensure we're creating a new dialog each time
def add_dashboard(project_organizer):
    """Add dashboard functionality to the project organizer
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Add a method to open the dashboard
    def open_dashboard(self):
        """Open the dashboard dialog"""
        # Create a fresh dialog instance each time
        dialog = DashboardDialog(self)
        dialog.exec_()
    
    project_organizer.open_dashboard = open_dashboard.__get__(project_organizer)
    
    # Add a dashboard button to the UI
    for i in range(project_organizer.centralWidget().layout().count()):
        item = project_organizer.centralWidget().layout().itemAt(i)
        if isinstance(item, QHBoxLayout):
            # This is likely the action buttons layout
            dashboard_button = QPushButton("Dashboard")
            dashboard_button.setIcon(QIcon.fromTheme("dashboard"))
            dashboard_button.clicked.connect(project_organizer.open_dashboard)
            
            # Insert the button at the beginning
            item.insertWidget(0, dashboard_button)
            break