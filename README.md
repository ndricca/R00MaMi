# R00MaMI 
## Bakeka.it Milan room 4 rent crawler

## ...still working on it!

This is a basic Python 2.7 implementation I did for excercise in order to keep me informed about rooms announcement in Milan.
In fact, what I learnt looking for a room is that the main factor in order to find a room is __velocity__. You have good chances only if you are among the first three or four people that contact the owner/previous inmate.

Long story short, here a basic explanation of every script inside this folder:

* __bakeka_parser.py__ : it starts parsing Milano-Bakeka RSS url related to room for rent announcements, then it scrapes every announcement URL writing down on a pandas dataframe all useful informations;
* __bakeka_mailer.py__ : it sends an e-mail with an HTML table of all new announcements (where is considered new every announcement not already scraped); _(check "new" logic)_
* __bakeka_scheduler.py__ : this one wraps the two previous scripts scheduling their run every hour; _(make frequency a parameter)_
* __bakeka_mapper.py__ : since most of the announcements already include geographical coordinates, it maps all geocoded results with the __folium__ library _(still a lot to work of)_

Everything is still a work in progress and I hope that when I will have some spare time I will try to keep working on R00MaMI.
