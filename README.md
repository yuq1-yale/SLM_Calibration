# SLM_Calibration

A tool to calibrate Spatial Light Modulators (SLMs) by measuring how grayscale input values affect light output.

## Equipment & Settings

**Hardware needed:**
- Meadowlark Optics Blink Plus SLM (1024x1024) - connected via PCIe
- Thorlabs PM100 Power Meter - connected via USB (SEE Repo https://github.com/yuq1-yale/ThorlabControlKit)
- Laser source
- Optical setup to capture 1st-order diffracted light

**Key settings:**
- SLM: 1024x1024 pixels, 8-bit input / 12-bit output
- Wavelength: 1550 nm
- Stripe pattern: 4-8 pixels per stripe
- Wait time: 1 second between measurements

## Requirements

**Hardware drivers:**
- Meadowlark Blink SDK (installed at `C:\Program Files\Meadowlark Optics\Blink Plus\SDK\`)
- Thorlabs PM100 VISA driver

## Steps

1. **Setup hardware**
   - Connect SLM to PCIe port
   - Connect power meter via USB
   - Align optics to measure 1st-order diffraction

2. **Run calibration** (`PCIeDiffractiveTest.py`)
   - Tests all 256 grayscale levels
   - Creates stripe patterns on SLM
   - Measures light power for each level
   - Saves results to CSV file

3. **Analyze results** (`\Meadowlark Optics\Blink Plus\Cal Kit\Diffractive LUT GUI`)
   - Upload the CSV file to get the calibrated LUT file

4. **Verify calibration** (`PCIeDiffractiveVerify.py`)
   - Tests the new LUT file
   - With `plot_result.ipynb` to verify the results.