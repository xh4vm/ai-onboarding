import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from gigahack.etl.pg_to_es import run as run_etl_pg_to_es
from datetime import timedelta


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_etl_pg_to_es = DAG(
    
    dag_id="dag_etl_pg_to_es",
    default_args=default_args,
    description="Postgres messages to elastic",
    # schedule=None,
    # schedule="*/3 * * * *",
    schedule_interval=timedelta(seconds=5),
    max_active_runs=1,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["gigahack"],
    catchup=False,
)


etl_pg_to_es = PythonOperator(
    python_callable=run_etl_pg_to_es,
    task_id="etl_pg_to_es",
    dag=dag_etl_pg_to_es,
)

etl_pg_to_es