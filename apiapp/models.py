from apiapp import db
from apiapp import ma


class Survivor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survived = db.Column(db.Integer)
    passengerClass = db.Column(db.Integer)
    name = db.Column(db.Text)
    sex = db.Column(db.Text)
    # Some ages are decimals - store as text for consistency
    age = db.Column(db.Text)
    siblingsOrSpousesAboard = db.Column(db.Integer)
    parentsOrChildrenAboard = db.Column(db.Integer)
    # Decimals - store as text for consistency
    fare = db.Column(db.Text)

    def __init__(self, **data):

        self.setvalues(**data)

    def setvalues(self, **data):

        self.survived = data['survived']
        self.passengerClass = data['passengerClass']
        self.name = data['name']
        self.sex = data['sex']
        self.age = data['age']
        self.siblingsOrSpousesAboard = data['siblingsOrSpousesAboard']
        self.parentsOrChildrenAboard = data['parentsOrChildrenAboard']
        self.fare = data['fare']


class SurvivorSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'survived',
            'passengerClass',
            'name',
            'sex',
            'age',
            'siblingsOrSpousesAboard',
            'parentsOrChildrenAboard',
            'fare'
        )
