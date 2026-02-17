import os

def merge_files(output_file, input_files):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for fname in input_files:
            if os.path.exists(fname):
                with open(fname, 'r', encoding='utf-8') as infile:
                    outfile.write(f"<!-- Start of {fname} -->\n")
                    outfile.write(infile.read())
                    outfile.write(f"\n\n<!-- End of {fname} -->\n\n")
                print(f"Merged: {fname}")
            else:
                print(f"File not found: {fname}")

input_files = [
    'docs/chapter1_intro.md',
    'docs/chapter2_theory_full.md',
    'docs/chapter3_system_design.md',
    'docs/chapter4_implementation.md',
    'docs/chapter5_testing.md',
    'docs/chapter6_conclusion_appendices.md'
]

output_file = 'docs/final_project_report.md'

merge_files(output_file, input_files)
print(f"Successfully created {output_file}")
