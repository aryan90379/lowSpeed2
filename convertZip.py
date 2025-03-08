import zipfile
import os

def zip_files(zip_name, file_paths):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file)) 
                print(f"Added: {file}")
            else:
                print(f"File not found: {file}")


# Type all the files down here to convert to zip
files_to_zip = ["Circulation.py", "showAirfoil.py"]
zip_files("Low_Speed_Assignment.zip", files_to_zip)
