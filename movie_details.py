#It is just a simple script which displays the movie details like - 
#Movie Summary, Directors, Stars, Rating, Trailer from IMDb - Movies, TV and Celebrities .

import requests
import unicodedata
from bs4 import BeautifulSoup
 
def get_url_response(url):
    result = requests.get(url)
    return BeautifulSoup(result.content,"html.parser")
    
def find_movie(movie_name):
    url = "http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=all" %movie_name
    soup = get_url_response(url)
    article = soup.find_all("table",{"class":"findList"})[0]
    table_row = article.find_all("tr")
    a_tag = table_row[0].find_all("a")
    url_for_movie ="http://www.imdb.com" + a_tag[1].get('href')
    i=0
    print "\n!!! SEARCHED RESULTS : !!!\n"
    for movies in table_row:
        print str(i+1) + ") " + table_row[i].text.lstrip()
        i=i+1
 
    soup = get_url_response(url_for_movie)
    print "\n!!! ACCORDING TO OUR SEARCH RESULTS THERE ARE %i MOVIES !!!\n" %i
    print "\n!!! SEARCHING RECORD FOR THE LATEST MOVIE i.e. 1) %s" %table_row[0].text.lstrip()
    i=0
    while i<3:
        print "\n--------------------------------------------------------\n"
        print "\n!!! MENU !!! : \n"
        print "\n1) SUMMARY \n2) TRAILER \n3) RATING\n"
        print "\nENTER YOUR CHOICE: \t"
        ch = int(input())
        if ch==1:
            print "\n!!! SUMMARY !!!\n"
            summary = soup.find_all("div",{"class":"summary_text"})[0]
            print summary.text.lstrip()
            credit_summary = soup.find_all("div",{"class":"credit_summary_item"})
            print "\nDIRECTOR : " + credit_summary[0].span.text.lstrip()
            print "\nWRITER : " + credit_summary[1].span.text.lstrip()
            actors = credit_summary[2].find_all("span",{"itemprop":"actors"})
            j=0
            s=""
            for a in actors:
                s = s + actors[j].text
                j=j+1
            print "\nSTARS : " + s
 
        elif ch==2:
            print "\n !!! TRAILER !!!\n"
            trailer = "http:/www.imdb.com" + soup.find_all("div",{"class":"slate"})[0].find_all("a")[0].get('href')
            print "TRAILER: " + trailer
        elif ch==3:
            print "\n !!! RATING FROM IMDB !!! : \n"
            rating = soup.find_all("div",{"class":"ratingValue"})[0].find_all("strong")[0].text
            print rating + " out of 10 \nRated by %s users.\n" % soup.find_all("div",{"class":"imdbRating"})[0].find_all("a")[0].span.text
        i=i+1
 
if __name__ == '__main__':
    print "!!!! WELCOME TO MOVIE FINDER !!! \n"
    print "Enter movie name to be searched : \t"
    movie_name = raw_input()
    find_movie(movie_name)
