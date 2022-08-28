from datetime import datetime, timedelta
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

def del_task():
    q = session.query(Task).order_by(Task.deadline).all()
    if q:
        print('Choose the number of the task you want to delete:')
        print_query(q, True)
        i = int(input())
        if 0 < i <= len(q):
            session.delete(q[i - 1])
            session.commit()
            print('The task has been deleted!')
        else:
            print('Nothing to delete')
    else:
        print('Nothing to delete')

def add_task():
    t = input('Enter a task\n')
    d = input('Enter a deadline\n')
    date = datetime.strptime(d, "%Y-%m-%d")
    task = Task(task=t, deadline=date)
    session.add(task)
    session.commit()
    print(task)
    print('The task has been added!')

def print_query(q, with_date):
    if q:
        for i in range(len(q)):
            s = f'{i+1}. {q[i].task}'
            if with_date:
                s += f'. {q[i].deadline.strftime("%#d %b")}'
            print(s)
    else:
        print('Nothing to do!')

def read_task(p):
    d = datetime.today().date()
    if p == 1:
        print(f'\nToday {d.strftime("%#d %b")}:')
        q = session.query(Task).filter(Task.deadline==d).all()
        print_query(q, False)
    elif p == -1:
        print(f'\nMissed tasks:')
        q = session.query(Task).filter(Task.deadline < d).all()
        if q:
            print_query(q, True)
        else:
            print('All tasks have been completed!')
    elif p == 7:
        for i in range(7):
            date = d + timedelta(days=i)
            print(f'\n{date.strftime("%A %#d %b")}:')
            q = session.query(Task).filter(Task.deadline == date).order_by(Task.deadline).all()
            print_query(q, False)
    else:
        print('\nAll tasks:')
        q = session.query(Task).order_by(Task.deadline).all()
        print_query(q, True)
    print()

Base.metadata.create_all(engine)
menu = '''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add a task
6) Delete a task
0) Exit
'''

while True:
    cmd = int(input(menu))
    if cmd == 1:
        read_task(1)
    elif cmd == 2:
        read_task(7)
    elif cmd == 3:
        read_task(0)
    elif cmd == 4:
        read_task(-1)
    elif cmd == 5:
        add_task()
    elif cmd == 6:
        del_task()
    else:
        break
print('Bye!')
session.close()
