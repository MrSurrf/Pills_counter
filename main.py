import datetime
import json

import flet as ft

def main(page: ft.Page):
    page.title = ('Pills Counter')
    page.window_width = 560
    page.window_height = 600
    page.count = 1
    page.bgcolor = "BLACK"
    page.scroll = 'adaptive'
    pill_now = [0]
    list_date = []
    pills_list = []



    def change_date(e):

        date_v = date_picker.value.date()
        dt = date_picker.value.strftime("%d.%m.%y")

        if pills_range.value == None:
            open_alert_view_2(e)
            del list_date[-1]
        else:
            pill = int(pills_range.value)

        if list_date == []:
            list_date.append(date_v)
        list_date.append(date_v)
        count_day = (list_date[-1] - list_date[-2]).days # дней между приемами

        if count_day <= 0:
            if len(list_date) == 2:
                pill_now.append(pill - count_day)
                column.controls.append(ft.Text(value=f'Первый визит пациента\nДата приема -  {dt}', size=15, color=ft.colors.WHITE70))
                # with open('pills_list.txt', 'a') as f:
                #     f.write(f'Первый визит пациента - Дата приема -  {dt} - Режим приема {pill}\n')
            else:
                del list_date[-1]
                open_alert_view(e)

        else:
            pills = pill_now[-1] - count_day
            if pills < 0:
                column.controls.append(ft.Text(value=f"Дата приема -  {dt}   Количество таблеток - 0, Пропущено дней {pills}", size=15,color=ft.colors.WHITE70))
                pills = 0
                pill_now.append(pills + pill)
                pills_list.append(pills)
            else:
                pill_now.append(pills + pill)
                pills_list.append(pills)

                column.controls.append(ft.Text(value=f"Дата приема -  {dt}   Количество таблеток {pills_list[-1]}", size=15, color=ft.colors.WHITE70))
                # d = column.controls.copy()
                # s = str(d[0]).replace("text ","").replace("'", "\"")
                # s = json.loads(s)
                # print(s['value'])

            # with open('pills_list.txt', 'a') as f:
            #     f.write(f'Дата приема -  {dt}   Количество таблеток {pills_list[-1]}\n')

        page.update()

    def export(e):
        d = column.controls.copy()
        exp_list = []
        for i in d:
            s = str(i).replace("text ", "").replace("'", "\"")
            s = json.loads(s)
            exp_list.append(s['value'])
        with open('exp_list.txt', 'a') as f:
            f.writelines(f"{item}\n" for item in exp_list)
            print(s['value'])


    def del_date(e):

        if len(list_date) > 2:
            del list_date[-1]
        else:
            list_date.clear()

        if len(pills_list) > 0:
            del pills_list[-1]

        del pill_now[-1]
        with open('pills_list.txt', 'a') as f:
            f.write('<---отмена предыдущей записи--->\n')

        column.controls.pop()
        page.update()

    def clear(e):

        # with open('pills_list.txt', 'a') as f:
        #     f.write('---------------------------------------------\n')
        pill_now = [0]
        list_date.clear()
        pills_list.clear()

        column.controls.clear()
        page.update()

    date_picker = ft.DatePicker(

        on_change=change_date,
        cancel_text="Отмена",
        confirm_text="Ok",
        first_date=datetime.datetime(2020, 11, 1),
        last_date=datetime.datetime(2024, 12, 1),
        help_text="Выберете дату",

    )
    page.overlay.append(date_picker)

    clear_buttom = ft.ElevatedButton(
        "Очистить",
        on_click=clear,
        tooltip="Удалить все записи"

    )


    date_button = ft.ElevatedButton(
        "Выберете дату визита пациента",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date()
    )

    exp_button = ft.IconButton(
        icon=ft.icons.IMPORT_EXPORT,
        tooltip="Экспорт данных в файл",
        on_click=export
    )

    buttom_cont = ft.Container(
        alignment=ft.alignment.top_right,
        content=ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED,
            icon_color="pink600",
            tooltip="Удалить последнюю запись",
            on_click=del_date,
            icon_size=40
        )
    )
    pills_range = ft.Dropdown(
        width=170,
        color='blue',
        label="Режим приема",

        border_color='white',
        options=[
            ft.dropdown.Option('14'),
            ft.dropdown.Option('21'),
            ft.dropdown.Option('28'),
            ft.dropdown.Option('30'),
        ]
    )

    def close_dlg(e):
        Alert_view.open = False
        page.update()

    def close_dlg_2(e):
        Alert_view_2.open = False
        page.update()

    Alert_view = ft.AlertDialog(
        modal=True,
        title=ft.Text("Введена некорректная дата"),
        actions =[
            ft.TextButton("OK", on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    Alert_view_2 = ft.AlertDialog(
        modal=True,
        title=ft.Text("Не выбран режим приема"),
        actions=[
            ft.TextButton("OK", on_click=close_dlg_2)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def open_alert_view(e):
        page.dialog = Alert_view
        Alert_view.open = True
        page.update()

    def open_alert_view_2(e):
        page.dialog = Alert_view_2
        Alert_view_2.open = True
        page.update()

    main_row = ft.Row(
        width=page.window_width,
        controls=[
            pills_range,
            date_button,
            exp_button
        ]
    )
    column = ft.Column(
        width=page.window_width,
        height=400,
        scroll=ft.ScrollMode.ALWAYS,
        auto_scroll=True
    )

    buttom_row = ft.Row(
        width=page.window_width,
        alignment=ft.MainAxisAlignment.END,
        controls=[
            clear_buttom,
            buttom_cont
        ]

    )
    page.add(
        main_row,
        column,
        buttom_row,

    )
ft.app(target=main)