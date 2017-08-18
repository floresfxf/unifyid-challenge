import operator, urllib2
from struct import pack
from PIL import Image
from numpy import random #used only for testing/debugging PIL


MIN_MAX_LEN = 10000000000
MIN_NUM_LEN = 1
MAX_NUM_LEN = 100000
MIN_COL_LEN = 1
MAX_COL_LEN = 10000000000
MIN_STR_LEN = 1
MAX_STR_LEN = 20
useragent = "client: %s | email addr: %s" % ('Francisco Flores','floresfxf@gmail.com')
#adding required headers (docs)

def IntegerGeneratorList(num,nmin,nmax,col=1,base=10,rnd="new"):#set base to 10 since I will only be using decimal integers
        #Perform checks
        quota = QuotaChecker()
        if quota < 0:#Will not proceed if I am past the quota limit and warn me (prevents ban)
            print "You have a negative quota (%d). Try your request again in ten minutes." % quota
            return None
        if num < MIN_NUM_LEN or num > MAX_NUM_LEN: #checks if requests stay within guidelines
            return None
        if nmin < -MIN_MAX_LEN or nmin > MIN_MAX_LEN:
            return None
        if nmax < -MIN_MAX_LEN or nmin > MIN_MAX_LEN:
            return None
        if nmin > nmax:
            return None
        if col < MIN_COL_LEN or col > MAX_COL_LEN:
            return None
        if reduce(operator.and_,[base != 2, base != 8, base != 10, base != 16]) == True: #checks correct base
            return None
        numlst = []#return list
        url = "http://www.random.org/integers/?num=%d&min=%d&max=%d&col=%d&base=%d&format=plain&rnd=%s" \
            % (num,nmin,nmax,col,base,rnd) #using % notation for readability sake 
        req = urllib2.Request(url)
        req.add_header('User-Agent',useragent)#IMPORTANT: Including headers as specified in docs
        opener = urllib2.build_opener()
        u = opener.open(req)
        map(lambda i: map(lambda j: numlst.append(float(j)),i.split()),u.readlines())#Processes response into usable array
        return numlst
def QuotaChecker(ipaddr=None): #"Client to examine remaining quota at regular interval" - Guidelines
        if ipaddr == None:  #quote will appear on the first index of response
            url = "http://www.random.org/quota/?format=plain"
            req = urllib2.Request(url)
            req.add_header('User-Agent',useragent)
            opener = urllib2.build_opener()
            u = opener.open(req)
            return int(u.readlines()[0])
        else: #added functionlity to add IP to request
            url = "http://www.random.org/quota/?ip=%s&format=plain" % (ipaddr)
            req = urllib2.Request(url)
            req.add_header('User-Agent',useragent)
            opener = urllib2.build_opener()
            u = opener.open(req)
            return float(u.readlines()[0])
def main():
    colors = []
    width = 128
    height = 128
    max_reqs = 10000 # must request 10000 numbers or shorter (sequence docs)
    total = width*height*3 #must fill byte array with enough values
    while total > max_reqs:
        byteArr = IntegerGeneratorList(max_reqs, 0, 255)
        if byteArr == None: #Breaks cleanly if user is over quota
            return
        colors+= byteArr
        total -= max_reqs
    colors += IntegerGeneratorList(total, 0, 255) #get remaining amount of numbers for byte array
    print colors
    image = Image.frombytes(#convert from byte array to image
            'RGB',
            size=(128, 128),
            data=''.join([pack('B', x) for x in colors]),
            )
    image.save('img','JPEG')#save image as JPEG, chose to override format parameter
    print "Successfully saved"
    
    
if __name__== "__main__":
  main()
