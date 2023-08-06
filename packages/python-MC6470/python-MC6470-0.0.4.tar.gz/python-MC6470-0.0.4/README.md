# python-MC6470
A python library for accessing MC6470 6-axis accelerometer from mCube via python-smbus using the I2C interface.

Default settings are suitable for Raspberry Pi3 and was successfully tested.

# Usage
Follow below mention steps:
1. Briefly walk through the [data sheet](https://github.com/Vitaliz-Embedded-solutions/python-MC6470/blob/main/MC6470-Datasheet-APS-048-0033v1.7-1.pdf) 
2. Install this package using the command "pip3 install python-MC6470==0.0.4". Please note that pip3 should be used for installation instead of pip as this package supports only python3
3. Run the command "pip install -r [requirements_dev.txt](https://github.com/Vitaliz-Embedded-solutions/python-MC6470/blob/main/requirements.txt)"
4. See the example application [demo.py](https://github.com/Vitaliz-Embedded-solutions/python-MC6470/blob/main/demo.py) to understand how to use this library.

# Develop
Please send pull requests for improvements and bug fixes in [this](https://github.com/Vitaliz-Embedded-solutions/python-MC6470) github repository.

# License
Python files in this repository are released under the MIT license.
