# Zip Uploader
At work, the team I work for creates and sends a lot of zip files. Previously files was sent to processing team manually one by one at intervals of at least 5 minutes. It was annoying to send it manually also keeping an eye on the clock was distractful, so I created this simple script  

Script is running on one PC on shared drive  

Colleague creates zips (sometimes zips has the same name (requirement from the processing team and this is due to the server specification)), changes its name adding e.g. 01_ at the beginning (depends on an already existing queue) and moves it to waiting/ directory

Script - by default - every one minute checks if something is in waiting/, moves it to tmp/, changes file name removing e.g. '01_', sends it to the server via sftp, changes the name again by adding e.g. 001_ and moves the file to uploaded/ directory

Of course whole process can be done without tmp folder but I wanted to limit any actions in this folder. Files could flash there when user will be adding new files to waiting/, changing names etc. This could be confusing for user, and lead to missclicks etc

Beginning of file names in waiting/ should end on 99_ because its impossible (for now :v) to create that number of files by our team at the same time

Another reason is that ... it's simpler and cleaner


I decided to limit file names in uploaded/ to 999_ to limit this folder from growing too much. Theoretically those files are no longer needed but I wanted to keep them for a while. Maybe we will need them in some specific situation


TO DO; soon (tm)

Add function to remove zips older than e.g. 7 days

Automation of adding the 'waiting/', 'uploaded/' and 'tmp/' folders if they are not present
