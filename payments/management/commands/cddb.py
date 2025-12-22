from django.core.management import BaseCommand
import psycopg2
from config.settings import USER, HOST, PASSWORD, PAD_DATABASE, PORT, DATABASE


class Command(BaseCommand):
    def handle(self, *args, **options):
        connectString = f"""
            dbname={PAD_DATABASE}
            user={USER}
            password={PASSWORD}
            host={HOST}
            port={PORT}
        """

        try:

            conn = psycopg2.connect(connectString)
            conn.autocommit = True


            cursor = conn.cursor()

            cursor.execute(f"DROP DATABASE {DATABASE}")
        except psycopg2.Error as ex:
            print(f"Произошла ошибка: {ex}")
        else:
            print("База данных Удалена успешно")