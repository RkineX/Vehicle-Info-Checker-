import sys
import requests
from bs4 import BeautifulSoup
import re

def get_vehicle_details(reg_number):
    """Ethical vehicle information checker with proper user consent"""
    
    # Validate input format
    if not re.match(r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{1,4}$', reg_number):
        raise ValueError("Invalid registration number format")

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://parivahan.gov.in/'
    }

    try:
        # Initial request
        home_url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=102'
        response = session.get(home_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        viewstate = soup.find('input', {'name': 'javax.faces.ViewState'})['value']
        button = soup.find('button', id=re.compile(r'^form_rcdl'))

        if not button:
            return {"Error": "Website structure changed"}

        # Prepare request data
        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': button['id'],
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
            button['id']: button['id'],
            'form_rcdl': 'form_rcdl',
            'form_rcdl:tf_reg_no1': reg_number[:4],
            'form_rcdl:tf_reg_no2': reg_number[4:],
            'javax.faces.ViewState': viewstate
        }

        # Post request
        post_url = 'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml'
        response = session.post(post_url, headers=headers, data=data)
        response.raise_for_status()

        return parse_response(response.text)

    except requests.exceptions.RequestException as e:
        return {"Error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"Error": f"Processing error: {str(e)}"}

def parse_response(html):
    """Parse website response ethically with data minimization"""
    
    result = {
        "Registration No": "N/A",
        "State": "N/A",
        "RTO": "N/A",
        "Vehicle": "N/A",
        "Class": "N/A",
        "Fuel": "N/A",
        "Registration Date": "N/A",
        "Engine": "N/A",
        "Chassis": "N/A",
        "Insurance Valid Until": "N/A",
        "Pollution Check": "N/A"
    }

    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        
        if not table:
            return result

        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                
                # Map keys to our standardized format
                if 'Registration No' in key:
                    result["Registration No"] = value
                elif 'Owner Name' in key:
                    continue  # Skip private information
                elif 'Vehicle Class' in key:
                    result["Class"] = value
                elif 'Fuel Type' in key:
                    result["Fuel"] = value
                elif 'Engine No' in key:
                    result["Engine"] = value[:4] + '****' + value[-4:] if len(value) > 8 else value
                elif 'Chassis No' in key:
                    result["Chassis"] = value[:4] + '****' + value[-4:] if len(value) > 8 else value
                elif 'Insurance Upto' in key:
                    result["Insurance Valid Until"] = value
                elif 'PUCC Upto' in key:
                    result["Pollution Check"] = value

        # Extract state and RTO from registration number
        reg_parts = result["Registration No"].split()
        if len(reg_parts) > 0:
            state_code = reg_parts[0][:2]
            rto_code = reg_parts[0][2:4]
            result["State"] = get_state_name(state_code)
            result["RTO"] = get_rto_name(state_code, rto_code)

        return result

    except Exception as e:
        result["Error"] = f"Parsing error: {str(e)}"
        return result

def get_state_name(code):
    """Convert state code to name"""
    states = {
        'KL': 'Kerala',
        'DL': 'Delhi',
        'MH': 'Maharashtra',
        'KA': 'Karnataka',
        'TN': 'Tamil Nadu'
    }
    return states.get(code, 'N/A')

def get_rto_name(state_code, rto_code):
    """Convert RTO code to name"""
    rto_db = {
        'KL07': 'Ernakulam',
        'DL04': 'West Delhi',
        'MH01': 'Mumbai Central',
        'KA03': 'Bangalore East'
    }
    return rto_db.get(state_code + rto_code, 'N/A')

def main():
    if len(sys.argv) != 2:
        print("Usage: python vehicle_info_checker.py <REG_NUMBER>")
        print("Example: python vehicle_info_checker.py KL07CN3645")
        sys.exit(1)

    print("\nFetching vehicle details (ethical use only)...\n")
    details = get_vehicle_details(sys.argv[1])
    
    # Display results in specified format
    template = """Registration No: {Registration No}
State: {State} | RTO: {RTO}
Vehicle: {Vehicle}
Class: {Class}
Fuel: {Fuel}
Registration Date: {Registration Date}
Engine: {Engine}
Chassis: {Chassis}
Insurance Valid Until: {Insurance Valid Until}
Pollution Check: {Pollution Check}"""
    
    print(template.format(**details))
    print("\nNote: Always verify through official channels for critical use cases\n")

if __name__ == "__main__":
    main()
