import ftplib
import os
import datetime

FTP_HOST = "test.rebex.net"
FTP_USER = "anonymous"
FTP_PASS = ""

UPLOAD_FILENAME = "upload_test_file.txt"

def ftp():

    with open(UPLOAD_FILENAME, "w") as f:
        f.write(f"Read-only test: {datetime.datetime.now()}")
    print(f" Created local file '{UPLOAD_FILENAME}' for upload attempt.")

    try:
        with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
            print(f"Connected to read-only server: {FTP_HOST}")
            print(f"Server Welcome: {ftp.getwelcome()}")

            print("\n Listing remote directory contents (Read Success)")
            ftp.dir()

            print(f"\n-Attempting to upload '{UPLOAD_FILENAME}' (Write Failure Expected)")
            with open(UPLOAD_FILENAME, "rb") as f:
               
                ftp.storbinary(f"STOR {UPLOAD_FILENAME}", f)
            
            print("Upload successful.")

    except ftplib.error_perm as e:
    
        print(f"\nSUCCESS: The script failed as expected.")
        print(f"The read-only server correctly denied the upload with the error: {e}")

    except ftplib.all_errors as e:
        print(f"\n An unexpected FTP Error occurred: {e}")
        
    finally:
        # clean up the local file
        if os.path.exists(UPLOAD_FILENAME):
            os.remove(UPLOAD_FILENAME)
        print("\nLocal test file cleaned up.")

if __name__ == "__main__":
    ftp()