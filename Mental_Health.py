from flask import Flask, request, render_template, redirect, session
from DBConnection import Db
import time

app = Flask(__name__)
app.secret_key="hiii"
static_path=r"C:\Users\USER\PycharmProjects\mental_new\Mental_Health\static\\"


@app.route('/', methods=['get', 'post'])
def login():
    if request.method=="POST":
        uname=request.form['donation-email']
        pswd=request.form['donation-name']
        db=Db()
        res=db.selectOne("SELECT * FROM login WHERE username='"+uname+"' AND PASSWORD='"+pswd+"'")
        if res is None:
            return "<script>alert('Invalid details');window.location='/';</script>"
        else:
            session['lg']="yes"
            session['lid']=res['login_id']
            type=res['usertype']
            if type == "admin":
                return redirect("/admin_home")
            elif type == "psychiatrist":
                return redirect("/psych_home")
            elif type == "user":
                return redirect("/user_home")
            else:
                return "<script>alert('Invalid user');window.location='/';</script>"
    else:
        return render_template("login.html")

@app.route("/psych_reg", methods=['get', 'post'])
def psych_reg():
    if request.method=="POST":
        name=request.form['pysch-name']
        place=request.form['pysch-place']
        email=request.form['donation-email']
        phone=request.form['pysch-phone']
        qual=request.form['pysch-qual']
        password=request.form['pysch-pass']
        img=request.files['pysch-img']
        dt=time.strftime("%Y%m%d_%H%M%S")
        img.save(static_path + "psych_img\\" + dt + ".jpg")
        path="/static/psych_img/" + dt + ".jpg"
        db=Db()
        lid=db.insert("INSERT INTO login VALUES(NULL, '" + email + "', '" + password + "', 'pending')")
        db.insert("INSERT INTO `psychiatrist` VALUES('" + str(lid) + "', '" + name + "', '" + place + "', '" + email + "', '" + phone + "', '" + qual + "', '" + path + "')")
        return "<script>alert('Registered');window.location='/';</script>"
    else:
        return render_template("psych_reg.html")

@app.route("/user_reg", methods=['get', 'post'])
def user_reg():
    if request.method=="POST":
        name=request.form['pysch-name']
        email=request.form['donation-email']
        phone=request.form['pysch-phone']
        password=request.form['pysch-pass']
        img=request.files['pysch-img']
        dt=time.strftime("%Y%m%d_%H%M%S")
        img.save(static_path + "user_imgs\\" + dt + ".jpg")
        path="/static/user_imgs/" + dt + ".jpg"
        db=Db()
        lid=db.insert("INSERT INTO login VALUES(NULL, '" + email + "', '" + password + "', 'user')")
        db.insert("INSERT INTO `user` VALUES('" + str(lid) + "', '" + name + "', '" + email + "', '" + phone + "', '" + path + "')")
        return "<script>alert('Registered');window.location='/';</script>"
    else:
        return render_template("user_reg.html")


@app.route("/logout")
def logout():
    session['lg']=""
    return redirect("/")

##############          ADMIN
@app.route("/admin_home")
def admin_home():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("admin/index.html")

@app.route("/admin_view_pending_psych")
def admin_view_pending_psych():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `psychiatrist`, login WHERE `psychiatrist`.psych_id=login.login_id AND login.usertype='pending'")
    return render_template("admin/view_psych_pending.html", data=res)

