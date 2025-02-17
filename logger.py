from datetime import datetime
import csv
import os

class logger(object):
    def __init__(self, usb_path):
        """Init logger"""
        self.time_stamp = 0
        self.data = []
        self.usb_path = usb_path
        self.file_path = None
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
        self.file_path = file_path
    
    def log_data(self, data_lable, value):
        """ Temporarily stores sensor data in memory. """
        self.data_buffer[data_lable] = value  
    
    def write_data_to_csv(self):
        """Writes all buffered data to CSV in one row, updating headers if needed."""
        if not self.data_buffer:
            print("No data to write.")
            return

        # Read existing headers and data
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            data = list(reader)  # Convert iterator to a list for modification
            existing_headers = data[0] if data else ["Timestamp"]  # Use first row as header

        # Ensure all new sensor names are added to headers
        header_updated = False
        for sensor_name in self.data_buffer.keys():
            if sensor_name not in existing_headers:
                existing_headers.append(sensor_name)
                header_updated = True

        # If headers were updated, rewrite the entire file
        if header_updated:
            data[0] = existing_headers  # Update the first row (headers)
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)  # Re-write updated headers + existing data

        # Create a new row with the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {header: "" for header in existing_headers}  # Initialize all columns as empty
        new_row["Timestamp"] = timestamp

        # Fill in sensor data
        for sensor_name, value in self.data_buffer.items():
            new_row[sensor_name] = value

        # Write updated data to the CSV
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=existing_headers)
            writer.writerow(new_row)

        # Clear buffer after writing
        self.data_buffer.clear()
        print(f"Data written to CSV: {new_row}")
