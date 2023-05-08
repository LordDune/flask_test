from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # создали объект класса Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # уникальные значения, не повторяются
    title = db.Column(db.String(100), nullable=False)  # нельзя иметь нулевое значение
    intro = db.Column(db.String(300), nullable=False)  # нельзя иметь нулевое значение
    text = db.Column(db.Text, nullable=False)  # нельзя иметь нулевое значение
    date = db.Column(db.DateTime, default=datetime.utcnow)  # текущая дата

    def __repr__(self):
        return '<Article %r>' % self.id  # когда мы будем выбирать какой-либо объект на основе класса Article, то будет выдавать этот объект и его id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(
        Article.date.desc()).all()  # вывод первой записи из базы данных Article.query.first()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create_article.html")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        article = Article.query.get(id)
        return render_template("post_update.html", article=article)


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page " + name + " - " + str(id)


if __name__ == "__main__":
    app.run(debug=True)

# region important
# endregion
