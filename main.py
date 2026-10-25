from __future__ import annotations
from typing import Callable

from exceptions import ProjectManagementError, ValidationError
from system import ProjectManagementSystem
from storage import FileStorage
from models import (
    Employee,
    Client,
    Project,
    Task,
    Milestone,
    Resource,
    Risk,
    Meeting,
    Report,
)

STORAGES: dict[str, tuple[str, str]] = {
    "1": ("JSON", "data/project_data.json"),
    "2": ("XML", "data/project_data.xml"),
}


def ask_text(prompt: str) -> str:
    return input(prompt).strip()


def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число.")


def ask_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Нужно ввести число.")


class ConsoleApp:
    def __init__(self) -> None:
        self._system = ProjectManagementSystem()
        self._menu: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Добавить сотрудника", self.add_employee),
            "2": ("Добавить клиента", self.add_client),
            "3": ("Создать проект", self.add_project),
            "4": ("Добавить задачу в проект", self.add_task),
            "5": ("Добавить этап (Milestone) в проект", self.add_milestone),
            "6": ("Добавить ресурс в проект", self.add_resource),
            "7": ("Добавить риск в проект", self.add_risk),
            "8": ("Добавить встречу в проект", self.add_meeting),
            "9": ("Добавить отчет в проект", self.add_report),
            "10": ("Показать все данные", self.show_all),
            "11": ("Изменить проект", self.update_project),
            "12": ("Удалить проект", self.delete_project),
            "13": ("Сохранить в файл", self.save),
            "14": ("Загрузить из файла", self.load),
        }

    def add_employee(self) -> None:
        employee = Employee(ask_int("ID сотрудника: "), ask_text("Имя: "), ask_text("Должность: "))
        self._system.add_employee(employee)
        print(f"Сотрудник добавлен: {employee.name}")

    def add_client(self) -> None:
        client = Client(ask_int("ID клиента: "), ask_text("Имя: "), ask_text("Компания: "))
        self._system.add_client(client)
        print(f"Клиент добавлен: {client.company}")

    def add_project(self) -> None:
        project = Project(ask_int("ID проекта: "), ask_text("Название: "), ask_float("Бюджет: "))
        self._system.add_project(project)
        print(f"Проект создан: {project.title}")

    def add_task(self) -> None:
        project = self._system.get_project(ask_int("ID проекта: "))
        project.tasks.append(Task(ask_int("ID задачи: "), ask_text("Название: "), ask_text("Статус: ")))
        print("Задача добавлена.")

    def add_milestone(self) -> None:
        project = self._system.get_project(ask_int("ID проекта: "))
        project.milestones.append(Milestone(ask_int("ID этапа: "), ask_text("Название: "), ask_text("Дедлайн: ")))
        print("Этап добавлен.")

    def add_resource(self) -> None:
        project = self._system.get_project(ask_int("ID проекта: "))
        project.resources.append(Resource(ask_int("ID ресурса: "), ask_text("Название: "), ask_float("Стоимость: ")))
        print("Ресурс добавлен.")

    def add_risk(self) -> None:
        project = self._system.get_project(ask_int("ID проекта: "))
        project.risks.append(
            Risk(ask_int("ID риска: "), ask_text("Описание: "), ask_float("Вероятность (0.0 - 1.0): ")))
        print("Риск добавлен.")

    def add_meeting(self) -> None:
        project = self._system.get_project(ask_int("ID проекта: "))
        project.meetings.append(Meeting(ask_int("ID встречи: "), ask_text("Тема: "), ask_text("Дата и время: ")))
        print("Встреча добавлена.")

    def add_report(self) -> None:
        project = self._system.get_project(ask_int("ID проекта: "))
        project.reports.append(Report(ask_int("ID отчета: "), ask_text("Содержимое: "), ask_text("Дата создания: ")))
        print("Отчет добавлен.")

    def show_all(self) -> None:
        sys = self._system
        print("\n--- СОТРУДНИКИ ---")
        for e in sys.employees:
            print(f"- ID: {e.id}, Имя: {e.name}, Должность: {e.position}")

        print("\n--- КЛИЕНТЫ ---")
        for c in sys.clients:
            print(f"- ID: {c.id}, Компания: {c.company}")

        print("\n--- ПРОЕКТЫ ---")
        if not sys.projects:
            print("Нет проектов.")
        for p in sys.projects:
            print(f"\n[Проект #{p.project_id}] {p.title} (Бюджет: {p.budget})")
            print(f"  Задач: {len(p.tasks)}, Этапов: {len(p.milestones)}, Ресурсов: {len(p.resources)}")

    def update_project(self) -> None:
        self._system.update_project(ask_int("ID проекта: "), ask_text("Новое название: "), ask_float("Новый бюджет: "))
        print("Проект обновлен.")

    def delete_project(self) -> None:
        self._system.delete_project(ask_int("ID проекта: "))
        print("Проект удален.")

    @staticmethod
    def _ask_storage_path() -> tuple[str, str]:
        choice = ask_text("Формат (1 - JSON, 2 - XML): ")
        if choice not in STORAGES:
            raise ValidationError("Нужно выбрать 1 или 2.")
        return STORAGES[choice]

    def save(self) -> None:
        file_type, filename = self._ask_storage_path()
        if file_type == "JSON":
            FileStorage.save_to_json(filename, self._system)
        else:
            FileStorage.save_to_xml(filename, self._system)
        print(f"Данные сохранены в файл: {filename}")

    def load(self) -> None:
        file_type, filename = self._ask_storage_path()
        if file_type == "JSON":
            FileStorage.load_from_json(filename, self._system)
        else:
            FileStorage.load_from_xml(filename, self._system)
        print(f"Данные загружены из файла: {filename}")

    def run(self) -> None:
        try:
            while True:
                print("\n=== Система управления проектами ===")
                for key, (title, _) in self._menu.items():
                    print(f"{key}. {title}")
                print("0. Выход")

                choice = input("Выберите пункт: ").strip()
                if choice == "0":
                    break
                if choice not in self._menu:
                    print("Нет такого пункта меню.")
                    continue

                try:
                    self._menu[choice][1]()
                except ProjectManagementError as error:
                    print(f"[Ошибка]: {error}")
                except Exception as ex:
                    print(f"[Непредвиденная ошибка]: {ex}")
        except (EOFError, KeyboardInterrupt):
            print()
        print("До свидания!")


if __name__ == "__main__":
    ConsoleApp().run()