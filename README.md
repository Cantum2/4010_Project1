# 4010_Project1
This project will ask for a exe file from the cli and generate an html report with useful information such as, compiled date, imports, functions, strings etc. 

### How does this work? 
The python generates an html string which is then read to an html file. In the html header we declare use of a __JS__ and a __CSS__ file. The JS file is used to make the page more dynamic while the css is used to make everything look better(well thats the idea of css). 

## Set up
1. Make sure you have python downloaded if you dont go [here](https://www.python.org/downloads/)
2. Download an editor such as [Pycharm](https://www.jetbrains.com/pycharm/), [VsCode](https://code.visualstudio.com/download) or [Anaconda](https://www.anaconda.com/distribution/)
3. Once the editor you choose is configured create a folder for this project and run: `git clone https://github.com/Cantum2/4010_Project1.git`

## Running
Great! Now lets run the code. This could vary depending on editor. For the most part just click the giant play button where ever you see it. Enter the file path or just press enter for the default file. If you would like to analyze a new file just run the script again.

### Running Notes
1. You will be prompted to enter a password which is `mal-ware`. This *isnt* for security! This is just to make sure that you are in a vm if you are analyzing a potentially malicious executable. 
2. I have included two exe files. They are both of the [Strings](https://docs.microsoft.com/en-us/sysinternals/downloads/strings) library from microsoft. One is packed with upx and one is not.
3.  I also included the upx files so you can pack files as needed just shove the file into the dir containing the upx.exe file and cd into that directory. Then run `upx file_name.exe` and it will pack it
4. The script will generate the `index.html` file. Open that file in a browser and it will have the results. 

## Samples
View the current `index.html` file in a browser to see a sample of an analysis done on `notepad.exe`

## Contributing
1. git pull
2. git add .
3. git commit -am "ENTER YOUR MESSAGE HERE"
4. git push

## Testing
1. Tests are in the tests.py file and should try to pass

## Goals of the project
### Part 1 goals
- add security measure to make sure we aren't running this no in a vm?
- run analysis of the strings and create a regex to match ip addresses 
 so we can predict outbound network traffic

- use packer detection to determine if file is packed or not and if so with what
- get date compiled with the pe.dump_info()
- list imports
- functionality will be tough to do 

### Part 2 goals
- we can create a simple web page 
- we can also make the pe file that is good seem malicous. 
- add a button to make the file seem good
