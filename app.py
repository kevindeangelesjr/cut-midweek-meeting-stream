from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
import logging
import sys
from src.MeetingPart import MeetingPart

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cut Midweek Meeting Recording")
        self.resize(800, 520)

        main_layout = QVBoxLayout(self)

        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Recording file:"))
        self.recording_path = QLineEdit()
        file_layout.addWidget(self.recording_path)
        browse_file_btn = QPushButton("Browse...")
        browse_file_btn.clicked.connect(self.select_recording_file)
        file_layout.addWidget(browse_file_btn)
        main_layout.addLayout(file_layout)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output directory:"))
        self.output_path = QLineEdit()
        output_layout.addWidget(self.output_path)
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self.select_output_directory)
        output_layout.addWidget(browse_output_btn)
        main_layout.addLayout(output_layout)

        self.parts_table = QTableWidget(0, 3)
        self.parts_table.setHorizontalHeaderLabels(["Part Name", "Start Timestamp", "End Timestamp"])
        self.parts_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.parts_table)

        buttons_layout = QHBoxLayout()
        add_part_btn = QPushButton("Add Part")
        add_part_btn.clicked.connect(self.add_part)
        buttons_layout.addWidget(add_part_btn)

        remove_part_btn = QPushButton("Remove Selected")
        remove_part_btn.clicked.connect(self.remove_selected_part)
        buttons_layout.addWidget(remove_part_btn)

        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.start_processing)
        buttons_layout.addWidget(start_btn)

        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def select_recording_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Recording File",
            "",
            "MP4 Files (*.mp4);;All Files (*)",
        )
        if file_name:
            self.recording_path.setText(file_name)

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", "")
        if directory:
            self.output_path.setText(directory)

    def add_part(self):
        row = self.parts_table.rowCount()
        self.parts_table.insertRow(row)
        for column in range(3):
            item = QTableWidgetItem()
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.parts_table.setItem(row, column, item)
        self.parts_table.editItem(self.parts_table.item(row, 0))

    def remove_selected_part(self):
        selected_rows = {item.row() for item in self.parts_table.selectedItems()}
        for row in sorted(selected_rows, reverse=True):
            self.parts_table.removeRow(row)

    def start_processing(self):
        if not self.recording_path.text():
            QMessageBox.warning(self, "Validation Error", "Please select a recording file.")
            return
        if not self.output_path.text():
            QMessageBox.warning(self, "Validation Error", "Please select an output directory.")
            return
        if self.parts_table.rowCount() == 0:
            QMessageBox.warning(self, "Validation Error", "Please add at least one part.")
            return

        parts = []
        for row in range(self.parts_table.rowCount()):
            name_item = self.parts_table.item(row, 0)
            start_item = self.parts_table.item(row, 1)
            end_item = self.parts_table.item(row, 2)

            name = name_item.text().strip() if name_item else ""
            start = start_item.text().strip() if start_item else ""
            end = end_item.text().strip() if end_item else ""

            if not name or not start or not end:
                QMessageBox.warning(self, "Validation Error", f"Complete all fields for row {row + 1}.")
                return

            parts.append(MeetingPart(name=name, start_time=start, end_time=end, recording_file=self.recording_path.text()))
        
        # Cut the parts from the recording file
        for part in parts:

            video_format = self.recording_path.text().split('.')[-1]

            logging.info(f"Processing part '{part.name}' with start time {part.start_time} and end time {part.end_time}.")
            if part.timestamps_sequence_valid():
                part.cut_part(self.output_path.text(), video_format)
            
            logging.info("All parts have been cut successfully.")

            QMessageBox.information(self, "Success", "All parts have been cut successfully.")

if __name__ == "__main__":
    logging.info("Initializing application...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    logging.info("Application initialized successfully.")
    sys.exit(app.exec())