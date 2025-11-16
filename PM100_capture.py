from ctypes import (
    c_double, c_int16, c_uint32,
    byref, create_string_buffer, c_bool, c_char_p, c_int
)
from TLPMX import TLPMX, TLPM_DEFAULT_CHANNEL
import time
import statistics
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class PM100():
    def __init__(self, wavelength_nm=1550):
        self.tlPM = TLPMX()
        self.unit = 1e-6 # uW
        self.pow_capture = []
        self.time_capture = []
        self.val_capture = []
        self.wavelength = wavelength_nm
        self.mean_capture = None
        self.start_time_capture = None

    def search_device(self):
        deviceCount = c_uint32()
        self.tlPM.findRsrc(byref(deviceCount))
        print("Number of found devices: " + str(deviceCount.value))
        resourceName = create_string_buffer(1024)
        self.resnamelist = []  # to store resource names
        for i in range(0, deviceCount.value):
            self.tlPM.getRsrcName(c_int(i), resourceName)
            print("Resource name of device", i, ":", c_char_p(resourceName.raw).value)
            self.resnamelist.append(c_char_p(resourceName.raw).value.decode('utf-8'))
    
    def connect_device(self, index):
        resourceName = create_string_buffer(1024)
        self.tlPM.getRsrcName(c_int(index), resourceName)
        self.tlPM.open(resourceName, c_bool(True), c_bool(True))
        time.sleep(2)
        self.set_wavelength(self.wavelength)
        print("Connected to device:", c_char_p(resourceName.raw).value.decode('utf-8'))

    def capture(self, num_samples=1, unit='mW'):
        self.capture_data(num_samples, unit)
        self.mean_capture = statistics.mean(self.val_capture)
        return self.mean_capture

    def capture_data(self, num_samples=1, unit='mW'):
        self.pow_capture = []
        self.time_capture = []
        self.val_capture = []
        self.start_time_capture = time.time()
        power = c_double()
        for i in range(num_samples):
            self.tlPM.measPower(byref(power), TLPM_DEFAULT_CHANNEL)
            self.pow_capture.append(power.value)
            self.time_capture.append(time.time() - self.start_time_capture)
        self.unit_conversion(unit)
        self.val_capture = [p / self.unit for p in self.pow_capture]
        return self.val_capture
    
    def unit_conversion(self, unit='mW'):
        if unit == 'uW':
            self.unit = 1e-6
        elif unit == 'mW':
            self.unit = 1e-3
        elif unit == 'W':
            self.unit = 1.0
        else:
            raise ValueError("Unsupported unit. Use 'uW', 'mW', or 'W'.")
    
    def set_wavelength(self, wavelength_nm):
        self.tlPM.setWavelength(c_double(wavelength_nm), TLPM_DEFAULT_CHANNEL)
        print(f"Wavelength set to {wavelength_nm} nm")
    
    def print_capture(self, unit='mW'): 
        self.unit_conversion(unit)
        if self.unit == 1e-6:
            print("Captured Power Values (in uW):", [f"{v:0.4f}" for v in self.val_capture])
        elif self.unit == 1e-3:
            print("Captured Power Values (in mW):", [f"{v:0.4f}" for v in self.val_capture])
        elif self.unit == 1.0:
            print("Captured Power Values (in W):", [f"{v:0.4f}" for v in self.val_capture])

    def disconnect_device(self):
        self.tlPM.close()

if __name__ == "__main__":
    pm = PM100(wavelength_nm=1550)
    pm.search_device()
    pm.connect_device(0)
    print(pm.capture(10, 'mW'))
    pm.disconnect_device()