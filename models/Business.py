from app import db

class Business(db.Model):
  #  id` int NOT NULL AUTO_INCREMENT,
  # `name` varchar(255) NOT NULL,
  # `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  # `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }


