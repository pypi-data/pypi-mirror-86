import requests
import logging
import json
import sys
from lxml import etree
from io import StringIO
from dataclasses import dataclass
from qportalwrapper.datatypes import Student, Assignment, Class, ProgressReport


class QError(Exception):
    """
    A Q Portal Error (e.g. login error)
    """
    def __init__(self, msg, *args):
        super().__init__(*args)
        self.msg = msg


class QPortalWrapper(requests.Session):
    """
    A Python wrapper for accessing Aequitas Solutions's
    Q Portal service.

    NOTE: All API endpoints, etc. used in this wrapper
    are unofficial and subject to change at any time, which
    can cause the wrapper to break. If the wrapper no longer works,
    file an issue.
    """

    def __init__(self, q_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q_url = q_url
        self.parser = etree.HTMLParser()
        self.students = []
        self.selected_student = None

    def __get_students(self):
        """
        Get a list of viewable Students from Q.

        Endpoint: /Home/PortalMainPage (no student selected)

        NOTE: This method is meant for internal use
        only. If you want to get a list of viewable Students,
        use `get_students()`.

        NOTE: This method will only work if a student has not yet
        been selected. Once a student has been selected, this method
        will fail. This is by design, as this internal method is intended
        to only run once.
        """
        if self.selected_student != None:
            # Student is already selected, this won't work
            raise QError("Student already selected, cannot fetch new student list")

        res = self.get(self.q_url + "/Home/PortalMainPage")
        root = etree.parse(StringIO(res.text), self.parser)
        students = [Student.from_html(el) for el in root.xpath("//tr[contains(@class, 'sturow') and @id]")]
        return students

    def login(self, user, password):
        """
        Log in to the Q Portal, given a user and password.
        Sets a session cookie which will be used to authenticate
        for other methods.

        Endpoint used: /Home/Login
        """
        # Post login data
        login_data = {"Pin": user, "Password": password}
        res = self.post(self.q_url + "/Home/Login", login_data).json()

        # Check that everything went ok
        # NOTE: Does not catch exceptions (e.g. timeouts)
        if res["valid"] != "1":
            if res["msg"] == "Login Not Found":
                print("Login Not Found! check user or password.")
            else:
                print(res)

            raise QError(res["msg"])

        # Get list of students
        self.students = self.__get_students()

    def get_students(self):
        """
        Get a list of viewable students.
        """
        return self.students

    def select_student(self, student_id: int):
        """
        Select a student in Q Portal.
        This method is required to fetch student information.
        """
        self.selected_student = list(filter(lambda s: s.id == student_id, self.students))[0]
        res = self.get(self.q_url + f"/StudentBanner/SetStudentBanner/{student_id}")

        if res.status_code != 200:
            raise QError(res.text)

    def get_assignments(self):
        """
        Return a list of assignments for the selected Student.

        Endpoint: /Home/LoadProfileData/Assignments
        """
        if self.selected_student is None:
            raise QError("No student selected. Please use wrapper.select_student().")

        res = self.get(self.q_url + "/Home/LoadProfileData/Assignments")
        root = etree.parse(StringIO(res.text), self.parser)
        classes_xml = root.xpath("//table[contains(@id, 'tblassign')]")
        classes = []

        for q_class in classes_xml:
            assignments_xml = q_class.xpath("./tbody/tr")
            assignments = []
            for assignment in assignments_xml:
                assignments.append(Assignment.from_html(assignment))

            # Magically parse the caption and t_head into class metadata
            # Found through the power of Inspect Element :)
            class_info = q_class.xpath("./caption")[0]
            period = int(class_info.xpath("./text()")[1][2:])
            class_name = class_info.xpath("./b")[0].text.strip()

            # Get grade info as well
            # TODO: Find a better way to parse semester/trimester grading period
            class_info = q_class.xpath("./thead/tr")[0]
            grade_info = class_info[0]
            class_id = int(grade_info.xpath("./a")[0].get("id")[3:])
            grading_period = grade_info.xpath("./input[@type='hidden']")[0].get("value")
            grade = grade_info.xpath("./text()")[1].strip()
            teacher = class_info[1].xpath("./text()")[1].strip()

            classes.append(Class(class_id, period, class_name, teacher, grade, grading_period, assignments))

        return classes

    def get_progress_reports(self, class_id):
        """
        Given a class ID and term, return a list of available progress reports.
        Equivalent to "View Progress Reports".
        """
        if self.selected_student is None:
            raise QError("No student selected. Please use wrapper.select_student().")

        res = self.get(self.q_url + f"/Home/AssignmentProgRpt/{class_id}")
        root = etree.parse(StringIO(res.text), self.parser)
        progress_reports_xml = root.xpath("//table/tbody/tr")
        progress_reports = []
        for report in progress_reports_xml:
            progress_reports.append(ProgressReport.from_html(class_id, report))

        return progress_reports
