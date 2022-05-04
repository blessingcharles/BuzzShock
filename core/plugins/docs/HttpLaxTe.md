```
Transfer-Encoding = 1#transfer-coding

transfer-coding    = "chunked" ; Section 4.1
                        / "compress" ; Section 4.2.1
                        / "deflate" ; Section 4.2.2
                        / "gzip" ; Section 4.2.3
                        / transfer-extension
     transfer-extension = token *( OWS ";" OWS transfer-parameter )

Parameters are in the form of a name or name=value pair.

transfer-parameter = token BWS "=" BWS ( token / quoted-string )

```

```
chunked-body   = *chunk
                 last-chunk
                 trailer-part
                 CRLF

chunk          = chunk-size [ chunk-ext ] CRLF
                 chunk-data CRLF
chunk-size     = 1*HEXDIG
last-chunk     = 1*("0") [ chunk-ext ] CRLF
chunk-data     = 1*OCTET ; a sequence of chunk-size octets


chunk-ext      = *( ";" chunk-ext-name [ "=" chunk-ext-val ] )
chunk-ext-name = token
chunk-ext-val  = token / quoted-string

```