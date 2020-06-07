# Interactive map of Moscow

Personal site and city poster about the most interesting places in Moscow.

Site example – [alpden.pythonanywhere.com](http://alpden.pythonanywhere.com/)

[![2020-06-03-18-19-33.png](https://i.postimg.cc/0ykTf6sT/2020-06-03-18-19-33.png)](https://postimg.cc/JGFY7ztx)

## How to install

Should use a virtual environment for the best project isolation. Activate venv and install dependencies:

```bash
pip install -r requirements.txt
```

And set environment variables:

```bash
export SECRET_KEY=secret key
```

## How to prepare and run

``` bash
python manage.py migrate
```

It's possible to fill places with management command.

From single json file from url:

```bash
python manage.py load_place --json_url http://url/file.json
```

Or use batch operation:

```bash
python manage.py load_place -B
```

Run locally:

```bash
python manage.py runserver
```
