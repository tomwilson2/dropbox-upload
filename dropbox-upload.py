"""
    Script takes two arguments.

    ARG1 | sys.argv[1] : Is the `file_path` in which the thing being backed up is (e.g. '/var/www/websaga-api/.tmp/data.db')
    ARG2 | sys.argv[2] : Is the folder in Dropbox it is going to be saved to (e.g. 'websaga').
"""
from os.path import join, dirname, isfile, getsize, basename
from os import environ
from dotenv import load_dotenv
import sys
import dropbox

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

access_token = environ.get('DROPBOX_ACCESS_TOKEN')
chunk_size = 4 * 1024 * 1024

# Ensures both arguements are being used and file referenced in argv[1] is a file.
if len(sys.argv) <= 1 or len(sys.argv) >= 4 or not isfile(sys.argv[1]):
    sys.exit('Usage: python dropbox-upload.py path_to_file')

# Sort out filename variables
file_path = sys.argv[1]
file_size = getsize(file_path)
file_name = basename(file_path)
file = open(file_path, 'rb')

# Sort out destination naming for dropbox
if sys.argv[2]:
    destination_path = '/' + sys.argv[2] + '/' + file_name
else:
    destination_path = '/' + file_name
    
dbx = dropbox.Dropbox(access_token)

if file_size <= chunk_size:
    try:
        dbx.files_upload(file.read(), destination_path, mode=dropbox.files.WriteMode.overwrite)
        print('Upload to Dropbox completed')
    except Exception as error:
        sys.exit(error.error)
else:
    try:
        upload_session_start_result = dbx.files_upload_session_start(file.read(chunk_size))
        cursor = dropbox.files.UploadSessionCursor(upload_session_start_result.session_id, file.tell())
        commit = dropbox.files.CommitInfo(destination_path, dropbox.files.WriteMode.overwrite)
        while file.tell() < file_size:
            if ((file_size - file.tell()) <= chunk_size):
                dbx.files_upload_session_finish(file.read(chunk_size), cursor, commit)
                print('Upload to Dropbox completed')
            else:
                dbx.files_upload_session_append(file.read(chunk_size), cursor.session_id, cursor.offset)
                cursor.offset = file.tell()
    except Exception as error:
        sys.exit(error.error)
