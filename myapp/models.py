from django.db import models
from django.contrib.auth.models import User

# models.pyはデータベース内のテーブルを定義。変更した際はそれをデータベースに反映させるためのコマンド操作が必要(ターミナルで)

class Category(models.Model):
  name = models.CharField('カテゴリ名', max_length=50)
  name_en = models.CharField('カテゴリ名英語', max_length=10)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def post_count(self):
      n = Post.objects.filter(category = self).count()
      return n 

  def __str__(self):
      return self.name


class Post(models.Model):
  author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)#authorがUserと紐づく(Userは元々あるから記述していない)
  title = models.CharField('タイトル', max_length=50)
  content = models.TextField('内容', max_length=1000)
  category = models.ForeignKey('Category', on_delete=models.PROTECT)
  thumbnail = models.ImageField(upload_to='images/', blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

# postを参照する時にタイトル出してくれる
  def __str__(self):
      return self.title

class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name="投稿", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Likeしたユーザー", on_delete=models.PROTECT)

