"""
----------------------------------------
  - Developed by Mencho: 08/02/2017

  - Last Update: 09/10/2017
----------------------------------------

- Functions
  - get_links_filter
  - get_links_all
  - encode_ascii
  - read_links
  - get_rss
  - download_file
  - podcast_download
  - mp3_tagging
   -write_file
"""
import os
import csv
import datetime
import warnings
import unicodedata
import socket
from dateutil import parser
import feedparser
import requests
import requests.packages.urllib3
from mutagen.easyid3 import EasyID3
import mutagen


## Timeout Requests
TIMEOUT = 120


def get_links_filter(rss, keyword, number_links):
    """Generate podcast_list with a number_links
       for download in based on a specific keyword 
       and rss list. 

       keyword arguments:
       rss                   --  list with rss elements
       keyword               --  Filter links by keyword 
       number_links          --  Number of links

       Return arguments:
       podcast_list          --  list with 'podcast_data' elements

       Each element of the list contains a unique podcast_data:

       entry.published = u'Thu, 3 Aug 2017 11:09:51 +0100' --> '2017-08-03'
       publishedDate = str(parser.parse(entry.published))[:10]

       podcast_data = [publishedDate, 
                      entry.enclosures[0]['href'], 
                      rss.feed.title]
    
       podcast_data = [u'Thu, 3 Aug 2017 11:09:51 +0100', 
                       u'Tertulia de Federico: M\xe1s ataques de las CUP contra el turismo', 
                       u'http://audios.esradio.fm/espana/17/08/03/
                         tertulia-de-federico-mas-ataques-de-las-cup-contra-el-turismo-116287.mp3', 
                       u'Es la Ma\xf1ana de Federico']
    """
    podcast_list = []
    podcast_data = []

    for entry in rss.entries:
        if keyword in entry.title:          
            try:
                podcast_data = [entry.published, entry.title, 
                                entry.enclosures[0]['href'], 
                                rss.feed.title]
            except IOError as error:
                print 'Error' + (error) + ': File - ' + str(entry.title)
            podcast_list.append(podcast_data)
            if number_links != 0:
                if len(podcast_list) == number_links: 
                    return podcast_list
    return podcast_list


def get_links_all(rss, number_links):
    """Generate podcast_list with a number_links
       for download in based on a rss list. 

       keyword arguments:
       rss                   --  list with rss elements 
       number_links          --  Number of links

       Return arguments:
       podcast_list          --  list with 'podcast_data' elements

       Each element of the list contains 
       a unique podcast_data:

       entry.published = u'Thu, 3 Aug 2017 11:09:51 +0100' --> '2017-08-03'

       podcast_data = [publishedDate, 
                      entry.enclosures[0]['href'], 
                      rss.feed.title]
    
       podcast_data = [u'Thu, 3 Aug 2017 11:09:51 +0100', 
                       u'Tertulia de Federico: M\xe1s ataques de las CUP contra el turismo', 
                       u'http://audios.esradio.fm/espana/17/08/03/
                         tertulia-de-federico-mas-ataques-de-las-cup-contra-el-turismo-116287.mp3', 
                       u'Es la Ma\xf1ana de Federico']
    """
    podcast_list = []
    podcast_data = []

    for entry in rss.entries:
        try:
            podcast_data = [entry.published, entry.title, 
                            entry.enclosures[0]['href'], 
                            rss.feed.title]
        except IOError as error:
            print 'Error' + (error) + ': File - ' + str(entry.title)
        podcast_list.append(podcast_data)
        if number_links != 0:
            if len(podcast_list) == number_links: 
                return podcast_list
    return podcast_list


def encode_ascii(input_str):
    """Encode text to avoid accents and special chars (ASCII)
        
       keyword arguments:
       input_str             --  Input string

       Return arguments:
       Encode ASCII string
    """
    line_unicode = unicode(input_str, "utf-8")
    return unicodedata.normalize('NFKD', line_unicode).encode('ASCII', 'ignore')


def read_links(foldername, filename):
    """Return list with the RSS link save in csv file

       keyword arguments:
       foldername             --  CSV folder
       filename               --  CSV filename 

       Return arguments:
       List with rss links

       rss_links: ['http://esradio.libertaddigital.com/es-la-manana-de-federico/podcast.xml', 
                   'http://www.ondacero.es/rss/podcast/8272/podcast.xml', 
                   'http://feeds.kexp.org/kexp/songoftheday']
    """
    rss_links = []
    file_input = filename

    if foldername:
        file_input = os.path.join(foldername, file_input)
    try:
        with open(file_input, 'rb') as csvfile:
            file_read = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in file_read:
                rss_links.append(row[1])
    except IOError as error:
        print error
    return rss_links


