import csv
import json

def csv2dict(csv_file):
    """
    Конвертация данных .csv файла в словарь
    """
    #Читаем данные с файла
    results_dict = {}
    reader = csv.DictReader(open(csv_file),delimiter=';')
    #По каждой строчке читаем данные
    for row in reader:
        #По каждому значению в строчке пишем в единый словарь
        for key, value in row.items():
            #Добавляем данные в словарь
            if key not in results_dict:
                results_dict[key] = []
            results_dict[key].append(value)
    
    #Возвращаем результат
    return results_dict

def score2mark(score):
    """Конвертация баллов в оценку"""
    score = int(score)
    if score < 50:
        return 2
    elif score < 70:
        return 3
    elif score < 86:
        return 4
    return 5

def first_task(search_teacher_id, search_group_id):
    """
    1. Написать функцию, которая принимает id преподавателя и id группы.
    Функция возвращает False, если данный преподаватель не преподавал у данной группы,
    None, если такого прподавателя не существует, иначе возвращается словарь,
    в котором ключами являются наименования предметов,
    а значениями словари, которые хранят в себе информации о количестве студентов,
    сдавших на 5, 4, 3 и 2 по данному предмету.
    """
    search_teacher_id = str(search_teacher_id)
    search_group_id = str(search_group_id)
    
    results_csv  = csv2dict("./csv/results.csv")
    students_csv = csv2dict("./csv/students.csv")
    subjects_csv = csv2dict("./csv/subjects.csv")

    students_groups = {}
    students_teachers = {}
    #Добавляем группу каждому студенту
    for i in range(len(students_csv["id"])):
        group_id = students_csv["group_id"][i]
        student_id = students_csv["id"][i]
        students_groups[student_id] = group_id
        #Добавляем данные в словарь учителей
        students_teachers[student_id] = []
    
    #Добавляем преподавателя каждому студенту
    for i in range(len(results_csv["id"])):

        teacher_id = results_csv["teacher_id"][i]
        student_id = results_csv["student_id"][i]
        students_teachers[student_id].append(teacher_id)

    groups_teachers = {}
    #Создаем словарь групп и учителей
    for student, group in students_groups.items():
        teachers = students_teachers[student]
        groups_teachers[group] = list(set(teachers))

    #Поиск по id преподавателя и id группы
    if search_group_id not in groups_teachers:
        print("Запрошенного id группы не существует!")
        return
    
    #Возврат None, если преподавателя с таким id не существует
    if search_teacher_id not in results_csv["teacher_id"]:
        return None
    
    #Если преподаватель не ведет занятия в группе, то возвращаем Flase
    if not search_teacher_id in groups_teachers[search_group_id]:
        return False

    #Если преподаватель ведет занятия в группе, то 
    #Формируем словарь в котором ключами являются наименования предметов,
    #а значениями словари, которые хранят в себе информации о количестве студентов, сдавших на 5, 4, 3 и 2 по данному предмету и возвращаем его
    subject_marks_dict = {}

    #Формируем словарь id предмета - название предмета
    subjectid_names = {}
    for i in range(len(subjects_csv["id"])):
        subjectid_names[subjects_csv["id"][i]] = subjects_csv["subject_name"][i]

    #Формируем словарь id предмета - оценки
    subjectid_marks = {}
    for i in range(len(results_csv["id"])):

        subject_id = results_csv["subject"][i]
        score = results_csv["total"][i]
        if subject_id not in subjectid_marks:
            subjectid_marks[subject_id] = []
        subjectid_marks[subject_id].append(score)

    #Формируем словарь итоговый
    for key, value in subjectid_names.items():
        #Список оценок по предмету
        marks_list = subjectid_marks[key]
        #Для каждого элемента применяем функцию score2mark
        newmarks_list = list(map(score2mark, marks_list))
        #Считаем кол-во каждой оценки с помощью count и формируем словарь с кол-вом каждой оценки
        buf_dict = {"mark_2" : newmarks_list.count(2), "mark_3" : newmarks_list.count(3), "mark_4" : newmarks_list.count(4), "mark_5" : newmarks_list.count(5)}
        subject_marks_dict[value] = buf_dict

    return subject_marks_dict


