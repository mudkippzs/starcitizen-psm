import sys
import random
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QHeaderView, QLabel,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)

from PySide2.QtCore import Slot, Qt

class StarCitizenShipPrices(QWidget):
    @property
    def ship_list_table(self):
        ship_table = []
        for ship in self.ship_list:
            row = [ship["name"], ship["price"], ship["state"]]
            ship_table.append(row)

        return ship_table
    
    @property
    def ship_list_formatted(self):
        formatted_list = []

        for ship in self.ship_list:
            formatted_list.append("%s%s%s%s%s\n" % (ship["name"]," " * (50 - len(ship["name"])), ship["price"]," " * (30 - len(ship["price"])) , ship["state"]))

        return ('').join(formatted_list)
    

    def __init__(self, ship_scanner=None):
        QWidget.__init__(self)

        if ship_scanner:
            self.ship_scanner = ship_scanner            
            self.ship_list = self.ship_scanner.get_ship_list()
        else:
            self.ship_list = [
                {'name': 'DemoShip', 'price': '$15.00', 'state': 'In stock!'},
                {'name': 'DemoShip', 'price': '$25.00', 'state': 'Sold out!'},
                {'name': 'WatchedDemoShip', 'price': '$35.00', 'state': 'In stock!'},
            ]

        # Create widgets, table and configure them.
        self.update_button = QPushButton("Update Prices")
        self.options_button = QPushButton("Configure...")
        self.refresh_bool = QCheckBox("Automatically refresh?")                
        self.refresh_freq = QComboBox()
        self.refresh_freq.addItem("1 hour")
        self.refresh_freq.addItem("6 hours")
        self.refresh_freq.addItem("12 hour")
        self.refresh_freq.addItem("24 hour")
        self.refresh_freq.addItem("3 days")
        self.refresh_freq.addItem("7 days")
        

        self.refresh_bool.nextCheckState()
        
        button_width = 150
        button_height = 20

        combo_box_width = 150
        combo_box_height = 20

        self.update_button.setStyleSheet("max-width:%dpx;height:%dpx;" % (button_width, button_height))
        self.options_button.setStyleSheet("max-width:%dpx;height:%dpx;" % (button_width, button_height))
        self.refresh_freq.setStyleSheet("max-width:%dpx;height:%dpx;" % (combo_box_width, combo_box_height))
        
        self.tableWidget = QTableWidget(1,3)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem('Ship')) 
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem('Price')) 
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem('Availability')) 
        
        # Size columns
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # Set layout and add widgets to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.update_button, 0)
        self.setLayout(self.layout)

        # Connecting the signal
        self.update_button.clicked.connect(self.refresh)
        self.update_button.clicked.connect(self.show_options)
        

    @Slot()
    def show_options(self):
        pass

    @Slot()
    def refresh(self):
        row_count = 0
        self.tableWidget.setRowCount(len(self.ship_list_table))
        for row in self.ship_list_table:
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(row[2]))
            row_count = row_count + 1

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = StarCitizenShipPrices()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())