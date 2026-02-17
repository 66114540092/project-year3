import os
import subprocess
import shutil

def main():
    # Configuration
    puml_source = 'docs/plantuml_sequence_12_uc.puml'
    output_dir = 'docs/images/sequence_diagrams'
    jar_path = 'docs/plantuml-1.2026.1.jar'

    # Check Prereqs
    if not os.path.exists(jar_path):
        print(f"Error: PlantUML JAR not found at {jar_path}")
        return

    if not os.path.exists(puml_source):
        print(f"Error: PlantUML source file not found at {puml_source}")
        return

    # Check Java
    try:
        subprocess.run(["java", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: 'java' command not found. Please install Java (JRE/JDK).")
        return

    # Create Output Directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Helper function to extract individual diagrams into temporary files
    # This is needed because running the jar on the whole file might generate images 
    # but we want to ensure we have control or if the user wants individual control.
    # Actually, PlantUML jar can handle the whole file and will generate separate images 
    # based on @startuml [filename]. 
    
    # We will try running it directly on the file first.
    # Command: java -jar docs/plantuml-1.2026.1.jar -tpng docs/plantuml_sequence_12_uc.puml -o docs/images/sequence_diagrams -charset UTF-8
    
    # Correction: The -o option in PlantUML is relative to the SOURCE file directory if not absolute, 
    # or sometimes relative to current dir. Let's use absolute paths to be safe.
    
    # However, running the command is simpler.
    print(f"Generating diagrams from {puml_source} using local JAR...")
    
    cmd = [
        "java", 
        "-Dfile.encoding=UTF-8", # Force Java to use UTF-8
        "-jar", jar_path, 
        "-tpng", 
        puml_source, 
        "-o", os.path.abspath(output_dir), # Output directory
        "-charset", "UTF-8" # PlantUML charset
    ]
    
    print("Executing command:", " ".join(cmd))
    
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("PlantUML Output:")
        print(result.stdout)
        
        if result.stderr:
             # PlantUML often prints progress to stderr, which is normal
             pass
             
        print(f"\nSuccess! Check '{output_dir}' for generated images.")
        
    except subprocess.CalledProcessError as e:
        print("Error running PlantUML:")
        print(e.stderr)

if __name__ == "__main__":
    main()
