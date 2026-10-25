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
                "employees": [e.to_dict() for e in system_data.employees],
                "clients": [c.to_dict() for c in system_data.clients],
                "projects": [p.to_dict() for p in system_data.projects]
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

            # Сотрудники
            employees_el = ET.SubElement(root, "Employees")
            for e in system_data.employees:
                e_el = ET.SubElement(employees_el, "Employee", id=str(e.id))
                ET.SubElement(e_el, "Name").text = e.name
                ET.SubElement(e_el, "Position").text = e.position

            # Клиенты
            clients_el = ET.SubElement(root, "Clients")
            for c in system_data.clients:
                c_el = ET.SubElement(clients_el, "Client", id=str(c.id))
                ET.SubElement(c_el, "Name").text = c.name
                ET.SubElement(c_el, "Company").text = c.company

            # Проекты со всей вложенной структурой
            projects_el = ET.SubElement(root, "Projects")
            for p in system_data.projects:
                p_el = ET.SubElement(projects_el, "Project", id=str(p.project_id))
                ET.SubElement(p_el, "Title").text = p.title
                ET.SubElement(p_el, "Budget").text = str(p.budget)

                tasks_el = ET.SubElement(p_el, "Tasks")
                for t in p.tasks:
                    t_el = ET.SubElement(tasks_el, "Task", id=str(t.task_id))
                    ET.SubElement(t_el, "Title").text = t.title
                    ET.SubElement(t_el, "Status").text = t.status

                milestones_el = ET.SubElement(p_el, "Milestones")
                for m in p.milestones:
                    m_el = ET.SubElement(milestones_el, "Milestone", id=str(m.milestone_id))
                    ET.SubElement(m_el, "Title").text = m.title
                    ET.SubElement(m_el, "Deadline").text = m.deadline

                resources_el = ET.SubElement(p_el, "Resources")
                for r in p.resources:
                    r_el = ET.SubElement(resources_el, "Resource", id=str(r.resource_id))
                    ET.SubElement(r_el, "Name").text = r.name
                    ET.SubElement(r_el, "Cost").text = str(r.cost)

                risks_el = ET.SubElement(p_el, "Risks")
                for rk in p.risks:
                    rk_el = ET.SubElement(risks_el, "Risk", id=str(rk.risk_id))
                    ET.SubElement(rk_el, "Description").text = rk.description
                    ET.SubElement(rk_el, "Probability").text = str(rk.probability)

                meetings_el = ET.SubElement(p_el, "Meetings")
                for mt in p.meetings:
                    mt_el = ET.SubElement(meetings_el, "Meeting", id=str(mt.meeting_id))
                    ET.SubElement(mt_el, "Topic").text = mt.topic
                    ET.SubElement(mt_el, "DateTime").text = mt.date_time

                reports_el = ET.SubElement(p_el, "Reports")
                for rp in p.reports:
                    rp_el = ET.SubElement(reports_el, "Report", id=str(rp.report_id))
                    ET.SubElement(rp_el, "Content").text = rp.content
                    ET.SubElement(rp_el, "CreatedDate").text = rp.created_date

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
            system_data.employees.clear()
            system_data.clients.clear()

            # Загрузка сотрудников
            emp_root = root.find("Employees")
            if emp_root is not None:
                for e_el in emp_root.findall("Employee"):
                    eid = int(e_el.get("id", 0))
                    name = e_el.findtext("Name", "")
                    pos = e_el.findtext("Position", "")
                    system_data.employees.append(Employee(eid, name, pos))

            # Загрузка клиентов
            cli_root = root.find("Clients")
            if cli_root is not None:
                for c_el in cli_root.findall("Client"):
                    cid = int(c_el.get("id", 0))
                    name = c_el.findtext("Name", "")
                    comp = c_el.findtext("Company", "")
                    system_data.clients.append(Client(cid, name, comp))

            # Загрузка проектов и их подсущностей
            proj_root = root.find("Projects")
            if proj_root is not None:
                for p_el in proj_root.findall("Project"):
                    pid = int(p_el.get("id", 0))
                    title = p_el.findtext("Title", "Без названия")
                    budget = float(p_el.findtext("Budget", "0.0"))

                    proj = Project(pid, title, budget)

                    # Задачи
                    tasks_el = p_el.find("Tasks")
                    if tasks_el is not None:
                        for t_el in tasks_el.findall("Task"):
                            tid = int(t_el.get("id", 0))
                            t_title = t_el.findtext("Title", "")
                            t_status = t_el.findtext("Status", "")
                            proj.tasks.append(Task(tid, t_title, t_status))

                    # Этапы
                    mil_el = p_el.find("Milestones")
                    if mil_el is not None:
                        for m_el in mil_el.findall("Milestone"):
                            mid = int(m_el.get("id", 0))
                            m_title = m_el.findtext("Title", "")
                            m_deadline = m_el.findtext("Deadline", "")
                            proj.milestones.append(Milestone(mid, m_title, m_deadline))

                    # Ресурсы
                    res_el = p_el.find("Resources")
                    if res_el is not None:
                        for r_el in res_el.findall("Resource"):
                            rid = int(r_el.get("id", 0))
                            r_name = r_el.findtext("Name", "")
                            r_cost = float(r_el.findtext("Cost", "0.0"))
                            proj.resources.append(Resource(rid, r_name, r_cost))

                    # Риски
                    risk_el = p_el.find("Risks")
                    if risk_el is not None:
                        for rk_el in risk_el.findall("Risk"):
                            rk_id = int(rk_el.get("id", 0))
                            rk_desc = rk_el.findtext("Description", "")
                            rk_prob = float(rk_el.findtext("Probability", "0.0"))
                            proj.risks.append(Risk(rk_id, rk_desc, rk_prob))

                    # Встречи
                    meet_el = p_el.find("Meetings")
                    if meet_el is not None:
                        for mt_el in meet_el.findall("Meeting"):
                            mt_id = int(mt_el.get("id", 0))
                            mt_topic = mt_el.findtext("Topic", "")
                            mt_dt = mt_el.findtext("DateTime", "")
                            proj.meetings.append(Meeting(mt_id, mt_topic, mt_dt))

                    # Отчеты
                    rep_el = p_el.find("Reports")
                    if rep_el is not None:
                        for rp_el in rep_el.findall("Report"):
                            rp_id = int(rp_el.get("id", 0))
                            rp_content = rp_el.findtext("Content", "")
                            rp_date = rp_el.findtext("CreatedDate", "")
                            proj.reports.append(Report(rp_id, rp_content, rp_date))

                    system_data.projects.append(proj)
        except (ET.ParseError, IOError, ValueError) as e:
            raise ProjectManagementError(f"Ошибка чтения из XML: {e}")