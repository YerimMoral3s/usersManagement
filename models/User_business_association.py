from app import db

class UserBusinessAssociation(db.Model): 
	# id INT AUTO_INCREMENT PRIMARY KEY,
  # user_id INT,
  # business_id INT,
  # FOREIGN KEY (user_id) REFERENCES Users(id),
  # FOREIGN KEY (business_id) REFERENCES Business(id)
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, nullable=False)
  business_id = db.Column(db.Integer, nullable=False)

  def to_dict(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'business_id': self.business_id
    }