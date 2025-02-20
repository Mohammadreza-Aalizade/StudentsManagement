from bot.Logger import Logger

db_file = "students_management.db"
bot_token = '5595352211:AAESfGZLpQWxvZPOoCUAV9HYEytDKcfrJ4Y'
glogger = Logger("./log.txt")


class TXT:
    err_unable = 'متاسفانه مشکلی پیش امده و فعلا امکان ارسال پیام وجود ندارد.'
    sent_to_teacher = 'پیام شما با موفقیت تحویل استاد شد.'
    you_have_new_messge = 'شما یک پام جدید از طرف دانشجو با شماره دانشجویی <b>{sid}</b> در درس <b>{cname}</b> دارید.'
    enter_your_text_or_file = 'لطفا متن، فایل یا وویس مورد نظر را بفرستید، کل محتوای قابل ارسال شما باید در قالب یک پیام باشد.\n\nاولین پیامی که بفرستید مستقیما برای استاد ارسال خواهد شد. برای لغو <b>/cancel</b> را بفرستید.'
    login_or_signup = "<b>ثبت نام یا ورود</b>\n\n<i><b>ورود</b></i>: برای ورود  به حساب کاربری در یک پیام، در خط اول شماره کاربری و در خط دوم رمز را وارد کنید.\n\n<i><b>ثبت نام</b></i>: برای ثبت نام دانشجو در یک پیام، در خط اول شماره دانشجویی، در خط دوم نام کامل، در خط سوم رشته و در خط آخر رمز ورود را وارد کنید."
    student_wrong_password = "❌ رمز ورود دانشجو اشتباه است لطفا دوباره تلاش کنید\n/start"
    teacher_wrong_password = "❌ رمز ورود استاد اشتباه است لطفا دوباره تلاش کنید\n/start"
    no_account_matched = "⚠️ هیچ حسابی مطابق اطلاعات شما وجود ندارد، لطفا دوباره تلاش کنید\n/start"
    login_successful = "✅ شما با موفقیت وارد حساب کاربری %s شدید"
    logout_successfully = "✅ شما با موفقیت از حساب کاربری %s خارج شدید"
    err_id_must_be_digits = "❌ شماره کاربری باید عدد باشد، لطفا دوباره تلاش کنید\n/start"
    student_main_menu_title = "<b>نام</b>: {name}\n<b>شماره دانشجو‌یی</b>: {s_id}\n<b>تعداد درس های اخذ شده</b>: {c_cnt}\n"
    open_students_channel = "↗️ ورود به کانال این درس"
    back = "بازگشت ⬅️"
    message_teacher = 'پیام به استاد ✉️'
    logout = "خروج از حساب کاربری ⬅️"
    take_new_course = "➕ اخذ درس جدید"
    err_login_again = "مشکلی رخ داد، دوباره وارد شوید \n/start"
    err_duplicate_s_id = "⚠️ در حال حاظر یک حساب کاربری برای شماره دانشجویی {s_id} موجود است، لطفا دوباره تلاش کنید.\n/start"
    give_course_id_to_take = 'لطفا شماره درسی که میخواهید اخذ کنید را وارد کنید. برای لغو عملیات  <b>/cancel</b> را ارسال کنید.'
    err_enter_course_id = "لطفا شماره درسی که میخواهد اخذ کنید را وارد کنید"
    err_enter_message = 'متن پیام را ارسال کنید'
    err_course_not_found = "درسی که قصد اخذ آن را دارید وجود ندارد، لطفا در وارد کردن شماره درس دقت کنید."
    err_course_not_exist = 'درس مورد نظر حذف شده است'
    teacher_not_login = 'متاسفانه درحال حاضر هیچ حساب تلگرامی داخل حساب کاربری استاد این درس نیست.'
    course_taken_successfully = "✅ درس مورد نظر با موفقیت اخذ شد."
    student_see_course = "<b>نام درس</b>: {name}\n<b>تعداد واحد</b>: {units}\n<b>نام استاد</b>: {teacher}\n<b>تاریخ اخذ</b>: {date}\n<b>نمره</b>: {mark}\n\n<b>اطلاعیه</b>: {notif}"
    err_duplicate_course = "شما این درس را قبلا یک بار اخذ کردید."

    teacher_main_menu_title = "<b>نام</b>: {name}\n<b>شماره استاد</b>: {t_id}\n<b>تعداد درس ها</b>: {c_cnt}\n"
    give_new_course_info = 'لطفا اطلاعات درس جدید را وارد کنید یا برای لغو <b>/cancel</b> را بفرستید. اطلاعات باید فقط در یک پیام به طوری که در خط اول نام درس، در خط دوم تعداد واحد آن باشد ارسال شود.'
    err_enter_new_course_info = 'لطفا اطلاعات درس جدید را وارد کنید'
    err_wrong_course_info = '❌ اطلاعات درس جدید صحیح نیست'
    err_wrong_course_units = '❌ تعداد واحد درس صحیح نیست'
    course_created_successfully = '✅ درس با موفقیت ساخته شد'
    change_marks = '📝 تغییر نمره دانشجویان'
    delete_student = '❌ حذف یک دانشجو'
    send_broadcast = '📨 تغییر اطلاعیه'
    new_poll = '📊 نظرسنجی جدید'
    finish_poll = '⏹ توقف نظرسنجی'
    create_new_course = "➕ ارائه درس جدید"
    teacher_course_students = '<b>نام درس</b>:{name}\n<b>تعداد واحد</b>:{units}\n<b>تعداد دانشجو</b>:{students}\n<b>اطلاعیه</b>:{notif}\n<b>رای گیری</b>:{poll}\n\n'
    enter_marks = 'لطفا نمرات دانشجویان درس <b>{name}</b> را وارد کنید. \nباید در هر خط ابتدا شماره دانشجویی، بعد یک دو نقطه و بعد از آن نمره آن دانشجو را وارد کنید. مثال:\n<pre>40013212101 : 20\n40013212102 : 16.5\n</pre>\n\nبرای لغو  فقط کلمه <b>/cancel</b> را بفرستید.'
    enter_student_for_delete = 'لطفا شماره دانشجویی از درس <b>{name}</b> که میخواهید حذف شود را وارد کنید. برای لغو  فقط کلمه <b>/cancel</b> را بفرستید.'
    err_enter_new_marks = 'نمرات دانشجویان را وارد کنید'
    err_enter_student_to_delete = 'شماره دانشجویی که باید حذف شود را وارد کنید'
    canceled_successfully = "✔️ عملیات با موفقیت لغو شد"
    err_marks_no_colon = "در خط <b>\"{line}\"</b> دو نقطه پیدا نشد. دوباره تلاش کنید."
    err_s_id_is_invalid = "شماره دانشجویی در خط <b>\"{line}\"</b> نا معتبر است یا عضو این کلاس نیست. دوباره تلاش کنید."
    err_invalid_mark = "نمره داده شده در خط <b>\"{line}\"</b> نا معتبر است. دوباره تلاش کنید."
    err_invalid_mark_range = "نمره داده شده در خط <b>\"{line}\"</b> خارج از بازه 0 تا 20 است. دوباره تلاش کنید."
    err_student_is_not_in_course = "شماره دانشجویی غلط است یا دانشجو عضو این کلاس نیست."
    student_deleted_successfully = "✅ دانشجو با موفقیت حذف شد."
    course_is_removed = 'متاسفانه درس مورد نظر حذف شده است\n\start'
    already_has_poll = 'این درس در حال حاظر یک رای گیری فعال دارد'
    enter_poll = 'لطفا در خط اول عنوان رای گیری و در خطوط بعدی در هر خط یک گذینه برای انتخاب توسط دانشجویان را وارد کنید.'
    err_enter_poll_info = 'باید یک متن شامل اطلاعات رای گیری بفرستید'
    err_invalid_poll_info = 'متن ارسالی باید حداقل شامل سه خط باشد، خط اول عنوان رای گیری و در دو خط بعدی متن گذینه های اول و دوم (میتوانید گذینه های بیشتری در خطوط بعدی قرار دهید)'
    poll_created_successfully = 'رای گیری با عنوان <b>\"{title}\"</b> و {n} گذینه در دسترس دانشجویان درس <b>\"{course}\"</b> قرار گرفت. دانشجویان از منو درس در حساب کاربری خود میتوانند در رای گیری شرکت کنند.'
    alert_for_new_poll = 'سلام شما یک رای گیری با عنوان <b>\"{title}\"</b> در درس <b>\"{course}\"</b> دارید. از منو درس میتوانید در رای گیری شرکت کنید.'
    participate_poll = 'شرکت در رای گیری'
    enter_broadcast_text = "لطفاً متن اطلاعیه را وارد کنید برای حذف کردن اطلاعیه کلمه <b>\"حذف\"</b> را بفرستید."
    you_have_new_notif = "شما یک اطلاعیه جدید در درس <b>\"{course}\"</b> دارید."


class StudentState:
    main_menu = 0
    wait_for_enter_taking_course_id = 1
    wait_for_enter_message = 2


class TeacherState:
    main_menu = 0
    wait_for_enter_new_course_info = 1
    wait_for_enter_new_marks = 2
    wait_for_enter_delete_student = 3
    wait_for_enter_poll_info = 4
    wait_for_enter_broadcast_text = 5


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def persian_to_english(s):
    nums = [
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ],
        ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', ],
    ]
    for i in range(10):
        s = s.replace(nums[1][i], nums[0][i])
    return s


def override(_):
    return _

