from __future__ import annotations
from typing import List
from exceptions import ValidationError, EntityNotFoundError
from models import Project, Employee, Client
from storage import FileStorage


class ProjectManagementSystem:
    def __init__(self) -> None:
        self.projects: List[Project] = []
        self.employees: List[Employee] = []
        self.clients: List[Client] = []

    def add_project(self, project: Project) -> None:
        if any(p.project_id == project.project_id for p in self.projects):
            raise ValidationError(f"Проект с ID {project.project_id} уже существует.")
        self.projects.append(project)

    def get_project(self, project_id: int) -> Project:
        for p in self.projects:
            if p.project_id == project_id:
                return p
        raise EntityNotFoundError(f"Проект с ID {project_id} не найден.")

    def update_project(self, project_id: int, title: str, budget: float) -> None:
        project = self.get_project(project_id)
        if budget < 0:
            raise ValidationError("Бюджет не может быть отрицательным.")
        project.title = title
        project.budget = budget

    def delete_project(self, project_id: int) -> None:
        project = self.get_project(project_id)
        self.projects.remove(project)

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def save_to_json(self, filename: str) -> None:
        FileStorage.save_to_json(filename, self)

    def load_from_json(self, filename: str) -> None:
        FileStorage.load_from_json(filename, self)

    def save_to_xml(self, filename: str) -> None:
        FileStorage.save_to_xml(filename, self)

    def load_from_xml(self, filename: str) -> None:
        FileStorage.load_from_xml(filename, self)