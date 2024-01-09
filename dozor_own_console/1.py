from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Agents, db
from host_and_sniffer_api import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Неправильный позывной или секретное слово')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@login_required  # Ограничиваем доступ только для авторизованных пользователей
def register():
    if current_user.username !='odmen': # Ограничиваем доступ для админа
        flash('Это не входит в твои должностные обязанности')
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Этот боец уже в строю')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/logs', methods=['GET', 'POST'])
@login_required  # Ограничиваем доступ только для авторизованных пользователей
def logs():
    if request.method == 'POST':
        print(1)
    return render_template('logs.html')

@app.route('/agents', methods=['GET', 'POST'])
@login_required
def agents():
    if request.method == 'POST':
        ip = request.form['agent-ip']
        agent = Agents.query.filter_by(ip=ip).first()
        if agent:
            flash('Этот агент уже добавлен')
        else:
            description = request.form['agent-description']
            type = request.form['scanner-type']
            new_agent = Agents(ip = ip, description = description, type = type)
            db.session.add(new_agent)
            db.session.commit()
            return redirect('agents')

    agents = Agents.query.all()
    return render_template('agents.html', agents=agents)

@app.route('/delete=<int:agent_id>', methods=['GET', 'POST'])
def delete(agent_id):
    agent = Agents.query.get_or_404(agent_id)
    if request.method == 'POST':
        db.session.delete(agent)
        db.session.commit()
        flash('Futyn удален')
        return redirect(url_for('agents'))
    return render_template('delete.html', agent=agent)

@app.route('/agent=<int:agent_id>')
@login_required
def agent_details(agent_id):
    agents = Agents.query.all()
    for agent in agents:
        if agent_id == agent.id:
            if agent.type == 'Сетевой сканер':
                return render_template('network_scanner.html', agent=agent)
            else:
                return render_template('endpoint_scanner.html', agent=agent)

@app.route('/antivirus=<int:agent_id>')
@login_required
def antivirus(agent_id):
    agents = Agents.query.all()
    for agent in agents:
        if agent_id == agent.id:
            name = agent.ip
            viruses = host_antivirus(name)
            for virus in viruses:
                flash(virus)
            return redirect(f'agent={agent_id}')
        

@app.route('/host_logs=<int:agent_id>')
@login_required
def host_logs(agent_id):
    name = request.form.get('agentIP')
    logs = host_select_logs(name)
    for log in logs:
        flash(log)
    return redirect(f'agent={agent_id}')
        
@app.route('/sniffer_start=<int:agent_id>')
@login_required
def sniffer_start(agent_id):
    agents = Agents.query.all()
    for agent in agents:
        if agent_id == agent.id:
            name = agent.ip
            logs = start_sniffer(name)
            for log in logs:
                flash(log)
            return redirect(f'agent={agent_id}')

@app.route('/sniffer_stop=<int:agent_id>')
@login_required
def sniffer_stop(agent_id):
    agents = Agents.query.all()
    for agent in agents:
        if agent_id == agent.id:
            name = agent.ip
            logs = stop_sniffer(name)
            for log in logs:
                flash(log)
            return redirect(f'agent={agent_id}')

@app.route('/sniffer_alerts=<int:agent_id>', methods=['GET', 'POST'])
@login_required
def sniffer_alerts(agent_id):
    if request.method == 'POST':
        date = request.form['date-picker']
        agents = Agents.query.all()
        for agent in agents:
            if agent_id == agent.id:
                name = agent.ip
                logs = select_sniffer_alerts(name, date)
                for log in logs:
                    flash(log)
                return redirect(f'agent={agent_id}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)