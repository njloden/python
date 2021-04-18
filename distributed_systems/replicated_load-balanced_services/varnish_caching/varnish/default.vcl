vcl 4.0;

backend default {
  .host = "web_app:5001";
}

# disable caching for specific URLs where unique dynamic content will be generated with each request
sub vcl_recv {
  if (req.url == "/time") {
    return (pass);
  }
}

# set http header containing a cache hit or miss
sub vcl_deliver {
  if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }
}
