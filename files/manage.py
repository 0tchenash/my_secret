from app import create_app, db
from flask_migrate import upgrade, migrate, init, stamp
from dao.models.models import User

def deploy():
	"""Run deployment tasks."""

	app = create_app()
	app.app_context().push()
	db.drop_all()
	db.create_all()

	init()
	stamp()
	migrate()
	upgrade()
	
deploy()

