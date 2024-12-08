from multiprocessing import cpu_count

 # Socket Path
bind = 'unix:/home/alabaii/mts_hack/mts/gunicorn.sock'


 # Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

 # Logging Options
loglevel = 'debug'
accesslog = '/home/alabaii/mts_hack/mts/access_log'
errorlog =  '/home/alabaii/mts_hack/mts/error_log'
