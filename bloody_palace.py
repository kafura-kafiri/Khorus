from Choori import Choori
from config import db
from crud.paper import bp as paper, papers
from crud.user import bp as user, users

server = Choori(db)
server.blueprint(paper, papers)
server.blueprint(user, users)
server.run()
