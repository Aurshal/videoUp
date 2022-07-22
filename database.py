from datetime import datetime
from dataclasses import dataclass
from app import db


@dataclass
class UploadedVideo(db.Model):
    id:int
    name:str
    duration:str
    size:str
    date_added:datetime
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique=True)
    duration = db.Column(db.Float, nullable = False)
    size = db.Column(db.Float, nullable = False)
    date_added = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self) -> str:
        return self.name 
        
