from __future__ import annotations
import os
import json
import xml.etree.ElementTree as ET
from models import Project, Employee, Client, Task, Milestone, Resource, Risk, Meeting, Report
from exceptions import ProjectManagementError


class FileStorage:
    """Класс для управления сохранением и загрузкой данных в JSON и XML."""

    @staticmethod
    def _ensure_dir(filename: str) -> None:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    @classmethod
    def save_to_json(cls, filename: str, system_data) -> None:
        try:
            cls._ensure_dir(filename)
            data = {
                "projects": [p.to_dict() for p in system_data.projects],
                "employees": [e.to_dict() for e in system_data.employees],
                "clients": [c.to_dict() for c in system_data.clients]
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise ProjectManagementError(f"Ошибка записи в JSON: {e}")

    @classmethod
    def load_from_json(cls, filename: str, system_data) -> None:
        try:
            if not os.path.exists(filename):
                raise ProjectManagementError(f"Файл {filename} не найден.")
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                system_data.projects.clear()
                system_data.employees.clear()
                system_data.clients.clear()

                for ed in data.get("employees", []):
                    system_data.employees.append(Employee(ed["id"], ed["name"], ed["position"]))

                for cd in data.get("clients", []):
                    system_data.clients.append(Client(cd["id"], cd["name"], cd["company"]))

                for pd in data.get("projects", []):
                    proj = Project(pd["project_id"], pd["title"], pd["budget"])

                    for td in pd.get("tasks", []):
                        proj.tasks.append(Task(td["task_id"], td["title"], td["status"]))
                    for md in pd.get("milestones", []):
                        proj.milestones.append(Milestone(md["milestone_id"], md["title"], md["deadline"]))
                    for rd in pd.get("resources", []):
                        proj.resources.append(Resource(rd["resource_id"], rd["name"], rd["cost"]))
                    for rkd in pd.get("risks", []):
                        proj.risks.append(Risk(rkd["risk_id"], rkd["description"], rkd["probability"]))
                    for mtd in pd.get("meetings", []):
                        proj.meetings.append(Meeting(mtd["meeting_id"], mtd["topic"], mtd["date_time"]))
                    for rpd in pd.get("reports", []):
                        proj.reports.append(Report(rpd["report_id"], rpd["content"], rpd["created_date"]))

                    system_data.projects.append(proj)
        except (IOError, json.JSONDecodeError) as e:
            raise ProjectManagementError(f"Ошибка чтения из JSON: {e}")

    @classmethod
    def save_to_xml(cls, filename: str, system_data) -> None:
        try:
            cls._ensure_dir(filename)
            root = ET.Element("ProjectManagementSystem")

            projects_el = ET.SubElement(root, "Projects")
            for p in system_data.projects:
                p_el = ET.SubElement(projects_el, "Project", id=str(p.project_id))
                ET.SubElement(p_el, "Title").text = p.title
                ET.SubElement(p_el, "Budget").text = str(p.budget)

            tree = ET.ElementTree(root)
            tree.write(filename, encoding="utf-8", xml_declaration=True)
        except IOError as e:
            raise ProjectManagementError(f"Ошибка записи в XML: {e}")

    @classmethod
    def load_from_xml(cls, filename: str, system_data) -> None:
        try:
            if not os.path.exists(filename):
                raise ProjectManagementError(f"Файл {filename} не найден.")
            tree = ET.parse(filename)
            root = tree.getroot()
            system_data.projects.clear()

            proj_root = root.find("Projects")
            if proj_root is not None:
                for p_el in proj_root.findall("Project"):
                    pid_str = p_el.get("id")
                    pid = int(pid_str) if pid_str is not None else 0

                    title_el = p_el.find("Title")
                    title = title_el.text if title_el is not None and title_el.text else "Без названия"

                    budget_el = p_el.find("Budget")
                    budget_str = budget_el.text if budget_el is not None and budget_el.text else "0.0"
                    budget = float(budget_str)

                    system_data.projects.append(Project(pid, title, budget))
        except (ET.ParseError, IOError, ValueError) as e:
            raise ProjectManagementError(f"Ошибка чтения из XML: {e}")