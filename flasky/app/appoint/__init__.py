# -*- coding: utf-8 -*-
from flask import Blueprint

appoint = Blueprint('appoint', __name__)

from . import views
