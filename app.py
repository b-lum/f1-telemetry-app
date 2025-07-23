import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
import pyqtgraph as pg
from socketreader import SocketReader


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("F1 2020 Telemetry")
        self.setGeometry(500, 500, 1000, 600)

        self.status = QLabel("Waiting for data...")
        self.button = QPushButton("Start")
        self.button.clicked.connect(self.start_socket_reader)

        self.speed_label = QLabel("Speed (km/h)")
        self.plot_speed = pg.PlotWidget()
        self.plot_speed.setYRange(0, 400)  # Adjust based on speed
        self.speed_data = [0] * 100
        self.speed_curve = self.plot_speed.plot(self.speed_data, pen='g')

        self.tb_label = QLabel("Throttle (G) and Brake (R)")
        self.plot_tb = pg.PlotWidget() # tb = throttle and brake
        self.plot_tb.setYRange(0, 1)

        self.throttle_data = [0.0] * 100
        self.brake_data = [0.0] * 100

        self.throttle_curve = self.plot_tb.plot(self.throttle_data, pen = 'g', name = 'Throttle')
        self.brake_curve = self.plot_tb.plot(self.brake_data, pen = 'r', name = 'Brake')

        layout = QGridLayout()
        layout = QGridLayout()
        layout.addWidget(self.status, 0, 0)
        layout.addWidget(self.button, 0, 1)

        layout.addWidget(self.speed_label, 1, 0)
        layout.addWidget(self.plot_speed, 2, 0)

        layout.addWidget(self.tb_label, 3, 0)
        layout.addWidget(self.plot_tb, 4, 0)

        self.setLayout(layout)

        self.reader = SocketReader()
        self.reader.new_data.connect(self.update_graph)

    def start_socket_reader(self):
        if not self.reader.isRunning():
            self.reader.start()
            self.status.setText("Receiving data...")

    def update_graph(self, speed, throttle, brake):
        self.speed_data = self.speed_data[1:] + [speed]
        self.speed_curve.setData(self.speed_data)

        self.throttle_data = self.throttle_data[1:] + [throttle]
        self.throttle_curve.setData(self.throttle_data)

        self.brake_data = self.brake_data[1:] + [brake]
        self.brake_curve.setData(self.brake_data)



app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())