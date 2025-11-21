Task 1 instruction to run on PyCharm

datanode.py needs to be run with a Python template and not FlaskServer template
On the configurations for 'scrip parameters', add the folder name for each node, for example: node1, node2 and node3.
You can choose to configure Modify options -> Allow multiple instances

namenode.py can be run as a FlaskServer template normally.
Set Working directory to be Lab9
You can choose to configure Modify options -> additional option , with argument
--host=localhost --port=9000
