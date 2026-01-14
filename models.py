from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    summary = db.Column(db.Text)
    technical_skills = db.Column(db.Text)

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(150))
    description = db.Column(db.Text)
    technologies_used = db.Column(db.Text)

class EmployeeProject(db.Model):
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
    role = db.Column(db.String(100))
