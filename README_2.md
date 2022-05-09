Zip file uploader  
  
-----------------------------------------  
  
Maintainer: X Y; X.Y@Z.com  
  
Script requires at least Python 3.4  
  
-----------------------------------------  
  
Do not open logs.log file wile scrip is running. Windows doesn't like that and script may crash  
If you have to open it during run create a copy  
  
-----------------------------------------  
  
If server address or server key is changed:  
	1.	Holding shift key right click e.g. on a free space on desktop and open and select 'Open PowerShell Window here'  
	2.	Type:   
			ssh -p x y  
		x - port number; probably 22  
		y - server address; previously xxx  
		With old settings this looked like this: ssh -p 22 xxx  
		After this console should ask you if you want to accept connection, type yes and after that you will be asked for password, type it as well  
		This will create entry into file %USERPROFILE%\.ssh\known_hosts file  
		Exit PowerShell and open it again  
	3.	Now in PowerShell type:  
			ssh-keyscan -p x y > 1.txt  
		x - port number; probably 22  
		y - server adress; previously xxx  
		with old settings this looked like this: ssh-keyscan -p 22 xxx > 1.txt  
		This will create file 1.txt; probably on desktop if you right-clicked on desktop  
		Open it. It will contain something like this:  
		xxx ssh-rsa ...  
		If there are multiple entries select and copy that one with 'ssh-rsa' in it (it will contain be a long string of letters and numbers)  
		In key.txt file in Uploader folder delete old entry and paste a new one, save and exit  
	4.	If everything went well script should be working again  
  
-----------------------------------------  

Changelog:  
  
1.0	22.04.2022	First run  
1.1	25.04.2022	User provides password right after entering upload section/loop  
1.2	04.05.2022	Added logging into logs.log file3  
1.21	06.05.2022	Script will wait 10 seconds when it detects a new file at the beginning of the queue (with a name that starts with '01'). Without it, script was crashing sometimes with message:  
			2022-05-06 14:26:18,001 ERROR __main__ [Errno 13] Permission denied: 'waiting\\01_xxx.zip'  
			I believe that windows was blocking access to a file while it was copied to the waiting/ directory by user  
			Script at the same time was trying to move it to tmp/. Now script will wait 10s. It will give some time to finish copying and will allow Windows to unlock the file  
