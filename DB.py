from sqlalchemy import create_engine

from singleton import Singleton
from sqlalchemy.orm import sessionmaker

class Singleton(type):
  def __call__(cls, *args):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Singleton, cls).__call__(*args)
    return cls.instance
    
class DB:
  __metaclass__ = Singleton

  def __init__(self):

    url = 'postgresql://maboss:py03thon@localhost:5432/maboss'
    engine = create_engine(url,echo = False)
    Session = sessionmaker(bind=engine)
    self.session = Session()

  def execute(self, sql):
      self.session.execute(sql)
      self.session.execute("commit")

  def query(self,sql):
      return self.session.execute(sql)

  def main(self):
    sql = """update mi_monitor set active = 22 where pointgroup = '21103'"""
    rt = db.execute(sql)
    # for rows in rt.fetchall():
    #     print rows

if __name__ == '__main__':
   db = DB()
   db.main()
