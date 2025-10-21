# Импорт встроенной библиотеки для работы веб-сервера
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "127.0.0.1"
serverPort = 5000


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        # 1. Узнаём какой файл запросили
        path = self.path.split('?')[0].lstrip('/')
        if path == '':
            path = 'index.html'

        # 2. Проверяем есть ли файл
        if os.path.exists(path):
            # 3. Отправляем УСПЕШНЫЙ ответ
            self.send_response(200)

            # 4. Определяем тип контента
            ext = os.path.splitext(path)[1].lower()
            content_types = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript'
            }
            content_type = content_types.get(ext, 'text/plain')
            self.send_header("Content-type", content_type)
            self.end_headers()

            # 5. Отправляем содержимое файла в сеть
            with open(path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            # 6. Если файла нет - ошибка 404
            self.send_error(404, f" ❌ File not found: {path}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":

    print("⭐ ⭐ ⭐ Домашняя работа 21.2 ⭐ ⭐ ⭐")

    # Инициализация веб-сервера, который будет по заданным параметрам в сети
    # принимать запросы и отправлять их на обработку специальному классу,
    # который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("🟢 Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("⚠️ Server stopped.")
