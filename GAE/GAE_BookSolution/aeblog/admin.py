# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import model

class Init(webapp.RequestHandler):
    def get(self):
        blog = model.Blog.get_by_key_name('blog')
        if blog is None:
            blog = model.Blog(key_name='blog',
                       title='My Blog',
                       description='This is my blog')
            blog.put()
        self.response.out.write('部落格建立完成')

class EditBlog(webapp.RequestHandler):
    def get(self):
        blog = model.Blog.get_by_key_name('blog')
        if blog is None:
            self.response.out.write('Blog Not Found')
        else:
            self.response.out.write(
                template.render('templates/edit_blog.html', {
                    'blog': blog,
                    'page_title': blog.title + u' -  編輯部落格資料'
                })
            )
            
    def post(self):
        title = self.request.get('title')
        desc = self.request.get('description')
        articles_per_page = int(self.request.get('articles_per_page', default_value='10'))

        blog = model.Blog.get_by_key_name('blog')
        if blog is None:
            self.response.out.write('Blog Not Found')
        else:
            blog.title = title
            blog.description = desc
            blog.articles_per_page = articles_per_page
            blog.put()
            self.redirect('/admin/edit_blog')
            
   
class Article(webapp.RequestHandler):
    def get(self):
        blog = model.Blog.get_by_key_name('blog')
        action = self.request.get('action', default_value='unknown')
        if action == 'new':
            output = template.render('templates/article_new.html', {
                        'blog': blog,
                        'status': 'new',
                        'page_title': blog.title + u' - 發表新文章'
                     })
        elif action == 'list':
            articles = model.Article.all()
            output = template.render('templates/article_list.html', {
                        'blog': blog,
                        'articles': articles,
                        'page_title': blog.title + u' - 文章列表'
                     })
        elif action == 'edit':
            key = self.request.get('key')
            article = db.get(key)
            tags = ', '.join(article.tags)
            output = template.render('templates/article_new.html', {
                        'blog': blog,
                        'status': 'edit',
                        'article': article,
                        'tags': tags
                     })
        elif action == 'delete':
            key = self.request.get('key')
            db.delete(key)
            self.redirect('/admin/article?action=list')
            return
        else:
            output = '未知的操作'

        self.response.out.write(output)
        
    def post(self):
        action = self.request.get('action', default_value='unknown')
        if action == 'save':
            status = self.request.get('status')
            title = self.request.get('title')
            content = self.request.get('content')
            raw_tags = self.request.get('tags').split(',')
            striped_tags = map(lambda x: x.strip(), raw_tags)

            if status == 'new':
                # 將操作定義成交易函式
                def tx():
                    # 先取得Blog資料實體
                    blog = model.Blog.get_by_key_name('blog')
                    # 取得最新的文章index
                    counter = model.Counter.get_by_key_name('blog_index', 
                                                            parent=db.Key.from_path('Blog', 'blog'))
                    if counter is None:
                        counter = model.Counter(key_name='blog_index',
                                                parent=blog)
                    counter.count += 1
                    counter.put()

                    article = model.Article(key_name='article' + str(counter.count),
                                  parent=blog,
                                  blog=blog,
                                  title=title,
                                  content=db.Text(content),
                                  tags=striped_tags)
                    article.put()

                db.run_in_transaction(tx)
                self.redirect('/admin/article?action=new')
                
            elif status == 'edit':
                key = self.request.get('key')
                article = db.get(key)
                article.title = self.request.get('title')
                article.content = db.Text(self.request.get('content'))
                article.tags = map(lambda x: x.strip(), self.request.get('tags').split(','))
                article.put()
                self.redirect('/admin/article?action=list')

        else:
            self.response.out.write('未知的操作')

def main():
    app = webapp.WSGIApplication([
        ('/admin/init', Init),
        ('/admin/edit_blog', EditBlog),
        ('/admin/article', Article)
    ])
    run_wsgi_app(app)

if __name__ == '__main__':
    main()