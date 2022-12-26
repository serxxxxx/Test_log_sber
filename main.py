import datetime

def parse_log_line(line):
    # Извлекаем время из строки и преобразуем его в формат datetime
    timestamp = datetime.datetime.strptime(line[:23], "%Y-%m-%d %H:%M:%S.%f")
    # Извлекаем DocId из строки
    doc_id = line.split("<DocId>")[1].split("</DocId>")[0]
    return timestamp, doc_id

# Открываем файлы и считываем строки в списки
with open("start.log") as f:
    start_lines = f.readlines()

with open("stop.log") as f:
    stop_lines = f.readlines()

# Создаем словарь для хранения результатов
results = {}

# Проходим по списку start_lines и добавляем в словарь новые записи
for line in start_lines:
    timestamp, doc_id = parse_log_line(line)
    if doc_id not in results:
        results[doc_id] = {
            "start_time": timestamp,
            "stop_time": None,
            "count": 0,
            "duration": 0
        }

# Проходим по списку stop_lines и обновляем существующие записи
for line in stop_lines:
    timestamp, doc_id = parse_log_line(line)
    if doc_id in results:
        data = results[doc_id]
        data["stop_time"] = timestamp
        data["count"] += 1
        duration = (timestamp - data["start_time"]).total_seconds()
        data["duration"] += duration

# Открываем файл itog.txt в режиме записи и записываем в него результаты из словаря results
with open("itog.txt", "w") as f:
    for doc_id, data in results.items():
        start_time = data["start_time"]
        stop_time = data["stop_time"]
        count = data["count"]
        duration = data["duration"]
        # Вычисляем среднюю длительность запроса в миллисекундах
        average_duration = duration / count
        # Формируем строку для записи в файл
        line = f"{start_time};{count};{average_duration}"
        # Записываем строку в файл
        f.write(line + "\n")

