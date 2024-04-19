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
        """ Funcion para insertar multiples valores en la abse de datos
        Args: 
            tabla(str): nombre de la tabla en la base de datos
            campos(list): nombre de las columnas de la tabla que se va a insertar
            valores(list): cadena de valores de los datos que se vana a insertar
        
        returns: Cadena de texto en caso de exito y expecion de error en caso de fallo 
        """
        try:
            conexion = self.__connectBD()
            campos_str = ', '.join(campos)
            valores_placeholders = ', '.join(['%s'] * len(valores)) 

            sql = f"INSERT INTO {self.schema}.{tabla} ({campos_str}) VALUES ({valores_placeholders})"

            self.cursor.execute(sql, valores)  
            self.connection.commit()
            return "Se ha insertado en la base de datos"
        except Exception as e:
            return f"error: {e}"
