from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/sqlite/sqlite-create', methods=['POST', 'GET'])
def create_sqlite():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        article = Article(title=title, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/sqlite/sqlite-posts')
        except:
            return "При добавлении статьи в SQLite произошла ошибка"
    else:
        return render_template('sqlite/sqlite-create.html')


@app.route('/sqlite/sqlite-posts')
def sqlite_posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('/sqlite/sqlite-posts.html', articles=articles)

@app.route('/sqlite/sqlite-posts/<int:id>')
def sqlite_detail(id):
    article = Article.query.get(id)
    return render_template('sqlite/sqlite_detail.html', article=article)

@app.route('/sqlite/sqlite-posts/<int:id>/update', methods=['POST', 'GET'])
def sqlite_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/sqlite/sqlite-posts')
        except:
            return "При редактировании статьи SQLite произошла ошибка"
    else:
        return render_template('sqlite/sqlite_update.html', article=article)

@app.route('/sqlite/sqlite-posts/<int:id>/delete')
def sqlite_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/sqlite/sqlite-posts')
    except:
        return "При удалении статьи SQLite произошла ошибка"


if __name__ == '__main__':
    app.run(debug=True)