from trello import TrelloClient
import psycopg2
import config

trelloClient = TrelloClient(
    api_key=config.api_key,
    api_secret=config.api_secret
)

db = psycopg2.connect(host="localhost", database="trelloData", user=config.db_user, password=config.db_password)
db.set_session(autocommit=True)
# clear db of tasks
cur = db.cursor()
cur.execute("DELETE FROM api_task;")
cur.close()

cardExists = False

cursor = db.cursor()
query = "INSERT INTO api_task(title, description, done, due_date, list) VALUES "

# fetch from trelloAPI
allBoards = trelloClient.list_boards()
weekBoard = ''
for board in allBoards:
    if board.name == 'Week':
        weekBoard = board

if weekBoard != '':
    lists = weekBoard.list_lists()
    for list in lists:
        for card in list.list_cards():
            cardExists = True
            query += "('%s','%s','%s','%s','%s'), " % \
                     (card.name, card.description, str(card.badges['dueComplete']), str(card.due_date), list.name)
    query = query[:-2]
    query += ";"
    if cardExists:
        cursor.execute(query)
cursor.close()
db.close()