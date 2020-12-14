from flask import Flask, render_template, flash, redirect, url_for, app
from flask_sqlalchemy import SQLAlchemy

from Dependency.RegistrationDependency import BankService, MailService
from forms import RegistrationForm
from provider.database_provider import DatabaseProvider
from repository.sqlite_db import SQliteRepository
from service import RegistrationService


app = Flask(__name__)
app.config['SECRET_KEY'] = '5327276e6ca815ae038cf07a38f68975'
provider = DatabaseProvider('/home/kamila/Documents/auction_area_2')
db_config = provider.get_database_configuration(section='sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = SQliteRepository.get_connection_path(db_path=db_config)
db = SQLAlchemy(app)


repository = SQliteRepository(db)
bank = BankService()
mail = MailService()
service = RegistrationService(data_base=repository, bank_service=bank, mail_service=mail)


@app.route('/')
@app.route('/home')
def home():
    return 'Hello World!'


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        service.registration(username=form.username.data, phone=form.phone.data, email=form.email.data)
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)
