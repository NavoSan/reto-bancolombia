#!/bin/bash


# Clonar el repositorio si no existe, de lo contrario hacer pull para actualizarlo
if [ -d "$GIT_URL/.git" ]; then
    echo "Actualizando el repositorio existente..."
    git -C "$REPO_DIR" pull
else
    echo "Clonando el repositorio..."
    git clone "$GIT_URL" "$REPO_DIR"
fi

# Moverse al directorio del repositorio y ejecutar la aplicación Flask
cd "$REPO_DIR"
python app.py
