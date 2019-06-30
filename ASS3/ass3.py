import csv
import numpy as np
import matplotlib.pyplot as plt
import sqlite3,json


def create_db(db_file):
    '''
    uase this function to create a db, don't change the name of this function.
    db_file: Your database's name.
    '''
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ASS3
               (age INTEGER,
               sex    INTEGER,
               chest_pain_type   INTEGER,
               resting_blood_pressure  INTEGER,
               serum      INTEGER,
               blood_sugar    INTEGER,
               resting   INTEGER,
               heart rate   INTEGER,
               angina   INTEGER,
               oldpeak   FLOAT,
                ST  INTEGER,
                vessels   INTEGER,
                thal   INTEGER,
                target    INTEGER);''')
    except Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

def import_data():
    with open('processed.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    data=np.array(rows)
    create_db('data.db')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    for i in range(0,data.shape[0]):
        for j in range(0,data.shape[1]):
            if data[i,j] == '?':
                data[i,j] = 0
        c.execute("insert into ASS3 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (data[i,0],data[i,1],data[i,2],data[i,3],data[i,4],data[i,5],data[i,6],
                data[i, 7], data[i, 8], data[i, 9], data[i, 10], data[i, 11], data[i, 12], data[i, 13]))
        conn.commit()


conn = sqlite3.connect('data.db')
c = conn.cursor()
temp = []
data_list = {}
c.execute('select age from ASS3;')
for age in c:
    temp.append(age[0])
if len(temp) == 0:
    import_data()
else:
    c.execute('select * from ASS3 group by age,sex;')

def chest_pain(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT chest_pain_type,count(chest_pain_type) FROM ASS3 where age =? and sex = 0 group by sex,chest_pain_type;',(age,))
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT chest_pain_type,count(chest_pain_type) FROM ASS3 where age =? and sex = 1 group by sex,chest_pain_type;',(age,))
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    total_width, n = 0.8, 2
    width = total_width / n
    lable_list = ['typical angin','atypical angina','non-anginal pain','asymptomatic']
    plt.bar(male_type, male_list,width=width, label='male', fc='y')
    for i in range(len(female_type)):
        female_type[i] += width
    plt.bar(female_type, female_list,width=width, label='female', fc='r')
    plt.legend()
    plt.show()


def  blood_sugar(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT  blood_sugar,count(blood_sugar) '
                   'FROM ASS3 where age =? and sex=0 group by blood_sugar;',(age,))
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT  blood_sugar,count(blood_sugar) '
                   'FROM ASS3 where age =? and sex=1 group by blood_sugar;',(age,))
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    label = ['<120 mg/dl','>120 mg/dl']
    plt.subplot(211)
    plt.pie(male_list,autopct = '%3.2f%%',)
    plt.subplot(212)
    plt.pie(female_list,autopct = '%3.2f%%',)
    plt.show()


def electrocardiographic(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT resting,count(resting) FROM ASS3 where age =? and sex = 0 group by sex,resting;',(age,))
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT resting,count(resting) FROM ASS3 where age =? and sex = 1 group by sex,resting;',(age,))
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    total_width, n = 0.8, 2
    width = total_width / n

    plt.bar(male_type, male_list,width=width, label='male', fc='y')
    for i in range(len(female_type)):
        female_type[i] += width
    plt.bar(female_type, female_list,width=width, label='female', fc='r')
    plt.legend()
    plt.show()



def  exercise_induced_angina(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT angina,count(angina) FROM ASS3 where age =? and sex = 0 group by sex,angina;',(age,))
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT angina,count(angina) FROM ASS3 where age =? and sex = 1 group by sex,angina;',(age,))
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    total_width, n = 0.8, 2
    width = total_width / n

    plt.bar(male_type, male_list,width=width, label='male', fc='y')
    for i in range(len(female_type)):
        female_type[i] += width
    plt.bar(female_type, female_list,width=width, label='female', fc='r')
    plt.legend()
    plt.show()


def  slope_of_ST(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT ST,count(ST) FROM ASS3 where age =? and sex = 0 group by sex,ST;',(age,))
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT ST,count(ST) FROM ASS3 where age =? and sex = 1 group by sex,ST;',(age,))
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    total_width, n = 0.8, 2
    width = total_width / n

    plt.bar(male_type, male_list,width=width, label='male', fc='y')
    for i in range(len(female_type)):
        female_type[i] += width
    plt.bar(female_type, female_list,width=width, label='female', fc='r')
    plt.legend()
    plt.show()



def  number_of_vessels(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT vessels,count(vessels) FROM ASS3 where age =? and sex = 0 group by sex,vessels;',(age,))
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT vessels,count(vessels) FROM ASS3 where age =? and sex = 1 group by sex,vessels;',(age,))
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    total_width, n = 0.8, 2
    width = total_width / n

    plt.bar(male_type, male_list,width=width, label='male', fc='y')
    for i in range(len(female_type)):
        female_type[i] += width
    plt.bar(female_type, female_list,width=width, label='female', fc='r')
    plt.legend()
    plt.show()


def  thal(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT thal,count(thal) FROM ASS3 where age =? and sex = 0 group by sex,thal;',(age,))
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT thal,count(thal) FROM ASS3 where age =? and sex = 1 group by sex,thal;',(age,))
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    total_width, n = 0.8, 2
    width = total_width / n

    plt.bar(male_type, male_list,width=width, label='male', fc='y')
    for i in range(len(female_type)):
        female_type[i] += width
    plt.bar(female_type, female_list,width=width, label='female', fc='r')
    plt.legend()
    plt.show()



def  target(age):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT target,count(target) FROM ASS3 where age =? and sex = 0 group by sex,target;',(age,))
    male_type = [0,1]
    male_list = [0,0]
    for item in c1:
        if item[0] == 0:
            male_list[0]  = item[1]
        else:
            male_list[1] += item[1]
    c2 = c.execute('SELECT target,count(target) FROM ASS3 where age =? and sex = 1 group by sex,target;',(age,))
    female_type = [0,1]
    female_list = [0,0]
    for item in c2:
        if item[0] == 0:
            female_list[0] = item[1]
        else:
            female_list[1] += item[1]

    total_width, n = 0.8, 2
    width = total_width / n
    label = ['no disease','have disease']
    plt.bar(male_type, male_list,width=width, label='male', fc='y')
    for i in range(len(female_type)):
        female_type[i] += width
    plt.bar(female_type, female_list,width=width, label='female' ,fc='r')
    plt.legend()
    plt.show()


def resting_blood_pressure():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c1 = c.execute('SELECT age,resting_blood_pressure FROM ASS3 where sex = 0;')
    male_type = []
    male_list = []
    for item in c1:
        male_type.append(item[0])
        male_list.append(item[1])
    c2 = c.execute('SELECT age,resting_blood_pressure FROM ASS3 where sex = 1 ;')
    female_type = []
    female_list = []
    for item in c2:
        female_type.append(item[0])
        female_list.append(item[1])
    plt.scatter(male_type,male_list,marker='o')
    plt.scatter(female_type, female_list, marker='o')
    plt.xticks(np.arange(29, 77, 3.0))

    plt.show()

resting_blood_pressure()
target(51)
thal(51)
number_of_vessels(51)
slope_of_ST(51)
exercise_induced_angina(51)
electrocardiographic(51)
blood_sugar(51)
chest_pain(51)