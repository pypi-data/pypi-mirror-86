import sys, tempfile, os
import editor
import pyperclip
from os.path import isfile, join
from os import listdir



class Snipper():

    def create_dir(self):
        dir = os.path.join("Snippets")
        os.mkdir(dir)
        
    def list(self):
        onlyfiles = [f for f in listdir("./snippy/Snippets")]
        
        for i in onlyfiles:
            print("----------------------------")
            print(i)
        print("----------------------------")

    def make_snip(self,name,extention):
        code_snippet = editor.edit()
        code_snippet = code_snippet.decode("utf-8")  
        f = open("snippy/Snippets/{}.{}".format(name,extention), "a")
        f.write(code_snippet)
    
    def open(self, name):
        onlyfiles = [f for f in listdir("./snippy/Snippets")]
        
        if(name not in onlyfiles):
            print(" The snippet does not exist ")
        else:
         file = open("snippy/Snippets/"+name,"r+")
          
         result = editor.edit(contents = file.read())

    def copy(self, name):
        onlyfiles = [f for f in listdir("./snippy/Snippets")]
        if(name not in onlyfiles):
            print(" The snippet does not exist ")
        else:
            file = open("./snippy/Snippets/"+name,"r+")
            pyperclip.copy(file.read())




sc = Snipper()






# snipper.create_dir()