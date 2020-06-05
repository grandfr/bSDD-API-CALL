import requests

"""
 bSDD API CALLS
 (c) Frederic Grand
 grandfr@gmail.com
"""

email = "myemail@myprovider.com"
password = "*****"
#API_Endpoint = "http://bsdd.buildingsmart.org/api/4.0/"    
API_Endpoint = "http://test.bsdd.buildingsmart.org/api/4.0/"    


class bsddPostman():
    
    cookie = ''

    def setHeader(self):                 
        if self.cookie == '':
         myheader = {
          'content-type': 'application/json',
          'Accept' :'application/json', # We want JSON
         }
        else : 
         myheader = {
          'content-type': 'application/json',
          'Accept' :'application/json', # We want JSON
          'Cookie' : self.cookie
         }
        return myheader    
    
    def get(self, _resource, _params):
        print("--------------- GET --------------- ")
        print("--------------- " + _resource)
        resp = requests.get(API_Endpoint + _resource, headers=self.setHeader() , data=_params)
        print(resp.text) #uncomment to see the result of the call in the console
        #sometimes it is needed to be able to access the header of the response
        self.header = resp.headers
        print("----------------------------------- ")
        return resp.json()

    def post(self, _resource, _params):
        print("--------------- POST --------------- " + _resource)
        resp = requests.post(API_Endpoint + _resource, data=_params, headers=self.setHeader())
        #print(resp.text) #uncomment to see the result of the call in the console
        #sometimes it is needed to be able to access the header of the response
        self.header = resp.headers
        print("----------------------------------- ")
        return resp.json()

    def login(self):
        print("--------------- LOGIN --------------- " )
        payload = {
            "email" : email,
            "password" : password
        }
        resp = requests.post(API_Endpoint + "session/login", data=payload, headers=self.setHeader())
        #Get the cookie, needed for API calls needing specific right access
        self.cookie = resp.headers['Set-Cookie']
        #Get the peregrine session id
        self.sessionID = resp.json()['guid']
        #guid of the connected user
        self.userID = resp.json()['user']['guid']
        #email of the connected user
        self.userName = resp.json()['user']['email']
        print("----------------------------------- ")
        return resp.json()
    
bsdd = bsddPostman()

#---------------------------------------------------
#                        Login                     #
#---------------------------------------------------

bsdd.login()
print ("cookie : " + bsdd.cookie)
print ("user connected : " + bsdd.userName)
print ("session id : " + bsdd.sessionID)


#---------------------------------------------------
#                        Search                    #
#---------------------------------------------------

#Define the search string
searchString = "wall"

print ("---------------------- Searching bSDD for : " + searchString)

response = bsdd.get("IfdConcept/search/" + searchString, "")

#Browse the results
counter = 0
for item in response['IfdConcept']:
    print("found " + item['conceptType'] + " (" + item['guid'] +")")
    counter = counter + 1

print (str(counter) + " result(s)")
print bsdd.header

#------------------------------------------------------
#              Query a concept from its guid          #
#------------------------------------------------------

#Define the guid to query
conceptGuid = "0Q6r2s4Kv6jfSUNP5b90D5"

print ("---------------------- Query bSDD for : " + conceptGuid)
response = bsdd.get("IfdConcept/" + conceptGuid, "")
#Concept type
print ("concept found is a ") + response['conceptType']
#Names of the found concept and the attached language
print("#------------------------------------------------------")
print("#                    names of the concept by language #")
print("#------------------------------------------------------")
for item in response["fullNames"]:
    print ( item['language']["nameInEnglish"] + " : " + item['name'])

#------------------------------------------------------
#              Query all concept of a conceptType     #
#------------------------------------------------------

conceptType = 'BAG'

print ("---------------------- Query bSDD for all " + conceptType)

#params ={
#    'page' : '' #to be filled to access next pages
#}
response = bsdd.get("IfdConcept/filter/" + conceptType, "")
#if there are more results, the header "Next-page" in the answser provides the code to send in a new call as the parameter "page"
nextPage = bsdd.header['Next-Page'] 
#Browse the results
counter = 0
for item in response['IfdConcept']:
    print("found " + item['conceptType'] + " (" + item['guid'] +")")
    counter = counter + 1

print (str(counter) + " result(s)")
print ('next page : ' + nextPage)
