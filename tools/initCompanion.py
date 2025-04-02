import time
import os

def detect_USB_drive():
    """Finds the first mounted USB drive and returns its path."""
    def find_usb_drive():
        base_path = "/media/FMRCompanion/"  # Default USB mount location on Raspberry Pi
        if os.path.exists(base_path):
            usb_drives = os.listdir(base_path)  # List all mounted devices
            if usb_drives:
                return os.path.join(base_path, usb_drives[0])  # Return first detected USB path
        return None  # No USB detected
    
    usb_path = None
    # If no usb_path is given, automatically detect a mounted USB drive
    while usb_path is None:
        usb_path = find_usb_drive()
        # Small delay to allow the usb stick to initialise on boot
        time.sleep(1)

    if usb_path:
        print(f"USB drive detected at: {usb_path}")
        # Create a test file to verify access
        return usb_path
    else:
        print("No USB drive detected.")