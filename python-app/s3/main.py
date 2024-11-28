import os
import sys
from minio import Minio
from minio.error import S3Error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import backet, user, password, endpoint


class MinioClient:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        """
        Инициализация клиента для взаимодействия с MinIO.

        :param endpoint: Адрес MinIO сервера (например, localhost:9000)
        :param access_key: Access Key
        :param secret_key: Secret Key
        :param secure: True, если используете HTTPS, иначе False
        """
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def bucket_exists(self, bucket_name):
        """
        Проверяет, существует ли бакет.

        :param bucket_name: Название бакета
        :return: True, если бакет существует, иначе False
        """
        try:
            return self.client.bucket_exists(bucket_name)
        except S3Error as e:
            print(f"Ошибка при проверке бакета: {e}")
            return False

    def create_bucket(self, bucket_name):
        """
        Создает новый бакет, если он не существует.

        :param bucket_name: Название нового бакета
        """
        if not self.bucket_exists(bucket_name):
            try:
                self.client.make_bucket(bucket_name)
                print(f"Бакет '{bucket_name}' создан.")
            except S3Error as e:
                print(f"Ошибка при создании бакета: {e}")
        else:
            print(f"Бакет '{bucket_name}' уже существует.")

    def upload_file(self, bucket_name, file_path, object_name=None):
        """
        Загружает файл в MinIO.

        :param bucket_name: Название бакета
        :param file_path: Путь к локальному файлу
        :param object_name: Имя объекта в MinIO. Если не указано, используется имя файла.
        """
        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"Файл '{file_path}' успешно загружен как '{object_name}' в бакет '{bucket_name}'.")
        except S3Error as e:
            print(f"Ошибка при загрузке файла: {e}")

    def download_file(self, bucket_name, object_name, file_path):
        """
        Скачивает файл из MinIO.

        :param bucket_name: Название бакета
        :param object_name: Имя объекта в MinIO
        :param file_path: Путь для сохранения файла
        """
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"Файл '{object_name}' успешно скачан в '{file_path}'.")
        except S3Error as e:
            print(f"Ошибка при скачивании файла: {e}")

    def list_objects(self, bucket_name):
        """
        Список объектов в бакете.

        :param bucket_name: Название бакета
        :return: Список объектов в бакете
        """
        try:
            objects = self.client.list_objects(bucket_name)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            print(f"Ошибка при получении списка объектов: {e}")
            return []

    def delete_object(self, bucket_name, object_name):
        """
        Удаляет объект из бакета.

        :param bucket_name: Название бакета
        :param object_name: Имя объекта для удаления
        """
        try:
            self.client.remove_object(bucket_name, object_name)
            print(f"Объект '{object_name}' удален из бакета '{bucket_name}'.")
        except S3Error as e:
            print(f"Ошибка при удалении объекта: {e}")

    def delete_bucket(self, bucket_name):
        """
        Удаляет бакет.

        :param bucket_name: Название бакета
        """
        try:
            self.client.remove_bucket(bucket_name)
            print(f"Бакет '{bucket_name}' удален.")
        except S3Error as e:
            print(f"Ошибка при удалении бакета: {e}")


minio_client = MinioClient(endpoint, user, password)
minio_client.create_bucket(backet)

if __name__ == "__main__":
    # from dotenv import load_dotenv

    # load_dotenv(override=True)
    # endpoint = f"{os.getenv('MINIO_HOST')}:{os.getenv('MINIO_PORT')}"
    # user = os.getenv("MINIO_ROOT_USER")
    # password = os.getenv("MINIO_ROOT_PASSWORD")
    # s3_client = MinioClient(endpoint, user, password)
    minio_client.create_bucket("new-bucket")
    print(minio_client.bucket_exists("new-bucket"))
    minio_client.upload_file('new-bucket', 'faiss/test.json', 'test.json')
    print(minio_client.list_objects('new-bucket'))
