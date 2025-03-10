# Vehicle Registration Details Checker

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based tool to ethically retrieve vehicle registration details from India's Parivahan portal (Educational Use Only)

## 📌 Important Disclaimer
**This project is intended for educational purposes only.**  
❌ Not affiliated with Government of India  
❌ Not for commercial use  
❌ Never store/share retrieved data  

## ✨ Features
- Basic vehicle information retrieval
- Sensitive data masking (engine/chassis numbers)
- RTO code to name conversion
- Ethical request rate limiting
- Error handling for website changes

## 📋 Prerequisites
- Python 3.6+
- `requests` library
- `beautifulsoup4` library

## 🛠 Installation
```bash
pip install requests beautifulsoup4
```
## 🚀 Usage
```bash
python vehicle_info_checker.py <REGISTRATION_NUMBER>
```
## Example
- python `vehicle_info_checker.py KL07CN3645`
- Registration No: `KL07CN3645`
- State: `Kerala` | RTO: `Ernakulam`
- Vehicle: `Maruti Suzuki Swift VXi`
- Class: `Motor Car (LMV)`
- Fuel: `PETROL`
- Registration Date: `15/07/2018`
- Engine: `K12N*****67`
- Chassis: `MA3E*****89`
- Insurance Valid Until: `30/11/2024`
- Pollution Check: `01/01/2025`

