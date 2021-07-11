from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView,ListView#djangoが持ってるviewの機能を引継ぐ
from .models import Post, Like, Category#テーブルをインポート
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm, SearchForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# views.pyは表示する内容やデータベースの処理を定義

class OnlyMyPostMixin(UserPassesTestMixin):#これをアップデートとデリートで使う
    raise_exception = True#例外処理をするかどうか。下の==がfalseなら403へ
    def test_func(self):#どういう関数かというと
        post = Post.objects.get(id = self.kwargs['pk'])#今開いている記事をobjectsでpostに入れます
        return post.author == self.request.user#そのobjectsの中のauthorが、ログインしているユーザーと同じかを判断


class Index(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list  = Post.objects.all().order_by('-created_at')
        context = {
          'post_list': post_list,
        }
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post#Postモデルの内容をcreateしますよ
    form_class = PostForm#Postformはforms.pyで定義してimport
    success_url = reverse_lazy('myapp:index')#登録が成功successしたらこのページindexに遷移するよ。reverse_lazyはdjangoからimport
#ログイン中のユーザーをセットするため関数
    def form_valid(self, form):#formがvalidかどうか
        form.instance.author_id = self.request.user.id #authorをセット
        return super(PostCreate, self).form_valid(form)#idがセットされたformを返しますよ
#メッセージを出すための関数
    def get_success_url(self):
        messages.success(self.request, 'Postを登録しました。')
        return resolve_url('myapp:index')


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        detail_data = Post.objects.get(id=self.kwargs['pk'])
        category_posts = Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5]
        params = {
          'object': detail_data,
          'category_posts': category_posts,
        }
        return params


class PostUpdate(OnlyMyPostMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
      messages.info(self.request, 'Postを更新しました。')
      return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])


class PostDelete(OnlyMyPostMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.info(self.request, 'Postを削除しました。')
        return resolve_url('myapp:index')


class PostList(ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class Login(LoginView):
    form_class = LoginForm
    template_name =  'myapp/login.html'


class Logout(LogoutView):
    template_name = 'myapp/logout.html'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'ユーザー登録しました。')
        return HttpResponseRedirect(self.get_success_url())

@login_required#LoginRequiredMixinはクラスでのみ。defはこっち。ログインしてなかったらLike_add機能しないdjangoの機能
def Like_add(request, post_id):
    post = Post.objects.get(id = post_id)#関数ベースだと←これ明示しなきゃ。classベースだと明示しない
    is_liked = Like.objects.filter(user = request.user, post = post_id).count()#filter内条件のところがイマイチ
    if is_liked > 0:#上のcount()で数が出てるから、０ならif文飛ばしてお気に入り追加の処理へすすむ
        messages.info(request, 'すでにお気に入りに追加済みです。')
        return redirect('myapp:post_detail', post.id)

    like = Like()#Likeモデルの空っぽの箱、like.userも、like.postも空っぽ、をlikeに代入
    like.user = request.user#空っぽの箱にいれる
    like.post = post#98行目のpost。空っぽの箱にいれる
    like.save()#このタイミングでデータが保存saveされる

    messages.success(request, 'お気に入りに追加しました。')
    return redirect('myapp:post_detail', post.id)#元々開いているページだから繊維はしないが明示する。id無いと判別できない96行目で取ってきたid


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'

    def get_context_data(self, *args, **kwargs):
        detail_data = Category.objects.get(name_en = self.kwargs['name_en'])
        category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')

        params = {
            'object': detail_data,
            'category_posts': category_posts,
        }

        return params


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            search_list = Post.objects.filter(Q(title__icontains = freeword)|Q(content__icontains = freeword))

            params = {
                'search_list': search_list,
            }

            return render (request, 'myapp/search.html', params)
