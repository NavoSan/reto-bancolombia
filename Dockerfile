# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Instalar git para clonar/pull el repositorio
RUN apt-get update && apt-get install -y git

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script de entrada y el archivo de requerimientos
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
COPY requirements.txt /app/

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

# Hacer que el script de entrada sea ejecutable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Exponer el puerto en el que Flask se ejecutará
EXPOSE 8880

# Establecer el script de entrada como el punto de entrada
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
