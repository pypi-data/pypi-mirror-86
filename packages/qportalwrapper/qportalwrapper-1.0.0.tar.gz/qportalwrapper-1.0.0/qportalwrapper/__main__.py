"""
Example usage of the QPortalWrapper.
This will login to Q and fetch assignments.
"""
from qportalwrapper.qportalwrapper import QPortalWrapper, QError

conn = QPortalWrapper("https://sis.pleasantonusd.net/StudentPortal")

try:
    conn.login("98027", "Bb2004")
except QError as e:
    print(e.msg)

students = conn.get_students()
print(students)

conn.select_student(students[0].id)
class1 = conn.get_assignments()[1]
print(class1.name)
print(class1.assignments)
reports = conn.get_progress_reports(class1.id)
with open("out.pdf", "wb") as f:
    # Write pdf report
    f.write(reports[0].pdf(conn))
