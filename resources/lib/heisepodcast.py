#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# heise podcast - The video Podcast Kodi Plug-in
# by Oscar Open & Achim Barczok

import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import feedparser
from bs4 import BeautifulSoup
import requests

def run():
    #Selbst-Referenzierung fürs Plug-in
    base_url = sys.argv[0]
    addon_handle = int(sys.argv[1])
    args = urlparse.parse_qs(sys.argv[2][1:])
    
    #Siedle Plug-in in den Bereich Video
    xbmcplugin.setContent(addon_handle, 'video')

    def build_url(query):
        return base_url + '?' + urllib.urlencode(query)

    mode = args.get('mode', None)

    if mode is None:
        url = build_url({'mode': 'folder', 'foldername': 'heiseshow'})
        li = xbmcgui.ListItem('#heiseshow', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

        url = build_url({'mode': 'folder', 'foldername': 'ctuplink'})
        li = xbmcgui.ListItem('c\'t uplink', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        
        url = build_url({'mode': 'folder', 'foldername': 'kurzinformiert'})
        li = xbmcgui.ListItem('Kurz informiert', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        
        url = build_url({'mode': 'folder', 'foldername': 'nachgehakt'})
        li = xbmcgui.ListItem('Nachgehakt', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(addon_handle)

    elif mode[0] == 'folder':
        foldername = args['foldername'][0]
        if foldername == 'heiseshow':
            #generate heiseshow list
            d = feedparser.parse('http://www.heise.de/heiseshowhd.rss')
            listing = []
            
            for item in d['entries']:
                title = item['title']
                url = item.enclosures[0].href
                
                summary = item['description']    
                
                try:
                    thumb = item['image'].href
                except:
                    thumb = "https://heise.cloudimg.io/bound/480x270/q75.png-lossy-75.webp-lossy-75.foil1/_www-heise-de_/ct/imgs/04/1/4/2/6/3/2/5/9cc02d4fe2a3a731.jpeg"
            
                list_item = xbmcgui.ListItem(label=title, label2=summary)
            
                #Fanart des Plug-ins als Hintergrundbild nutzen
                ctuplink_plugin = xbmcaddon.Addon('plugin.video.heiseshowrss')
                list_item.setArt({'fanart': ctuplink_plugin.getAddonInfo('fanart'), 'thumb': thumb})
                
                list_item.setProperty('IsPlayable', 'true')            
                list_item.setInfo('video', {'plot': summary})
                listing.append((url, list_item, False))    
                    
            xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
            xbmcplugin.endOfDirectory(addon_handle, succeeded=True)
        elif foldername == 'ctuplink':
                #generate c't uplink list
                d = feedparser.parse('https://blog.ct.de/ctuplink/ctuplinkvideohd.rss')
                
                listing = []
                
                for item in d['entries']:
                    title = item['title']
                    url = item.enclosures[0].href
                    date = item['published']
                    summary = item['description']

                    try:
                        thumb = item['image'].href
                    except:
                        thumb = "https://heise.cloudimg.io/bound/480x270/q75.png-lossy-75.webp-lossy-75.foil1/_www-heise-de_/ct/imgs/04/1/4/2/6/3/2/5/9cc02d4fe2a3a731.jpeg"
                
                    list_item = xbmcgui.ListItem(label=title, label2=summary)
                
                    #Fanart des Plug-ins als Hintergrundbild nutzen
                    ctuplink_plugin = xbmcaddon.Addon('plugin.video.ctuplinkrss')
                    list_item.setArt({'fanart': ctuplink_plugin.getAddonInfo('fanart'), 'thumb': thumb})
                    
                    list_item.setProperty('IsPlayable', 'true')            
                    list_item.setInfo('video', {'plot': summary, 'aired': date})
                    listing.append((url, list_item, False))    
                        
                xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
                xbmcplugin.endOfDirectory(addon_handle, succeeded=True)

        elif foldername == 'kurzinformiert':
                #generate kurz informiert list
                d = feedparser.parse('https://www.heise.de/rss/topnews-video.rss')
                
                listing = []
                
                for item in d['entries']:
                    title = item['title']
                    url = item.enclosures[0].href
                    date = item['published']
                    summary = item['description']

                    try:
                        thumb = item['image'].href
                    except:
                        thumb = "https://heise.cloudimg.io/bound/480x270/q75.png-lossy-75.webp-lossy-75.foil1/_www-heise-de_/ct/imgs/04/1/4/2/6/3/2/5/9cc02d4fe2a3a731.jpeg"
                
                    list_item = xbmcgui.ListItem(label=title, label2=summary)
                
                    #Fanart des Plug-ins als Hintergrundbild nutzen
                    ctuplink_plugin = xbmcaddon.Addon('plugin.video.ctuplinkrss')
                    list_item.setArt({'fanart': ctuplink_plugin.getAddonInfo('fanart'), 'thumb': thumb})
                    
                    list_item.setProperty('IsPlayable', 'true')            
                    list_item.setInfo('video', {'plot': summary, 'aired': date})
                    listing.append((url, list_item, False))    
                        
                xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
                xbmcplugin.endOfDirectory(addon_handle, succeeded=True)
        
        elif foldername == 'nachgehakt':
                #generate kurz informiert list
                URL = 'https://www.heise.de/ct/entdecken/?hauptrubrik=%40ctmagazin&unterrubrik=nachgehakt'
                page = requests.get(URL)

                soup = BeautifulSoup(page.content, 'html.parser')
                art_elems = soup.find_all('article')

                d = feedparser.parse('https://www.heise.de/rss/topnews-video.rss')
                
                listing = []
                
                for item in art_elems[0:10]:
                    title = item.h3.text
                    url = art_elems[0].find_all('a')[1]['href']
                    date = item.find('li', class_='teaser_date').text
                    summary = item.find('div', class_='teaser_text').text

                    try:
                        thumb = item.img['src']
                    except:
                        thumb = "https://heise.cloudimg.io/bound/480x270/q75.png-lossy-75.webp-lossy-75.foil1/_www-heise-de_/ct/imgs/04/1/4/2/6/3/2/5/9cc02d4fe2a3a731.jpeg"
                
                    list_item = xbmcgui.ListItem(label=title, label2=summary)
                
                    #Fanart des Plug-ins als Hintergrundbild nutzen
                    ctuplink_plugin = xbmcaddon.Addon('plugin.video.ctuplinkrss')
                    list_item.setArt({'fanart': ctuplink_plugin.getAddonInfo('fanart'), 'thumb': thumb})
                    
                    list_item.setProperty('IsPlayable', 'true')            
                    list_item.setInfo('video', {'plot': summary, 'aired': date})
                    listing.append((url, list_item, False))    
                        
                xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
                xbmcplugin.endOfDirectory(addon_handle, succeeded=True)
