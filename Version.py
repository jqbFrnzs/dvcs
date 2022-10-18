from mimetypes import init
import os
import glob
import sys
import shutil



class Versioning():

    def __init__(self,fileName):
        self.name = fileName;
        self.version = '';

    def versionNumbering(self):
        
        filename = os.path.basename(self.name);\
        print('file name: ',filename);

        print("1st step take out the extension", )
        concatName = filename[:-4];
        print(concatName);

        count = 0;

        print('2nd step search in directory for occurences of selected file name')
        filelist = os.listdir(directory);
        print('Total files: ',len(filelist));

        for f in filelist:
            if(concatName in f):
                count+=1;

        print('Matching files: ',count);

        listOfDigits = [int(digit) for digit in str(count)];

        version = '';

        try:
            for i in listOfDigits:
                version = version + str(i);
                version += '.';
        except IndexError:
            print('EOF')

        print('version:',version[:-1]);
        self.version = version[:-1];

        return version[:-1];


    def saveGeneratedFile(self):
        sourceFileObject = open(self.name);
        
        print('Generating finished file',self.name);
        extension = self.name[-4:];
        genFileName = self.name[:-4];
        separator = '_'
        print(genFileName);
        print(extension);
        print(self.version);

        result = genFileName + separator + self.version + extension;

        print(result);
        shutil.copy(self.name,result);


    def closeFile(self,file):
        file.close();

###########################

path ='C:\\Users\\margo\\Projekt';
folder = 'spot';

print("Please remember that file name can't contain '_' and has to have extension example TEST.txt ");

filename = 'pliczek.txt';
if(filename.find('_')== True):
    print("your file name contains '_' ending program");
else:
    directory = os.path.join(path,folder);
    os.makedirs(directory,exist_ok=True);
    print("I'm printing directory here: ",directory)
    print("I'm printing directory and file here: ",directory + "\\" + filename);

#fileObj = open(directory + '\\' + filename, "r");

    file = directory + '\\' + filename;

#initialize object from class

    for i in range(50):
        fileObj = Versioning(file);
        fileObj.versionNumbering();
        fileObj.saveGeneratedFile();
        fileObj.closeFile;