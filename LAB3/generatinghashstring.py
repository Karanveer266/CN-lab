import hashlib
import os

# The name of the file to hash
file_name = "index.html"

# Check if the file exists before proceeding
if not os.path.exists(file_name):
    print(f"Error: File '{file_name}' not found.")
else:
    # 1. Open the file in binary read mode ('rb')
    with open(file_name, 'rb') as f:
        # 2. Read the entire content of the file
        file_content = f.read()
        
        # 3. Create the MD5 hash from the file's content
        md5_hash = hashlib.md5(file_content).hexdigest()

        print(f"The MD5 hash of the file '{file_name}' is: {md5_hash}")
