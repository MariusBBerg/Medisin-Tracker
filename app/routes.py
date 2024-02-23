from flask import request, jsonify, Blueprint, redirect, url_for, flash,session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager
from .models import User, MilkLog, PillLog
from datetime import datetime, timedelta
from dateutil.parser import parse
from flask import render_template
from sqlalchemy import func
from pytz import timezone,utc


bp = Blueprint('bp', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return jsonify({'username': current_user.username}), 200
    else:
        return jsonify({'username': None}), 200


@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username').lower()
        password = data.get('password')
        timezone = data.get('timezone')
        
        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already taken'}), 409

        new_user = User(username=username, password_hash=generate_password_hash(password),timezone=timezone)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return jsonify({'message': 'User successfully registered'}), 201


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username').lower()
        password = data.get('password')
        
        user = authenticate_user(username, password)
        if user:
            login_user(user)
            return jsonify({'message': 'Logged in successfully', 'username': user.username}), 200
        return jsonify({'message': 'Invalid username or password'}), 401

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/drink_milk', methods=['POST'])
@login_required
def drink_milk():
    last_pill = PillLog.query.filter_by(user_id=current_user.id).order_by(PillLog.timestamp.desc()).first()
    now = datetime.utcnow()  # Nåværende tid i UTC som offset-naive
    
    if last_pill:
        # Forsikre deg om at last_pill.timestamp også er offset-naive eller konverter begge til samme type
        pill_timestamp = last_pill.timestamp.replace(tzinfo=None)

        if now - pill_timestamp < timedelta(hours=1):
            return jsonify({'message': 'Cannot drink milk less than 1 hour after taking pill'}), 400
    
    milk_log = MilkLog(user_id=current_user.id, timestamp=now)
    db.session.add(milk_log)
    db.session.commit()
    return jsonify({'message': 'Milk logged successfully'}), 200



@bp.route('/take_pill', methods=['POST'])
@login_required
def take_pill():
    last_pill = PillLog.query.filter_by(user_id=current_user.id).order_by(PillLog.timestamp.desc()).first()
    now = datetime.utcnow() # Endre til UTC nåtid

    if last_pill and now - last_pill.timestamp < timedelta(hours=5):
        return jsonify({'message': 'Cannot take pill less than 5 hours apart'}), 400
    pill_log = PillLog(user_id=current_user.id, timestamp=now)
    db.session.add(pill_log)
    db.session.commit()
    return jsonify({'message': 'Pill logged successfully'}), 200


@bp.route('/can_i', methods=['GET'])
@login_required
def can_i():
    last_milk = MilkLog.query.filter_by(user_id=current_user.id).order_by(MilkLog.timestamp.desc()).first()
    last_pill = PillLog.query.filter_by(user_id=current_user.id).order_by(PillLog.timestamp.desc()).first()
    now = datetime.utcnow()  # Endre til UTC nåtid

   
    can_take_pill = True if (not last_milk or now - last_milk.timestamp > timedelta(hours=1)) and (not last_pill or now - last_pill.timestamp > timedelta(hours=5)) else False
    can_drink_milk = True if (not last_pill or now - last_pill.timestamp > timedelta(hours=1)) else False

    return jsonify({
        'can_take_pill': can_take_pill,
        'can_drink_milk': can_drink_milk,
        'last_milk_time_utc': last_milk.timestamp.isoformat() if last_milk else None,
        'last_pill_time_utc': last_pill.timestamp.isoformat() if last_pill else None,
        'user_timezone': current_user.timezone
    }), 200


@bp.route('/api/auth/check')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True}), 200
    else:
        return jsonify({'authenticated': False}), 401
    


@bp.route('/two_pills_days', methods=['GET'])
@login_required
def two_pills_days():
    two_pills_days = db.session.query(func.date(PillLog.timestamp)).filter_by(user_id=current_user.id).group_by(func.date(PillLog.timestamp)).having(func.count(PillLog.id) >= 2).all()
    return jsonify({'two_pills_days': [day[0] for day in two_pills_days]}), 200


@bp.route('/milk_logs', methods=['GET', 'POST', 'DELETE','PUT'])
@login_required
def milk_logs():
    if request.method == 'GET':
        milk_logs = MilkLog.query.filter_by(user_id=current_user.id).order_by(MilkLog.timestamp.desc()).all()
        return jsonify({'milk_logs': [milk_log.timestamp.isoformat() for milk_log in milk_logs]}), 200
    elif request.method == 'POST':
        now = datetime.utcnow()
        milk_log = MilkLog(user_id=current_user.id, timestamp=now)
        db.session.add(milk_log)
        db.session.commit()
        return jsonify({'message': 'Milk logged successfully'}), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        timestamp_str = data.get('timestamp')
        timestamp = parse(timestamp_str)
        milk_log = MilkLog.query.filter_by(user_id=current_user.id, timestamp=timestamp).first()
        if milk_log:
            db.session.delete(milk_log)
            db.session.commit()
            return jsonify({'message': 'Milk log deleted successfully'}), 200
        else:
            return jsonify({'message': 'Milk log not found'}), 404
    elif request.method == 'PUT':
            data = request.get_json()
            old_timestamp_str = data.get('old_timestamp')
            new_timestamp_str = data.get('new_timestamp')
            old_timestamp = parse(old_timestamp_str)
            new_timestamp = parse(new_timestamp_str)
            milk_log = MilkLog.query.filter_by(user_id=current_user.id, timestamp=old_timestamp).first()
            if milk_log:
                milk_log.timestamp = new_timestamp
                db.session.commit()
                return jsonify({'message': 'Milk log updated successfully'}), 200
            else:
                return jsonify({'message': 'Milk log not found'}), 404

@bp.route('/pill_logs', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def pill_logs():
    if request.method == 'GET':
        pill_logs = PillLog.query.filter_by(user_id=current_user.id).order_by(PillLog.timestamp.desc()).all()
        return jsonify({'pill_logs': [pill_log.timestamp.isoformat() for pill_log in pill_logs]}), 200
    elif request.method == 'POST':
        data = request.get_json()
        timestamp_str = data.get('timestamp')
        timestamp = parse(timestamp_str)
        pill_log = PillLog(user_id=current_user.id, timestamp=timestamp)
        db.session.add(pill_log)
        db.session.commit()
        return jsonify({'message': 'Pill logged successfully'}), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        timestamp_str = data.get('timestamp')
        timestamp = parse(timestamp_str)
        pill_log = PillLog.query.filter_by(user_id=current_user.id, timestamp=timestamp).first()
        if pill_log:
            db.session.delete(pill_log)
            db.session.commit()
            return jsonify({'message': 'Pill log deleted successfully'}), 200
        else:
            return jsonify({'message': 'Pill log not found'}), 404

    elif request.method == 'PUT':
            data = request.get_json()
            old_timestamp_str = data.get('old_timestamp')
            new_timestamp_str = data.get('new_timestamp')
            old_timestamp = parse(old_timestamp_str)
            new_timestamp = parse(new_timestamp_str)
            pill_log = PillLog.query.filter_by(user_id=current_user.id, timestamp=old_timestamp).first()
            if pill_log:
                pill_log.timestamp = new_timestamp
                db.session.commit()
                return jsonify({'message': 'Pill log updated successfully'}), 200
            else:
                return jsonify({'message': 'Pill log not found'}), 404
def init_app(app):
    app.register_blueprint(bp)
