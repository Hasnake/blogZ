from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
class Blog(db.Model):



    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))


    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route("/blog", methods=["POST", "GET"])
@app.route('/', methods=['POST', 'GET'])
def index():


    posts = Blog.query.all()



    return render_template('blog.html', posts= posts)
@app.route('/newpost', methods=['post', 'get'])
def add():


    post = ""
    new_blog = ""
    title_error = ""
    content_error =""
    if request.method == "POST":
        #blog_id = request.form['id']
        blog_title = request.form['title']

        if not blog_title:
            title_error = "Please type a title for your blog post"
        elif len(blog_title) > 120:
            title_error = "Your title length exceeds the limit, please shorten your title."

        else:
            blog_content = request.form['content']

            if not blog_content:
                content_error="Please type something for blog body."
            elif len(blog_content)>1000:
                content_error= "Your blog body is more than 1000 words."
            else:
                new_blog = Blog(blog_title, blog_content)
                db.session.add(new_blog)
                db.session.commit()

                blog_id = new_blog.id

                return redirect("/singlepost?id=" + str(blog_id))

    return render_template("newpost.html", post=new_blog, title_error=title_error,content_error=content_error)

@app.route("/singlepost")
def singlepost():

    posts = db.session.query(Blog)
    post = ""
    for post in posts:
        post = post
    return render_template("single_post.html", post=post)
if __name__ == '__main__':
    app.run()
