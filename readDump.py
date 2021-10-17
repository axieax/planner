from sqlalchemy import *
import json
import re

def makeDB():
    engine = create_engine("postgresql://postgres:postgres@localhost/degrees", echo=True, future=True)
    meta = MetaData(engine)
    degrees = Table(
        'degrees', meta,
        Column('id', Integer, primary_key = True), 
        Column('courseCode', String),
        Column('offerings', String),
        Column('prereqs', String),
        Column('uoc', Integer),
        Column('title', String)
    )
    meta.create_all(engine)
# first you need to set up sql with the dbname "degrees"
def sqlMake(dump):
    for myJson in dump:
        try:
            uoc = myJson['creditPoints']
        except:
            uoc = 0
        
        title = myJson['title']
        data = json.loads(myJson['data'])

        try:
            offerings = data['offering_detail']['offering_terms'].split("Term")
            if offerings[0] == 'Summer ':
                offerings[0] = '0'
            else:
                del offerings[0]
            offerings = [*map(cleanOffering, offerings)]
        except:
            offerings = [-1]

        try:
            prereqs = data['enrolment_rules']
            prereqs = "\n".join([*map(lambda a: cleanPrereq(a), prereqs)])
        except:
            prereqs = 'not found'
        

        courseCode = myJson['urlMap'].split('/')[-2]
        mydict = {}
        mydict['courseCode'] = courseCode
        mydict['prereqs'] = prereqs
        mydict['uoc'] = uoc
        mydict['offerings'] = offerings
        mydict['title'] = title
        return mydict


def cleanPrereq(rawPrereq):
    unHTMLedPrereq = re.sub("<.*?>", " ", rawPrereq['description'])
    return unHTMLedPrereq.strip()
def cleanOffering(offering):
    try:
        return int(re.sub(',', '', offering.strip()))
    except:
        return -1

if __name__ == '__main__':
    #makeDB()
    jsonObject = {}
    for dumpInt in range(0, 7114, 100):
        with open(f"./dumps/dump from {dumpInt}", mode='r') as file:
            dump = json.loads(file.read())
            returnedDict = sqlMake(dump)
            jsonObject[returnedDict["courseCode"]] = returnedDict
    print(json.dumps(jsonObject))