import psycopg2
import os

class conexionBD():
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.schema = 'public'
        

    def __connectBD(self):
        """
        funcion para establecer la conexion con la base de datos
        """
        try:
            self.connection = psycopg2.connect(
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'db_reto_bancolombia')
            )

            self.connection.autocommit=True
            self.cursor=self.connection.cursor()

            return "Se establece conexion con la base de datos"
        except Exception as e:
            return f"error: {e}"
    
    def insertBD(self, tabla, campos, valores):
        try:
            conexion = self.__connectBD()
            campos_str = ', '.join(campos)
            valores_placeholders = ', '.join(['%s'] * len(valores))  # Usa %s como placeholder para los valores

            sql = f"INSERT INTO {self.schema}.{tabla} ({campos_str}) VALUES ({valores_placeholders})"

            self.cursor.execute(sql, valores)  # Usar execute cuando es una sola fila
            self.connection.commit()
            return "Se ha insertado en la base de datos"
        except Exception as e:
            return f"error: {e}"
