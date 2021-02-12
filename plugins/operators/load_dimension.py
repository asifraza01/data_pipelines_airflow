from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    
    insert_sql = """
        TRUNCATE TABLE {};
        INSERT INTO {}
        {};
        COMMIT;
    """

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id="",
                 table="",
                 select_sql="",
                  truncate = False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql
        self.truncate = truncate
        

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"Loading dimension table {self.table} in Redshift")
       # redshift = PostgresHook(postgres_conn_id=conn_id)
        if self.truncate:
            redshift.run(f"TRUNCATE TABLE {self.table}")
        redshift.run(f"INSERT INTO {self.table} {self.select_sql}")