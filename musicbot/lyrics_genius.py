# -*- coding: utf-8 -*-

import sys
import re
import urllib.parse
import urllib.request
import json
import csv
import codecs
import os
import socket
from socket import AF_INET, SOCK_DGRAM

def load_credentials():
    lines = [line.rstrip('\n') for line in open('credentials.ini')]
    chars_to_strip = " \'\""
    for line in lines:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        #Currently only need access token to run, the other two perhaps for future implementation
        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
    return client_id, client_secret, client_access_token

async def search(search_term,client_access_token, number_page=5):
    page=1
    lyrics_results = []
    while page < number_page+1:
        querystring = "http://api.genius.com/search?q=" + urllib.parse.quote(search_term) + "&page=" + str(page)
        request = urllib.request.Request(querystring)
        request.add_header("Authorization", "Bearer " + client_access_token)
        request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
        while True:
            try:
                response = urllib.request.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
                raw = response.read().decode('utf-8')
            except socket.timeout:
                print("Timeout raised and caught")
                continue
            break
        json_obj = json.loads(raw)
        body = json_obj["response"]["hits"]

        num_hits = len(body)
        if num_hits==0:
            if page==1:
                print("No results for: " + search_term)
            break
        #print("page {0}; num hits {1}".format(page, num_hits))

        for result in body:
            result_id = result["result"]["id"]
            title = result["result"]["title"]
            url = result["result"]["url"]
            path = result["result"]["path"]
            header_image_url = result["result"]["header_image_url"]
            annotation_count = result["result"]["annotation_count"]
            pyongs_count = result["result"]["pyongs_count"]
            primaryartist_id = result["result"]["primary_artist"]["id"]
            primaryartist_name = result["result"]["primary_artist"]["name"]
            primaryartist_url = result["result"]["primary_artist"]["url"]
            primaryartist_imageurl = result["result"]["primary_artist"]["image_url"]
            lyrics_results.append(title + " : " + url + "\n")
        page+=1
    return lyrics_results

def main():
    search_term = "Blackpink"
    client_id, client_secret, client_access_token = load_credentials()
    print(search(search_term, client_access_token))

if __name__ == '__main__':
    main()