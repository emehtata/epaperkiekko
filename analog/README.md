
# E-paper Parking Disc

## Overview

This project is an electronic parking disc (pysäköintikiekko) implemented using an e-paper display. The disc shows the current time, updated every half hour, using an analog clock image. It uses the `my_epaper` library to interface with a specific e-paper module and `my_clock` library to generate the clock images.

## Requirements

- Python 3.x
- PIL (Python Imaging Library)
- `my_epaper` module
- `my_clock` module

## Installation

Ensure you have Python 3 installed. Install the required dependencies with:

```bash
pip install -r requirements.txt
```

Additionally, ensure you have the `my_epaper` and `my_clock` modules available in your Python path.

## Usage

To run the script, you can provide the time manually in the format `HH:MM` or let the script use the current system time. 

```bash
python script.py HH:MM
```

or

```bash
python script.py
```

## How It Works

1. **Initialization**:
    - The script initializes logging to capture and display logs for debugging and information purposes.
    - It imports necessary modules including `datetime`, `time`, `math`, `sys`, `PIL.Image`, and custom modules `epd2in7b` from `my_epaper` and `my_clock`.

2. **Analog Clock Image**:
    - The function `analog_kiekko(h, m)` is responsible for generating the clock image based on provided hours and minutes.
    - It initializes the e-paper display, clears it, and then displays the generated clock image.

3. **Main Loop**:
    - The script checks if time is provided as a command-line argument; if not, it defaults to the current system time.
    - It enters an infinite loop where:
        - The current time is rounded up to the nearest half-hour.
        - If a time update is required, it calls `analog_kiekko(h, m)` to update the display.
        - The script sleeps for 30 seconds before updating the time variables and checking again.

## Logging

The script uses Python’s `logging` module to log information, including the current half-hour time slot being displayed. This helps in debugging and ensures the script is running correctly.

## Example

To run the script using the current system time:

```bash
python script.py
```

To run the script with a specific time, for example, 14:30:

```bash
python script.py 14:30
```

## Notes

- Ensure that your e-paper display is properly connected and configured as per the `my_epaper` module's requirements.
- Modify the `my_clock` and `my_epaper` modules according to your specific hardware and image generation needs.

## Author

This project was created to demonstrate the integration of e-paper technology with Python for creating a functional and automated parking disc.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
