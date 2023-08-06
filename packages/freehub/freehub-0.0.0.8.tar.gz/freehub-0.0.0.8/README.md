#freehub
With one command, upload file to freehub , or download from freehub. Easy to use.

#install
```shell script
pip3 install freehub
``` 

#usage
```shell script
#upload
freehub upload path(can be file or directory) [key](key is optional,by default is the same as path)
 
#upload file
freehub upload a.jpg a 
#upload directory
freehub upload demo demo

#download
freehub download key(the key you use for uploading) [path](optional, default value: "./")

#download file
freehub download a ./downloads
#download directory
freehub download demo ./downloads
```