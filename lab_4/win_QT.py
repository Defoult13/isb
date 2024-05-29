import sys
import logging

from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QWidget, 
    QLineEdit, 
    QMessageBox, 
    QFileDialog)

from multiprocessing import cpu_count

from functions import number_selection, graph


logging.basicConfig(level=logging.INFO)


class CreditCardCheckerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Credit Card Checker")
        self.setGeometry(100, 100, 400, 300)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.hash_label = QLabel("Hash String:")
        self.hash_input = QLineEdit()
        layout.addWidget(self.hash_label)
        layout.addWidget(self.hash_input)

        self.last_digits_label = QLabel("Last Digits:")
        self.last_digits_input = QLineEdit()
        layout.addWidget(self.last_digits_label)
        layout.addWidget(self.last_digits_input)

        self.bins_label = QLabel("Bins (comma-separated):")
        self.bins_input = QLineEdit()
        layout.addWidget(self.bins_label)
        layout.addWidget(self.bins_input)

        self.process_label = QLabel("Number of Processes:")
        self.process_input = QLineEdit(str(cpu_count()))
        layout.addWidget(self.process_label)
        layout.addWidget(self.process_input)

        self.run_button = QPushButton("Run Checker")
        self.run_button.clicked.connect(self.run_checker)
        layout.addWidget(self.run_button)

        self.graph_button = QPushButton("Generate Graph")
        self.graph_button.clicked.connect(self.generate_graph)
        layout.addWidget(self.graph_button)

        self.central_widget.setLayout(layout)

    def run_checker(self):
        hash_str = self.hash_input.text()
        last_numbers = self.last_digits_input.text()
        bins = [int(bin.strip()) for bin in self.bins_input.text().split(',')]
        process_count = int(self.process_input.text())

        output_file, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "JSON Files (*.json)")

        if output_file:
            try:
                number_selection(output_file, hash_str, last_numbers, bins, process_count)
                QMessageBox.information(self, "Success", f"Checker completed. Results saved to {output_file}")
            except Exception as ex:
                logging.error(f"Error running checker: {ex}")
                QMessageBox.critical(self, "Error", f"Error running checker: {ex}")

    def generate_graph(self):
        hash_str = self.hash_input.text()
        last_numbers = self.last_digits_input.text()
        bins = [int(bin.strip()) for bin in self.bins_input.text().split(',')]

        output_file, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "PNG Files (*.png)")

        if output_file:
            try:
                graph(output_file, hash_str, last_numbers, bins)
                QMessageBox.information(self, "Success", f"Graph generated. Saved as {output_file}")
            except Exception as ex:
                logging.error(f"Error generating graph: {ex}")
                QMessageBox.critical(self, "Error", f"Error generating graph: {ex}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreditCardCheckerUI()
    window.show()
    sys.exit(app.exec_())
