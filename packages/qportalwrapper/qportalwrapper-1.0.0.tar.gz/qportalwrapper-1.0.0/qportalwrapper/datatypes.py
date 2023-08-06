from typing import List
from dataclasses import dataclass
from lxml import etree
import requests

@dataclass
class Student:
    """
    A representation of a Q Student
    (e.g. name, grade, etc)
    """
    id: int
    name: str
    grade: int
    school: str
    year: str
    birthdate: str

    @staticmethod
    def from_html(html: etree._Element):
        """
        Create a Student object from a parsed
        HTML element.
        """
        id = html.get("id")

        (name,
         grade,
         school,
         year,
         birthdate,
         *other) = [attr.text if attr.text != None else "" for attr in html][2:]

        return Student(id, name, grade, school, year, birthdate)


@dataclass
class Assignment:
    """
    A representation of a Q Assignment (entry in gradebook)
    """
    due: str
    assigned: str
    name: str
    total_pts: float
    score: float
    pct: float
    class_avg: float
    scored_as: str
    extra_credit: bool
    graded: bool
    comments: str = ""

    def from_html(assignment: etree._Element):
        """
        Create an Assignment from HTML.
        Assumes input is a <tr> element from
        /Home/LoadProfileData.
        """
        if len(assignment) == 10:
            # Normal variant, no pct_score category
            (detail,
             due_date,
             assigned,
             name,
             total_pts,
             score,
             scored_as,
             extra_credit,
             not_graded,
             comments) = [attr.text for attr in assignment]
            percent = None
            class_avg = None
        elif len(assignment) == 11:
            # Variant with pct_score category
            (detail,
             due_date,
             assigned,
             name,
             total_pts,
             score,
             percent,
             scored_as,
             not_graded,
             extra_credit,
             comments) = [attr.text for attr in assignment]
            class_avg = None
        else:
            # Variant with pct_score and class_avg category
            (detail,
             due_date,
             assigned,
             name,
             total_pts,
             score,
             percent,
             class_avg,
             scored_as,
             extra_credit,
             not_graded,
             comments) = [attr.text for attr in assignment]

        if percent == None:
            if score != None and float(total_pts) != 0:
                percent = float(score) / float(total_pts) * 100
            elif float(total_pts) == 0:
                score = 0
                percent = 100
            else:
                score = 0
                percent = 0
        else:
            # Remove % sign
            percent = percent[:-1]

        if class_avg != None:
            # Remove % sign
            class_avg = class_avg[:-1]

        return Assignment(due_date,
                          assigned,
                          name,
                          float(total_pts),
                          float(score) if score != None else None,
                          float(percent) if percent != None else None,
                          float(class_avg) if class_avg != None else None,
                          scored_as,
                          bool(extra_credit),
                          not bool(not_graded),
                          comments)


@dataclass
class Class:
    """
    A representation of a Class in Q.
    Used for grouping assignments.
    """
    id: int
    period: str
    name: str
    teacher: str
    grade: str
    grading_period: str
    assignments: List[Assignment]


@dataclass
class ProgressReport:
    """
    Container for a Progress Report in Q.
    Used for storing data about a progress report
    (download link, grade, etc).
    """
    class_id: int
    term_id: str
    term_name: str
    begin_date: str
    end_date: str
    grade: str

    def pdf(self, wrapper):
        """
        Downloads the progress report PDF.
        Requires a wrapper to download from (so we
        can use the session id).
        """
        res = wrapper.get(wrapper.q_url + f"/Home/PrintProgressReport/{self.class_id}^{self.term_id}")
        return res.content

    @staticmethod
    def from_html(class_id: int, report: etree._Element):
        """
        Create a ProgressReport from HTML, given a class_id.
        Assumes input is in <tr> format
        (see QPortalWrapper.get_progress_reports()).
        """
        (term_name,
         begin_date,
         end_date,
         grade, *other) = [attr.text.strip() for attr in report]
        term_id = report[-1].xpath("./a")[0].get("href").split("'")[1]

        return ProgressReport(class_id, term_id, term_name, begin_date, end_date, grade)
