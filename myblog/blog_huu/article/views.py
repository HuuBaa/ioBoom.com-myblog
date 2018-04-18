from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Comment,Article,Tag,UserProfile
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .forms import UserProfileForm
# Create your views here.

def index(request):
    articles = Article.objects.all()
    return render(request,'article/index.html',{'articles':articles})

def all_articles(request):

    all_articles_list=Article.objects.order_by('-post_time').all()

    current_page=request.GET.get('page',1)
    paginator=Paginator(all_articles_list,5)

    try:
        all_articles_list=paginator.page(current_page)
    except PageNotAnInteger:
        all_articles_list=paginator.page(1)
    except EmptyPage:
        all_articles_list=paginator.page(paginator.num_pages)

    con_dict={
        'articles':all_articles_list.object_list,
        'page_info':all_articles_list
    }

    return render(request,'article/',con_dict)

def tag_articles(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)

    if tag is not None:
        tag_articles_list=tag.articles.order_by('-post_time').all()

        current_page = request.GET.get('page', 1)
        paginator = Paginator(tag_articles_list, 5)

        try:
            tag_articles_list = paginator.page(current_page)
        except PageNotAnInteger:
            tag_articles_list = paginator.page(1)
        except EmptyPage:
            tag_articles_list = paginator.page(paginator.num_pages)

        con_dict = {
            'tag':tag,
            'articles': tag_articles_list.object_list,
            'page_info': tag_articles_list
        }

        return render(request, 'article/', con_dict)


def article_detail(request,article_id):
    article=get_object_or_404(Article,id=article_id)
    comments=article.comments.order_by('-post_time').all()

    con_dict={
        'article':article,
        'comments':comments
    }
    return render(request,'article/',con_dict)

@login_required
def post_comment(request,article_id):
    if request.method=='POST':
        article = get_object_or_404(Article, id=article_id)
        author=request.user
        content=request.POST.get('content')
        c=Comment.objects.create(articl=article,author=author,content=content)
        #评论成功后刷新即可
        return reverse('')

@login_required
def profile(request):
    form=UserProfileForm()

    return render(request,'article/profile.html',{'form':form})