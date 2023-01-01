from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<int:id>')
def user_profile(id):
    return 'Profile page of user #{}'.format(id)


@app.route('/books/<string:genre>')
def books(genre):
    return 'All books in {} category.'.format(genre)

if __name__ == '__main__':
    app.run(debug=True)