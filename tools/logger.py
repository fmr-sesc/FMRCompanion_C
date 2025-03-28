from datetime import datetime
import time
import csv
import os

class Logger(object):
    def __init__(self, usb_path=None, sample_time=1):
        """Initialize logger. Detect USB drive if no path is provided."""
        self.time_stamp = 0
        self.data = []
        self.file_path = None
        self.data_buffer = {}
        self.headers = ["Timestamp"]
        self.sample_time = sample_time

        # If no usb_path is given, automatically detect a mounted USB drive
        while usb_path is None:
            usb_path = self.find_usb_drive()
            # Small delay to allow the usb stick to initialise on boot
            time.sleep(1)

        self.usb_path = usb_path  # Set the USB path (either provided or detected)

        if self.usb_path:
            print(f"USB drive detected at: {self.usb_path}")
            # Create a test file to verify access
            test_file = os.path.join(self.usb_path, "test_log.txt")
            with open(test_file, "w") as file:
                file.write("USB logging test successful!")
        else:
            print("No USB drive detected.")

    def find_usb_drive(self):
        """Finds the first mounted USB drive and returns its path."""
        base_path = "/media/FMRCompanion/"  # Default USB mount location on Raspberry Pi
        if os.path.exists(base_path):
            usb_drives = os.listdir(base_path)  # List all mounted devices
            if usb_drives:
                return os.path.join(base_path, usb_drives[0])  # Return first detected USB path
        return None  # No USB detected

    def create_csv(self, date_time):
        """ Creates a new CSV file with a timestamped name. """
        filename = f"sensor_log_{date_time}.csv"
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
