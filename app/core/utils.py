import os
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename


def save_upload_file(app_name, file_data) -> str:
    file_ext = os.path.splitext(secure_filename(file_data.filename))[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = uuid.uuid4().hex[:6]
    filename = f"{timestamp}_{random_str}{file_ext}"
    os.makedirs(f"app/static/{app_name}/uploads/", exist_ok=True)
    with open(f"app/static/{app_name}/uploads/" + filename, "wb") as file:
        file.write(file_data.read())
    return filename
