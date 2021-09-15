from .base import swagger_doc
from flask import Blueprint, redirect

@swagger_doc.route('/')
def index():
    return redirect('/api/v1', code=302)