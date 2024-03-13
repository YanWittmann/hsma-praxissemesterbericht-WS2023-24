import os

svg_directory = r"./"

# Iterate over all files in the directory
for filename in os.listdir(svg_directory):
    if filename.endswith(".svg"):
        svg_file = os.path.join(svg_directory, filename)

        pdf_file = os.path.join(svg_directory, filename[:-4] + ".pdf")

        command = f'draw.io -x -f pdf --crop -o "{pdf_file}" "{svg_file}"'
        os.system(command)

        print(f"Converted {filename} to {filename[:-4]}.pdf")

print("Conversion completed.")
