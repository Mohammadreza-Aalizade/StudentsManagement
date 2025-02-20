import json

import jdatetime
from telegram import Update, Message, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from bot.Constants import *
from bot import Responder


class StudentResponder(Responder):
    def __init__(self, dbc):
        super().__init__(dbc)

    @override
    def handel_command(self, update: Update, context: CallbackContext, user):
        message = update.message
        chat_id, s_id, state = user[0], user[2], user[3]
        student = self.dbc.get_student(s_id)
        if student is not None:
            student = student[0]
            if state == StudentState.main_menu:
                if message.text == "/start":
                    self.show_taken_courses(message, student)

            elif state == StudentState.wait_for_enter_taking_course_id:
                if message.text == "/cancel":
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, StudentState.main_menu)
                    self.show_taken_courses(message, student)
                else:
                    message.reply_text(TXT.err_enter_course_id)

            elif state == StudentState.wait_for_enter_message:
                if message.text == "/cancel":
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, StudentState.main_menu)
                    self.show_taken_courses(message, student)
                else:
                    message.reply_text(TXT.err_enter_message)
        else:
            message.reply_text(TXT.err_login_again)

    @override
    def handel_private_message(self, update: Update, context: CallbackContext, user):
        message = update.message
        chat_id, s_id, state, udata = user[0], user[2], user[3], user[4]
        student = self.dbc.get_student(s_id)
        if student is not None:
            student = student[0]
            if state == StudentState.main_menu:
                self.show_taken_courses(message, student)

            elif state == StudentState.wait_for_enter_taking_course_id:
                txt = message.text.strip()
                if txt.isdigit():
                    course = self.dbc.get_course(txt)
                    if course is not None:
                        course = course[0]
                        student_courses = self.dbc.get_student_courses(s_id)
                        if student_courses is not None:
                            for student_course in student_courses:
                                if student_course[4] == course[0]:
                                    message.reply_text(TXT.err_duplicate_course)
                                    self.dbc.update_user_state(chat_id, StudentState.main_menu)
                                    self.show_taken_courses(message, student)
                                    return

                        self.dbc.take_course(s_id, course[0])
                        message.reply_text(TXT.course_taken_successfully)

                    else:
                        message.reply_text(TXT.err_course_not_found)
                else:
                    message.reply_text(TXT.err_course_not_found)
                self.dbc.update_user_state(chat_id, StudentState.main_menu)
                self.show_taken_courses(message, student)

            elif state == StudentState.wait_for_enter_message:
                course = self.dbc.get_course(udata)
                if course is not None:
                    course = course[0]
                    teacher = self.dbc.get_course_teacher_login(udata)
                    if teacher is not None:
                        teacher = teacher[0]
                        try:
                            context.bot.send_message(chat_id=teacher[6],
                                                     parse_mode=ParseMode.HTML,
                                                     text=TXT.you_have_new_messge.format(sid=student[0], cname=course[1]))
                            context.bot.forward_message(chat_id=teacher[6], from_chat_id=chat_id,
                                                        message_id=message.message_id)
                            message.reply_text(TXT.sent_to_teacher)
                            self.dbc.update_user_state(chat_id, StudentState.main_menu)
                            self.show_course(message, student, udata, edit=False)
                        except BaseException as error:
                            message.reply_text(TXT.err_unable)
                            self.dbc.update_user_state(chat_id, StudentState.main_menu)
                            self.show_course(message, student, udata, edit=False)
                    else:
                        message.reply_text(TXT.teacher_not_login)
                        self.dbc.update_user_state(chat_id, StudentState.main_menu)
                        self.show_course(message, student, udata, edit=False)
                else:
                    message.reply_text(TXT.err_course_not_found)
                    self.dbc.update_user_state(chat_id, StudentState.main_menu)
                    self.show_taken_courses(message, student, edit=False)

        else:
            message.reply_text(TXT.err_login_again)

    @override
    def handel_call_back_query(self, update: Update, context: CallbackContext, user):
        callback_query = update.callback_query
        chat_id, s_id, state = user[0], user[2], user[3]
        student = self.dbc.get_student(s_id)
        if student is not None:
            student = student[0]
            if state == StudentState.main_menu:
                if callback_query.data == "take_new_course":
                    all_courses = ''
                    for crs in self.dbc.get_all_taking_courses():
                        all_courses += f"{crs[0]}: {crs[1]} - {crs[7]} ({crs[2]} واحد)\n"

                    txt = TXT.give_course_id_to_take + "\n\n" + all_courses
                    callback_query.message.edit_text(text=txt, parse_mode=ParseMode.HTML)
                    self.dbc.update_user_state(chat_id, StudentState.wait_for_enter_taking_course_id)

                elif callback_query.data.startswith("see_course"):
                    course_id = callback_query.data.split("/")[1]
                    self.dbc.update_user_data(chat_id, course_id)
                    if self.show_course(callback_query.message, student, course_id, True) == 0:
                        callback_query.answer(TXT.err_course_not_exist)

                elif callback_query.data.startswith("participate_poll"):
                    course_id = callback_query.data.split("/")[1]
                    self.show_course_poll(callback_query.message, student, course_id, True)

                elif callback_query.data.startswith("message_to_teacher"):
                    course_id = callback_query.data.split("/")[1]
                    course = self.dbc.get_course(course_id)
                    if course is not None:
                        teacher = self.dbc.get_course_teacher_login(course_id)
                        if teacher is not None:
                            callback_query.message.reply_text(TXT.enter_your_text_or_file, parse_mode=ParseMode.HTML)
                            self.dbc.update_user_state(chat_id, StudentState.wait_for_enter_message)
                        else:
                            callback_query.message.reply_text(TXT.teacher_not_login)
                            self.show_course(callback_query.message, student, course_id, edit=False)
                    else:
                        callback_query.message.reply_text(TXT.err_course_not_found)
                        self.show_taken_courses(callback_query.message, student, edit=False)

                elif callback_query.data.startswith("select_option_poll"):
                    course_id = callback_query.data.split("/")[1]
                    choice = callback_query.data.split("/")[2]
                    self.dbc.update_student_choice(course_id, student[0], choice)
                    self.show_course_poll(callback_query.message, student, course_id, True)

                elif callback_query.data == "back_to_main":
                    self.show_taken_courses(callback_query.message, student, edit=True)

                elif callback_query.data == "logout":
                    callback_query.message.edit_text(text=TXT.logout_successfully % student[1],
                                                     reply_markup=InlineKeyboardMarkup([[]]))
                    self.dbc.delete_user(chat_id)
                    context.bot.send_message(chat_id=chat_id, text=TXT.login_or_signup, parse_mode=ParseMode.HTML)

            elif state == StudentState.wait_for_enter_taking_course_id:
                callback_query.answer(TXT.err_enter_course_id)

            elif state == StudentState.wait_for_enter_message:
                callback_query.answer(TXT.err_enter_message)
        else:
            callback_query.answer(TXT.err_login_again)

    def show_course_poll(self, message: Message, student, course_id, edit=False):
        info = self.dbc.student_see_course(student[0], course_id)
        if info is not None:
            info = info[0]
            if info[14] != '':
                poll_info = json.loads(info[14])
                poll_info_prnt = ' <b>' + poll_info['title'] + '</b>\n\n'
                btns = [[InlineKeyboardButton(TXT.back, callback_data=f'see_course/{course_id}')]]
                i = 0
                for opt in poll_info['options']:
                    poll_info_prnt += f'<b>[{i + 1}]</b>  <i>' + opt + '</i>\n'
                    btns.append([InlineKeyboardButton(f'گزینه {i + 1} {" — انتخاب شده" if info[8] == i else ""}',
                                                      callback_data=f'select_option_poll/{course_id}/{i}')])
                    i += 1

                if edit:
                    message.edit_text(text=poll_info_prnt, parse_mode=ParseMode.HTML,
                                      reply_markup=InlineKeyboardMarkup(btns))
                else:
                    message.reply_text(text=poll_info_prnt, parse_mode=ParseMode.HTML,
                                       reply_markup=InlineKeyboardMarkup(btns))
            else:
                self.show_course(message, student, course_id, True)
        else:
            self.show_taken_courses(message, student, edit=True)

    def show_course(self, message: Message, student, course_id, edit=False):
        info = self.dbc.student_see_course(student[0], course_id)
        if info is None:
            return 0

        info = info[0]
        mark = "<i>نامشخص</i>" if info[7] == -1 else info[7]
        text = TXT.student_see_course.format(name=info[10], units=info[11], teacher=info[16], date=info[6],
                                             mark=mark, notif=info[13] if info[13] != '' else '----')
        btns = []

        if info[14] != '':
            btns.append([InlineKeyboardButton(TXT.participate_poll, callback_data=f'participate_poll/{course_id}')])

        btns.append([InlineKeyboardButton(TXT.message_teacher, callback_data=f'message_to_teacher/{course_id}')])
        btns.append([InlineKeyboardButton(TXT.back, callback_data='back_to_main')])

        if edit:
            message.edit_text(text=text, parse_mode=ParseMode.HTML,
                              reply_markup=InlineKeyboardMarkup(btns))
        else:
            message.reply_text(text=text, parse_mode=ParseMode.HTML,
                               reply_markup=InlineKeyboardMarkup(btns))

    def show_taken_courses(self, message: Message, student, edit=False):
        courses = self.dbc.get_student_courses(student[0])
        text = TXT.student_main_menu_title.format(name=str(student[1]), s_id=str(student[0]),
                                                  c_cnt=0 if courses is None else len(courses))
        btns = [
            [InlineKeyboardButton(TXT.take_new_course, callback_data="take_new_course")]
        ]
        if courses is not None:
            for crs in courses:
                btns.append([InlineKeyboardButton(crs[10], callback_data=f"see_course/{crs[9]}")])

        btns.append([InlineKeyboardButton(TXT.logout, callback_data="logout")])

        if edit:
            message.edit_text(text=text, parse_mode=ParseMode.HTML,
                              reply_markup=InlineKeyboardMarkup(btns))
        else:
            message.reply_text(text=text, parse_mode=ParseMode.HTML,
                               reply_markup=InlineKeyboardMarkup(btns))


