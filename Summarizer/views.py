from decimal import Context
from os import link
from django.http.request import HttpRequest
from numpy import tile
import sumy
import nltk; nltk.download('punkt')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from youtube_transcript_api import YouTubeTranscriptApi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import requests
from django.shortcuts import render, redirect
from isodate import parse_duration
from django.conf import settings
from newspaper import Article
from .models import Comment, save_sum, all_sum, ContactForm
from django.urls import reverse
API_KEY = '6e74986113f945c79f538ce657601f88'
# Create your views here.
def home(request):
    return render(request,'home.html')

def short(request):
    link=request.GET['url-link']
    n=request.GET['url-no']
    d = YouTubeTranscriptApi.get_transcript(link)
    l=[]
    for x in d:
        new_dict={key:val for key, val in x.items() if key == 'text'}
        l.append(new_dict['text'])
    l=". ".join(l)

    parser = PlaintextParser.from_string(l,Tokenizer("english"))
    summarizer = LexRankSummarizer()    
    summary = summarizer(parser.document, n)
    context= {'summary': summary}
    return render(request,'result.html',context)

def short_art(request):
    link=request.GET['url-link']
    n=request.GET['url-no']
    article= Article(link)
    article.download()
    article.parse()
    val=article.text
    parser = PlaintextParser.from_string(val,Tokenizer("english"))
    summarizer = LexRankSummarizer()    
    sum = summarizer(parser.document, n)
    context={'summary':sum}
    return render(request,'result.html',context)

def short_text(request):
    val=request.GET['url-link']
    n=request.GET['url-no']
    parser = PlaintextParser.from_string(val,Tokenizer("english"))
    summarizer = LexRankSummarizer()    
    sum = summarizer(parser.document, n)
    context={'summary':sum}
    return render(request,'result.html',context)

def articles(request):
    category = request.GET.get('category')
    
    query = request.GET.get('q', None)

    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
    elif query != None:
        url = f'https://newsapi.org/v2/everything?q=news&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
    elif category:
        url = f'https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={API_KEY}'    
        response = requests.get(url)
        data = response.json()    
        articles = data['articles']
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey={API_KEY}'    
        response = requests.get(url)
        data = response.json()    
        articles = data['articles']
    articles=articles[:8]  
    context = {
        'articles' : articles,
    }
    return render(request, 'articles.html',context)
def get_sum(request):
    if request.method=='GET':
        title=request.GET.get('title')
        link=request.GET.get('url')
        article= Article(link)
        article.download()
        article.parse()
        val=article.text
        parser = PlaintextParser.from_string(val,Tokenizer("english"))
        summarizer = LexRankSummarizer()    
        sum = summarizer(parser.document, 8)
        context={'sum':sum,'title':title}
        if all_sum.objects.filter(title=title).exists():
            pass
        else:
            summary=str(sum)
            l=summary.split("<Sentence:")
            l.pop(0)
            summary=" ".join(l)
            l=summary.split(">")
            summary=" ".join(l) 
            summary=summary[:-1] 
            sumry=all_sum(link=link,summary=summary,title=title)
            sumry.save()

        return render(request,'get_sum.html',context)
def videos(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 6,
            'videoCaption' : 'closedCaption',
            'isCC' : True,
            'videoDuration' : 'medium',
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results=r.json()['items']
     
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 6,
            'videoCaption' : 'closedCaption',
            'videoDuration' : 'medium',
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)
        
    context = {
        'videos' : videos
    }
    
    return render(request, 'res.html', context)

def get_vid_sum(request):
    if request.method=='GET':
        id=request.GET.get('id')
        title=request.GET.get('title')
        try:
            d = YouTubeTranscriptApi.get_transcript(id)
            l=[]
            for x in d:
                new_dict={key:val for key, val in x.items() if key == 'text'}
                l.append(new_dict['text'])
            l=". ".join(l)
            parser = PlaintextParser.from_string(l,Tokenizer("english"))
            summarizer = LexRankSummarizer()    
            summary = summarizer(parser.document, 10)
        except:
            summary="Subtitles not available for this video"
        context= {'summary': summary,'title':title}
        if all_sum.objects.filter(title=title).exists():
            pass
        else:
            summary=str(summary)
            l=summary.split("<Sentence:")
            l.pop(0)
            summary=" ".join(l)
            l=summary.split(">")
            summary=" ".join(l) 
            summary=summary[:-1] 
            sumry=all_sum(link=id,summary=summary,title=title)
            sumry.save()
        return render(request,'get_vid_sum.html',context)

def save_summary(request):
    summary=request.POST['summary']
    title=request.POST['title']
    sumry=save_sum(user=request.user,summary=summary,title=title)
    sumry.save()
    return redirect('home')

def saved(request):
    summary = save_sum.objects.filter(user=request.user).order_by('-id')
    context = {'summary' : summary,'id' : id}
    return render(request,"saved.html",context)

def saved_title(request):
    if request.method=='GET':
        title=request.GET.get('title')
        summary=request.GET.get('summary')
        summary=str(summary)
        l=summary.split("<Sentence:")
        l.pop(0)
        summary=" ".join(l)
        l=summary.split(">")
        summary=" ".join(l) 
        summary=summary[:-1]     
        context = {'title':title,'summary':summary}
        return render(request,"saved_title.html",context)

def save_art(request):
    if request.method=='GET':
        title=request.GET.get('title')
        summary=request.GET.get('summary')
        if len(title)>50:
            title=title[:50]
        sumry=save_sum(user=request.user,summary=summary,title=title)
        sumry.save()
        return redirect('home')

def delete(request):
    if request.method=='GET':
        id=request.GET.get('id')
        post_to_delete=save_sum.objects.get(id=id)
        post_to_delete.delete()
        return redirect('saved')

def view_all_sum(request):
    all_posts = all_sum.objects.all()
    context = {'posts':all_posts}
    return render(request,'view_all_sum.html',context)

def add_comment(request):
    id=request.GET.get('id')
    obj=all_sum.objects.get(id=id)
    context={'post':obj}
    return render(request,'add_comment.html',context)

def save_comment(request):
    id=request.GET.get('id')
    id=int(id)
    name=request.GET['name']
    body=request.GET['comment']
    p_obj=all_sum.objects.get(id=id)
    c_obj=Comment(post=p_obj,name=name,body=body)
    c_obj.save()
    return redirect('view_all_sum')

def contact_form(request):
    return render(request,'contact_form.html')

def add_contact(request):
    name=request.GET.get('name')
    body=request.GET.get('body')
    obj=ContactForm(name=name,body=body)
    obj.save()
    return redirect('home')

def messages(request):
    messages=ContactForm.objects.all()
    context = {'messages':messages}
    return render(request,'messages.html',context)





        