def second_task(search_teacher_fio, to_json=False):

    """
    2. Написать функцию, которая принимает ФИО преподавателя и необязательный параметр to_json,
    который по умолчанию равен False и принимает имя файла.
    Если указан параметр to_json, то он должен сохранить итоговый результат в данный файл и вернуть 
    значение True, иначе просто вернуть словарь.
    В словаре ключами являются наименования групп, в которых он преподавал,
    а значениям - результат выполнения первой функции.
    """
    #Загрузка данных
    groups_csv = csv2dict("./csv/groups.csv")
    teachers_csv = csv2dict("./csv/teachers.csv")
    students_csv = csv2dict("./csv/students.csv")
    results_csv = csv2dict("./csv/results.csv")

    #Промежуточные словари
    teachersid_teachersfio = {}
    teachersfio_teachersid = {}
    groupsid_groupsnames = {}
    groupsnames_groupsid = {}
    students_groups = {}
    teachers_students = {}
    allteachers_allgroups = {}

    #Результирующий словарь
    result_dict = {}

    #Заполнение словаря teachersid_teachersfio
    for i in range(len(teachers_csv["id"])):
        teacher_id = teachers_csv["id"][i]
        #Формируем ФИО в одну строку
        teacher_name = teachers_csv["last_name"][i] + " " + teachers_csv["first_name"][i] + " " + teachers_csv["middle_name"][i]
        #Заносим значения в словарь
        teachersid_teachersfio[teacher_id] = teacher_name
        #Заносим значения в обратный словарь
        teachersfio_teachersid[teacher_name] = teacher_id
        #Добавляем данные в словарь учителей
        teachers_students[teacher_id] = []

    #Проверка на существование преподавателя
    if search_teacher_fio not in teachersid_teachersfio.values():
        print("Преподаватель с ФИО {} не найден".format(search_teacher_fio))
        return
    
    #Добавляем группу каждому студенту
    for i in range(len(students_csv["id"])):
        group_id = students_csv["group_id"][i]
        student_id = students_csv["id"][i]
        students_groups[student_id] = group_id
    
    #Добавляем каждого студента преподавателю
    for i in range(len(results_csv["id"])):
        teacher_id = results_csv["teacher_id"][i]
        student_id = results_csv["student_id"][i]
        teachers_students[teacher_id].append(student_id)
    
    #Избавляемся от дубликатов студентов
    for key, value in teachers_students.items():
        teachers_students[key] = list(set(value))

    #Создаем словарь учителей и групп 
    for student_id, group_id in students_groups.items():
        for teacher_id, students_list in teachers_students.items():
            #Если есть студент в списке, то меняем его значение на id группы, к которой он относится
            if student_id in students_list:
                students_list[students_list.index(student_id)] = group_id
    
    teacher_groups = teachers_students
    
    #Избавляемся от дубликатов групп
    for key, value in teacher_groups.items():
        teacher_groups[key] = list(set(value))

    #Создаем словарь id группы -> название группы, а также обратный
    for i in range(len(groups_csv["id"])):
        groupsid_groupsnames[groups_csv["id"][i]] = groups_csv["name"][i]
        groupsnames_groupsid[groups_csv["name"][i]] = groups_csv["id"][i]

    # Формируем словарь учителей - групп путем замены id на названия
    for teacher_id, groupsid_list in teacher_groups.items():
        
        #ФИО учителя по id
        teacherfio = teachersid_teachersfio[teacher_id]
        #Названия групп по id
        groupsnames_list = [groupsid_groupsnames[id] for id in groupsid_list]
        #Запись в финальный словарь
        allteachers_allgroups[teacherfio] =  groupsnames_list

    #Выбираем только группы, которые нам нужны по ФИО преподавателя
    thisgroups = allteachers_allgroups[search_teacher_fio]
    
    #id запрашиваемого преподавателя
    thisteacher_id = teachersfio_teachersid[search_teacher_fio]
    #Записываем данные в финальный словарь
    for group in thisgroups:
        #id группы по ее имени
        group_id = groupsnames_groupsid[group]
        #результат работы 1 функции
        result_dict[group] = first_task(thisteacher_id,group_id)

    if to_json == False:
        #Просто возвращаем словарь
        return result_dict
    else:
        #Сохраняем итоговый результат в файл и возвращаем значение True
        try:
            with open(to_json,"w") as file:
                file.write(json.dumps(result_dict,ensure_ascii=False))
            return True
        #Если мы указали некорректный путь для записи файла
        except Exception:
            return False

