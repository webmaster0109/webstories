from django.shortcuts import render
import feedparser
# Create your views here.

def feed_list(request):
    feed_url = "https://feeds.bbci.co.uk/hindi/rss.xml"
    feeds = feedparser.parse(feed_url)
    feed_entries = feeds.entries[:50]  # Limit to 50 entries
    return render(request, 'feed_list.html', {'feeds': feed_entries})