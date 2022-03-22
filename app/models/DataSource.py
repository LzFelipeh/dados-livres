from app import db


class DataSource(db.Model):
  __tablename__ = "data_sources"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(84))
  category = db.Column(db.String(84))
  page_link = db.Column(db.String(84))
  description = db.Column(db.String(2048))
  sphere = db.Column(db.String(84))
  country = db.Column(db.String(84))
  state = db.Column(db.String(84))
  city = db.Column(db.String(84))

  def __str__(self):
    return self.title