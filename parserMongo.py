
"""
FILE: skeleton_parser.py
------------------
Author: Garrett Schlesinger (gschles@cs.stanford.edu)
Author: Chenyu Yang (chenyuy@stanford.edu)
Modified: 10/13/2012

Skeleton parser for cs3057 lab #6. Has useful imports and functions for parsing,
including:

1) Directory handling -- the parser takes a list of eBay xml files
and opens each file inside of a loop. You just need to fill in the rest.

2) Dollar value conversions -- the xml files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.

3) Date/time conversions -- the xml files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

4) A function to get the #PCDATA of a given element (returns the empty string
if the element is not of #PCDATA type)

5) A function to get the #PCDATA of the first subelement of a given element with
a given tagname. (returns the empty string if the element doesn't exist or
is not of #PCDATA type)

6) A function to get all elements of a specific tag name that are children of a
given element

7) A function to get only the first such child

Your job is to implement the parseXml function, which is invoked on each file by
the main function. We create the dom for you; the rest is up to you! Get familiar
with the functions at http://docs.python.org/library/xml.dom.minidom.html and
http://docs.python.org/library/xml.dom.html

Happy parsing!
"""

import sys
import json
from pymongo import MongoClient
from xml.dom.minidom import parse
from re import sub

client = MongoClient('localhost', 27017)
db = client['ebay']
Items = db['Item']
Users = db['User']


columnSeparator = "<>"
categorias = []
paises = []
usuarios = []
bidID = 0;

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
                'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

# Atributos

"""
Returns true if a file ends in .xml
"""
def isXml(f):
    return len(f) > 4 and f[-4:] == '.xml'

"""
Non-recursive (NR) version of dom.getElementsByTagName(...)
"""
def getElementsByTagNameNR(elem, tagName):
    elements = []
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            elements.append(child)
    return elements

"""
Returns the first subelement of elem matching the given tagName,
or null if one does not exist.
"""
def getElementByTagNameNR(elem, tagName):
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            return child
    return None

"""
Parses out the PCData of an xml element
"""
def pcdata(elem):
        return elem.toxml().replace('<'+elem.tagName+'>','').replace('</'+elem.tagName+'>','').replace('<'+elem.tagName+'/>','')

"""
Return the text associated with the given element (which must have type
#PCDATA) as child, or "" if it contains no text.
"""
def getElementText(elem):
    if len(elem.childNodes) == 1:
        return pcdata(elem)
    return ''

"""
Returns the text (#PCDATA) associated with the first subelement X of e
with the given tagName. If no such X exists or X contains no text, "" is
returned.
"""
def getElementTextByTagNameNR(elem, tagName):
    curElem = getElementByTagNameNR(elem, tagName)
    if curElem != None:
        return pcdata(curElem)
    return ''

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return "0.0"
    return sub(r'[^\d.]', '', money)


