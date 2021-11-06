###Creating service to connect to GoogleDrive API v3###

#Before running the script install Google client libraries as per README.md instructions
#importing Google.py for neccessary library imports automatically
from Google import Create_Service

#Client secret file : Downloaded from google cloid console after filling up the OAuth conscent form
CLIENT_SECRET_FILE = 'client_secret_key.json'

API_NAME = 'drive'
API_VERSION = 'v3'

#Full, permissive scope to access all of a user's files, excluding the Application Data folder.
#Authentication links to request Google for particular scope of access
#more info: https://developers.google.com/drive/api/v3/about-auth
SCOPES = ['https://www.googleapis.com/auth/drive']

#Service creation
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

print(dir(service))


###Creating multiple dictionaries within an array with student names and emails###

accounts = [{'Name':'example1','Email':'example1@gmail.com'},{'Name':'example2','Email':'example2@gmail.com'},{'Name':'example3','Email':'example3@gmail.com'}]

###Creating NAME Folders and permitting permissions to their respective emails###

#Using *for loop* to crate folders
for account in accounts:
    print(account['Name'])
    print(account['Email'])

    #info of the folder/file to be created
    file_metadata = {
        'name': str(account['Name']),
        #media type file to create specific nature of document to create
        'mimeType': 'application/vnd.google-apps.folder',

        #folderid in which u want to create the document
        #leave blank to create the doc in home folder
        'parents': ['RANDOM_FOLDER_ID']
        }

    #creating folders
    file = service.files().create(body=file_metadata,fields='id').execute()
    
    #saving the generated folder id in a variable for later uses
    id = file.get('id')

    print ('Folder ID: %s' % id)

    #a service to request for granting permissions
    batch = service.new_batch_http_request()

    #info to grant permissions 
    user_permission = {
        'type': 'user',

        #writer aka editor
        'role': 'writer',

        'emailAddress': account['Email'],
        'emailMessage': 'test_googlle drive automation'
    }

    #creating the permission
    batch.add(service.permissions().create(
            fileId=id,
            body=user_permission,
            fields='id',
    ))

    #granting permission
    batch.execute()
