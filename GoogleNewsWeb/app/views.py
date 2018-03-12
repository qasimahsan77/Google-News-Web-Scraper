"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from datetime import datetime
from bs4 import BeautifulSoup
import json
import smtplib
import requests
import time

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })

def SendEmailLink(Keyword, url, Title, Image):
    print('\t\t\t  Sending Email  ')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("yello5w7@gmail.com", "zxcv75321")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "News Link"
    msg['From'] = 'yello5w7@gmail.com'
    msg['To'] = 'yello5w7@gmail.com'
    text = "Keyword:" + Keyword + '\n'"URL:" + url + '\n'"Title:" + Title + '\n'"Image:" + Image
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)
    server.sendmail("yello5w7@gmail.com", "yello5w7@gmail.com", msg.as_string())
    print('\t\t\t  Email Send Succssfully  ')
    server.quit()
    pass


def SendEmailLinks(Keyword, url, Title, Image, Title_2, Image_2):
    print('\t\t\t  Sending Email  ')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("yello5w7@gmail.com", "zxcv75321")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "News Link"
    msg['From'] = 'yello5w7@gmail.com'
    msg['To'] = 'yello5w7@gmail.com'
    text = "Keyword:" + Keyword + '\n'"URL:" + url + '\n'"Title:" + Title + '\n'"Image:" + Image + '\n'"Title:" + Title_2 + '\n'"Image:" + Image_2
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)
    server.sendmail("yello5w7@gmail.com", "yello5w7@gmail.com", msg.as_string())
    print('\t\t\t  Email Send Succssfully  ')
    server.quit()
    pass