@app.route("/admin_approve_psych/<pid>")
def admin_approve_psych(pid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.update("UPDATE login SET usertype='psychiatrist' WHERE login_id='"+pid+"'")
    return redirect("/admin_view_pending_psych#aaa")

@app.route("/admin_reject_psych/<pid>")
def admin_reject_psych(pid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.update("UPDATE login SET usertype='rejected' WHERE login_id='"+pid+"'")
    return redirect("/admin_view_pending_psych#aaa")


@app.route("/admin_view_approved_psych")
def admin_view_approved_psych():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `psychiatrist`, login WHERE `psychiatrist`.psych_id=login.login_id AND login.usertype='psychiatrist'")
    return render_template("admin/view_psych_approved.html", data=res)


@app.route("/admin_view_rejected_psych")
def admin_view_rejected_psych():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `psychiatrist`, login WHERE `psychiatrist`.psych_id=login.login_id AND login.usertype='rejected'")
    return render_template("admin/view_psych_rejected.html", data=res)

@app.route("/admin_view_users")
def admin_view_users():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `user`")
    return render_template("admin/view_users.html", data=res)


@app.route("/admin_change_password", methods=['get', 'post'])
def admin_change_password():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    if request.method == "POST":
        psw=request.form['t1']
        db=Db()
        db.update("update login set password='" + psw + "' where login_id='" + str(session['lid']) + "'")
        return "<script>alert('Password changed');window.location='/';</script>"
    else:
        return render_template("admin/change_password.html")

@app.route("/admin_view_complaints")
def admin_view_complaints():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db = Db()
    res = db.select("SELECT * FROM `complaints`, `user` WHERE `complaints`.user_id=`user`.user_id ORDER BY comp_id DESC")
    return render_template("admin/view_complaints.html", data=res)
@app.route("/send_reply/<cid>", methods=['get', 'post'])
def send_reply(cid):
    if request.method == "POST":
        reply=request.form['t1']
        db=Db()
        db.update("UPDATE `complaints` SET reply='" + reply + "' WHERE comp_id='" + cid + "'")
        return redirect("/admin_view_complaints")
    else:
        return render_template("admin/send_reply.html")

#####################           PSYCHIATRIST
@app.route("/psych_home")
def psych_home():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("psychiatrist/index.html")

@app.route("/psych_view_profile")
def psych_view_profile():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.selectOne("SELECT * FROM `psychiatrist` WHERE psych_id='"+str(session['lid'])+"'")
    return render_template("psychiatrist/view_profile.html", data=res)

@app.route("/psych_add_sched", methods=['get', 'post'])
def psych_add_sched():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    if request.method == "POST":
        date=request.form['t1']
        ftime=request.form['t2']
        ttime=request.form['t3']
        db=Db()
        db.insert("INSERT INTO `schedule` VALUES(NULL, '" + str(session['lid']) + "', '" + date + "', "
                            "'" + ftime + "', '" + ttime + "')")
        return "<script>alert('Schedule added');window.location='/psych_add_sched';</script>"
    else:
        return render_template("psychiatrist/add_schedule.html")

@app.route("/psych_view_sched")
def psych_view_sched():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("select * from schedule where psych_id='" + str(session['lid']) + "'")
    return render_template("psychiatrist/view_schedule.html", data=res)

@app.route("/psych_delete_sched/<sid>")
def psych_delete_sched(sid):
    db=Db()
    db.delete("delete from schedule where sched_id='" + sid + "'")
    return redirect("/psych_view_sched#aaa")


@app.route("/psych_view_booking/<sid>")
def psych_view_booking(sid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `booking`, USER WHERE `booking`.userid=user.user_id AND booking.sched_id='" + sid + "'")
    return render_template("psychiatrist/view_booking.html", data=res)


@app.route("/psych_view_requests")
def psych_view_requests():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `patient`, USER WHERE patient.user_id=user.user_id AND "
                  "patient.status='pending' AND patient.psych_id='" + str(session['lid']) + "'")
    return render_template("psychiatrist/view_requests.html", data=res)

@app.route("/psych_accept_request/<rid>")
def psych_accept_request(rid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.update("UPDATE patient SET STATUS='accepted' WHERE patient_id='"+rid+"'")
    return redirect("/psych_view_requests")

@app.route("/psych_reject_request/<rid>")
def psych_reject_request(rid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.update("UPDATE patient SET STATUS='rejected' WHERE patient_id='"+rid+"'")
    return redirect("/psych_view_requests")



@app.route("/psych_view_patients")
def psych_view_patients():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `patient`, USER WHERE patient.user_id=user.user_id AND "
                  "patient.status='accepted' AND patient.psych_id='" + str(session['lid']) + "'")
    return render_template("psychiatrist/view_patients.html", data=res)


@app.route("/psych_view_records/<uid>")
def psych_view_records(uid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `health_state`  WHERE user_id='" + uid + "' order by health_id desc")
    return render_template("psychiatrist/view_health_records.html", data=res)


@app.route("/psych_change_password", methods=['get', 'post'])
def psych_change_password():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    if request.method == "POST":
        psw=request.form['t1']
        db=Db()
        db.update("update login set password='" + psw + "' where login_id='" + str(session['lid']) + "'")
        return "<script>alert('Password changed');window.location='/';</script>"
    else:
        return render_template("psychiatrist/change_password.html")


########################            USER
@app.route("/user_home")
def user_home():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("user/index.html")

@app.route("/user_view_profile")
def user_view_profile():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.selectOne("SELECT * FROM USER WHERE user_id='"+str(session['lid'])+"'")
    return render_template("user/view_profile.html", data=res)


@app.route("/user_view_approved_psych")
def user_view_approved_psych():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `psychiatrist`, login WHERE `psychiatrist`.psych_id=login.login_id AND login.usertype='psychiatrist'")
    return render_template("user/view_psych_approved.html", data=res)

@app.route("/user_send_request/<pid>")
def user_send_request(pid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.insert("INSERT INTO `patient` VALUES( NULL, CURDATE(), '" + str(session['lid']) + "', '" + pid + "', 'pending')")
    return "<script>alert('Requested');window.location='/user_view_approved_psych';</script>"

@app.route("/user_view_req_status")
def user_view_req_status():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `patient`, `psychiatrist` WHERE `psychiatrist`.psych_id=`patient`.psych_id "
                           "AND patient.user_id='"+ str(session['lid']) + "'")
    return render_template("user/view_request_status.html", data=res)


@app.route("/user_delete_request/<rid>")
def user_delete_request(rid):
    db=Db()
    db.delete("DELETE FROM `patient` WHERE patient_id='" + rid + "'")
    return redirect("/user_view_req_status")


@app.route("/user_view_schedules/<pid>")
def user_view_schedules(pid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `schedule` WHERE date>=curdate() and psych_id='"+ pid + "'")
    return render_template("user/view_schedule.html", data=res)

@app.route("/user_book_schedule/<sid>")
def user_book_schedule(sid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.insert("INSERT INTO `booking` VALUES(NULL, CURDATE(), CURTIME(), '" + str(session['lid']) + "', '" + sid + "')")
    return redirect("/user_view_approved_psych")

@app.route("/user_view_booking")
def user_view_booking():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `booking`, `schedule`, `psychiatrist` WHERE `booking`.sched_id=`schedule`.sched_id AND"
                  " `schedule`.psych_id=`psychiatrist`.psych_id AND `booking`.userid='" + str(session['lid']) + "'")
    return render_template("user/view_booking.html", data=res)

@app.route("/user_view_reply")
def user_view_reply():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `complaints` WHERE user_id='" + str(session['lid']) + "'")
    return render_template("user/view_reply.html", data=res)

@app.route("/user_delete_comp/<cid>")
def user_delete_comp(cid):
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.delete("DELETE FROM `complaints` WHERE comp_id='" + cid + "'")
    return redirect("/user_view_reply")

@app.route("/user_send_complaint", methods=['get', 'post'])
def user_send_complaint():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    if request.method=="POST":
        comp=request.form['t1']
        db=Db()
        db.insert("INSERT INTO `complaints` VALUES(NULL, '" + str(session['lid']) + "', CURDATE(), '" + comp + "', 'pending')")
        return "<script>alert('Complaint sent');window.location='/user_send_complaint';</script>"
    else:
        return render_template("user/send_complaint.html")

@app.route("/user_change_password", methods=['get', 'post'])
def user_change_password():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    if request.method == "POST":
        psw=request.form['t1']
        db=Db()
        db.update("update login set password='" + psw + "' where login_id='" + str(session['lid']) + "'")
        return "<script>alert('Password changed');window.location='/';</script>"
    else:
        return render_template("user/change_password.html")

@app.route("/user_questionnaire", methods=['get', 'post'])
def user_questionnaire():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    if request.method=="POST":
        score=request.form['radio']
        session['q_score'] = session['q_score'] + int(score)
        btn = request.form['btn']
        if btn == "NEXT":
            cnt = session['q_cnt'] + 1
            session['q_cnt'] = cnt
            questions = ["Feeling low in energy or slowed down", "Crying easily", "Feeling of being trapped or caught",
                         "Blaming yourself for things", "Feeling lonely", "Worrying too much about things",
                         "Feeling no interest in things", "Feeling hopeless about the future",
                         "Feeling everything is an effort",
                         "Feelings of worthlessness"]
            return render_template("user/questionnaire.html", qn=questions[cnt], cnt=cnt)
        else:
            print("Final score : ", session['q_score'])
            avg_score=session['q_score']/10
            if avg_score <=0.2:
                avg_score = 0.0
            elif avg_score >0.2 and avg_score <=0.7:
                avg_score = 0.5
            elif avg_score >0.7 and avg_score <=1.2:
                avg_score = 1.0
            elif avg_score >1.2 and avg_score <=1.7:
                avg_score = 1.5
            elif avg_score >1.7 and avg_score <=2.2:
                avg_score = 2.0
            session['q_avg'] = avg_score
            return "<script>alert('Test Completed');window.location='/user_home';</script>"
    else:
        session['q_score']=0
        session['q_cnt']=0
        questions=["Feeling low in energy or slowed down", "Crying easily", "Feeling of being trapped or caught",
                   "Blaming yourself for things", "Feeling lonely", "Worrying too much about things",
                   "Feeling no interest in things", "Feeling hopeless about the future", "Feeling everything is an effort",
                   "Feelings of worthlessness"]
        return render_template("user/questionnaire.html", qn=questions[0], cnt=session['q_cnt'])


@app.route("/face_emotion")
def face_emotion():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    from new_cam import start_camera
    emo=start_camera()
    emo_scores={"angry":0, "disgust":0.5, "sad":1, "neutral":1.5, "happy":2, "very happy": 2.5, "joyful": 3}
    session['emo']=emo_scores[emo]
    return "<script>alert('Test Completed');window.location='/user_home';</script>"



@app.route("/user_chatbot", methods=['get', 'post'])
def user_chatbot():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    if request.method=="POST":
        answer=request.form['annn']
        words = answer.split(" ")
        import nltk
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        ngtv = 0
        pstv = 0
        ntl = 0
        sid = SentimentIntensityAnalyzer()
        lst = []
        for word in words:
            ss = sid.polarity_scores(word)
            print("Pl  :", ss)
            a = float(ss['pos'])
            b = float(ss['neg'])
            c = float(ss['neu'])
            lst.append({'word': word, 'scr': ss})
            if a > b:
                if a > c:
                    pstv = pstv + 1
                else:
                    ntl = ntl + 1
            else:
                if b > c:
                    ngtv = ngtv + 1
                else:
                    ntl = ntl + 1
        print(lst)
        session['ngtv']=session['ngtv'] + ngtv

        btn = request.form['btn']
        if btn == "NEXT":
            cnt = session['q_cnt'] + 1
            session['q_cnt'] = cnt
            questions = ["How was your day", "Describe your current situation", "How do others see you",
                         "What do you think about your social connections"]
            return render_template("user/chatbot.html", qn=questions[cnt], cnt=cnt)
        else:
            print("Final score : ", session['ngtv'])
            avg_score=session['ngtv']/4
            if avg_score <=0.2:
                avg_score = 0.0
            elif avg_score >0.2 and avg_score <=0.7:
                avg_score = 0.5
            elif avg_score >0.7 and avg_score <=1.2:
                avg_score = 1.0
            elif avg_score >1.2 and avg_score <=1.7:
                avg_score = 1.5
            else:
                avg_score = 2.0
            session['q_avg_chat'] = avg_score
            return "<script>alert('Test Completed');window.location='/user_home';</script>"
    else:

        session['q_cnt']=0
        session['ngtv']=0
        questions=["How was your day", "Describe your current situation", "How do others see you",
                   "What do you think about your social connections"]
        return render_template("user/chatbot.html", qn=questions[0], cnt=session['q_cnt'])


@app.route("/user_view_result")
def user_view_result():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    emo=session['emo']
    qstn=session['q_avg']
    chat=session['q_avg_chat']
    avg = (emo + qstn + chat) / 3

    final=""
    if avg < 1:
        final = "Sad"
    elif avg >= 1 and avg < 1.5:
        final = "Neutral"
    elif avg >= 1.5 and avg < 2:
        final = "Happy"
    else:
        final = "Very Happy"
    db=Db()
    db.insert("INSERT INTO `health_state` VALUES(NULL, '" + str(session['lid']) + "', CURDATE(), CURTIME(), '" + final + "')")
    return "<script>alert('You are " + str(final) + "');window.location='/user_home';</script>"


@app.route("/user_view_records")
def user_view_records():
    if session['lg']!="yes":
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("SELECT * FROM `health_state`  WHERE user_id='" + str(session['lid']) + "' order by health_id desc")
    return render_template("user/view_health_records.html", data=res)

if __name__ == '__main__':
    app.run()
