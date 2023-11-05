import logging

from postgres_in import PostgresIn
from postgres_out import PostgresOut

logging.info("Exporting tables from source with pg started")
pg_out = PostgresOut()
pg_out.export_tables()
logging.info("Exporting tables from source with pg  completed")

logging.info("Importing tables to target with pg  started")
pg_in = PostgresIn()
pg_in.import_tables()
logging.info("Importing tables to target with pg completed")