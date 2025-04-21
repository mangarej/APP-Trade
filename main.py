import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDockWidget, QTextEdit, 
                            QMenuBar, QMenu, QFileDialog, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt, QSettings, QByteArray
from PyQt5.QtGui import QColor, QPalette

class CustomDockWidget(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setFeatures(QDockWidget.DockWidgetMovable | 
                        QDockWidget.DockWidgetFloatable |
                        QDockWidget.DockWidgetClosable |
                        QDockWidget.DockWidgetVerticalTitleBar)
        
    def event(self, event):
        # Handle floating state changes
        if event.type() == event.NonClientAreaMouseButtonDblClick:
            self.setFloating(not self.isFloating())
            if self.isFloating():
                # Adjust floating window behavior
                self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | 
                                   Qt.WindowTitleHint | Qt.WindowMinMaxButtonsHint)
                self.show()
        return super().event(event)

class AdvancedDockingSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Dockable Window System")
        self.resize(1400, 900)
        
        # Custom styling for better visual feedback
        self.setStyleSheet("""
            QDockWidget {
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(float.png);
                border: 1px solid #444;
            }
            QDockWidget::title {
                background: #353535;
                padding: 4px;
                text-align: center;
            }
            QDockWidget::float-button, QDockWidget::close-button {
                border: 1px solid #555;
                padding: 2px;
            }
        """)
        
        # Enhanced docking options
        self.setDockOptions(QMainWindow.AllowNestedDocks | 
                          QMainWindow.AllowTabbedDocks |
                          QMainWindow.AnimatedDocks |
                          QMainWindow.GroupedDragging |
                          QMainWindow.VerticalTabs)
        
        # Window management
        self.windows = {}
        self.create_windows()
        self.setup_initial_layout()
        self.create_menus()
        
        # Load previous state if available
        self.settings = QSettings("MyCompany", "DockingSystem")
        self.load_window_state()

    def create_windows(self):
        """Create all dockable windows with custom properties"""
        colors = {
            'A': QColor(240, 248, 255),  # AliceBlue
            'B': QColor(255, 228, 196),  # Bisque
            'C': QColor(220, 255, 220),  # Honeydew
            'D': QColor(255, 218, 185),  # PeachPuff
            'E': QColor(230, 230, 250),  # Lavender
            'F': QColor(255, 228, 225)   # MistyRose
        }
        
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            dock = QDockWidget(f"Window {letter}", self)
            text_edit = QTextEdit()
            
            # Set colored background for visual distinction
            pal = text_edit.palette()
            pal.setColor(QPalette.Base, colors[letter])
            text_edit.setPalette(pal)
            
            text_edit.setHtml(f"""
            <h2>Window {letter}</h2>
            <p><b>Drag</b> this window to dock in different positions</p>
            <p><b>Drop</b> on another window's title bar to create tabs</p>
            <p><b>Double-click</b> title bar to float/dock</p>
            <p><b>Right-click</b> title bar for options</p>
            """)
            
            dock.setWidget(text_edit)
            dock.setFeatures(QDockWidget.DockWidgetMovable | 
                           QDockWidget.DockWidgetFloatable |
                           QDockWidget.DockWidgetClosable |
                           QDockWidget.DockWidgetVerticalTitleBar)
            
            # Add context menu to dock title bar
            dock.setContextMenuPolicy(Qt.CustomContextMenu)
            dock.customContextMenuRequested.connect(
                lambda pos, l=letter: self.show_dock_context_menu(l, pos)
            )
            
            self.windows[letter] = dock

    def setup_initial_layout(self):
        """Set up a default layout with nested docks"""
        # Main docking areas
        self.addDockWidget(Qt.LeftDockWidgetArea, self.windows['A'])
        self.addDockWidget(Qt.RightDockWidgetArea, self.windows['D'])
        
        # Tabbed docks
        self.tabifyDockWidget(self.windows['A'], self.windows['B'])
        self.tabifyDockWidget(self.windows['D'], self.windows['C'])
        
        # Top and bottom docks
        self.addDockWidget(Qt.TopDockWidgetArea, self.windows['E'])
        self.addDockWidget(Qt.BottomDockWidgetArea, self.windows['F'])
        
        # Nested splits
        self.splitDockWidget(self.windows['A'], self.windows['E'], Qt.Vertical)
        self.splitDockWidget(self.windows['D'], self.windows['F'], Qt.Vertical)
        
        # Show initial tabs
        self.windows['A'].raise_()
        self.windows['D'].raise_()

    def create_menus(self):
        """Create comprehensive menu system"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        file_menu.addAction('Save Layout', self.save_layout)
        file_menu.addAction('Load Layout', self.load_layout)
        file_menu.addSeparator()
        file_menu.addAction('Reset Layout', self.reset_layout)
        file_menu.addSeparator()
        file_menu.addAction('Exit', self.close)

        # Window menu
        window_menu = menubar.addMenu('Windows')
        for letter in sorted(self.windows.keys()):
            action = window_menu.addAction(f"Window {letter}")
            action.setCheckable(True)
            action.setChecked(True)
            action.triggered.connect(
                lambda checked, l=letter: self.toggle_window(l, checked)
            )
        
        # Layout menu
        layout_menu = menubar.addMenu('Layouts')
        layout_menu.addAction('Float All', self.float_all_windows)
        layout_menu.addAction('Dock All', self.dock_all_windows)
        layout_menu.addSeparator()
        layout_menu.addAction('Tabbed Layout', self.set_tabbed_layout)
        layout_menu.addAction('Grid Layout', self.set_grid_layout)

    def show_dock_context_menu(self, window_letter, pos):
        """Context menu for individual dock widgets"""
        dock = self.windows[window_letter]
        menu = QMenu(self)
        
        menu.addAction(f"Float Window {window_letter}", 
                      lambda: dock.setFloating(not dock.isFloating()))
        menu.addAction(f"Close Window {window_letter}", 
                      lambda: self.toggle_window(window_letter, False))
        menu.addSeparator()
        menu.addAction("Lock Position", 
                      lambda: dock.setFeatures(dock.features() & ~QDockWidget.DockWidgetMovable))
        menu.addAction("Unlock Position", 
                      lambda: dock.setFeatures(dock.features() | QDockWidget.DockWidgetMovable))
        
        menu.exec_(dock.mapToGlobal(pos))

    def toggle_window(self, letter, visible):
        """Show or hide the specified window"""
        if visible:
            self.windows[letter].show()
        else:
            self.windows[letter].hide()

    def save_window_state(self):
        """Save current window state and geometry"""
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue("geometry", self.saveGeometry())

    def load_window_state(self):
        """Load previous window state and geometry"""
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        if self.settings.contains("windowState"):
            self.restoreState(self.settings.value("windowState"))

    def save_layout(self):
        """Save layout to file"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Layout", "", "Layout Files (*.layout)", options=options)
        if filename:
            state = {
                'windowState': self.saveState().toHex().data().decode(),
                'geometry': self.saveGeometry().toHex().data().decode()
            }
            with open(filename, 'w') as f:
                json.dump(state, f)

    def load_layout(self):
        """Load layout from file"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Layout", "", "Layout Files (*.layout)", options=options)
        if filename:
            try:
                with open(filename, 'r') as f:
                    state = json.load(f)
                self.restoreGeometry(QByteArray.fromHex(state['geometry'].encode()))
                self.restoreState(QByteArray.fromHex(state['windowState'].encode()))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load layout: {str(e)}")

    def reset_layout(self):
        """Reset to default layout"""
        reply = QMessageBox.question(
            self, 'Confirm Reset', 
            'Are you sure you want to reset to default layout?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Hide all first
            for window in self.windows.values():
                window.hide()
            # Then show with default layout
            self.setup_initial_layout()
            for window in self.windows.values():
                window.show()

    def float_all_windows(self):
        """Make all windows floating"""
        for window in self.windows.values():
            window.setFloating(True)

    def dock_all_windows(self):
        """Dock all floating windows"""
        for window in self.windows.values():
            window.setFloating(False)

    def set_tabbed_layout(self):
        """Arrange all windows in tabs"""
        # First dock all windows
        self.dock_all_windows()
        
        # Start with first window
        first = None
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            if first is None:
                self.addDockWidget(Qt.LeftDockWidgetArea, self.windows[letter])
                first = self.windows[letter]
            else:
                self.tabifyDockWidget(first, self.windows[letter])

    def set_grid_layout(self):
        """Arrange windows in a 2x3 grid"""
        self.dock_all_windows()
        
        # Top row
        self.addDockWidget(Qt.TopDockWidgetArea, self.windows['A'])
        self.addDockWidget(Qt.TopDockWidgetArea, self.windows['B'])
        self.addDockWidget(Qt.TopDockWidgetArea, self.windows['C'])
        self.splitDockWidget(self.windows['A'], self.windows['B'], Qt.Horizontal)
        self.splitDockWidget(self.windows['B'], self.windows['C'], Qt.Horizontal)
        
        # Bottom row
        self.addDockWidget(Qt.BottomDockWidgetArea, self.windows['D'])
        self.addDockWidget(Qt.BottomDockWidgetArea, self.windows['E'])
        self.addDockWidget(Qt.BottomDockWidgetArea, self.windows['F'])
        self.splitDockWidget(self.windows['D'], self.windows['E'], Qt.Horizontal)
        self.splitDockWidget(self.windows['E'], self.windows['F'], Qt.Horizontal)

    def closeEvent(self, event):
        """Save state when closing"""
        self.save_window_state()
        super().closeEvent(event)
        
if __name__ == "__main__":
    app = QApplication([])
    window = AdvancedDockingSystem()
    window.show()
    app.exec_()