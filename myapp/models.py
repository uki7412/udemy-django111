from django.db import models

# models.pyはデータベース内のテーブルを定義

class Post(models.Model):
  title = models.CharField('タイトル', max_length=50)
  content = models.TextField('内容', max_length=1000)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

# postを参照する時にタイトル出してくれる
  def __str__(self):
      return self.title
