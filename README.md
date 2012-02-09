# Cookbook #

---
### Heroku Reverse Proxy ###

> Django behind Heroku's reverse proxy causes ```request.is_secure()``` to always return ```False```.

> #### Solutions #####
> * Add ```secure_scheme_headers = {'X-FORWARDED-PROTO': 'https'}``` to Gunicorn's config. See [Sample config](https://github.com/allanlei/django-heroku-helpers/blob/master/heroku/gunicorn.py)
> * Add ```SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')``` in Django settings(development/1.4+). See [Django Docs](https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header)
> * Add ```heroku.middleware.SecureReverseProxyMiddleware``` to ```MIDDLEWARE_CLASSES```

---

### Https Requests Only ###

> 1. Apply one of the solutions from **Heroku Reverse Proxy**
> 2. Add ```heroku.middleware.HttpsRedirectMiddleware``` to ```MIDDLEWARE_CLASSES```
