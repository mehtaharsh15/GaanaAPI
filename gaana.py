#Old Handler
from bs4 import BeautifulSoup
import requests
import lxml
#New Handler
from Crypto.Cipher import AES
import re
import sys
import os
import argparse
from json import JSONDecoder
from traceback import print_exc
import m3u8
import base64
import subprocess
#Add Metadata
import eyed3
import lyricwikia
unpad = lambda s : s[0:-ord(s[-1])]
REGEX = re.compile('> ({[^<]*}) <')
JSONDEC = JSONDecoder()
DOWN_FOLDER = '.'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}

def fix_share_url(s):
    s=s.replace("\\",'')
    s='https://gaana.com'+s
    return (s)

def decryptLink(message):
    IV = 'asd!@#!@#@!12312'.encode('utf-8')
    KEY = 'g@1n!(f1#r.0$)&%'.encode('utf-8')
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    #message=message.encode('utf-8')
    return unpad((aes.decrypt(base64.b64decode(message))).decode('utf-8'))

def fix_artist_name(t):
    t=t.split(',')
    l=[]
    for i in t:
      i=i.split('#')[0]
      l.append(i)

    singers=''
    for i in l:
      singers=singers+i+', '
    singers=singers[:len(singers)-2]
    return singers

def downloadAndParsePage(link):
    response=''
    try:
        response = requests.get(link,headers=headers).text
    except Exception as e:
        print(e)
    raw_songs = list(set(REGEX.findall(response)))
    songs = []
    for raw_song in raw_songs:
        json_song = JSONDEC.decode(raw_song)
        enc_message = None
        try:
            if 'high' in json_song['path']:
                enc_message = json_song['path']['high'][0]
            elif 'medium' in json_song['path']:
                enc_message = json_song['path']['medium'][0]
            elif 'normal' in json_song['path']:
                enc_message = json_song['path']['normal'][0]
            else:
                #print(json_song)
                enc_message = json_song['path']['auto'][0]


            song = {'title' : json_song['title'],
                    'album' : json_song['albumtitle'],
                    'thumb' : json_song['albumartwork_large'],
                    'language' : json_song['language'],
                    'gaana_url' : fix_share_url(json_song['share_url']),
                    'duration' : json_song['duration'],
                    'artist' : json_song['artist'],
                    'released' : json_song['release_date'],
                    'bitrate' : enc_message['bitRate'],
                    'link' : decryptLink(enc_message['message'])
            }
            songs.append(song)
        except Exception as e:
            pass
    return songs

#print(downloadAndParsePage('https://gaana.com/song/vaaste'))
