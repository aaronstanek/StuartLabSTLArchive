import os
import time

stl_path = "C:/Users/Aaron/Desktop/stl_archive/" #needs correct ending slash

def fileExists(path):
    return os.path.isfile(path)

def loadFile(path):
    infile = open(path,"r")
    data = infile.read()
    infile.close()
    return data

def writeFile(path,data):
    outfile = open(path,"w")
    outfile.truncate(0)
    outfile.seek(0,0)
    outfile.write(data)
    outfile.close()

def spliceIn(ori,spl):
    w = ori.split("SPLITHERE")
    ou = w[0]
    for i in range(len(spl)):
        ou = ou+spl[i]+w[i+1]
    return ou

class stlFile:
    def __init__(self,name,fullPath):
        self.name = name
        self.fullPath = fullPath

class project:
    def __init__(self,name,fullPath):
        self.name = name
        self.fullPath = fullPath
        self.stls = []
    def addSTL(self,name,fullPath):
        self.stls.append(stlFile(name,fullPath))
    def findSTL(self):
        fl = os.listdir(self.fullPath)
        fl.sort()
        for x in fl:
            s = x.split(".")
            if (s[-1]=="stl") and os.path.isfile(self.fullPath+x):
                self.addSTL(str(x[:(len(x)-4)]),self.fullPath+str(x))
    def makeOwnDescription(self,templates):
        des = spliceIn(templates["pdes"],[str(self.name)])
        writeFile(self.fullPath+"description.html",des)
    def makeOwnList(self,templates):
        data = ""
        for x in self.stls:
            data = data+"<a href=\""+x.name+".stl.html\">"+x.name+".stl</a><br><br>"
        lst = spliceIn(templates["plist"],[str(self.name),data])
        writeFile(self.fullPath+"list.html",lst)
    def makeSTLDescription(self,stl,templates):
        pathName = stl.name+".stl"
        des = spliceIn(templates["stl"],[pathName,pathName])
        writeFile(self.fullPath+stl.name+".stl.html",des)
    def addDefaults(self,templates):
        #first for the project
        #if fileExists(self.fullPath+"description.html")==False:
        if True:
            self.makeOwnDescription(templates)
        if True:
            self.makeOwnList(templates)
        for x in self.stls:
            #for each stl
            if fileExists(x.fullPath+".html")==False:
                self.makeSTLDescription(x,templates)

class stl_archive:
    def __init__(self,fullPath):
        self.fullPath = fullPath
        self.projects = []
    def addProject(self,name,fullPath):
        self.projects.append(project(name,fullPath))
    def findAll(self):
        pl = os.listdir(self.fullPath+"projects/")
        pl.sort()
        pl_edit = []
        for x in pl:
            if os.path.isdir(self.fullPath+"projects/"+x):
                pl_edit.append(x)
        for x in pl_edit:
            self.addProject(str(x),self.fullPath+"projects/"+str(x)+"/")
        for x in self.projects:
            x.findSTL()
    def makeMainPage(self,templates):
        data = ""
        for x in self.projects:
            data = data+"<a href=\"projects/"+x.name+"/description.html\">"+x.name+"</a><br><br>"
        dateTime = time.strftime("on %x at %X")
        lst = spliceIn(templates["alist"],[dateTime,data])
        writeFile(self.fullPath+"archive.html",lst)
    def addDefaults(self,templates):
        for x in self.projects:
            x.addDefaults(templates)
        self.makeMainPage(templates)

def loadTemplates(stl_path):
    ou = dict()
    ou["stl"] = loadFile(stl_path+"template_stl.html")
    ou["pdes"] = loadFile(stl_path+"template_pdes.html")
    ou["plist"] = loadFile(stl_path+"template_plist.html")
    ou["alist"] = loadFile(stl_path+"template_alist.html")
    return ou

def main():
    global stl_path
    if os.path.exists(stl_path+"projects")==False:
        os.makedirs(stl_path+"projects")
    arc = stl_archive(stl_path)
    arc.findAll()
    templates = loadTemplates(stl_path)
    arc.addDefaults(templates)

main()
