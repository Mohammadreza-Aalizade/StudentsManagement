import jdatetime
from telegram import Update, ParseMode
from telegram.error import NetworkError
from telegram.ext import Updater, ChatMemberHandler, CommandHandler, Filters, \
    CallbackQueryHandler, MessageHandler, CallbackContext
from bot import DatabaseConnector, StudentResponder, TeacherResponder
from bot.Constants import *


class MainBot:
    def __init__(self):
        self.dbc = DatabaseConnector(db_file)
        self.student_responder = StudentResponder(self.dbc)
        self.teacher_responder = TeacherResponder(self.dbc)
        commands = ['start', 'myid', 'cancel']

        self.updater = Updater(bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(ChatMemberHandler(callback=self.handel_join))
        self.dispatcher.add_handler(CommandHandler(filters=Filters.chat_type.private,
                                                   command=commands,
                                                   callback=self.handel_command))
        self.dispatcher.add_handler(CallbackQueryHandler(self.handel_call_back_query))
        self.dispatcher.add_handler(MessageHandler(filters=Filters.chat_type.private,
                                                   callback=self.handel_private_message))
        self.dispatcher.add_error_handler(self.handel_error)

        glogger("--- bot created ---")

    def handel_command(self, update: Update, context: CallbackContext):
        chat_id = update.message.from_user.id
        glogger(f"{chat_id} => cmnd:{update.message.text}")
        if update.message.text == '/myid':
            update.message.reply_text(chat_id)
        else:
            user = self.dbc.get_user(chat_id)
            if user is None:
                update.message.reply_text(TXT.login_or_signup, parse_mode=ParseMode.HTML)
            elif user[0][1] == 1:  # teacher
                self.teacher_responder.handel_command(update, context, user[0])
            elif user[0][1] == 2:  # student
                self.student_responder.handel_command(update, context, user[0])

    def handel_private_message(self, update: Update, context: CallbackContext):
        chat_id = update.message.from_user.id
        user = self.dbc.get_user(chat_id)
        glogger(f"{chat_id} => txt:{update.message.text}")
        if update.message.text is not None:
            update.message.text = persian_to_english(update.message.text)
        if user is None:
            if update.message.text is not None:
                text = update.message.text
                lines = text.strip().split('\n')
                if len(lines) == 2:
                    s_t_id, password = lines[0], lines[1]
                    if not s_t_id.isdigit():
                        update.message.reply_text(TXT.err_id_must_be_digits)
                        return

                    student = self.dbc.get_student(s_t_id)
                    if student is not None:
                        student = student[0]  # pick the first row
                        if student[3] == password:
                            update.message.reply_text(TXT.login_successful % student[1])
                            self.dbc.set_user(chat_id, 2, s_t_id)
                            self.student_responder.show_taken_courses(update.message, student)
                        else:
                            update.message.reply_text(TXT.student_wrong_password)
                    else:
                        teacher = self.dbc.get_teacher(s_t_id)
                        if teacher is not None:
                            teacher = teacher[0]  # pick the first row
                            if teacher[2] == password:
                                update.message.reply_text(TXT.login_successful % teacher[1])
                                self.dbc.set_user(chat_id, 1, s_t_id)
                                self.teacher_responder.show_teaching_courses(update.message, teacher)
                            else:
                                update.message.reply_text(TXT.teacher_wrong_password)
                        else:
                            update.message.reply_text(TXT.no_account_matched)

                elif len(lines) == 4:
                    s_id, name, major, password = lines[0], lines[1], lines[2], lines[3]
                    if self.dbc.get_student(s_id) is None:
                        self.dbc.create_student(s_id, name, major, password)
                        self.dbc.set_user(chat_id, 2, s_id)
                        self.student_responder.show_taken_courses(update.message, (s_id, name, major, password))
                    else:
                        update.message.reply_text(TXT.err_duplicate_s_id.format(s_id=s_id))
                else:
                    update.message.reply_text(TXT.login_or_signup, parse_mode=ParseMode.HTML)
            else:
                update.message.reply_text(TXT.login_or_signup, parse_mode=ParseMode.HTML)
        elif user[0][1] == 1:  # teacher
            self.teacher_responder.handel_private_message(update, context, user[0])
        elif user[0][1] == 2:  # student
            self.student_responder.handel_private_message(update, context, user[0])

    def handel_call_back_query(self, update: Update, context: CallbackContext):
        chat_id = update.callback_query.from_user.id
        user = self.dbc.get_user(chat_id)
        glogger(f"{chat_id} => data:{update.callback_query.data}")
        if user is None:
            context.bot.send_message(chat_id=chat_id, text=TXT.login_or_signup, parse_mode=ParseMode.HTML)
        elif user[0][1] == 1:  # teacher
            self.teacher_responder.handel_call_back_query(update, context, user[0])
        elif user[0][1] == 2:  # student
            self.student_responder.handel_call_back_query(update, context, user[0])

    def handel_join(self, update: Update, context: CallbackContext):
        new_status = update.my_chat_member.new_chat_member.status
        chat = update.my_chat_member.chat.type
        uid = update.my_chat_member.from_user.id
        chat_id = update.my_chat_member.chat.id
        if new_status == 'member' or new_status == 'administrator' or new_status == 'creator':
            glogger(f"leave {chat}[{chat_id}] which [{uid}] had added ==> new status:({new_status})")
            context.bot.leave_chat(chat_id)
        else:
            glogger(f"ignore join-update from {chat}[{chat_id}] by [{uid}] ==> new status:({new_status})")

    def handel_error(self, update: Update, context: CallbackContext):
        glogger(f"handel_error:\n{context.error}")

    def start(self):
        try:
            glogger("--- bot starts polling ---")
            self.updater.start_polling()
            self.updater.idle()
        except (NetworkError, ConnectionResetError):
            glogger("--- Network error (bot is offline) ---")


if __name__ == '__main__':
    bot = MainBot()
    bot.start()

