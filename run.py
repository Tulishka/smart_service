"""
Точка входа для запуска приложения.

"""

import os
from app import app


if __name__ == "__main__":
    # Запуск приложения с портом из переменной окружения PORT, без авто-перезагрузки при изменениях
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, use_reloader=False)