"""
Parses a single xml file. Currently, there's a loop that shows how to parse
item elements. Your job is to mirror this functionality to create all of the necessary SQL tables
"""
def parseXml(f):


    separador = ">"
    #Crear los arcivos si no existen, abrirlos e modo escribir si no
    usersFile = open("parseados/users.dat","a+")
    itemFile = open("parseados/items.dat","a+")
    bidFile = open("parseados/bids.dat","a+")
    countryFile = open("parseados/country.dat","a+")
    categoryFile = open("parseados/categ.dat", "a+")
    descCategoryFile = open("parseados/descCateg.dat", "a+")
    dom = parse(f) # creates a dom object for the supplied xml file
    """
    TO DO: traverse the dom tree to extract information for your SQL tables
    """
    a = getElementsByTagNameNR(dom, 'Items')
    items = getElementsByTagNameNR(a[0], 'Item')


    for i in items:
        #OBJETOS A SER LLENADOS
        iObj = {
            "_id" : 0.00,
            "name" : "",
            "currently":0.00,
            "category" : [],
            "first_bid" : 0.0,
            "bids" : [],
            "started" : "",
            "ends" : "",
            "buy_price":0.00,
            "seller" : "",
            "description": ""
        }

        uObj = {
            "_id":"",
            "country":"",
            "location":"",
            "rating":0
        }

        #global bidID
        bids =          getElementsByTagNameNR(i, 'Bids')
        bid =           getElementsByTagNameNR(bids[0], 'Bid')
        #sacar todo lo que esta dentro del item
        iID =           str(i.getAttribute('ItemID'))
        name =          getElementText(getElementByTagNameNR(i, 'Name'))
        currently =     transformDollar(getElementText(getElementByTagNameNR(i, 'Currently')))
        first =         transformDollar(getElementText(getElementByTagNameNR(i, 'First_Bid')))
        started =       transformDttm(getElementText(getElementByTagNameNR(i, 'Started')))
        ends =          transformDttm(getElementText(getElementByTagNameNR(i, 'Ends')))
        description =   getElementText(getElementByTagNameNR(i, 'Description'))
        bp =            getElementByTagNameNR(i, 'Buy_Price')

        #Llenar el diccionario
        iObj["_id"] = iID
        iObj["name"] = name
        iObj["currently"] = float(currently)
        iObj["first_bid"] = float(first)
        iObj["started"] = started
        iObj["ends"] = ends
        iObj["description"] = description

        #SACAR TODO LO QUE ESTA DENTRO DEL USUARIO
        sCountry =      getElementText(getElementByTagNameNR(i, 'Country'))
        #CONDICION PARA VER SI YA EXISTEN LOS PAISES
        if sCountry not in paises:
            paises.append(sCountry);
            countryFile.write(str(paises.index(sCountry))+separador+sCountry+"\r\n")
        sLocation =     getElementText(getElementByTagNameNR(i, 'Location'))
        s=              getElementByTagNameNR(i, 'Seller')
        seller =        str(s.getAttribute('UserID'))
        sellerRating =  str(s.getAttribute('Rating'))
        cats = getElementsByTagNameNR(i,'Category')
        uObj["_id"] = seller
        uObj["country"] = sCountry
        uObj["location"] = sLocation
        uObj["rating"] = sellerRating
        iObj["seller"] = seller
        for x in cats:
            cat = getElementText(x)
            iObj["category"].append(cat)
            if cat not in categorias:
                categorias.append(cat)
                categoryFile.write(str(len(categorias)) + separador + cat +"\r\n")
            descCategoryFile.write(str(iID)+separador+str(categorias.index(cat))+"\r\n")
        if seller not in usuarios:
            usuarios.append(seller)
            usersFile.write(seller+separador+sellerRating+separador+str(paises.index(sCountry))+separador+sLocation+"\r\n")
            #usuario
            Users.insert_one(uObj);
        buy_price = 0
        if (bp != None):
            buy_price = getElementText(bp)
        else:
            buy_price = "0.0"
        iObj['buy_price'] = float(transformDollar(buy_price))

        itemFile.write(iID+separador+seller+separador+name+separador+currently+separador+first+separador+started+separador+ends+separador+str(buy_price)+separador+description+"\r\n")

        #SACAR TODO LO QUE ESTA DENTRO DE CADA BID
        for j in bid:
            bObj = {
                "bidder_id":"",
                "time":"",
                "amount":0.0
            }
            bidder = getElementByTagNameNR(j, 'Bidder')
            try:
                bidderLoc = getElementText(getElementByTagNameNR(bidder, 'Location'))
            except Exception as e:
                bidderLoc = "Null"
            try:
                bidderCou = getElementText(getElementByTagNameNR(bidder, 'Country'))
            except Exception as e:
                bidderCou = "Null"
            if bidderCou not in paises:
                paises.append(bidderCou);
                countryFile.write(str(paises.index(bidderCou))+separador+bidderCou+"\r\n")
            time = transformDttm(getElementText(getElementByTagNameNR(j, 'Time')))
            amount = transformDollar(getElementText(getElementByTagNameNR(j, 'Amount')))
            bidFile.write(str(bidID)+separador+iID+separador+str(bidder.getAttribute('UserID'))+separador+time+separador+amount+"\r\n")

            bObj["bidder_id"] = str(bidder.getAttribute('UserID'))
            bObj["time"] = time
            bObj["amount"] = float(amount)
            iObj['bids'].append(bObj)
            if str(bidder.getAttribute('UserID')) not in usuarios:
                usuarios.append(str(bidder.getAttribute('UserID')))
                usersFile.write(str(bidder.getAttribute('UserID'))+separador+str(bidder.getAttribute('Rating'))+separador+str(paises.index(bidderCou))+separador+bidderLoc+"\r\n")
                uObj["_id"] = str(bidder.getAttribute('UserID'))
                uObj["country"] = bidderCou
                uObj["location"] = bidderLoc
                uObj["rating"] = float(str(bidder.getAttribute('Rating')))
                #usuario
                Users.insert_one(uObj)

            #sacar lo que esta dentro de bids
        #Objeto
        Items.insert_one(iObj)

"""
Loops through each xml files provided on the command line and passes each file
to the parser
"""

def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_parser.py <path to xml files>'
        sys.exit(1)
    # loops over all .xml files in the argument
    for f in argv[1:]:
        if isXml(f):
            parseXml(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
