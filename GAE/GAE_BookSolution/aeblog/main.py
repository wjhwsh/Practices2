# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import model

class Index(webapp.RequestHandler):
    def get(self):
        blog = model.Blog.get_by_key_name('blog')
        page = int(self.request.get('page', '1'))
        query = model.Article.all()
        query.order('-created')
        articles = query.fetch(blog.articles_per_page, (page-1)*blog.articles_per_page)
        self.response.out.write(
            template.render('templates/index.html', {
                'blog': blog,
                'articles': articles,
                'page_title': blog.title
            })
        )

class Article(webapp.RequestHandler):
    def get(self, key):
        blog = model.Blog.get_by_key_name('blog')
        article = db.get(key)
        self.response.out.write(
            template.render('templates/article.html', {
                'blog': blog,
                'article': article,
                'page_title': blog.title + ' - ' + article.title
            })
        )


class LeaveComment(webapp.RequestHandler):
    def post(self):
        # 文章的鍵值
        article_key = self.request.get('key')
        article = db.get(article_key)
        # 讀取參數
        username = self.request.get('username')
        message = self.request.get('comment')
        # 新增一筆留言資料
        comment = model.Comment(parent=article,
                                article=article,
                                user=username,
                                comment=message)
        comment.put()
        self.redirect('/article/%s' % article_key)

        
class Tag(webapp.RequestHandler):
    def get(self, tagname):
        import urllib
        blog = model.Blog.get_by_key_name('blog')
        tag = urllib.unquote(tagname).decode('utf-8')
        articles = model.Article.gql('WHERE tags = :1', tag)
        self.response.out.write(
            template.render('templates/index.html', {
                'blog': blog,
                'articles': articles,
                'page_title': blog.title + u' - 標籤為「%s」的文章' % tag
            })
        )
        
def main():
    app = webapp.WSGIApplication([
        ('/', Index),
        ('/article/(.*)', Article),
        ('/comment', LeaveComment),
        ('/tag/(.*)', Tag)
    ])
    run_wsgi_app(app)

if __name__ == '__main__':
    main()