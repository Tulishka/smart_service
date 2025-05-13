import os
import uuid
from datetime import datetime

from app.config import Config


def save_upload_file(file_data) -> str:
    """Сохраняет поле формы типа файл, переданного пользователем

    :param file_data: данные о файле из формы
    :return: возвращает название файла, в который были сохранены данные
    """
    file_ext = os.path.splitext(file_data.filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = uuid.uuid4().hex[:6]
    filename = f"{timestamp}_{random_str}{file_ext}"
    os.makedirs(f"app/{Config.MEDIA_FOLDER}/uploads/", exist_ok=True)
    with open(f"app/{Config.MEDIA_FOLDER}/uploads/" + filename, "wb") as file:
        file.write(file_data.read())
    return filename
