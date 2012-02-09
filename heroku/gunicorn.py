import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
loglevel = 'error'
secure_scheme_headers = {
    'X-FORWARDED-PROTO': 'https',
}
