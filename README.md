# isItAiredYet

### Search for _Picard_ restricted to _series_ type.

```shell
curl -X 'GET' \
  'https://api4.thetvdb.com/v4/search?query=Picard&type=series' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer xxx'
```

### Get next aired episode for series
```shell
curl -X 'GET' \
  'https://api4.thetvdb.com/v4/series/364093' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer xxx' | jq '.data.nextAired'
```

### Get token
```shell
curl -X 'POST' \
  'https://api4.thetvdb.com/v4/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "apikey": "",
  "pin": ""
}'
```

### Start a local server
```shell
python3 -m http.server
```