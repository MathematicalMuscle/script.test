## Installation via [`script.kodi_setter_upper`](https://github.com/MathematicalMuscle/script.kodi_setter_upper):

### Method 1: URL

Modify the IP address and port and go to this URL in your browser:
[http://10.0.0.120:8080/jsonrpc?request={"jsonrpc":"2.0","id":1,"method":"Addons.ExecuteAddon","params":{"addonid":"script.kodi_setter_upper","params":{"ksu_class":"Addon","addonid":"script.test","url":"https://github.com/MathematicalMuscle/script.test/archive/master.zip"}}}](http://10.0.0.120:8080/jsonrpc?request={"jsonrpc":"2.0","id":1,"method":"Addons.ExecuteAddon","params":{"addonid":"script.kodi_setter_upper","params":{"ksu_class":"Addon","addonid":"script.test","url":"https://github.com/MathematicalMuscle/script.test/archive/master.zip"}}})


### Method 2: Command Line

```bash
send_jsonrpc ()
{
  if ! [[ -v KODI_HOST ]]; then
    # EXAMPLE: KODI_HOST="http://10.0.0.120:8080"
    read -p "Kodi address:  " KODI_HOST
    export KODI_HOST
  fi

  # https://stackoverflow.com/a/44555048
  params=$(printf "\"%s\": \"%s\", " "$@")

  # https://stackoverflow.com/a/27658733
  payload="{\"jsonrpc\": \"2.0\", \"method\": \"Addons.ExecuteAddon\", \"id\": 1, \"params\": {\"addonid\": \"script.kodi_setter_upper\", \"params\": {${params::-2}}}}"

  curl -v -u xbmc:password -d "$payload" -H "Content-type:application/json" -X POST "${KODI_HOST}/jsonrpc"  &>/dev/null
}

send_jsonrpc "ksu_class" "Addon" "addonid" "script.test" "url" "https://github.com/MathematicalMuscle/script.test/archive/master.zip"
```
