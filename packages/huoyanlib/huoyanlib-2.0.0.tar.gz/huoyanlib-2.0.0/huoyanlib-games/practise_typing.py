from tkinter import *
import random
import string
import datetime


def practise_typing():
    root = Toplevel()
    root.title("练习打字,测试老师的速度!")
    Label(root, text='题目:', fg="#228424", bg="#FEF5AA").grid(row=0)
    Label(root, text='试卷:', fg="#228424", bg="#FEF5AA").grid(row=1)
    Label(root, text='考试结果:', fg="#228424", bg="#FEF5AA").grid(row=2)
    v1 = StringVar()
    v2 = StringVar()
    v3 = StringVar()
    v1.set("点击'开始测试'按钮开始出题,想复制?不可能的(调皮)")
    e1 = Entry(root, text=v1, state='disabled', fg="#228424", bg="#FEF5AA", width=40, font=('宋体', 14))
    e2 = Entry(root, textvariable=v2, width=40, fg="#228424", bg="#FEF5AA", font=('宋体', 14))
    e3 = Label(root, textvariable=v3, width=40, fg="#228424", bg="#FEF5AA", font=('宋体', 10), foreground='red')
    e1.grid(row=0, column=1, padx=10, pady=20)
    e2.grid(row=1, column=1, padx=10, pady=20)
    e3.grid(row=2, column=1, padx=10, pady=20)
    text = Text(root, width=80, height=7, fg="#71DE85", bg="#FCF492")
    text.grid(row=4, column=0, columnspan=2, pady=5)
    root.configure(bg="#FCF492")

    class TypingTest:
        def __init__(self):
            self.time_list = []
            self.letterNum = 20
            self.letterStr = ''.join(random.sample(string.printable.split(' ')[0], self.letterNum))
            self.examination_paper = ''

        def time_calc(self):
            self.time_list.append(datetime.datetime.now())
            yield

        def create_exam(self):
            text.delete(0.0, END)
            v1.set(self.letterStr)
            self.time_calc().__next__()
            text.insert(END, "开始：%s \n" % str(self.time_list[-1]))
            user_only1.config(state='active')

        def score(self):
            wrong_index = []
            self.time_calc().__next__()
            text.insert(END, "结束:%s\n" % str(self.time_list[-1]))
            use_time = (self.time_list[-1] - self.time_list[-2]).seconds
            self.examination_paper = v2.get()
            if len(self.examination_paper) > self.letterNum:
                v3.set("输入数据有错误，作答数大于考题数")
            else:
                right_num = 0
                for z in range(len(self.examination_paper)):
                    if self.examination_paper[z] == self.letterStr[z]:
                        right_num += 1
                    else:
                        wrong_index.append(z)
                if right_num == self.letterNum:
                    v3.set("完全正确,正确率%.2f%%用时：%s秒" % ((right_num * 1.0) / self.letterNum * 100, use_time))
                else:
                    v3.set("正确率%.2f%%用时：%s 秒" % ((right_num * 1.0) / self.letterNum * 100, use_time))
                    text.insert(END, "题目：%s\n" % self.letterStr)
                    tag_info = list(map(lambda x: '4.' + str(x + 3), wrong_index))
                    text.insert(END, "作答：%s\n" % self.examination_paper)
                    for i in range(len(tag_info)):
                        text.tag_add("tag1", tag_info[i])
                        text.tag_config("tag1", background='red')
                        user_only1.config(state='disabled')
    typingtest = TypingTest()
    Button(root, text="开始测试", width=10, command=TypingTest.create_exam, fg="#228424", bg="#FEF5AA").grid(row=3, column=0, sticky=W, padx=30, pady=5)
    user_only1 = Button(root, text="交卷", width=10, command=TypingTest.score, state='disable', fg="#228424", bg="#FEF5AA")
    user_only1.grid(row=3, column=1, sticky=E, padx=30, pady=5)
    mainloop()
