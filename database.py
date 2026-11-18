
import json
import os

FILE_NAME = "gym_data.json"


def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def add_member(data, member):
    if any(m["id"] == member["id"] for m in data):
        return False

    data.append(member)
    save_data(data)
    return True


def delete_member(data, member_id):
    for member in data:
        if member["id"] == member_id:
            data.remove(member)
            save_data(data)
            return True

    return False


def update_member(data, member_id, new_info):
    for member in data:
        if member["id"] == member_id:
            member.update(new_info)
            save_data(data)
            return True

    return False
