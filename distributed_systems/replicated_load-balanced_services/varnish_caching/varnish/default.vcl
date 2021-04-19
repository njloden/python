vcl 4.0;

# import directors module needed for loadbalancing across multiple backends
import directors;

# define backend nodes
backend node_1 {
  .host = "web_app_1:5001";
}

backend node_2 {
  .host = "web_app_2:5002";
}

# define backend resource pool and the type of loadbalancing method
sub vcl_init {
  new varnish_lb = directors.round_robin();
  varnish_lb.add_backend(node_1);
  varnish_lb.add_backend(node_2);
}

# disable caching for specific URLs where unique dynamic content will be generated with each request
sub vcl_recv {
  if (req.url == "/time") {
    return (pass);
  }

  # send all traffic to varnish_lb director
  set req.backend_hint = varnish_lb.backend();
}

# set http header containing a cache hit or miss
sub vcl_deliver {
  if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }
}
