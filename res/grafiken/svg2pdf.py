import os
import json

svg_directory = r"./"
cache_file_path = os.path.join(svg_directory, ".svg2pdf")

# Function to load the cache file
def load_cache():
    try:
        with open(cache_file_path, "r") as cache_file:
            return json.load(cache_file)
    except FileNotFoundError:
        return {}

# Function to save the cache file
def save_cache(cache):
    with open(cache_file_path, "w") as cache_file:
        json.dump(cache, cache_file)

# Load existing cache
cache = load_cache()

# Iterate over all files in the directory
for filename in os.listdir(svg_directory):
    if filename.endswith(".svg"):
        svg_file = os.path.join(svg_directory, filename)
        pdf_file = os.path.join(svg_directory, filename[:-4] + ".pdf")

        # Get the last modified time of the SVG file
        last_modified_time = os.path.getmtime(svg_file)

        # Check if the file is new or has been modified since last conversion
        not_in_cache = filename not in cache
        modified = not_in_cache or cache[filename] != last_modified_time

        if modified:
            print(f"Converting {filename} to {filename[:-4]}.pdf")

        if not_in_cache or modified:
            command = f'draw.io -x -f pdf --crop -o "{pdf_file}" "{svg_file}"'
            os.system(command)
            print(f"Converted {filename} to {filename[:-4]}.pdf")

            # Update the cache with the new timestamp
            cache[filename] = last_modified_time

# Save the updated cache
save_cache(cache)

print("Conversion completed.")
