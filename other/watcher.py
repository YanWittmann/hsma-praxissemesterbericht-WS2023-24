import os
import re
import subprocess
import time
from pathlib import Path
import filecmp

# Define paths
directory = Path("I:/projects/praxissemester/bericht")
temp_file = Path(os.getenv("TEMP")) / "dir_snapshot.txt"
temp_file_new = Path(f"{temp_file}_new")
bib_file = directory / "praksem.bib"
bib_timestamp_file = Path(os.getenv("TEMP")) / "bib_timestamp.txt"

# Function to create a snapshot of the directory
def create_snapshot(directory, snapshot_file):
    snapshot = subprocess.check_output(["dir", directory, "/a", "/s", "/-c", "/o-d", "/t:w"], shell=True, text=True, encoding='utf-8')
    snapshot_file.write_text(snapshot, encoding='utf-8')

# Ensure the bib timestamp file exists
if not bib_timestamp_file.exists():
    bib_timestamp_file.write_text("0", encoding='utf-8')

# Initial snapshot
create_snapshot(directory, temp_file)

while True:
    print("Checking for changes...")
    create_snapshot(directory, temp_file_new)

    # Compare the new snapshot with the previous one
    if not filecmp.cmp(temp_file, temp_file_new, shallow=False):
        print("Change detected")

        # find differences between the two files
        with open(temp_file, 'r', encoding='utf-8') as f:
            old_snapshot = f.readlines()
        with open(temp_file_new, 'r', encoding='utf-8') as f:
            new_snapshot = f.readlines()
        diff = [line for line in new_snapshot if line not in old_snapshot]
        diff = [re.sub(' +', ' ', line) for line in diff]
        diff = [line.split('\n')[0] for line in diff]
        for line in diff:
            if re.match(r"^(\d+) Dir\(s\) (\d+) bytes free$", line):
                print("False alarm: ", line)
                continue
            else:
                print(" ", line)

        os.chdir(directory / "res" / "grafiken")
        subprocess.run(["python", "svg2pdf.py"], shell=True)
        os.chdir(directory)
        create_snapshot(directory, temp_file_new)

        praksem_bib_file = directory / "praksem.bib"
        out_praksem_bib_file = Path("I:/projects/praxissemester/out") / "praksem.bib"
        print("copy", praksem_bib_file, out_praksem_bib_file)
        subprocess.run(["copy", str(praksem_bib_file), str(out_praksem_bib_file)], shell=True)

        try:
            pdflatex_output_bytes = subprocess.check_output(
                ["C:/Users/yan20/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex", "-file-line-error", "-interaction=nonstopmode", "-synctex=1", "-output-format=pdf", "-output-directory=I:/projects/praxissemester/out", "praksem.tex"],
                shell=True
            )
            pdflatex_output = pdflatex_output_bytes.decode('utf-8', errors='replace')
            print("got pdflatex_output with length", len(pdflatex_output))
        except subprocess.CalledProcessError as e:
            pdflatex_output = e.output
            print(pdflatex_output)
        except Exception as e:
            pdflatex_output = str(e)
            print(e)

        # Check if the bib file was updated
        new_timestamp = os.path.getmtime(bib_file)
        with open(bib_timestamp_file, 'r', encoding='utf-8') as f:
            old_timestamp = f.read().strip()

        try:
            if str(new_timestamp) != old_timestamp or "run biber" in pdflatex_output.lower():
                with open(bib_timestamp_file, 'w', encoding='utf-8') as f:
                    f.write(str(new_timestamp))

                os.chdir(Path("I:/projects/praxissemester/out"))
                subprocess.run(["C:/Users/yan20/AppData/Local/Programs/MiKTeX/miktex/bin/x64/biber", "praksem"], shell=True)
                os.chdir(directory)
                for _ in range(2):  # Run pdflatex twice
                    subprocess.run(["C:/Users/yan20/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex", "-file-line-error", "-interaction=nonstopmode", "-synctex=1", "-output-format=pdf", "-output-directory=I:/projects/praxissemester/out", "praksem.tex"], shell=True)
        except Exception as e:
            print("Error while running biber and pdflatex:", e)

        # Update the snapshot
        temp_file_new.replace(temp_file)
    else:
        temp_file_new.unlink()

    time.sleep(2)
