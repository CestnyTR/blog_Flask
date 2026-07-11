# Python Blog

Flask ve MySQL ile geliştirilmiş, kullanıcı kayıt/giriş sistemi ve makale yönetimi (CRUD) içeren basit bir blog uygulaması.

## Özellikler

- Kullanıcı kaydı ve girişi (parolalar `sha256_crypt` ile şifrelenir)
- Oturum (session) tabanlı kimlik doğrulama
- Kontrol paneli üzerinden makale ekleme, güncelleme ve silme
- Yalnızca makale sahibinin kendi makalesini düzenleyebilmesi/silebilmesi
- Tüm makaleleri listeleme ve tek makale detay sayfası
- WTForms ile form doğrulama
- Jinja2 şablon kalıtımı (template inheritance)

## Teknolojiler

- **Python** / **Flask**
- **MySQL** / **MariaDB** (`Flask-MySQLdb`, `PyMySQL`)
- **WTForms** — form doğrulama
- **passlib** — parola şifreleme
- **Jinja2** / Bootstrap tabanlı şablonlar

## Kurulum

### 1. Gereksinimler

```bash
pip install flask flask-mysqldb pymysql wtforms passlib
```

> Not: `mysqlclient` derleme gerektirdiği için proje `PyMySQL` kullanacak şekilde ayarlanmıştır (`pymysql.install_as_MySQLdb()`).

### 2. Veritabanı

MySQL/MariaDB üzerinde `pythonblog` veritabanını oluşturup şemayı içe aktarın:

```bash
mysql -u root -p -e "CREATE DATABASE pythonblog;"
mysql -u root -p pythonblog < pythonblog.sql
```

Veritabanı bağlantı ayarları [bootstrap.py](bootstrap.py#L48-L52) içinde tanımlıdır:

```python
app.config["MYSQL_HOST"]     = "localhost"
app.config["MYSQL_USER"]     = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"]       = "pythonblog"
```

Kendi ortamınıza göre bu değerleri güncelleyin.

### 3. Çalıştırma

```bash
python bootstrap.py
```

Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışır.

## Sayfalar / Rotalar

| Rota | Açıklama |
|------|----------|
| `/` , `/index` | Ana sayfa |
| `/about` | Hakkında |
| `/register` | Üye kaydı |
| `/login` | Giriş |
| `/logout` | Çıkış |
| `/dashboard` | Kontrol paneli (üye makaleleri) |
| `/articles` | Tüm makaleler |
| `/articles/<id>` | Makale detayı |
| `/addarticle` | Yeni makale ekle |
| `/update/<id>` | Makale güncelle |
| `/delete/<id>` | Makale sil |

## Veritabanı Şeması

- **users** — `id`, `name`, `username`, `email`, `password`
- **articles** — `id`, `title`, `author`, `content`, `create_date`

## Notlar

- `app.secret_key` ve veritabanı parolası kod içinde açık şekilde bulunmaktadır; üretim ortamında bunları ortam değişkenlerine taşımanız önerilir.
- Uygulama `debug=True` ile çalışmaktadır; yalnızca geliştirme amaçlıdır.
</content>
</invoke>
