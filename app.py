from flask import Flask, render_template, request, make_response
from models import db, Employee, Project, EmployeeProject
from weasyprint import HTML

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leelanjan@localhost:5432/resume_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/')
def dashboard():
    employees = Employee.query.all()
    projects = Project.query.all()
    return render_template(
        'dashboard.html',
        employees=employees,
        projects=projects
    )

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp = Employee(
            name=request.form['name'],
            designation=request.form['designation'],
            email=request.form['email'],
            phone=request.form['phone'],
            summary=request.form['summary'],
            technical_skills=request.form['technical_skills']
        )
        db.session.add(emp)
        db.session.commit()
        return f"Employee {emp.name} added successfully!"
    return render_template('add_employee.html')

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        proj = Project(
            project_name=request.form['project_name'],
            description=request.form['description'],
            technologies_used=request.form['technologies_used']
        )
        db.session.add(proj)
        db.session.commit()
        return f"Project {proj.project_name} added successfully!"
    return render_template('add_project.html')

@app.route('/assign_project', methods=['GET', 'POST'])
def assign_project():
    if request.method == 'POST':
        emp_id = int(request.form['employee_id'])
        proj_id = int(request.form['project_id'])
        role = request.form['role']

        mapping = EmployeeProject(
            employee_id=emp_id,
            project_id=proj_id,
            role=role
        )
        db.session.add(mapping)
        db.session.commit()
        return "Project assigned successfully!"
    employees = Employee.query.all()
    projects = Project.query.all()
    return render_template(
        'assign_project.html',
        employees=employees,
        projects=projects
    )

@app.route('/generate', methods=['POST'])
def generate_resume():
    query = request.form['query']

    if query.isdigit():
        employee = Employee.query.filter(
            Employee.employee_id == int(query)
        ).first()
    else:
        employee = Employee.query.filter(
            Employee.name.ilike(f"%{query}%")
        ).first()

    if not employee:
        return "Employee not found", 404

    projects = db.session.query(
        Project,
        EmployeeProject.role
    ).join(
        EmployeeProject,
        Project.project_id == EmployeeProject.project_id
    ).filter(
        EmployeeProject.employee_id == employee.employee_id
    ).all()

    html = render_template(
        'resume.html',
        employee=employee,
        projects=projects
    )

    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = (
        f'attachment; filename={employee.name}_Resume.pdf'
    )

    return response

if __name__ == '__main__':
    app.run(debug=True)
