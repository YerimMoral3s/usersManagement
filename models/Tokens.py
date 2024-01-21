from app import db

class Tokens(db.Model):
  #  `id` int NOT NULL AUTO_INCREMENT,
  # `user_id` int NOT NULL,
  # `business_id` int NOT NULL,
  # `access_token` varchar(200) NOT NULL,
  # `refresh_token` varchar(200) NOT NULL,
  # `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  # `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, nullable=False)
  business_id = db.Column(db.Integer, nullable=False)
  access_token = db.Column(db.String(200), nullable=False)
  refresh_token = db.Column(db.String(200), nullable=False)

  def to_dict(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'business_id': self.business_id,
      'access_token': self.access_token,
      'refresh_token': self.refresh_token
    }
