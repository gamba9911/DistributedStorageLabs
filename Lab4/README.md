We have the following tasks:
1. Create a new Sqlite3 database that can store the new representation of the stored files
(4 chunk names instead of 1 blob name)
2. Define the Protobuf messages between our components
3. Change the implementation of add_files(), download_file() and delete_file() in rest-server.py from writing and reading the file using the local file system to sending and receiving chunks to the storage nodes on ZMQ channels as described above
4. Implement the Storage Node component
5. Test the system

### Task 1: Create an Sqlite3 database for the File records.
Download the create_table.sql file from Blackboard to and move it next to your rest-server.py. 
Create a new database with this table definition using the following command in a terminal:
<br> Windows: `sqlite3.exe files.db ".read create_table.sql"`
<br> macOS and Linux: `sqlite3 files.db ".read create_table.sql"`

### Task 2: Save the protobuf message definition above as messages.proto, and generate Python code from it.
Run the following command after saving the file: `protoc messages.proto --python_out=.`
This should produce the messages_pb2.py source file in the same folder.

### Task 3 to 6
Implementation via code

### Task 7: Test the system on your local computer, using Postman!
First, start the Storage Node program four times in different terminal windows, passing different
folder names:
<pre>
<b>$ python storage-node.py node1</b>
Data folder: node1
Listening on tcp://localhost:5557
</pre>
<pre>
<b>$ python storage-node.py node2</b>
Data folder: node2
Listening on tcp://localhost:5557
</pre>
<pre>
<b>$ python storage-node.py node3</b>
Data folder: node3
Listening on tcp://localhost:5557
</pre>
<pre>
<b>$ python storage-node.py node4</b>
Data folder: node4
Listening on tcp://localhost:5557
</pre>
Then start the controller:
<pre>
<b>$ python rest-server.py</b>
Listening to ZMQ messages on tcp://*:5558
* Serving Flask app "rest-server" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://localhost:9000/ (Press CTRL+C to quit)
</pre>
The REST API is identical to Week 2, so you can test the system with Postman using the same
requests as we did before. The base URL is http://localhost:9000.
Additional Tasks

### Task 8 (optional): Extend the system with the DELETE functionality.
Use a ZMQ socket and message format that fits best for this request.
