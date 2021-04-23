vcl 4.0;

# define backend node
backend node {
  .host = "web_app_2:5002";
}

# set default time to live (lifespan of cached content) to 15 min
sub vcl_backend_response {
  set beresp.ttl = 15m;
}

# set http header containing a cache hit or miss
sub vcl_deliver {
  if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }
}
