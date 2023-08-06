import sys
from .app import Snipper

def main():
    snipper = Snipper()
    args = sys.argv[1:]
    if(args[0].lower() == "create"):
        snipper.make_snip(args[1],args[2])
    elif(args[0].lower() == "show"):
        snipper.list()
    elif(args[0].lower() == "open"):
        snipper.open(args[1])
    elif(args[0].lower() == "copy") :
        snipper.copy(args[1])   


if __name__ == '__main__':
    main()