def third_task(entry_year, subject_name, to_json=False):
    """
    3. Реализовать функцию, которая принимает параметры entry_year - год поступления,
    subject_name - наименование предмета и необязательный параметр to_json, по умолчанию равный False.
    Функция должна возвращать словарь со статистикой по группам по данному предмету.
    Ключами словаря являются id группы, а значениями словари.

    Внутренний словарь имеет ключи group_name (наименование группы), stats (статистика).
    Значением ключа статистика является словарь, который возвращает количество студентов
    получившие оценку 5, количество студентов получившие оценку 4, количество студентов получившие оценку 3, количество студентов получившие оценку 2.
    Если параметр to_json указан, то сохраняет полученный словарь в указанный файл и возвращает True,
    иначе просто возвращает словарь.
    """

    #Загрузка данных
    groups_csv = csv2dict("./csv/groups.csv")
    subjects_csv = csv2dict("./csv/subjects.csv")
    results_csv = csv2dict("./csv/results.csv")
    students_csv = csv2dict("./csv/students.csv")
    
    #Промежуточные словари
    subjectsid_subjectnames = {}
    subjectnames_subjectsid = {}
    groupsid_groupsname = {}
    students_groups = {}
    groups_students = {}
    students_marks = {}

    #Результирующий словарь
    result_dict = {}

    #Проверка на существование entry_year и subject_name
    if subject_name not in subjects_csv["subject_name"]:
        print("Указанной дисциплины {} не существует!".format(subject_name))
        return
    if entry_year not in groups_csv["entry_year"]:
        print("Указанного года послупления {} не существует!".format(entry_year))
        return

    #Заполнение subjectsid_subjectnames и обратного словаря
    for i in range(len(subjects_csv["id"])):
        subjectsid_subjectnames[subjects_csv["id"][i]] = subjects_csv["subject_name"][i]
        subjectnames_subjectsid[subjects_csv["subject_name"][i]] = subjects_csv["id"][i]
    
    #id предмета, по которому вы ведем статистику
    thissubject_id = subjectnames_subjectsid[subject_name]
    
    #Список с id групп, с которыи можно работать
    allowed_groups_list = []
    #Заполнение groupsid_groupsname
    for i in range(len(groups_csv["id"])):
        if groups_csv["entry_year"][i] == str(entry_year):
            group_id = groups_csv["id"][i]
            groupsid_groupsname[group_id] = groups_csv["name"][i]
            allowed_groups_list.append(group_id)

    #Формируем статистику по каждому студенту, который сдавал указанный предмет
    for i in range(len(results_csv["id"])):

        #Фильтрация на предмет, по которому ведем статистику
        if results_csv["subject"][i] == thissubject_id:
            student_id = results_csv["student_id"][i]
            score = results_csv["total"][i]
            #Добавляем оценку для каждого студента
            students_marks[student_id] = score

    #Добавляем группу каждому студенту
    for i in range(len(students_csv["id"])):
        group_id = students_csv["group_id"][i]
        student_id = students_csv["id"][i]
        students_groups[student_id] = group_id
    
    #Формируем словарь группа -> список студентов
    for student_id, group_id in students_groups.items():
        
        #Фильтрация на то, чтоб год группы был нужный
        if group_id in allowed_groups_list:
            if group_id not in groups_students:
                groups_students[group_id] = []
            groups_students[group_id].append(student_id)
    
    #Формируем результирующий словарь
    for group_id, students_list in groups_students.items():

        #Список оценок по предмету
        marks_list = [students_marks[e] for e in students_list]
        #Для каждого элемента применяем функцию score2mark
        newmarks_list = list(map(score2mark, marks_list))
        #Считаем кол-во каждой оценки с помощью count и формируем словарь с кол-вом каждой оценки
        subbuf_dict = {"mark_2" : newmarks_list.count(2), "mark_3" : newmarks_list.count(3), "mark_4" : newmarks_list.count(4), "mark_5" : newmarks_list.count(5)}
        #Формируем промежуточный словарь
        buf_dict = {"group_name" : groupsid_groupsname[group_id], "stats" : subbuf_dict}
        #Записываем данные в основной словарь
        result_dict[group_id] = buf_dict

    if to_json == False:
        #Просто возвращаем словарь
        return result_dict
    else:
        #Сохраняем итоговый результат в файл и возвращаем значение True
        try:
            with open(to_json,"w") as file:
                file.write(json.dumps(result_dict,ensure_ascii=False))
            return True
        #Если мы указали некорректный путь для записи файла
        except Exception:
            return False

def main():
    result1 = first_task(4,1)
    print(result1)

    result2 = second_task("Иванов Петр Петрович")
    result2 = second_task("Петров Петр Петрович")
    print(result2)
    result3 = second_task("Петров Петр Петрович","./data.json")
    print(result3)
    
    result4 = third_task("2017", "Английский язык")
    print(result4)

    result5 = third_task("2018", "Машиностроение")
    result5 = third_task("2018", "Корпоративные информационные системы")
    print(result5)
    result5 = third_task("2018", "Программная инженерия")
    print(result5)

if __name__ == '__main__':
    main()