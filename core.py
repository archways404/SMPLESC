import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QGuiApplication, QScreen
from PyQt5.QtCore import Qt, QTimer

def take_screenshot(window, label):
    # Hide the window
    window.hide()
    # Give a delay to ensure the window is hidden before taking the screenshot
    QTimer.singleShot(500, lambda: capture_and_display(window, label))  # Increased delay to 500ms

def capture_and_display(window, label):
    # Take the screenshot using QScreen
    screen = QApplication.primaryScreen()
    if screen is not None:
        # Make sure to grab the entire screen
        pixmap = screen.grabWindow(0)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # Copy to clipboard
        clipboard = QGuiApplication.clipboard()
        clipboard.setPixmap(pixmap)
    # Show the window again
    window.show()

def save_screenshot(screenshot_label):
    pixmap = screenshot_label.pixmap()
    if pixmap:
        save_path, _ = QFileDialog.getSaveFileName(filter="PNG(*.png);;JPEG(*.jpg)")
        if save_path:
            pixmap.save(save_path)

def setup_ui():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Screenshot Tool")
    window.setGeometry(100, 100, 600, 400)

    layout = QVBoxLayout()

    # Label to display the screenshot
    screenshot_label = QLabel("Capture an image to display it here.")
    screenshot_label.setAlignment(Qt.AlignCenter)  # Center the text and image in the label
    layout.addWidget(screenshot_label)

    btn_capture = QPushButton("Capture Screen")
    btn_capture.clicked.connect(lambda: take_screenshot(window, screenshot_label))
    layout.addWidget(btn_capture)

    btn_save = QPushButton("Save to File")
    btn_save.clicked.connect(lambda: save_screenshot(screenshot_label))
    layout.addWidget(btn_save)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    setup_ui()
