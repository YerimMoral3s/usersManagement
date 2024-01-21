from app import db

class Users(db.Model):
  #  id` int NOT NULL AUTO_INCREMENT,
  # `user_name` varchar(255) DEFAULT NULL,
  # `password` varchar(255) DEFAULT NULL,
  # `phone` varchar(255) DEFAULT NULL,
  # `email` varchar(255) DEFAULT NULL,
  # `verified` tinyint(1) DEFAULT NULL,
  # `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  # `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  #  `password_email` varchar(255) DEFAULT NULL,
  #   `password_email_expire` timestamp NULL DEFAULT NULL,
  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(255), nullable=False)
  password = db.Column(db.String(255), nullable=False)
  phone = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  verified = db.Column(db.Boolean, nullable=False)
  created_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
  password_email = db.Column(db.String(255), nullable=False)
  password_email_expire = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())


  def to_dict(self):
    return {
      'id': self.id,
      'user_name': self.user_name,
      'phone': self.phone,
      'email': self.email,
      'verified': self.verified,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }

