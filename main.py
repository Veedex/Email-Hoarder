import requests
import os
import pickle
from string import ascii_lowercase
import argparse 
import threading
import sys
import time
import string
import argparse
import itertools
import pandas as pd
import re

def check(strg, search=re.compile(r'[^a#]').search):
    return not bool(search(strg))

def inputcandp():
    AUTH=input("[INPUT] Authorization:   ")
    try:
        cookie=input("[INPUT] Cookie:   ")
        SID=re.search(r'SID=(.*?);', cookie).group(1)
        HSID=re.search(r'HSID=(.*?);', cookie).group(1)
        SSID=re.search(r'SSID=(.*?);', cookie).group(1)
        APISID=re.search(r'APISID=(.*?);', cookie).group(1)
        SAPISID=re.search(r'SAPISID=(.*?);', cookie).group(1) 
    except:
        print("[ERROR] Cookie invalid")
        sys.exit()

    APIKEY=input("[INPUT] X-Goog-Api-Key:   ")

    cookie={
        "SID": SID,
        "HSID": HSID,
        "SSID": SSID,
        "APISID": APISID,
        "SAPISID": SAPISID,
        }

    payload={
        'X-Origin': 'https://docs.google.com',
        'Authorization': AUTH,
        'X-Goog-Api-Key': APIKEY,
    }
    return [cookie,payload]

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='Python Wordlist Generator')
parser.add_argument(
    '-char', '--characters',
    default=None, help='Characters to add to wordlist, underscores will count as spaces')
parser.add_argument(
    '-min', '--minimum', type=int,
    default=None, help='The minimum length for the characters')
parser.add_argument(
    '-max', '--maximum', type=int,
    default=None, help='The maximum length for the characters')
parser.add_argument(
    '-wl','--wordlist',
    default=None, help='Name of the wordlist')
parser.add_argument(
    '-s','--speed', type=int,
    default=1, help='The speed the wordlist goes at')
parser.add_argument(
    '-n','--name',
    default="data", help='The name of the csv output file')
args = parser.parse_args()

chrs=args.characters=args.characters
min_length=args.minimum
max_length=args.maximum
nameofdf=args.name

thespeed=round(args.speed)
if args.wordlist==None:
    print("[ERROR] You must choose a wordlist")
    sys.exit()
else:
    wordlist="wordlists/"+str(args.wordlist)+".txt"
for char in nameofdf:
    if char=="*":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char==".":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char=='"':
        print("[ERROR] Invalid name")
        sys.exit()
    elif char=="/":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char=="\\":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char=="[":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char=="]":        
        print("[ERROR] Invalid name")
        sys.exit()
    elif char==":":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char==";":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char=="|":
        print("[ERROR] Invalid name")
        sys.exit()
    elif char==",":
        print("[ERROR] Invalid name")
        sys.exit()
        
if thespeed==None:
    thespeed = 2
    print("[INFO] No speed given, using default")
    

if thespeed<=0:
    print("[ERROR] The speed must be greater than 0.")
    sys.exit()
if thespeed>20:
    print("[ERROR] The speed must be less than or equal to 20.")
    sys.exit()
chosewordlist=False
if min_length==None:
    if max_length==None:
        if chrs==None:
            if os.path.exists(wordlist) == True:
                chosewordlist=True

if chosewordlist==True:
    print("[LOG] Using wordlist "+wordlist)
else:
    if os.path.exists(wordlist) == True:           
        replacefile=input("[INPUT] A file with the path `"+wordlist+"` already exists, do you want to replace it?\n").lower()
        if replacefile=="yes":
            pass
        elif replacefile=="y":
            pass
        elif replacefile=="ye":
            pass
        elif replacefile=="yeah":
            pass
        else:
            print("[INFO] Exiting")
            sys.exit()
    
    if max_length==None:
        max_length=2
        print("[INFO] No maximum length given, using default")
    if min_length==None:
        min_length=1
        print("[INFO] No minimum length given, using default")
    if chrs == None:
        chrs = string.printable.replace(' \t\n\r\x0b\x0c', '')
        print("[INFO] No characters given, using default")
        
        
    round(min_length) 
    round(max_length)
    if min_length > max_length:
        print ("[ERROR] The minimum length must be less than or equal to maximum length")
        sys.exit()
    if min_length<=0:
        print ("[ERROR] The minimum length must be equal to or greater than 1")
        sys.exit()
    if max_length<=0:
        print ("[ERROR] The maximum length must be equal to or greater than 1")
        sys.exit()
    if wordlist==None:
        print("[ERROR] You must choose a wordlist")
        sys.exit()

    thewordlist = open(wordlist, 'w')
    start=time.time()
    for n in range(min_length, max_length + 1):
        for xs in itertools.product(chrs, repeat=n):
            chars = ''.join(xs)
            thewordlist.write("%s\n" % chars.replace("_", " "))
            sys.stdout.write('\r[INFO] Added character(s) `%s` to wordlist' % chars.replace("_", " "))
            sys.stdout.flush()
    thewordlist.close()
    print("\n[INFO] Wordlist created in "+str(time.time()-start))
    print("[LOG] Using wordlist "+wordlist)

while True:
        try:
            print("[LOG] Locating file with saved inputs")
            cookie,payload=pickle.load(open("information.pickle","rb"))
        except:
            print("[LOG] Couldn't locate file, asking for inputs")
            pickle.dump(inputcandp(),open("information.pickle","wb"))
            cookie,payload=pickle.load(open("information.pickle","rb"))
            
        try:
            print("[LOG] Testing cookie and payload")
            requests.request('GET','https://people-pa.clients6.google.com:443/v2/people/autocomplete?query=a&client=PERSONAL_DOMAIN_CONTACT_GROUPS&clientVersion.clientAgent=CONTACT_STORE&clientVersion.clientType=FORMS&pageSize=210&', cookies=cookie,headers=payload)
            print("[LOG] A working cookie and payload was found")
            break
        except:
            print("[ERROR] The inputted information isn't correct")

if thespeed!=1:
    averageresponse=0
    sys.stdout.write("[INFO] Determining average response")
    for i in range(50):
        averageresponse=averageresponse+requests.request('GET','https://people-pa.clients6.google.com:443/v2/people/autocomplete?query=a&client=PERSONAL_DOMAIN_CONTACT_GROUPS&clientVersion.clientAgent=CONTACT_STORE&clientVersion.clientType=FORMS&pageSize=210&', cookies=cookie,headers=payload).elapsed.seconds
        sys.stdout.write(".")
        sys.stdout.flush()
    print("\n[INFO] Average response %s seconds." % str(averageresponse/5))
    print("[INFO] Starting process with a speed of %s." % thespeed)
else:
    print("[INFO] Process starting.")

def extractionprocess(startnums,endnums):
    global df
    content=open(wordlist,"r").readlines()
    while startnums<endnums:
        while True:
            try:
                therequest=requests.request('GET','https://people-pa.clients6.google.com:443/v2/people/autocomplete?query='+content[startnums].strip()+'&client=PERSONAL_DOMAIN_CONTACT_GROUPS&clientVersion.clientAgent=CONTACT_STORE&clientVersion.clientType=FORMS&pageSize=210&', cookies=cookie,headers=payload)
                if therequest.status_code==429:
                    int('a')
                else:
                    break
            except:
                time.sleep(1)
        r=therequest.json()
        for i in range(210):
            try:
                thefirstname=r['results'][i]['person']['name'][0]['givenName']
                thefullname=r['results'][i]['person']['name'][0]['displayName']
                theemail=r['results'][i]['suggestion']
                theprofilepicture=r['results'][i]['person']['photo'][0]['url']
                
                print("[EXTRACTED] [%s] [%s] [%s] [%s]" %(content[startnums].strip(),thefirstname,thefullname,theemail))
                df=df.append({'Given Name':thefirstname,'Display Name':thefullname,'Email':theemail,'Profile Picture':theprofilepicture},ignore_index=True,sort=False)

                sys.stdout.flush()
            except:
                "a"
        df.to_csv(nameofdf+".csv")
        startnums=startnums+1

df=pd.DataFrame(columns=["Given Name","Display Name","Email","Profile Picture"])
if thespeed==1:
    extractionprocess(0,len(open(wordlist,"rb").readlines()))
else:
    threads={}
    for i in range(thespeed):
        threads[i+1]=threading.Thread(target=extractionprocess, args=(
            round(len(open(wordlist,"rb").readlines())/thespeed*i),round(len(open(wordlist,"rb").readlines())/thespeed*(i+1))
            ))
        
        print("[LOG] Thread number %s defined." % str(i+1))

    for i in range(thespeed):
        threads[i+1].start()
        time.sleep(averageresponse/thespeed)