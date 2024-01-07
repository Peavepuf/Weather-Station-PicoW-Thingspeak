# METEROLOGY ST. V2.4

## Overview
This repository contains a Python script for a meteorological station (Meterology St. V2.4). The script gathers data from various sensors and transmits it to ThingSpeak cloud services for monitoring and analysis.

## Description
The Python script in this repository interfaces with diverse sensors to collect crucial meteorological data. It integrates functionalities for measuring temperature, humidity (using DHT11 sensor), atmospheric pressure (using BMP180 sensor), light levels (using LDR), wind speed and direction (using Rotary Encoder), and analog-to-digital conversion (using ADS1115).

## Requirements
To run this script, ensure the following requirements are met:
- Python environment on a compatible microcontroller or development board.
- Necessary libraries installed:
  - `machine`
  - `time`
  - `urequests`
  - `network`
  - `bmp085` (for BMP180 sensor)
  - `dht` (for DHT11 sensor)
  - `rotary_irq_rp2` (for Rotary Encoder)
  - `ADS1115`

## Usage
1. **Library Installation:** Ensure that all necessary libraries are installed to run the script smoothly.
2. **Network Configuration:** Set up your network connection by providing your SSID and password in the designated fields within the script.
3. **ThingSpeak API Keys:** Adjust the API keys (MeterologyAir and MeterologySoil) in the script for ThingSpeak cloud services.
4. **Sensor Setup:** Connect the following sensors:
   - DHT11 for temperature and humidity measurement
   - BMP180 for atmospheric pressure measurement
   - Rotary Encoder for wind speed and direction measurement
   - LDR for light level measurement
   - ADS1115 for analog-to-digital conversion
5. **Execution:** Run the script on your microcontroller to start gathering meteorological data.

## Contribution Guidelines
Contributions to this project are greatly appreciated. To contribute:
1. Fork the repository.
2. Create a new branch for your changes (`git checkout -b feature/YourFeature`).
3. Commit your modifications (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## Credits
This project is developed and maintained by Peavepuf.
