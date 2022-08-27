from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'Task {self.task} {self.deadline.strftime("%Y-%m-%d")}'

def add_task():
    t = input('Enter a task\n')
    task = Task(task=t)
    session.add(task)
    session.commit()
    # print(task)
    print('The task has been added!')

def read_task():
    d = datetime.today().date()
    q = session.query(Task).filter(Task.deadline==d).all()
    print('\nToday:')
    if q:
        for i in range(len(q)):
            print(f'{i+1}. {q[i].task}')
    else:
        print('Nothing to do!')
    print()

Base.metadata.create_all(engine)
menu = '''1) Today's tasks
2) Add a task
0) Exit
'''

while True:
    cmd = int(input(menu))
    if cmd == 1:
        read_task()
    elif cmd == 2:
        add_task()
    else:
        break
print('Bye!')
session.close()
