import json

import jdatetime
from telegram import Update, InlineKeyboardButton, ParseMode, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.Constants import *
from bot import Responder


class TeacherResponder(Responder):
    def __init__(self, dbc):
        super().__init__(dbc)

    @override
    def handel_command(self, update: Update, context: CallbackContext, user):
        message = update.message
        chat_id, t_id, state = user[0], user[2], user[3]
        teacher = self.dbc.get_teacher(t_id)
        if teacher is not None:
            teacher = teacher[0]
            if state == TeacherState.main_menu:
                if message.text == "/start":
                    self.show_teaching_courses(message, teacher)

            elif state == TeacherState.wait_for_enter_new_course_info:
                if message.text == "/cancel":
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_teaching_courses(message, teacher)
                else:
                    message.reply_text(TXT.err_enter_new_course_info)

            elif state == TeacherState.wait_for_enter_new_marks:
                if message.text == "/cancel":
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_teaching_courses(message, teacher)
                else:
                    message.reply_text(TXT.err_enter_new_marks)

            elif state == TeacherState.wait_for_enter_delete_student:
                if message.text == "/cancel":
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_teaching_courses(message, teacher)
                else:
                    message.reply_text(TXT.err_enter_student_to_delete)

            elif state == TeacherState.wait_for_enter_poll_info:
                message.reply_text(TXT.err_enter_poll_info)
        else:
            message.reply_text(TXT.err_login_again)

    @override
    def handel_private_message(self, update: Update, context: CallbackContext, user):
        message = update.message
        chat_id, t_id, state, udata = user[0], user[2], user[3], user[4]
        teacher = self.dbc.get_teacher(t_id)
        if teacher is not None:
            teacher = teacher[0]
            if state == TeacherState.main_menu:
                self.show_teaching_courses(message, teacher, False)

            elif state == TeacherState.wait_for_enter_new_course_info:
                if message.text == 'لغو':
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_teaching_courses(message, teacher)
                    return

                lines = message.text.strip().split("\n")
                if len(lines) == 2:
                    name, unit = lines[0], lines[1]
                    if unit.isdigit():
                        self.dbc.create_course(name, unit, t_id)
                        self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                        message.reply_text(TXT.course_created_successfully)
                        self.show_teaching_courses(message, teacher)
                    else:
                        message.reply_text(TXT.err_wrong_course_units)
                else:
                    message.reply_text(TXT.err_wrong_course_info)

            elif state == TeacherState.wait_for_enter_new_marks:
                if message.text == 'لغو':
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_teaching_courses(message, teacher)
                    return

                lines = message.text.strip().split("\n")
                course_id = udata
                for line in lines:
                    colon = line.find(":")
                    if colon == -1:
                        message.reply_text(TXT.err_marks_no_colon.format(line=line), parse_mode=ParseMode.HTML)
                        return
                    stu_id = line[:colon]
                    mark = line[colon + 1:]
                    if self.dbc.is_student_of_course(stu_id, course_id) is None:
                        message.reply_text(TXT.err_s_id_is_invalid.format(line=line), parse_mode=ParseMode.HTML)
                        return

                    try:
                        mark = float(mark)
                    except ValueError:
                        message.reply_text(TXT.err_invalid_mark.format(line=line), parse_mode=ParseMode.HTML)
                        return

                    if mark > 20 or mark < 0:
                        message.reply_text(TXT.err_invalid_mark_range.format(line=line), parse_mode=ParseMode.HTML)
                        return
                    self.dbc.set_student_mark(stu_id, course_id, mark)
                self.show_course(message, course_id)
                self.dbc.update_user_state(chat_id, TeacherState.main_menu)

            elif state == TeacherState.wait_for_enter_delete_student:
                if message.text == 'لغو':
                    message.reply_text(TXT.canceled_successfully)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_teaching_courses(message, teacher)
                    return

                stu_id = persian_to_english(message.text.strip())
                course_id = udata
                if not stu_id.isdigit() or self.dbc.is_student_of_course(stu_id, course_id) is None:
                    message.reply_text(TXT.err_student_is_not_in_course)
                else:
                    self.dbc.remove_taken_course(stu_id, course_id)
                    message.reply_text(TXT.student_deleted_successfully)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_course(message, course_id)

            elif state == TeacherState.wait_for_enter_broadcast_text:
                course_id = udata
                course = self.dbc.get_course(course_id)
                if course is None:
                    message.edit_text(text=TXT.course_is_removed, reply_markup=InlineKeyboardMarkup([[]]))
                    return
                course = course[0]
                txt = '' if message.text == 'حذف' else f' [{jdatetime.datetime.now().strftime("%H:%M %Y/%m/%d")}]\n<i>{message.text}</i>\n'
                self.dbc.update_course_notif(course_id, txt)
                chat_ids = self.dbc.get_course_all_students_chatid(course_id)
                if chat_ids is not None and txt != '':
                    for s_chat_id in chat_ids:
                        s_chat_id = s_chat_id[0]
                        glogger(f"send new announcement notif to {s_chat_id}")
                        context.bot.send_message(chat_id=s_chat_id, parse_mode=ParseMode.HTML,
                                                 text=TXT.you_have_new_notif.format(course=course[1]))
                self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                self.show_course(message, course_id)

            elif state == TeacherState.wait_for_enter_poll_info:
                poll_info = message.text.split('\n')
                if len(poll_info) < 3:
                    message.reply_text(TXT.err_invalid_poll_info)
                else:
                    course_id = udata
                    course = self.dbc.get_course(course_id)
                    if course is None:
                        message.reply_text(text=TXT.course_is_removed, reply_markup=InlineKeyboardMarkup([[]]))
                        self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                        self.show_course(message, course_id)
                        return
                    course = course[0]
                    poll = {
                        'title': poll_info[0],
                        'options': [poll_info[i] for i in range(1, len(poll_info))]
                    }
                    self.dbc.update_course_poll(course_id, json.dumps(poll, ensure_ascii=False))

                    chat_ids = self.dbc.get_course_all_students_chatid(course_id)
                    if chat_ids is not None:
                        for s_chat_id in chat_ids:
                            s_chat_id = s_chat_id[0]
                            glogger(f"send new poll notif to {s_chat_id}")
                            context.bot.send_message(chat_id=s_chat_id,
                                                     text=TXT.alert_for_new_poll.format(course=course[1],
                                                                                        title=poll_info[0]),
                                                     parse_mode=ParseMode.HTML)

                    message.reply_text(text=TXT.poll_created_successfully.format(course=course[1], n=len(poll_info) - 1,
                                                                                 title=poll_info[0]),
                                       parse_mode=ParseMode.HTML)
                    self.dbc.update_user_state(chat_id, TeacherState.main_menu)
                    self.show_course(message, course_id)

        else:
            message.reply_text(TXT.err_login_again)

    @override
    def handel_call_back_query(self, update: Update, context: CallbackContext, user):
        callback_query = update.callback_query
        chat_id, t_id, state = user[0], user[2], user[3]
        teacher = self.dbc.get_teacher(t_id)
        if teacher is not None:
            teacher = teacher[0]
            if state == TeacherState.main_menu:
                if callback_query.data == "create_new_course":
                    callback_query.message.edit_text(text=TXT.give_new_course_info, parse_mode=ParseMode.HTML)
                    self.dbc.update_user_state(chat_id, TeacherState.wait_for_enter_new_course_info)

                elif callback_query.data.startswith("see_course"):
                    course_id = callback_query.data.split("/")[1]
                    self.dbc.update_user_data(chat_id, course_id)
                    self.show_course(callback_query.message, course_id, edit=True)

                elif callback_query.data == "logout":
                    callback_query.message.edit_text(text=TXT.logout_successfully % teacher[1],
                                                     reply_markup=InlineKeyboardMarkup([[]]))
                    self.dbc.delete_user(chat_id)
                    context.bot.send_message(chat_id=chat_id, text=TXT.login_or_signup, parse_mode=ParseMode.HTML)

                elif callback_query.data.startswith("change_marks"):
                    course_id = callback_query.data.split("/")[1]
                    course = self.dbc.get_course(course_id)
                    if course is None:
                        callback_query.message.edit_text(text=TXT.course_is_removed, parse_mode=ParseMode.HTML,
                                                         reply_markup=InlineKeyboardMarkup([[]]))
                        return
                    course = course[0]
                    callback_query.message.edit_text(TXT.enter_marks.format(name=course[1]), parse_mode=ParseMode.HTML)
                    self.dbc.update_user_state(chat_id, TeacherState.wait_for_enter_new_marks)

                elif callback_query.data.startswith("delete_student"):
                    course_id = callback_query.data.split("/")[1]
                    course = self.dbc.get_course(course_id)
                    if course is None:
                        callback_query.message.edit_text(text=TXT.course_is_removed,
                                                         reply_markup=InlineKeyboardMarkup([[]]))
                        return
                    course = course[0]
                    callback_query.message.edit_text(TXT.enter_student_for_delete.format(name=course[1]),
                                                     parse_mode=ParseMode.HTML)
                    self.dbc.update_user_state(chat_id, TeacherState.wait_for_enter_delete_student)

                elif callback_query.data.startswith("new_poll"):
                    course_id = callback_query.data.split("/")[1]
                    course = self.dbc.get_course(course_id)
                    if course is None:
                        callback_query.message.edit_text(text=TXT.course_is_removed,
                                                         reply_markup=InlineKeyboardMarkup([[]]))
                        return
                    course = course[0]
                    if course[5] == '':
                        callback_query.message.edit_text(text=TXT.enter_poll, reply_markup=InlineKeyboardMarkup([[]]))
                        self.dbc.update_user_state(chat_id, TeacherState.wait_for_enter_poll_info)
                    else:
                        callback_query.answer(text=TXT.already_has_poll)
                        self.show_course(callback_query.message, course[0], edit=True)

                elif callback_query.data.startswith("broadcast"):
                    callback_query.message.reply_text(TXT.enter_broadcast_text, parse_mode=ParseMode.HTML)
                    self.dbc.update_user_state(chat_id, TeacherState.wait_for_enter_broadcast_text)

                elif callback_query.data.startswith("finish_poll"):
                    course_id = callback_query.data.split("/")[1]
                    course = self.dbc.get_course(course_id)
                    message = callback_query.message
                    if course is None:
                        callback_query.message.edit_text(text=TXT.course_is_removed,
                                                         reply_markup=InlineKeyboardMarkup([[]]))
                        return
                    course = course[0]
                    students = self.dbc.students_of_course(course_id)
                    if course[5] != '':
                        poll_info = json.loads(course[5])

                        poll_info_prnt = 'نتایج نهایی رای گیری\n <b>' + poll_info['title'] + '</b>\n\n'
                        poll_res = [0 for _ in range(len(poll_info['options']))]
                        for s in students:
                            if 0 <= s[8] < len(poll_res):
                                poll_res[s[8]] += 1

                        total = sum(poll_res)
                        for i in range(len(poll_res)):
                            perc = poll_res[i] * 100 / total if total > 0 else 0
                            poll_info_prnt += f'<b>[{poll_res[i]} ({perc:.1f}%)]</b>  — <i>' + \
                                              poll_info['options'][i] + '</i> \n'
                            poll_info_prnt += '<i>رای دهنده ها: </i>'
                            for s in students:
                                if s[8] == i:
                                    poll_info_prnt += s[1] + ', '
                            poll_info_prnt += '\n\n'

                        self.dbc.update_course_poll(course[0], '')
                        for s in students:
                            self.dbc.update_student_choice(s[4], s[5], -1)

                        context.bot.deleteMessage(message.chat_id, message.message_id)
                        context.bot.send_message(message.chat_id, text=poll_info_prnt, parse_mode=ParseMode.HTML)
                        self.show_course(message, course[0])

                    else:
                        self.show_teaching_courses(callback_query.message, teacher, edit=True)


                elif callback_query.data == "back_to_main":
                    self.show_teaching_courses(callback_query.message, teacher, edit=True)

            elif state == TeacherState.wait_for_enter_new_course_info:
                callback_query.answer(TXT.err_enter_new_course_info)

            elif state == TeacherState.wait_for_enter_new_marks:
                callback_query.answer(TXT.err_enter_new_marks)

            elif state == TeacherState.wait_for_enter_delete_student:
                callback_query.answer(TXT.err_enter_student_to_delete)

            elif state == TeacherState.wait_for_enter_poll_info:
                callback_query.answer(TXT.err_enter_poll_info)

        else:
            callback_query.answer(TXT.err_login_again)

    def show_course(self, message, course_id, edit=False):
        course = self.dbc.get_course(course_id)
        if course is None:
            if edit:
                message.edit_text(text=TXT.course_is_removed, parse_mode=ParseMode.HTML,
                                  reply_markup=InlineKeyboardMarkup([[]]))
            else:
                message.reply_text(text=TXT.course_is_removed, parse_mode=ParseMode.HTML)
            return
        course = course[0]  # pick first row

        students = self.dbc.students_of_course(course_id)

        poll_info_prnt = ' —— '
        if course[5] != '':
            # calculate result
            poll_info = json.loads(course[5])
            poll_res = [0 for _ in range(len(poll_info['options']))]
            for s in students:
                if 0 <= s[8] < len(poll_res):
                    poll_res[s[8]] += 1
            poll_info_prnt = ' <i>' + poll_info['title'] + '</i>\n'
            total = sum(poll_res)
            for i in range(len(poll_res)):
                perc = poll_res[i] * 100 / total if total > 0 else 0
                poll_info_prnt += f'[{poll_res[i]} ({perc:.1f}%)]  — <i>' + poll_info['options'][i] + '</i> \n'

        text = TXT.teacher_course_students.format(name=course[1], units=course[2], poll=poll_info_prnt,
                                                  notif=course[4] if course[4] != '' else ' —— ',
                                                  students=0 if students is None else len(students))
        if students is not None:
            for stu in students:
                mark = "<i>نامشخص</i>" if stu[7] == -1 else stu[7]
                text += f"{stu[1]}({stu[0]}) : {mark} \n"

        btns = [
            [InlineKeyboardButton(TXT.change_marks, callback_data=f'change_marks/{course_id}')],
            [InlineKeyboardButton(TXT.delete_student, callback_data=f'delete_student/{course_id}')],
            [InlineKeyboardButton(TXT.send_broadcast, callback_data=f'broadcast/{course_id}')],

            [InlineKeyboardButton(TXT.new_poll, callback_data=f'new_poll/{course_id}')
             if course[5] == '' else
             InlineKeyboardButton(TXT.finish_poll, callback_data=f'finish_poll/{course_id}')],

            [InlineKeyboardButton(TXT.back, callback_data='back_to_main')],
        ]
        if edit:
            message.edit_text(text=text, parse_mode=ParseMode.HTML,
                              reply_markup=InlineKeyboardMarkup(btns))
        else:
            message.reply_text(text=text, parse_mode=ParseMode.HTML,
                               reply_markup=InlineKeyboardMarkup(btns))

    def show_teaching_courses(self, message, teacher, edit=False):
        courses = self.dbc.get_teacher_courses(teacher[0])
        text = TXT.teacher_main_menu_title.format(name=str(teacher[1]), t_id=str(teacher[0]),
                                                  c_cnt=0 if courses is None else len(courses))
        btns = [
            [InlineKeyboardButton(TXT.create_new_course, callback_data="create_new_course")]
        ]
        if courses is not None:
            for crs in courses:
                btns.append([InlineKeyboardButton(crs[1], callback_data=f"see_course/{crs[0]}")])

        btns.append([InlineKeyboardButton(TXT.logout, callback_data="logout")])

        if edit:
            message.edit_text(text=text, parse_mode=ParseMode.HTML,
                              reply_markup=InlineKeyboardMarkup(btns))
        else:
            message.reply_text(text=text, parse_mode=ParseMode.HTML,
                               reply_markup=InlineKeyboardMarkup(btns))

