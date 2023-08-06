from pysondb import db

def addtests():
    a=db.getDb("test.json")
    x=a.add({"name":"test"})
    assert type(x) == int
def gettests():
    pass
def wrongaddtest():
    pass
def updatetest():
    pass
def deletetest():
    pass    
if __name__=="__main__":
    addtests()
    gettests()
    wrongaddtest()
    updatetest()
    deletetest()
    
    print("All tests have passed")
