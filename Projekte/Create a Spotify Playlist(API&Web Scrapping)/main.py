import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID="95affd4b800143a2aac2c202e4cb75b4"
CLIENT_SECRET="6153d30028a24e22825fd9772e630e89"

date=input("Which year would you like to travel back to? Type the date in this format  YYYY-MM-DD:  ")
URL=f"https://www.billboard.com/charts/hot-100/{date}"

response=requests.get(URL)
content=response.text

soup=BeautifulSoup(content,"html.parser")

titles=soup.find_all(name="li", class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-050 lrv-u-padding-l-1@mobile-max")
# song_name=soup.find_all(name="span",class_="c-label  a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet")

# songs_list=[f"{artists[i].getText() } + '  ' + {song_name[i].getText()}" for i in range(len(artists)-1)]
# print(songs_list[0])

songs_list=[]
for i in range(len(titles)):
    songs_list.append((titles[i].find_next(name="h3").getText()))

# songs_list.append(artists[0].find_next(name="h3").getText())
# songs_list.append(artists[1].find_next(name="h3").getText())
final_songs_list=[]
for element in songs_list:
    translator = str.maketrans({chr(10): '', chr(9): ''})
    final_songs_list.append(element.translate(translator))
    # element= element.replace("\t","")

print(final_songs_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in final_songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)