David Branch baybee

First install the dependencies:
```
pip install -r requirements.txt
```
Then, start the server with:
```
nodemon main.py --ignore "**/data/**"
```

The --ignore "**/data/**" option is important if you have not pulled all pokemon
data from the APIResource as it will keep restarting the server upon changes
within the data/ folder.


NOTES:
If you want to test the pulling from API functionality, go to teh data folder at
*/data/pokemon_data/pokemon/pokemon_data.json and clear the folder.
Then try to populate the pokedex
