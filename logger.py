from datetime import datetime
import csv
import os

class logger(object):
    def __init__(self, usb_path):
        """Init logger"""
        self.time_stamp = 0
        self.data = []
        self.usb_path = usb_path
        self.data_buffer = {}
        self.headers = ["Timestamp"]

        def create_csv(self):
            """ Creates a new CSV file with a timestamped name. """
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"sensor_log_{timestamp}.csv"
            file_path = os.path.join(self.usb_path, filename)

            # Create the file with just the timestamp column
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp"]) 

            print(f"Created new log file: {file_path}")
            return file_path
        
        def log_data(self, data_lable, value):
            """ Temporarily stores sensor data in memory. """
            self.data_buffer[data_lable] = value  
        
        def write_data_to_csv(self):
            """ Writes all buffered data to CSV in one row with a single timestamp. """
            if not self.data_buffer:
                print("No data to write.")
                return
            
            # Read the current CSV headers
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.reader(file)
                existing_headers = next(reader)  # Read current headers

            # Ensure all new sensor names are added to headers
            for sensor_name in self.data_buffer.keys():
                if sensor_name not in existing_headers:
                    existing_headers.append(sensor_name)

            # Create a new row with the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = {header: "" for header in existing_headers}
            new_row["Timestamp"] = timestamp

            # Fill in sensor data
            for sensor_name, value in self.data_buffer.items():
                new_row[sensor_name] = value

            # Write updated data to the CSV
            with open(self.file_path, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=existing_headers)
                if file.tell() == 0:  # If file is empty, write the headers
                    writer.writeheader()
                writer.writerow(new_row)