def GoogleNewsScraper(TextData):
    CorrectArticleTitle = []
    CorrectArticleImageLink = []
    CorrectKeyword = []
    CorrectURL = []
    NewsLinkFind = False
    News24Hour = ""
    Response = requests.get('https://www.google.com/search?q=' + TextData[0])
    if Response.status_code == 200:
        Soup = BeautifulSoup(Response.content, 'html.parser')
        Links = Soup.find_all('a', {'class': '_Jhd'})
        NewsLink = ""
        for L in Links:
            if L.get('href').__contains__('&tbm=nws'):
                NewsLink = L.get('href')
            pass
        pass
        if NewsLink.__contains__('&tbm=nws'):
            print('\t\t\t  New Link Find  ')
            Response = requests.get('https://www.google.com' + NewsLink)
            if Response.status_code == 200:
                Soup = BeautifulSoup(Response.content, 'html.parser')
                PastLinks = Soup.find_all('a', {'class': 'q'})
                for P in PastLinks:
                    if P.text.__contains__('Past 24 hours'):
                        print('https://www.google.com' + P.get('href'))
                        GlobalLink = 'https://www.google.com' + P.get('href')
                        NewsLinkFind = True
                    pass
                pass
            pass
        pass
        if NewsLinkFind:
            TotalKeywords = 1
            while TotalKeywords < len(TextData):
                Remain = len(TextData) - TotalKeywords
                print('Keyword:{}'.format(TextData[TotalKeywords]))
                print('\t\t\t---------------------------')
                print('\t\t\t  Loading:{} & Remianing:{}'.format(TotalKeywords, Remain))
                print('\t\t\t---------------------------')
                #Session = requests.session()
                header = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
                QueryLink = GlobalLink.split('?q=')[1].split('&')[0]
                NewKeyword = TextData[TotalKeywords].replace(' ', '+')
                GlobalLink = GlobalLink.replace(QueryLink, NewKeyword)
                #print('New Link:{}'.format(GlobalLink))
                Response = requests.get(GlobalLink, headers=header)
                Soup = BeautifulSoup(Response.content, 'html.parser')
                ViewLink = ""
                ViewFind = False
                try:
                    V_Link = Soup.find('a', {'class': '_OMs'})
                    ViewLink = V_Link.get('href')
                    ViewFind = True
                except:
                    ViewFind = False
                pass
                if ViewFind:
                    #Response = Session.get(ViewLink, headers=header)
                    Response = requests.get(ViewLink, headers=header)
                    if Response.status_code == 200:
                        print('\t\t\t Checking Post  ')
                        Soup = BeautifulSoup(Response.content, 'html.parser')
                        FullCoverage = Soup.find_all('section', {'class': 'noky8'})
                        TotalTags = ""
                        AtricleTitle = []
                        ArticleImageLink = []
                        print('\t\t\t Finding Full Coverage  ')
                        for FC in FullCoverage:
                            if FC.text.__contains__('Full coverage'):
                                TotalTags = FC.find_all('c-wiz', {'class', 'lPV2Xe'})
                                for T in TotalTags:
                                    Title = T.find('a', {'class': 'nuEeue'})
                                    print(Title.text.encode('ascii', 'ignore'))
                                    AtricleTitle.append(Title.text)
                                    Image = T.find('img', {'class': 'b1XOjc'})
                                    try:
                                        print(Image.get('src'))
                                        ArticleImageLink.append(Image.get('src'))
                                    except:
                                        print('Image Not available')
                                        ArticleImageLink.append('Image Not available')
                                    pass
                                pass
                            pass
                        pass
                        if len(TotalTags) >= 3:
                            print('Total Post:{}'.format(len(TotalTags)))
                        elif 0 < len(TotalTags) <= 2:
                            if len(TotalTags) == 1:
                                print('Total Post:{}'.format(len(TotalTags)))
                                CorrectArticleTitle.append(AtricleTitle[0])
                                CorrectArticleImageLink.append(ArticleImageLink[0])
                                CorrectKeyword.append(TextData[TotalKeywords])
                                CorrectURL.append(Response.url)
                                """SendEmailLink(TextData[TotalKeywords], Response.url, AtricleTitle[0].encode('ascii','ignore'),ArticleImageLink[0].encode('ascii','ignore'))"""
                            elif len(TotalTags) == 2:
                                CorrectArticleImageLink.append(ArticleImageLink[0])
                                CorrectArticleTitle.append(AtricleTitle[0])
                                CorrectArticleImageLink.append(ArticleImageLink[1])
                                CorrectArticleTitle.append(AtricleTitle[1])
                                CorrectKeyword.append(TextData[TotalKeywords])
                                CorrectURL.append(Response.url)
                                CorrectKeyword.append(TextData[TotalKeywords])
                                CorrectURL.append(Response.url)
                                print('Total Post:{}'.format(len(TotalTags)))
                                """SendEmailLinks(TextData[TotalKeywords],Response.url,AtricleTitle[0].encode('ascii','ignore'),ArticleImageLink[0].encode('ascii','ignore'),AtricleTitle[1].encode('ascii','ignore'), ArticleImageLink[1].encode('ascii','ignore'))"""
                            pass
                        pass
                    pass
                else:
                    print('View All Links not Find')
                pass
                TotalKeywords += 1
            pass
        pass
    else:
        print('Unable to Send Request on Google!')
    pass
    return CorrectKeyword,CorrectURL,CorrectArticleTitle,CorrectArticleImageLink
    pass

def googlenews(request):
    """Renders the GoogleNews page."""
    Results=[]
    Total=0
    if request.method == 'POST':
        Data = request.POST.get('Keyword')
        TextData = Data.split('\r\n')
        Total=len(TextData)
        CorrectKeyword,CorrectURL,CorrectArticleTitle,CorrectArticleImageLink = GoogleNewsScraper(TextData)
        #Keyword=[]
        #URL=[]
        #Title=[]
        #Image=[]
        #for K in CorrectKeyword:
        #    Keyword.append(K)
        #for U in CorrectURL:
        #    URL.append(U)
        #for T in CorrectArticleTitle:
        #    Title.append(T)
        #for I in CorrectArticleImageLink:
        #    Image.append(I)
        #Results=zip(Keyword,URL,Title,Image)
        Results=zip(CorrectKeyword,CorrectURL,CorrectArticleTitle,CorrectArticleImageLink)
    return render(request, 'app/googlenews.html', {
        'title':'Google News',
        'Results':Results,
        'Total':Total
    })