def get_rss(rss_name):
    """Donwload and parse rss file

       keyword arguments:
       rss_name               --  RSS name

       Return arguments:
       RSS list 
    """
    rssfiles = []
    now = datetime.datetime.now() 
    for link in read_links('Links', rss_name):
        rssfiles.append(feedparser.parse(link))
    end = datetime.datetime.now()
    print'RSS download Time = ' + str(end-now) + '\n'
    return rssfiles


def download_file(url, outputfile):
    """Download file (GET URL)

       keyword arguments:
       url               --  podcast url
       outputfile        --  output file

       Return arguments:
       None
    """
    try:
        req = requests.get(url, stream=True, timeout=TIMEOUT)
        try:
            with open(outputfile, 'wb') as file_download:
                for chunk in req.iter_content(chunk_size=1024): 
                    if chunk: 
                        file_download.write(chunk)
        except IOError as error:
            print error
    except requests.exceptions.RequestException as err:
        print err
    except socket.error as err:
        print err
    return None


def podcast_download(podcast_list):
    """Manage the podcast donwload, record in a 
       log file and convert the file to a tagged mp3

       keyword arguments:
       podcast_list      --  podcast data

       Return arguments:
       None

       podcast_data = [u'Thu, 3 Aug 2017 11:09:51 +0100', 
                       u'Tertulia de Federico: M\xe1s ataques de las CUP contra el turismo', 
                       u'http://audios.esradio.fm/espana/17/08/03/
                         tertulia-de-federico-mas-ataques-de-las-cup-contra-el-turismo-116287.mp3', 
                       u'Es la Ma\xf1ana de Federico']
    """
    warnings.filterwarnings("ignore", category=UnicodeWarning)   
    published, name, link, title = podcast_list
    now = datetime.datetime.now()
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    if not os.path.exists('logs'):
        os.makedirs('logs')
    download_log = os.path.join('logs', 'log_download.csv')
    if not os.path.exists(download_log):    
        file(download_log, 'w').close()
        line_file = str('podcast_date' + ';' + 'podcast_title' + 'Name' + ';' + 'Link' + ';')
        write_file(download_log, line_file.encode("UTF-8"))     
    if podcast_list != []:
        line_file = (published + ';' + title + ';' + name + ';' + link).encode("utf-8") 
        if line_file in open(download_log).read():
            pass
        else:
            title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore')
            download_folder = os.path.join('downloads', title)
            if not os.path.exists(download_folder): 
                os.makedirs(download_folder)
            try:
                published = str(parser.parse(published))[:10]
            except IOError as error:
                print 'Error' + (error) + ': File - ' + str(title)
            download_folder = os.path.join(download_folder, published)
            if not os.path.exists(download_folder): 
                os.makedirs(download_folder)
            namefile_unicode = link[link.rfind('/')+1:]
            namefile_str = unicodedata.normalize('NFKD', namefile_unicode).encode('ASCII', 'ignore')
            namefile_str = namefile_str.decode('utf-8', 'ignore').encode("utf-8")
            if '.mp3' in namefile_str:
                len_name = namefile_str.index('.mp3')
            elif '.MP3' in namefile_str:
                len_name = namefile_str.index('.MP3')
            namefile_str = namefile_str[:len_name + 4]
            fileoutput = os.path.join(download_folder, namefile_str)
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore')
            print 'Downloading: ' + name
            print 'Date: ' + str(published)
            download_file(link, fileoutput) 
            mp3_tagging(fileoutput, podcast_list)
            write_file(download_log, line_file)
            end = datetime.datetime.now()
            print 'Download Time = ' + str(end-now) + '\r'
    return None


def mp3_tagging(file_input, podcast_list):
    """Tagging mp3 files
       
       keyword arguments:
       file_input      --  podcast filename
       podcast_list    --  podcast data

       Return arguments:
       None
    """
    try:
        tag = EasyID3(file_input)
    except mutagen.id3.ID3NoHeaderError:
        tag = mutagen.File(file_input, easy=True)
        tag.add_tags()
    tag['album'] = podcast_list[3]
    tag.save(v2_version=3)
    return None


def write_file(file_name, line):
    """ Writing File

        keyword arguments:
        file_input      --  log file
        line            --  podcast log line

        Return arguments:
        None
    """
    try:
        with open(file_name, "a") as filename:
            filename.write(line)
            filename.write('\n')
    except IOError as error:
        print error
    return None
