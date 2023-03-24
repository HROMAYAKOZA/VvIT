import psycopg2
import sys
import datetime  # для корректного отображения времени из базы данных
from PyQt5.QtGui import QColor  # для настройки цвета ячеек в таблице
from PyQt5.QtCore import Qt# для создания нередактирумых ячеек в таблице - Qt.ItemIsEnabled | Qt.ItemIsSelectable
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox)  # removed - QGroupBox, QHeaderView


class MainWindow(QWidget):
    """Создание окна с расписанием, предметами и учителями"""

    def __init__(self):
        """Запускает все функции, необходимые для отображения окна, вкладок, таблиц и работы с таблицами"""
        super(MainWindow, self).__init__()  # инициализация окна
        self.weekdays = ['Monday', 'Tuesday',
                         'Wednesday', 'Thursday', 'Friday', 'Saturday']

        self._connect_to_db()  # подключение курсора
        self.cursor.execute("SELECT start FROM time order by 1")
        self.start_at = list(self.cursor.fetchall())

        self.setWindowTitle("Shedule")  # название окна

        self.vbox = QVBoxLayout(self)  # вертикальная ось
        self.tabs = QTabWidget(self)  # создание структуры с вкладками
        self.vbox.addWidget(self.tabs)
        self.update_shedule_button = QPushButton("Update")
        self.vbox.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self._create_shedule_tab()
        self._create_subjects_tab()
        self._create_teacher_tab()
        

    def _connect_to_db(self):
        """Подключается к базе данных и создаёт курсор"""
        self.conn = psycopg2.connect(
            database="lab8_test", user="postgres", password="1234", host="localhost", port="5432")
        self.cursor = self.conn.cursor()

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")
        svbox_t = QVBoxLayout()
        shbox_t = QHBoxLayout()
        svbox_t.addLayout(shbox_t)
        self.teach_table = QTableWidget()
        self.teach_table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.teach_table.setColumnCount(5)
        self.teach_table.setHorizontalHeaderLabels(
            ["T_id", "Name", "Subejct", "Join", "Delete"])
        self.teach_table.horizontalHeader().setSectionResizeMode(3)
        self.teach_table.verticalHeader().setSectionResizeMode(3)
        self._update_teacher_table()
        shbox_t.addWidget(self.teach_table)
        self.teacher_tab.setLayout(svbox_t)

    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM teacher order by 1")
        records = list(self.cursor.fetchall())
        self.teach_table.clearContents()
        self.teach_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):  # построчное обновление таблицы
            r = list(r)
            joinButton = QPushButton("Edit")
            delButton = QPushButton("Del")
            self.teach_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teach_table.item(i, 0).setFlags(
                Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.teach_table.item(i, 0).setBackground(QColor(96, 96, 96))
            self.teach_table.item(i, 0).setForeground(QColor(255, 255, 255))
            self.teach_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teach_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teach_table.setCellWidget(
                i, 3, joinButton)  # помещает в ячейку виджет
            self.teach_table.setCellWidget(i, 4, delButton)
            joinButton.clicked.connect(
                lambda ch, num=i: self._change_teacher_from_table(num))  # если Join нажата
            delButton.clicked.connect(
                lambda ch, num=i: self._delete_teacher_from_table(num))
        addButton = QPushButton("Add")
        addButton.clicked.connect(
            lambda ch: self._create_teach_in_table(len(records)))
        self.teach_table.setCellWidget(len(records), 3, addButton)
        # self.teach_table.resizeRowsToContents()

    def _change_teacher_from_table(self, num):
        row = list()
        for i in range(self.teach_table.columnCount()-2):
            try:
                row.append(self.teach_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE teacher SET t_name='%s', t_sub='%s' where t_id='%s'" % (
                row[1], row[2], row[0]))
            self.conn.commit()
            self._update_teacher_table()
        except Exception as e:
            QMessageBox.about(self, "Error", "Something went wrong\n%s" % e)

    def _delete_teacher_from_table(self, num):
        i = self.teach_table.item(num, 0).text()
        try:
            self.cursor.execute("DELETE FROM teacher where t_id='%s'" % i)
            self.conn.commit()
            self._update_teacher_table()
        except Exception as e:
            QMessageBox.about(self, "Error", "Something went wrong\n%s" % e)

    def _create_teach_in_table(self, num):
        row = list()
        for i in range(self.teach_table.columnCount()-2):
            try:
                row.append(self.teach_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO teacher (t_id, t_name, t_sub) VALUES ('%s','%s','%s')" %
                                (row[0], row[1], row[2]))
            self.conn.commit()
            self._update_teacher_table()
        except Exception as e:
            QMessageBox.about(
                self, "Error", "Something went wrong\nMaybe you are trying to add teacher with existing id\nor with unexisting subject id\n%s" % e)

    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Subjects")
        svbox_s = QVBoxLayout()
        shbox_s = QHBoxLayout()
        svbox_s.addLayout(shbox_s)
        self.sub_table = QTableWidget()
        self.sub_table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.sub_table.setColumnCount(4)
        self.sub_table.setHorizontalHeaderLabels(
            ["id", "Subject", "Join", "Delete"])
        # self.sub_table.horizontalHeader().setStyleSheet("QHeaderView::section { color:white; background-color:blue; }")
        self.sub_table.horizontalHeader().setSectionResizeMode(3)
        self.sub_table.verticalHeader().setSectionResizeMode(3)
        self._update_subjects_table()
        shbox_s.addWidget(self.sub_table)
        self.subjects_tab.setLayout(svbox_s)

    def _update_subjects_table(self):
        self.cursor.execute("SELECT * FROM subjects order by 1")
        records = list(self.cursor.fetchall())
        self.sub_table.clearContents()
        self.sub_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):  # построчное обновление таблицы
            r = list(r)
            joinButton = QPushButton("Edit")
            delButton = QPushButton("Del")
            self.sub_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.sub_table.item(i, 0).setFlags(
                Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.sub_table.item(i, 0).setBackground(QColor(96, 96, 96))
            self.sub_table.item(i, 0).setForeground(QColor(255, 255, 255))
            self.sub_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            # помещает в ячейку виджет
            self.sub_table.setCellWidget(i, 2, joinButton)
            self.sub_table.setCellWidget(i, 3, delButton)
            joinButton.clicked.connect(
                lambda ch, num=i: self._change_subject_from_table(num))  # если Join нажата
            delButton.clicked.connect(
                lambda ch, num=i: self._delete_subject_from_table(num))
        addButton = QPushButton("Add")
        addButton.clicked.connect(
            lambda ch: self._create_sub_in_table(len(records)))
        self.sub_table.setCellWidget(len(records), 2, addButton)
        # self.sub_table.resizeRowsToContents()

    def _change_subject_from_table(self, num):
        row = list()
        for i in range(self.sub_table.columnCount()-2):
            try:
                row.append(self.sub_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(
                "UPDATE subjects SET sub_name='%s' where id='%s'" % (row[1], row[0]))
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", "Something went wrong\n%s" % e)

    def _delete_subject_from_table(self, num):
        i = self.sub_table.item(num, 0).text()
        try:
            self.cursor.execute("DELETE FROM subjects where id='%s'" % i)
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", "Something went wrong\n%s" % e)

    def _create_sub_in_table(self, num):
        row = list()
        for i in range(self.sub_table.columnCount()-2):
            try:
                row.append(self.sub_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(
                "INSERT INTO subjects (id, sub_name) VALUES ('%s','%s')" % (row[0], row[1]))
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(
                self, "Error", "Something went wrong\nMaybe you are trying to add subject with existing id\n%s" % e)

    def _create_shedule_tab(self):
        """Создание вкладки Schedule с вкладками расписаний на дни недели"""
        self.shedule_tab = QTabWidget()  # QWidget - создание вкладки/окна
        # вкладка с названием Schedule
        self.tabs.addTab(self.shedule_tab, "Shedule")

        self._create_week_table()

    def _create_week_table(self):
        """Вызов _create_day_table для каждого дня недели"""
        self.r = []
        for i in range(1, 7):
            self.r.append(self._create_day_table(i))

    # Отображение таблицы с расписанием на день
    def _create_day_table(self, day):
        """Создание таблицы с расписанием на один день"""
        day_schedule = QWidget()
        self.shedule_tab.addTab(day_schedule, self.weekdays[day-1])
        day_table = QTableWidget()  # QTableWidget - пустая таблица
        # возможность изменения размера под размер данных в ячейке.
        day_table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        day_table.horizontalHeader().setSectionResizeMode(0)
        day_table.verticalHeader().setSectionResizeMode(3)
        r_day_table = QTableWidget()
        r_day_table.setEditTriggers(QTableWidget.NoEditTriggers)
        r_day_table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        r_day_table.horizontalHeader().setSectionResizeMode(3)
        r_day_table.verticalHeader().setSectionResizeMode(3)

        day_table.setColumnCount(6)  # кол-во колонок
        day_table.setHorizontalHeaderLabels(
            ["time", "subject", "kab", "week", "edit", "delete"])  # названия колонок
        r_day_table.setColumnCount(5)
        r_day_table.setHorizontalHeaderLabels(
            ["time", "subject", "week", "kab", "teacher"])

        self._update_day_table(day, day_table, r_day_table)

        mvbox = QVBoxLayout()
        mvbox.addWidget(day_table)
        mvbox.addWidget(r_day_table)
        day_schedule.setLayout(mvbox)
        return (day_table, r_day_table)

    # обновление таблицы с расписанием на день
    def _update_day_table(self, day, day_table, r_day_table):
        """Заполняет или обновляет таблицу с расписанием на один день"""
        self.cursor.execute(
            "SELECT start_time, sub, cabinet, week FROM schedule WHERE day='%d' order by start_time, week" % day)
        records = list(self.cursor.fetchall())

        day_table.clearContents()
        day_table.setRowCount(len(records) + 1)  # количество строк

        for i, r in enumerate(records):  # построчное обновление таблицы
            r = list(r)
            joinButton = QPushButton("Edit")
            delButton = QPushButton("Del")
            day_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            day_table.item(i, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            day_table.item(i, 0).setBackground(QColor(96, 96, 96))
            day_table.item(i, 0).setForeground(QColor(255, 255, 255))
            day_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            day_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            day_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            day_table.item(i, 3).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            day_table.item(i, 3).setBackground(QColor(96, 96, 96))
            day_table.item(i, 3).setForeground(QColor(255, 255, 255))
            # помещает в ячейку виджет
            day_table.setCellWidget(i, 4, joinButton)
            day_table.setCellWidget(i, 5, delButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(
                num, day_table, day, r_day_table))  # если Join нажата
            delButton.clicked.connect(lambda ch, num=i: self._delete_day_from_table(
                num, day_table, day, r_day_table))
            if r[3] == 2:
                day_table.item(i, 1).setBackground(QColor(224, 224, 224))
                day_table.item(i, 2).setBackground(QColor(224, 224, 224))
        for i in range(1, len(records)):
            if (day_table.item(i, 0).text() == day_table.item(i-1, 0).text()):
                try:
                    day_table.setSpan(i-1, 0, 2, 1)
                except:
                    print("error with setting span")
            elif day_table.rowSpan(i-1, 0) > 1 and (i < 2 or day_table.item(i-1, 0).text() != day_table.item(i-2, 0).text()):
                try:
                    day_table.setSpan(i-1, 0, 1, 1)
                except:
                    print("error with removing span")
        addButton = QPushButton("Add")
        addButton.clicked.connect(lambda ch: self._create_day_in_table(
            len(records), day_table, day, r_day_table))
        day_table.setCellWidget(len(records), 4, addButton)
        # day_table.resizeRowsToContents() # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки - только в Qt6

        self.cursor.execute(
            "SELECT start, sub_name, week, cabinet, t_name, start_time FROM schedule, time, teacher, subjects WHERE sub>'0' \
            and day='%d' and sub_start=start_time and sub=id and t_sub=id order by start, week" % day)
        records = list(self.cursor.fetchall())
        r_day_table.clearContents()
        r_day_table.setRowCount(10)
        ti = 0
        for i in range(5):
            for j in range(2):
                if len(records) > ti and records[ti][2] == j+1 and records[ti][5] == i+1:
                    r_day_table.setItem(i*2+j, 0, QTableWidgetItem(str(records[ti][0])))
                    r_day_table.setItem(i*2+j, 1, QTableWidgetItem(str(records[ti][1])))
                    r_day_table.setItem(i*2+j, 2, QTableWidgetItem(str(records[ti][2])))
                    r_day_table.setItem(i*2+j, 3, QTableWidgetItem(str(records[ti][3])))
                    r_day_table.setItem(i*2+j, 4, QTableWidgetItem(str(records[ti][4])))
                    ti += 1

                else:
                    r_day_table.setItem(
                        i*2+j, 0, QTableWidgetItem(str(self.start_at[i][0])))
                    r_day_table.setItem(i*2+j, 1, QTableWidgetItem('-'))
                    r_day_table.setItem(i*2+j, 2, QTableWidgetItem(str(j+1)))
                    r_day_table.setItem(i*2+j, 3, QTableWidgetItem('-'))
                    r_day_table.setItem(i*2+j, 4, QTableWidgetItem('-'))
            # if records[ti][2] == 2:
            r_day_table.item(i*2+1, 1).setBackground(QColor(224, 224, 224))
            r_day_table.item(i*2+1, 2).setBackground(QColor(224, 224, 224))
            r_day_table.item(i*2+1, 3).setBackground(QColor(224, 224, 224))
            r_day_table.item(i*2+1, 4).setBackground(QColor(224, 224, 224))
        for i in range(1, 10):
            if (r_day_table.item(i, 0).text() == r_day_table.item(i-1, 0).text()):
                r_day_table.setSpan(i-1, 0, 2, 1)
        # r_day_table.resizeRowsToContents()

    def _change_day_from_table(self, num, day_table, day, r_day_table):
        row = list()
        for i in range(day_table.columnCount()-2):  # columnCount - len() колонок таблицы
            try:
                row.append(day_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE schedule set sub='%s', cabinet='%s' where week='%s' and start_time='%s' and day='%s'" %
                                (row[1], row[2], row[3], row[0], day))
            self.conn.commit()
            self._update_day_table(day, day_table, r_day_table)
        except Exception as e:
            QMessageBox.about(self, "Error", "Something went wrong\n%s" % e)

    def _delete_day_from_table(self, num, day_table, day, r_day_table):
        s = [day_table.item(num, 0).text(), day_table.item(
            num, 3).text()]  # 0 - time, 3 - week
        try:
            self.cursor.execute(
                "DELETE FROM schedule where week='%s' and start_time='%s' and day='%s'" % (s[1], s[0], day))
            self.conn.commit()
            self._update_day_table(day, day_table, r_day_table)
        except Exception as e:
            QMessageBox.about(
                self, "Error", "Something went wrong\nMaybe you are trying to delete unexisting lesson\n%s" % e)

    def _create_day_in_table(self, num, day_table, day, r_day_table):
        row = list()
        for i in range(day_table.columnCount()-2):
            try:
                row.append(day_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO schedule (start_time,sub,cabinet,week,day) VALUES ('%s','%s','%s','%s','%s')" %
                                (row[0], row[1], row[2], row[3], day))
            self.conn.commit()
            self._update_day_table(day, day_table, r_day_table)
        except Exception as e:
            QMessageBox.about(
                self, "Error", "Something went wrong\nMaybe you are trying to add lesson with wrong time or week\n%s" % e)

    def _update_shedule(self):  # создать обновление всех таблиц на вкладке
        """Обновляет все таблицы в окне"""
        try:
            self._update_teacher_table()
            self._update_subjects_table()
            for i in range(1, 7):
                self._update_day_table(i, self.r[i-1][0], self.r[i-1][1])
        except Exception as e:
            QMessageBox.about(self, "Error", e)


app = QApplication(sys.argv)
win = MainWindow()
print(MainWindow.__doc__)
win.setGeometry(550,100,840,840)
# win.move(550, 100)
win.show()
sys.exit(app.exec_())
