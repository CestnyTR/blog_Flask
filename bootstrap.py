from flask import Flask, render_template, redirect, request, url_for, flash, session
import wtforms
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt


class RegisterForm(wtforms.Form):
    name = wtforms.StringField(
        "İsim", validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=5, max=8, message="Girilen kullanıcı adı 5 ile 8 harf arasında olmalıdır.")])
    username = wtforms.StringField("Kullanıcı adı", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=5, max=12, message="Girilen kullanıcı adı 5 ile 12 harf arasında olmalıdır.")])
    email = wtforms.StringField(
        "E-Mail", validators=[wtforms.validators.Email(message="Lütfen geçerli bir E-Mail hesabı giriniz."),
                              wtforms.validators.DataRequired(),
                              wtforms.validators.Length(max=30, message="Girilen email en fazla 30 karekter olabilir.")])
    password = wtforms.PasswordField("Parola", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(max=8, min=5, message="Girilen kullanıcı adı 5 ile 8 harf arasında olmalıdır.")])


class LoginForm(wtforms.Form):
    username = wtforms.StringField("Kullanıcı adı", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=5, max=12, message="Girilen kullanıcı adı 5 ile 12 harf arasında olmalıdır.")])
    password = wtforms.PasswordField("Parola", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(max=8, min=5, message="Girilen kullanıcı adı 5 ile 8 harf arasında olmalıdır.")])


class ArticleForm(wtforms.Form):
    title = wtforms.StringField("Makale Başlığı ", validators=[wtforms.validators.DataRequired(
    ), wtforms.validators.Length(min=8, max=15, message="Makale başılığı 8 ile 15 karekter arasında olmalı")])
    content = wtforms.TextAreaField("Makale İçeriği ", validators=[
                                    wtforms.validators.data_required(),
                                    wtforms.validators.Length(min=8, max=10000, message="Makale içeriği 8 ile 10000 karekter arasında olmalı")])


app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = "cestnytr"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "pythonblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard")
def dashboard():
    if session:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM articles WHERE author=%s"
        cursor.execute(query, (session["username"],))
        articles = cursor.fetchall()
        return render_template("dashboard.html", articles=articles)
    else:
        flash("Kontrol paneline sadece üyeler erişebilir.", "danger")
        return redirect(url_for("login"))


@app.route("/addarticle", methods=["GET", "POST"])
def addarticle():
    if session:
        form = ArticleForm(request.form)
        if request.method == "POST" and form.validate():
            title = form.title.data
            content = form.content.data
            username = session["username"]
            cursor = mysql.connection.cursor()
            insert_article = "INSERT INTO articles ( title, content, author) VALUES (%s,%s,%s);"
            cursor.execute(insert_article, (title, content, username))
            mysql.connection.commit()
            cursor.close()
            flash("Makale kayıt işlemi başarılı", "success")
            return redirect(url_for("dashboard"))
        else:
            return render_template("addarticle.html", form=form)

    else:
        flash("Sadece üyeler makale ekleyebilir.", "danger")
        return redirect(url_for("login"))


@app.route("/delete/<string:id>")
def delete(id):
    if session:
        curser = mysql.connection.cursor()
        query = "SELECT * FROM articles WHERE author= %s and id= %s"
        result = curser.execute(query, (session["username"], id))
        if result > 0:
            query_delete = "DELETE FROM articles WHERE id= %s"
            curser.execute(query_delete, (id,))
            mysql.connection.commit()
            curser.close()
            return redirect(url_for("dashboard"))
        else:
            flash("Yetkisiz işlem.", "danger")
            return redirect(url_for("dashboard"))
    else:
        flash("Yetkisiz işlem.", "danger")
        return redirect(url_for("index"))


@app.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    if session:
        form = ArticleForm(request.form)
        curser = mysql.connection.cursor()

        if request.method == "POST" and form.validate():
            title = form.title.data
            content = form.content.data
            curser = mysql.connection.cursor()
            query = "SELECT * FROM articles WHERE author= %s and id= %s"
            result = curser.execute(query, (session["username"], id))
            if result > 0:
                query_update = "UPDATE articles SET title=%s, content=%s  WHERE articles.id = %s"
                curser.execute(query_update, (title, content, id))
                mysql.connection.commit()
                curser.close()
                flash("Başarı ile makale güncellenmiştir.", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Yetkisiz işlem.", "danger")
                return redirect(url_for("dashboard"))
        else:
            query = "SELECT * FROM articles WHERE author= %s and id= %s"
            result = curser.execute(query, (session["username"], id))
            if result > 0:
                article = curser.fetchone()
                form.title.data = article["title"]
                form.content.data = article["content"]
                return render_template("/update.html", form=form)

            else:
                flash("Yetkisiz işlem.", "danger")
                return redirect(url_for("dashboard"))

    else:
        flash("Yetkisiz işlem.", "danger")
        return redirect(url_for("dashboard"))


@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles"
    cursor.execute(query)
    articles = cursor.fetchall()
    return render_template("articles.html", articles=articles)


@app.route("/articles/<string:id>")
def article_detail(id):
    curser = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE id = %s"
    result = curser.execute(query, (id,))
    if result:
        articles = curser.fetchall()

        return render_template("article_detail.html", articles=articles)
    else:
        return render_template("article_detail.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        cursor = mysql.connection.cursor()
        register = "INSERT INTO users ( name, username, email, password) VALUES (%s,%s,%s,%s);"
        cursor.execute(register, (name, username, email, password))
        mysql.connection.commit()
        cursor.close()
        flash("Kayıt işlemi başarılı", "success")
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı", "success")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password_entered = form.password.data
        cursor = mysql.connection.cursor()
        quary = "SELECT username,password FROM users WHERE  username = %s"

        result = cursor.execute(quary, (username,))
        if result > 0:
            data = cursor.fetchone()
            password_real = data["password"]
            if sha256_crypt.verify(password_entered, password_real):
                flash("Giriş Başarılı", "success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Şifre hatalı", "danger")
                return redirect(url_for("login"))
        else:
            flash("Kullanıcı adı hatalı", "danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
