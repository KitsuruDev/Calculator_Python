from tkinter import *
from tkinter.ttk import *
import os, sys

def onKeyF1Click(event):
    def onCloseFormRef(): formRef.destroy()
    formRef = Toplevel()
    formRef.geometry("{}x{}+{}+{}".format(425, 115, (formRef.winfo_screenwidth() - 425) // 2, (formRef.winfo_screenheight() - 115) // 2))
    formRef.resizable(False, False)
    formRef.title('О программе')
    formRef.iconbitmap(default=os.path.join(application_path, 'icon.ico'))
    Label(formRef, text="Калькулятор - версия 1.0.\n© KitsuruDev, 2024. Все права защищены", font=('Segoe UI', 16)).place(x=8, y=8, width=400, height=92)
    formRef.protocol("WM_DELETE_WINDOW", onCloseFormRef)
    formRef.grab_set()
    formRef.mainloop()

def onClickNumeric(number):
    if len(label1['text']) >= 16 and label1['text'] != 'Нельзя делить на 0': return
    if '=' in label2['text']: label2['text'] = ''
    label1['text'] = number if label1['text'] in ['0', 'Нельзя делить на 0'] else label1['text'] + number

def onClickDot():
    if label1['text'] != 'Нельзя делить на 0':
        label1['text'] += ',' if not ',' in label1['text'] else ''

def onClickChange():
    if label1['text'] != 'Нельзя делить на 0':
        label1['text'] = '-' + label1['text'] if label1['text'][0] != '-' else label1['text'][1:]

def onClickOperBase(key_symbol):
    global calculation, operation, one
    if label1['text'] != 'Нельзя делить на 0':
        calculation, operation = True, {'+': '+', '-': '-', '×': '*', '÷': '/'}[key_symbol]
        one = float(label1['text'].replace(',', '.')) if ',' in label1['text'] and label1['text'][-1] != ',' else int(label1['text'].replace(',', ''))
        label1['text'], label2['text'] = '0', str(one).replace('.', ',') + key_symbol

def onClickResult():
    global calculation, operation, one
    if calculation:
        two = float(label1['text'].replace(',', '.')) if ',' in label1['text'] and label1['text'][-1] != ',' else int(label1['text'].replace(',', ''))
        try: one = eval(f'{one}{operation}{two}')
        except ZeroDivisionError: one = 'Нельзя делить на 0'
        label1['text'], label2['text'] = str(one).replace('.', ','), label2['text'] + str(two).replace('.', ',') + '='
        calculation = False

def onClickOperSpecial(key_symbol):
    if label1['text'] != 'Нельзя делить на 0':
        number = float(label1['text'].replace(',', '.')) if ',' in label1['text'] and label1['text'][-1] != ',' else int(label1['text'].replace(',', ''))
        dict = {'1/x': [f'1 / {number}', f'1 / {number}='], 'x²': [f'{number} ** 2', f'{number}²='], '√x': [f'{number} ** 0.5', f'√{number}=']}
        try: label1['text'] = str(eval(dict[key_symbol][0])).replace('.', ',')
        except ZeroDivisionError: label1['text'] = 'Нельзя делить на 0'
        label2['text'] = dict[key_symbol][1].replace('.', ',')

def onClickClear(key):
    label1['text'] = '0' if key == 0 or len(label1['text']) == 1 or len(label1['text']) == 2 and label1['text'][0] == '-' or label1['text'] == 'Нельзя делить на 0' else label1['text'][:-1]
    label2['text'] = ''

calculation, operation, one = False, '', 0
application_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

formMain = Tk()
formMain.geometry("{}x{}+{}+{}".format(425, 597, (formMain.winfo_screenwidth() - 425) // 2, (formMain.winfo_screenheight() - 597) // 2))
formMain.resizable(False, False)
formMain.iconbitmap(default=os.path.join(application_path, 'icon.ico'))
formMain.title('Калькулятор')
formMain.bind("<F1>", onKeyF1Click)

Style().configure(style=".", background="white", foreground="black", font=('Segoe UI', 17))

label1 = Label(text="0", anchor="e", font=('Segoe UI', 30))
label1.place(x=14, y=53, width=395, height=75)
label2 = Label(text="", foreground="grey", anchor="e", font=('Segoe UI', 18))
label2.place(x=14, y=0, width=395, height=56)

[Button(text=str(i), command=lambda i=i: onClickNumeric(str(i))).place(x=8+((i-1)%3)*102, y=439-((i-1)//3)*75, width=101, height=75) for i in range(1, 10)]

dict1 = {'±': 'onClickChange()', '0': 'onClickNumeric(\'0\')', ',': 'onClickDot()', '=': 'onClickResult()'}
list2, list3, list4 = ['+', '-', '×', '÷'], ['1/x', 'x²', '√x'], ['C', '←']

[Button(text=i, command=lambda i=i: eval(dict1[i])).place(x=8+102*list(dict1).index(i), y=514, width=101, height=75) for i in dict1]
[Button(text=i, command=lambda i=i: onClickOperBase(i)).place(x=314, y=439-75*list2.index(i), width=101, height=75) for i in list2]
[Button(text=i, command=lambda i=i: onClickOperSpecial(i)).place(x=8+102*list3.index(i), y=214, width=101, height=75) for i in list3]
[Button(text=i, command=lambda i=i: onClickClear(list4.index(i))).place(x=8+204*list4.index(i), y=139, width=202, height=75) for i in list4]

formMain.mainloop()
