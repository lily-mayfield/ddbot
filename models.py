# FIXME: primary key being avoided because you have to do
# some annoying copypaste code to get primary keys to show
import datetime

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from . import config


db = SQLAlchemy()


class AllowedDiscordAdminAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_id = Column(Integer, ForeignKey('choice.id'))
    identity_hash = db.Column(db.String(60), nullable=False)


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey('proposal.id'), nullable=False)
    votes = relationship('Vote')
    text = db.Column(db.String(1000), nullable=False)


class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(60), nullable=False)
    channel_name = db.Column(db.String(60), nullable=False)
    passed = db.Column(db.Bool(), default=False, nullable=False)
    failed = db.Column(db.Bool(), default=False, nullable=False)
    text = db.Column(db.String(1000))
    choices = relationship('Choice')
    discord_action = relationship('AllowedDiscordAdminAction')


if __name__ == '__main__':
    # FIXME: this is a horrible way to check for database
    # considering people may not even use sqlite!!!!
    if not os.path.isfile('bubblebbs/test.db'):
        models.db.create_all()
        test_user = models.User(login="admin", password=generate_password_hash("admin"))
        models.db.session.add(test_user)
        key_pairs = [
            ('site_tagline', config.SITE_TAGLINE),
            ('site_title', config.SITE_TITLE),
            ('site_footer', config.SITE_FOOTER),
        ]
        for key, value in key_pairs:
            models.db.session.add(models.ConfigPair(key=key, value=value))

        models.db.session.commit()

    return
