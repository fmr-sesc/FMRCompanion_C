from datetime import datetime
import csv
import os

class logger(object):
    def __init__(self, usb_path):
        """Init logger"""
        self.time_stamp = 0
        self.data = []
        self.usb_path = usb_path
        self.file_path = usb_path
        self.data_buffer = {}
        self.headers = ["Timestamp"]

    def create_csv(self):
        """Creates a CSV file if it doesn't exist and initializes headers."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"sensor_log_{timestamp}.csv"
        file_path = os.path.join(self.usb_path, filename)

        # Create an empty file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp"])  # Initial column
            print(f"Created new log file: {file_path}")

        return file_path

    def log_data(self, sensor_name, value):
        """Temporarily stores sensor data in memory."""
        self.data_buffer[sensor_name] = value  

    def write_data_to_csv(self):
        """Writes all buffered data to CSV in a single row, updating headers if needed."""
        if not self.data_buffer:
            print("No data to write.")
            return
        
        # Read existing data & headers
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            existing_headers = next(reader)  # Read current headers
            data_rows = list(reader)  # Read existing data

        # Ensure all new sensor names are added to headers
        for sensor_name in self.data_buffer.keys():
            if sensor_name not in existing_headers:
                existing_headers.append(sensor_name)  # Expand the header

        # Create a new row with the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {header: "" for header in existing_headers}  # Initialize all columns as empty
        new_row["Timestamp"] = timestamp

        # Fill in sensor data
        for sensor_name, value in self.data_buffer.items():
            new_row[sensor_name] = value

        # Convert previous data into dictionary format (for correct column alignment)
        formatted_data = []
        for row in data_rows:
            row_dict = {existing_headers[i]: row[i] if i < len(row) else "" for i in range(len(existing_headers))}
            formatted_data.append(row_dict)

        # Append the new row to the formatted data
        formatted_data.append(new_row)

        # Write updated data to the CSV
        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=existing_headers)
            writer.writeheader()
            writer.writerows(formatted_data)

        # Clear buffer after writing
        self.data_buffer.clear()