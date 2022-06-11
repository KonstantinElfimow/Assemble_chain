import random
from copy import deepcopy

from PyQt5.QtWidgets import QMessageBox


def game_over(table):
    """ Конец игры """
    """ Новое окно с кнопкой о закрытии игры """
    print("Game over")
    msg = QMessageBox()
    msg.resize(200, 150)
    msg.setWindowTitle("Player over")
    msg.setText("Конец игры")
    msg.setStandardButtons(QMessageBox.Cancel)
    btn = msg.exec_()
    if btn == QMessageBox.Cancel:
        table.par.close()


def new_lvl(table):
    for i, row in enumerate(table.data):
        for j, col, in enumerate(row):
            if i == 0:
                if col != '':
                    game_over(table)
                continue
            table.data[i - 1][j] = table.data[i][j]
            if i == len(table.data) - 1:
                table.data[i][j] = 0


def check_new_lvl(table, progress, settings):
    """ Проверяет прогресс игры на повышение уровня """
    if progress.number_destroyed > settings.step_to_next_lvl - 1:
        progress.number_destroyed = -1
        settings.lvl += 1
        progress.label_num_level.setText(f'LEVEL {settings.lvl}')
        progress.update()

        # Добавление ряда внизу table_data (игровой таблицы)
        new_lvl(table)
        table.draw_table()


def falling_cells(table_):
    """ Падение ячеек """
    for col in range(len(table_[0])):
        step = 0
        row = len(table_[0]) - 1
        while row >= 0:
            while table_[row][col] == '' and row > 0:
                step += 1
                row -= 1
            if step > 0:
                table_[row + step][col] = table_[row][col]
                table_[row][col] = ''
            row -= 1


def checking_all_direction_gray(table_, i, index_line):
    """ Проверка на серые ячейки вокруг взорвавшейся (удалившейся) """
    # check left
    if index_line > 0:
        if (table_[i][index_line - 1]) == 0:
            table_[i][index_line - 1] = 8
        elif (table_[i][index_line - 1]) == 8:
            table_[i][index_line - 1] = (random.randint(1, 7))

    # check right
    if index_line < len(table_[i]) - 1:
        if (table_[i][index_line + 1]) == 0:
            table_[i][index_line + 1] = 8
        elif (table_[i][index_line + 1]) == 8:
            table_[i][index_line + 1] = (random.randint(1, 7))

    # check up
    if i > 0:
        if (table_[i - 1][index_line]) == 0:
            table_[i - 1][index_line] = 8
        elif (table_[i - 1][index_line]) == 8:
            table_[i - 1][index_line] = (random.randint(1, 7))

    # check down
    if i < len(table_) - 1:
        if (table_[i + 1][index_line]) == 0:
            table_[i + 1][index_line] = 8
        elif (table_[i + 1][index_line]) == 8:
            table_[i + 1][index_line] = (random.randint(1, 7))

    return table_


def removed_columns(table_):
    """ Удаляет столбцы """
    for col in range(len(table_[0])):
        line = []
        row = 0
        while row < len(table_):
            while table_[row][col] != '':
                line.append(row)
                row += 1
                if row >= len(table_):
                    break
            if line:
                for i in line:
                    if int(table_[i][col]) == len(line):
                        table_ = checking_all_direction_gray(table_, i, col)
                        table_[i][col] = ''
                line = []
            row += 1

    return table_


def removed_rows(table_):
    """ Удаляет строки """
    for i, data in enumerate(table_):
        line = []
        index = 0
        while index < len(data):
            while data[index] != '':
                line.append(index)
                index += 1
                if index >= len(data):
                    break
            if line:
                for index_line in line:
                    if int(data[index_line]) == len(line):
                        checking_all_direction_gray(table_, i, index_line)
                        data[index_line] = ''
                line = []
            index += 1

    return table_


def removed_cells(table_, settings):
    """ Удаляет все возможные ячейки """
    data_r = removed_rows(deepcopy(table_))
    data_c = removed_columns(deepcopy(table_))

    removed = False
    for row in range(len(table_)):
        for col in range(len(table_[row])):

            if table_[row][col] == 0:
                if data_r[row][col] != 0:
                    table_[row][col] = data_r[row][col]
                elif data_c[row][col] != 0:
                    table_[row][col] = data_c[row][col]
            elif table_[row][col] == 8:
                if data_r[row][col] != 8:
                    table_[row][col] = data_r[row][col]
                elif data_c[row][col] != 8:
                    table_[row][col] = data_c[row][col]

            if table_[row][col] != '' and (data_r[row][col] == '' or data_c[row][col] == ''):
                removed = True
                table_[row][col] = ''
                settings.score += settings.points_per_default_cell


    if removed:
        falling_cells(table_)
        return removed_cells(table_, settings)


def fall_head_cell(table, row, column):
    if not table.data[row][column]:
        if row > 0:
            # Удаляет иконку упавшей head_icon
            table.data[row - 1][column] = ''
        # Задает head_icon на упавшую ниже ячейку
        table.data[row][column] = table.list_link_icon_num[table.head_icon]


def check_down_cell(table, row, column):
    """ Проверяет, может ли падать head_icon вниз """
    if row >= table.rowCount():
        return False
    if table.data[row][column] == '':
        return True
    return False


def update_screen(table, settings, progress):
    # Падание head_cell (head_icon)
    row = 0
    while check_down_cell(table, row, table.currentColumn()):
        fall_head_cell(table, row, table.currentColumn())
        row += 1

    """ ===================================== """
    """ ==== Обработка уничтожения ячеек ==== """
    removed_cells(table.data, settings)
    """ ===================================== """

    # Проверка на переход к следующему уровню
    check_new_lvl(table, progress, settings)

    # Перерисовывает table_data после изменения data
    table.draw_table()

    # Задает новый head_icon
    table.head_icon = random.randint(0, len(table.list_link_icon_str) - 2)
