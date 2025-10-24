## Distributed Storage Labs
A backend API in Python3, Flask, Sqlite3.
<br>
### Installing Python Packages
#### Run the following command to install everything
On the terminal shell
<br>`$ pip install gevent requests tinyrpc Flask protobuf pyzmq boto3 apscheduler`

### Sqlite3
#### Create a database and add a new table for the File entity.
On the terminal shell invoke sqlite3
<br>`$ sqlite3 files.db`
<br> Copy and paste the following SQL command to create a table for our File entity.
<br>
``CREATE TABLE `file` (
 `id` INTEGER PRIMARY KEY AUTOINCREMENT,
 `filename` TEXT,
 `size` INTEGER,
`content_type` TEXT,
 `created` DATETIME DEFAULT CURRENT_TIMESTAMP,
 `blob_name` TEXT
 );``

### Protocol Buffers (Protobuf)
#### Install protobuf
`$ pip install protobuf`
#### Verify protoc is installed
`$ protoc --version`
#### Generate Python classes from the proto files (messages.proto)
`$ protoc --python_out=. messages.proto`
<br>As a result, a new file called **messages_pb2.py** is created, 
which gives you a convenient Python class to work with, 
and also implement serialization and parsing file messages.

### Handling Files
#### Convert file to Base64 String
Use the website
https://www.browserling.com/tools/file-to-base64
<br> As an example, the result of the conversion for **dummyImage.png** was saved in [dummyImageBase64String.txt](dummyImageBase64String.txt)
#### File type code
Check here:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types
<br> As an example, the MIME Type for the .png is "image/png".