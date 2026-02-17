import os

def merge_chapters():
    files = [
        'docs/chapter2_theory_part1.md',
        'docs/chapter2_theory_part2.md', 
        'docs/chapter2_theory_part3.md',
        'docs/chapter2_theory_part4.md'
    ]
    output_file = 'docs/chapter2_theory_full.md'
    
    print(f"Merging {len(files)} files into {output_file}...")
    
    full_content = ""
    for f in files:
        if os.path.exists(f):
            print(f"Reading {f}...")
            with open(f, 'r', encoding='utf-8') as infile:
                full_content += infile.read() + "\n\n"
        else:
            print(f"Warning: {f} not found!")
            
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(full_content)
        
    print("Merge complete! File saved with UTF-8 encoding.")

if __name__ == "__main__":
    merge_chapters()
