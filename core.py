import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QGuiApplication, QPainter, QPen
from PyQt5.QtCore import Qt, QTimer, QPoint

# Global variables to store the drawing state
drawing = False
last_point = QPoint()
pixmap = None

def start_drawing(event):
    global drawing, last_point
    if event.button() == Qt.LeftButton:
        drawing = True
        last_point = event.pos()

def draw(event):
    global drawing, last_point, pixmap, label
    if (event.buttons() & Qt.LeftButton) and drawing:
        painter = QPainter(pixmap)
        pen = QPen(Qt.red, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        current_point = event.pos()
        painter.drawLine(last_point, current_point)
        last_point = current_point
        painter.end()  # End the painting session
        label.update()

def stop_drawing(event):
    global drawing
    if event.button() == Qt.LeftButton:
        drawing = False

def take_screenshot(window, label):
    global pixmap
    # Hide the window
    window.hide()
    # Give a delay to ensure the window is hidden before taking the screenshot
    QTimer.singleShot(500, lambda: capture_and_display(window, label))

def capture_and_display(window, label):
    global pixmap
    # Take the screenshot using QScreen
    screen = QApplication.primaryScreen()
    if screen is not None:
        pixmap = screen.grabWindow(0)
        label.setPixmap(pixmap)
        label.adjustSize()  # Adjust label size to image size
    # Show the window again
    window.show()

def save_screenshot(screenshot_label):
    pixmap = screenshot_label.pixmap()
    if pixmap:
        save_path, _ = QFileDialog.getSaveFileName(filter="PNG(*.png);;JPEG(*.jpg)")
        if save_path:
            pixmap.save(save_path)

def setup_ui():
    global pixmap, label
    window = QWidget()
    window.setWindowTitle("Screenshot Tool")
    window.setGeometry(100, 100, 800, 600)

    layout = QVBoxLayout()

    # Setup label for drawing
    label = QLabel(window)
    label.setAlignment(Qt.AlignCenter)  # Center the text and image in the label

    # Initialize pixmap where drawing will take place
    pixmap = QPixmap(window.size())  # Set initial size to match the window
    pixmap.fill(Qt.white)  # Start with a white pixmap
    label.setPixmap(pixmap)

    # Connect mouse events to the drawing functions
    label.mousePressEvent = start_drawing
    label.mouseMoveEvent = draw
    label.mouseReleaseEvent = stop_drawing

    layout.addWidget(label)

    btn_capture = QPushButton("Capture Screen")
    btn_capture.clicked.connect(lambda: take_screenshot(window, label))
    layout.addWidget(btn_capture)

    btn_save = QPushButton("Save to File")
    btn_save.clicked.connect(lambda: save_screenshot(label))
    layout.addWidget(btn_save)

    window.setLayout(layout)
    window.show()
    return app.exec_()  # This will start the event loop

if __name__ == '__main__':
    app = QApplication(sys.argv)  # The QApplication should be initialized only once
    sys.exit(setup_ui())  # setup_ui() is now responsible for starting the event loop
