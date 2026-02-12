import psycopg2

def get_connection():
    '''
    This function is for connecting to the database.
    '''
    try:
        connection = psycopg2.connect(
            dbname="restaurant_db",
            user="postgres",
            password="pass",
            host="localhost",
            port="5432"
        )
        return connection
    
    except Exception as error:
        print(f"Error in connection:\n {error}")
        return None

def manager_connection(fun):
    def wrapper(*args, **kwargs):
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                result = fun(cur, *args, **kwargs)
                conn.commit()
                return result
            
            except Exception as error:
                conn.rollback()
                print(f"Error: {error}")
                
            finally:
                cur.close()
                conn.close()
    return wrapper