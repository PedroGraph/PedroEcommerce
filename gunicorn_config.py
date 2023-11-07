# gunicorn_config.py

workers = 4  # Número de trabajadores
bind = "0.0.0.0:8000"  # Dirección IP y puerto en el que Gunicorn debe escuchar
module = "mainproject.wsgi"  # Ruta al módulo WSGI de tu proyecto
