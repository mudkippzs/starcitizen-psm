import sys
import random
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QHeaderView, QLabel,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)

from PySide2.QtCore import Slot, Qt

class StarCitizenShipPrices(QWidget):
   
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

        self.draw()        
        self.refresh()

    def draw(self):
        # Create widgets, table and configure them.
        self.update_button = QPushButton("Refresh")
        self.options_button = QPushButton("Configure")
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
        
        # Size columns.
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # Set layout and add widgets to it.
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.update_button, 0)
        # self.layout.addWidget(self.options_button, 1)
        self.setLayout(self.layout)

        # Connecting the signal.        
        self.update_button.clicked.connect(self.refresh)
        #TODO self.options_button.clicked.connect(self.show_options)
        # Draw the UI to the screen.
        self.resize(600, 1400)
        self.setWindowTitle("Star Citizen Ship Prices")
        self.show()


    def ship_list_table(self):
        ship_table = []
        ship_list = self.get_ship_list()
        for ship in ship_list:
            row = [ship["name"], ship["price"], ship["state"]]
            ship_table.append(row)

        return ship_table
    
    def clear_table(self):         
         self.tableWidget.setRowCount(0)
         return True if self.tableWidget.rowCount() < 1 else False

    def write_to_table(self):
        row_count = 0        
        self.tableWidget.setRowCount(len(self.ship_list_table()))
        for row in self.ship_list_table():
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(row[2]))
            row_count = row_count + 1
        if row_count <= len(self.ship_list_table()):
            return True
        else:            
            return False

    def get_ship_list(self):
        try:
            ship_list = self.ship_scanner.get_ship_list()
        except AttributeError:
            ship_list = [
                {'name': 'DemoShip', 'price': '$15.00', 'state': 'In stock!'},
                {'name': 'DemoShip', 'price': '$25.00', 'state': 'Sold out!'},
                {'name': 'WatchedDemoShip', 'price': '$35.00', 'state': 'In stock!'},
            ]
            
        return ship_list

    @Slot()
    def show_options(self):
        pass

    @Slot()
    def refresh(self):
        self.update_button.setEnabled(False)
        self.update_button.setText("Getting prices...")
        if self.clear_table():
            self.write_to_table()
        else:
            print("Error writing to table!")
        self.update_button.setEnabled(True)
        self.update_button.setText("Refresh")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = StarCitizenShipPrices()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())