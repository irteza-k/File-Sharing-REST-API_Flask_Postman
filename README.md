# File Sharing REST API_Flask_Postman

## Summary

This project involves creating a secure file-sharing system between two types of users: 
Operation Users and Client Users. Operation Users can perform login and upload files restricted to specific formats, 
while Client Users can sign up, verify emails, login, list uploaded files, and download files securely.

## Details

- **Framework**: Flask (Python Framework)
- **Database**: SQL 

## Features

### Operation User Actions:

1. **Login**: Operation Users can log in to the system.
2. **Upload File**: Allows only Ops User to upload pptx, docx, and xlsx file types.

### Client User Actions:

1. **Sign Up**: Enables Client Users to register and returns an encrypted URL.
2. **Email Verify**: Sends a verification email to the registered email for account verification.
3. **Login**: Allows Client Users to log in to the system.
4. **Download File**: Allows downloading files via a secure, encrypted URL.
5. **List Uploaded Files**: Provides a list of files uploaded by the Operation User.



### Installation

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.

##Clone the repository.

git clone 


##Activate a virtual environment 

.venv/Scripts/activate

##Install requirments

pip install -r requirements.txt



##Run the server

python app.py         




###########################################################################################################################

Postman link:-  https://documenter.getpostman.com/view/31844352/2s9YkrZeQR

Access the endpoints using a tool like Postman.

Endpoints

    /admin-login [POST]: Admin login route.
    /upload-file [POST]: Route for Ops User to upload files.
    /client-signup [POST]: Route for client signup.
    /client-signin [POST]: Route for client signin.
    /download/<username>/<file_name> [GET]: Route to download files securely.
    
Contributing

Feel free to contribute by reporting issues, suggesting enhancements, or submitting pull requests.



License

No License........................................... (-; 



