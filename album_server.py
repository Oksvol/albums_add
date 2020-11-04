from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        album_count = len(album_names)
        result = "У группы {0} найдено {1} альбомов: ".format(artist, album_count)
        result += ", ".join(album_names)
    return result

@route("/albums", method="POST")
def new_album():
    album_data = {
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
        "year": request.forms.get("year")
    }
    save_status = album.save_album(album_data)    # Сохранены ли данные?
    if save_status:
        print("User saved at: ", album.DB_PATH)
        return "Данные успешно сохранены"
    else:
        raise HTTPError(409)


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
