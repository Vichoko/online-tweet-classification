# Esquemas de tablas de tweets nuevas
Se obtuvieron bases de datos de las fechas:
Ago2016
Jun2016
Jul2016


```sql
DATABASE tweet<mes><año>
TABLE <año><mes><dia>_tweets

sys_partition
download_date*
creation_date*
id_tweet
blacklisted_tweet
id_user *
repeated_user
favorited *
truncated
type
lang_tweet *
text_tweet *
rt * 
rt_count *
rt_id
text_rt
quote
quote_id
text_quote
has_keyword *
src_href
src_rel
src_text
in_reply_to_status_id
in_reply_to_user_id
in_reply_to_screen_name
countries_text
geo_located
geo_latitude
geo_longitude
place_id
place_namet
place_country_code
place_country
place_fullname
place_street_address
place_url
place_place_type
counter

DATABASE users<mes><año>
TABLE <año><mes><dia>_users

sys_partition
download_date
creation_date
id_tweet
id_user
name
screen_name
blacklisted_user
description
statuses_count
favorites_count
followers_count
friends_count
listed_count
translator
geo_enabled
lang_user
location
countries_user
timezone
utc_offset_mins
follow_request_sent
uprotected
verified
contribution_enable
show_all_inline_media
url
profile_bkg_color
profile_bkg_img_url
profile_img_url
profile_link_color
profile_sidebar_border_color
profile_sidebar_color
profile_text_color

DATABASE detecciones<mes><año>
TABLE <año><mes><dia>_event_desc	

event_ini
event_mid
event_end
type
rank
n_terms
description
support

```