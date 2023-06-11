import csv
import os

def create_csv_file(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)

    table = [
        ["history_score", "building_score", "level_count"],
        [0, 0, 0]
    ]

    if not os.path.exists(filepath):
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(table)
    return

def delete_csv_file(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)
    os.remove(filepath)

def get_history_score(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)

    # Чтение значения history_score из CSV-файла
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            history_score = float(row["history_score"])
            return history_score

def get_building_score(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)

    # Чтение значения history_score из CSV-файла
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            building_score = float(row["building_score"])
            return building_score

def get_user_level(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)

    # Чтение значения history_score из CSV-файла
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            level_count = float(row["level_count"])
            return level_count

def increment_level_count(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)

    # Обновление значения level_count
    updated_rows = []
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["level_count"] = str(int(row["level_count"]) + 1)
            updated_rows.append(row)

    # Запись обновленных данных в CSV-файл
    fieldnames = ["history_score", "building_score", "level_count"]
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

def increment_history_score(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)

    # Обновление значения history_score
    updated_rows = []
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["history_score"] = str(float(row["history_score"]) + 1)
            updated_rows.append(row)

    # Запись обновленных данных в CSV-файл
    fieldnames = ["history_score", "building_score", "level_count"]
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

def increment_building_score(user_id):
    directory = "scores"
    filename = f"{user_id}.csv"
    filepath = os.path.join(directory, filename)

    # Обновление значения building_score
    updated_rows = []
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["building_score"] = str(float(row["building_score"]) + 1)
            updated_rows.append(row)

    # Запись обновленных данных в CSV-файл
    fieldnames = ["history_score", "building_score", "level_count"]
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)