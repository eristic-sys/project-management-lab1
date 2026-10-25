from __future__ import annotations
from typing import List
from exceptions import ValidationError


class Person:
    def __init__(self, person_id: int, name: str) -> None:
        if not name.strip():
            raise ValidationError("Имя не может быть пустым.")
        self.id: int = person_id
        self.name: str = name

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


class Employee(Person):
    def __init__(self, person_id: int, name: str, position: str) -> None:
        super().__init__(person_id, name)
        self.position: str = position

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"position": self.position})
        return d


class Client(Person):
    def __init__(self, person_id: int, name: str, company: str) -> None:
        super().__init__(person_id, name)
        self.company: str = company

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"company": self.company})
        return d


class Task:
    def __init__(self, task_id: int, title: str, status: str) -> None:
        self.task_id: int = task_id
        self.title: str = title
        self.status: str = status

    def to_dict(self) -> dict:
        return {"task_id": self.task_id, "title": self.title, "status": self.status}


class Milestone:
    def __init__(self, milestone_id: int, title: str, deadline: str) -> None:
        self.milestone_id: int = milestone_id
        self.title: str = title
        self.deadline: str = deadline

    def to_dict(self) -> dict:
        return {"milestone_id": self.milestone_id, "title": self.title, "deadline": self.deadline}


class Resource:
    def __init__(self, resource_id: int, name: str, cost: float) -> None:
        if cost < 0:
            raise ValidationError("Стоимость ресурса не может быть отрицательной.")
        self.resource_id: int = resource_id
        self.name: str = name
        self.cost: float = cost

    def to_dict(self) -> dict:
        return {"resource_id": self.resource_id, "name": self.name, "cost": self.cost}


class Risk:
    def __init__(self, risk_id: int, description: str, probability: float) -> None:
        if not (0.0 <= probability <= 1.0):
            raise ValidationError("Вероятность риска должна быть в диапазоне от 0.0 до 1.0.")
        self.risk_id: int = risk_id
        self.description: str = description
        self.probability: float = probability

    def to_dict(self) -> dict:
        return {"risk_id": self.risk_id, "description": self.description, "probability": self.probability}


class Meeting:
    def __init__(self, meeting_id: int, topic: str, date_time: str) -> None:
        self.meeting_id: int = meeting_id
        self.topic: str = topic
        self.date_time: str = date_time

    def to_dict(self) -> dict:
        return {"meeting_id": self.meeting_id, "topic": self.topic, "date_time": self.date_time}


class Report:
    def __init__(self, report_id: int, content: str, created_date: str) -> None:
        self.report_id: int = report_id
        self.content: str = content
        self.created_date: str = created_date

    def to_dict(self) -> dict:
        return {"report_id": self.report_id, "content": self.content, "created_date": self.created_date}


class Project:
    def __init__(self, project_id: int, title: str, budget: float) -> None:
        if budget < 0:
            raise ValidationError("Бюджет проекта не может быть отрицательным.")
        self.project_id: int = project_id
        self.title: str = title
        self.budget: float = budget

        self.tasks: List[Task] = []
        self.milestones: List[Milestone] = []
        self.resources: List[Resource] = []
        self.risks: List[Risk] = []
        self.meetings: List[Meeting] = []
        self.reports: List[Report] = []

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "title": self.title,
            "budget": self.budget,
            "tasks": [t.to_dict() for t in self.tasks],
            "milestones": [m.to_dict() for m in self.milestones],
            "resources": [r.to_dict() for r in self.resources],
            "risks": [rk.to_dict() for rk in self.risks],
            "meetings": [mt.to_dict() for mt in self.meetings],
            "reports": [rp.to_dict() for rp in self.reports],
        }