
import zlib
import base64
import urllib.request
import string

def deflate_and_encode(plantuml_code):
    """
    Compresses and encodes PlantUML code for the URL.
    """
    # Key fix for Thai/Unicode: verify utf-8 encoding
    zlibbed = zlib.compress(plantuml_code.encode('utf-8'))
    compressed = zlibbed[2:-4] # Strip zlib header and checksum
    
    # Custom Base64 encoding for PlantUML
    # Standard Base64: A-Za-z0-9+/
    # PlantUML Base64: 0-9A-Za-z-_
    
    # We'll use the standard base64 and then translate it
    b64 = base64.b64encode(compressed).decode('utf-8')
    
    # Translation map
    standard_b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    plantuml_b64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    
    trans_table = str.maketrans(standard_b64, plantuml_b64)
    return b64.translate(trans_table)

def download_image(puml_file_path, output_image_path):
    try:
        with open(puml_file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        encoded_code = deflate_and_encode(code)
        url = f"https://www.plantuml.com/plantuml/png/{encoded_code}"
        
        print(f"Downloading from: {url}")
        
        # Add User-Agent header to avoid 403 Forbidden
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                with open(output_image_path, 'wb') as f:
                    f.write(response.read())
                print(f"Success! Image saved to: {output_image_path}")
            else:
                print(f"Error: Server returned status code {response.status}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    puml_path = r"c:\Users\Zeta\Desktop\Project Year 3 Important\battlehub_phase1\docs\plantuml_use_case_diagram.puml"
    image_path = r"c:\Users\Zeta\Desktop\Project Year 3 Important\battlehub_phase1\docs\images\BattleHub_Final_Corrected.png"
    
    # Ensure directory exists
    import os
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
    download_image(puml_path, image_path)
