# SHOW MY MUSIC

this project will create a server that will show the current playing track

## How to use

simply install the requirements with

```bash
pip install -r requirements.txt
```

and run the server with

```bash
python main.py
```

then go to `http://localhost:5000` and you will see the current playing track

## Usage

the main use for this, is to integrate this with OBS, so you can show the current playing track on your stream

simply add a browser source to your OBS and set the url to `http://localhost:5000`

*the recommended size for the browser source is 1000x200

## Customization

* you can customize the source app of the music in `main.py` by changing the `WANTED_SOURCE` constant

* you can customize the look of the page by editing the `styles.css` file - 
there are some variables at the top of the file that you can change to customize the look of the page

## How it works

The programs start a http server that listens on port 5000, and it will serve a page that will load dynamically the
current playing track

dynamically?

the web page will fetch data from the server every 5 seconds, using the `/update` route

in `/update`, the server will get the current playing track using WINDOWS API (with winsdk package) and return it.

## Images

[screenshot](https://i.imgur.com/mOo0s1w.png)