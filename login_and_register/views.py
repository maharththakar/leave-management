from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm, LoginForm
# from django.http import JsonResponse
from django.contrib import messages
from bson.objectid import ObjectId
# from django.core.mail import EmailMessage
from django.shortcuts import render
# from django.http import HttpResponse
from django.core.mail import send_mail
from pymongo import MongoClient
from datetime import datetime
import json
import pymongo
from decouple import config
from django.contrib.auth.hashers import make_password, check_password
# from django.http import JsonResponse
# from dns import resolver, exception

client = MongoClient(
    config('MONGO_URI'))
db = client['Leave_Management_System']

def profile_page(request):

    facultytable = db['faculty info']
    reply = facultytable.find_one({'email': request.session.get('username')})

    if reply:
        context = {
            'user': reply,
        }
        return render(request, 'faculty-profile.html', context)

    studenttable = db['student info']
    reply = studenttable.find_one(
        {'email': request.session.get('username')})

    if reply:
        context = {
            'user': reply,
        }
        return render(request, 'student-profile.html', context)

    tatble = db['ta info']
    reply = tatble.find_one({'email': request.session.get('username')})

    if reply:
        context = {
            'user': reply,
        }
        return render(request, 'ta-profile.html', context)

    adminTablte = db['adminTable']
    reply = adminTablte.find_one(
        {'email': request.session.get('username')})

    if reply:
        context = {
            'user': reply,
        }
        return render(request, 'profile.html', context)


def logout_view(request):
    request.session['username'] = None
    messages.success(request, "You have been logged out successfully!")
    return redirect('index')


def index(request):

    if request.session.get('username'):
        leavetable = db['leaveTable']
        adminTable = db['adminTable']
        reply = adminTable.find_one({'email': request.session.get('username')})

        if reply:

            cursor1 = leavetable.find()
            nol_list = []
            a, p, r = 0, 0, 0
            for doc in cursor1:
                if doc['status'] == 'approved':
                    a = a+1
                elif doc['status'] == 'rejected':
                    r = r+1
                else:
                    p = p+1
            nol_list.append(a)
            nol_list.append(p)
            nol_list.append(r)
            nol_json = json.dumps(nol_list)

            # if reply:
            context = {
                'user': reply,
                'nol_json': nol_json
            }
            return render(request, 'admin_page.html', context)

        facultytable = db['faculty info']
        reply = facultytable.find_one(
            {'email': request.session.get('username')})
        if reply:
            # leavetable = db['leaveTable']
            cursor = facultytable.find(
                {'email': request.session.get('username')})
            cursor1 = leavetable.find(
                {'email': request .session.get('username')})
            nol_list = []
            for doc in cursor:
                nol_list.append(doc['nol'])
            a, p, r = 0, 0, 0
            for doc in cursor1:
                if doc['status'] == 'approved':
                    a = a+1
                elif doc['status'] == 'rejected':
                    r = r+1
                else:
                    p = p+1
            nol_list.append(a)
            nol_list.append(p)
            nol_list.append(r)
            nol_json = json.dumps(nol_list)

            # if reply:
            context = {
                'user': reply,
                'leaves': leavetable.find({'email': request.session.get('username')}).sort('from_date', pymongo.DESCENDING),
                'nol_json': nol_json
            }

            return render(request, 'faculty.html', context)

        studenttable = db['student info']
        reply = studenttable.find_one(
            {'email': request.session.get('username')})
        if reply:

            # leavetable = db['leaveTable']
            cursor = studenttable.find(
                {'email': request.session.get('username')})
            cursor1 = leavetable.find(
                {'email': request.session.get('username')})
            nol_list = []
            for doc in cursor:
                nol_list.append(doc['nol'])
            a, p, r = 0, 0, 0
            for doc in cursor1:
                if doc['status'] == 'approved':
                    a = a+1
                elif doc['status'] == 'rejected':
                    r = r+1
                else:
                    p = p+1
            nol_list.append(a)
            nol_list.append(p)
            nol_list.append(r)
            nol_json = json.dumps(nol_list)
            context = {
                'user': reply,
                'leaves': leavetable.find({'email': request.session.get('username')}).sort('from_date', pymongo.DESCENDING),
                'nol_json': nol_json
            }

            return render(request, 'student.html', context)

        tatble = db['ta info']
        reply = tatble.find_one({'email': request.session.get('username')})
        if reply:

            cursor = tatble.find({'email': request.session.get('username')})
            cursor1 = leavetable.find(
                {'email': request.session.get('username')})
            nol_list = []
            for doc in cursor:
                nol_list.append(doc['nol'])
            a, p, r = 0, 0, 0
            for doc in cursor1:
                if doc['status'] == 'approved':
                    a = a+1
                elif doc['status'] == 'rejected':
                    r = r+1
                else:
                    p = p+1
            nol_list.append(a)
            nol_list.append(p)
            nol_list.append(r)
            nol_json = json.dumps(nol_list)
            context = {
                'user': reply,
                'leaves': leavetable.find({'email': request.session.get('username')}).sort('from_date', pymongo.DESCENDING),
                'nol_json': nol_json
            }

            return render(request, 'ta.html', context)

    form = LoginForm(request.POST or None)

    msg = None
    if request.method == 'POST':

        if form.is_valid():
            leavetable = db['leaveTable']
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            adminTable = db['adminTable']
            reply = adminTable.find_one({'email': username})
            if reply:
                if check_password(password, reply['password']):

                    request.session['username'] = username
                    messages.success(
                        request, "You have been logged in successfully as admin!")

                    cursor1 = leavetable.find()
                    nol_list = []
                    a, p, r = 0, 0, 0
                    for doc in cursor1:
                        if doc['status'] == 'approved':
                            a = a+1
                        elif doc['status'] == 'rejected':
                            r = r+1
                        else:
                            p = p+1
                    nol_list.append(a)
                    nol_list.append(p)
                    nol_list.append(r)
                    nol_json = json.dumps(nol_list)

                    # if reply:
                    context = {
                        'user': reply,
                        'nol_json': nol_json
                    }
                    return render(request, 'admin_page.html', context)
                    # return render(request, 'admin_page.html', {'user': reply})

            studenttable = db['student info']
            reply = studenttable.find_one({'email': username})

            if reply:
                if check_password(password, reply['password']):
                    request.session['username'] = username
                    messages.success(
                        request, "You have been logged in successfully as Student!")

                    cursor = studenttable.find(
                        {'email': request.session.get('username')})
                    cursor1 = leavetable.find(
                        {'email': request.session.get('username')})
                    nol_list = []
                    for doc in cursor:
                        nol_list.append(doc['nol'])
                    a, p, r = 0, 0, 0
                    for doc in cursor1:
                        if doc['status'] == 'approved':
                            a = a+1
                        elif doc['status'] == 'rejected':
                            r = r+1
                        else:
                            p = p+1
                    nol_list.append(a)
                    nol_list.append(p)
                    nol_list.append(r)
                    nol_json = json.dumps(nol_list)
                    context = {
                        'user': reply,
                        'leaves': leavetable.find({'email': request.session.get('username')}).sort('from_date', pymongo.DESCENDING),
                        'nol_json': nol_json
                    }
                    return render(request, 'student.html', context)

            facultytable = db['faculty info']
            reply = facultytable.find_one({'email': username})

            if reply:
                print(password)
                print(reply['password'])
                if check_password(password, reply['password']):
                    
                    request.session['username'] = username
                    messages.success(
                        request, "You have been logged in successfully as Faculty!")

                    # leavetable = db['leaveTable']
                    cursor = facultytable.find(
                        {'email': request.session.get('username')})
                    cursor1 = leavetable.find(
                        {'email': request.session.get('username')})
                    nol_list = []
                    for doc in cursor:
                        nol_list.append(doc['nol'])
                    a, p, r = 0, 0, 0
                    for doc in cursor1:
                        if doc['status'] == 'approved':
                            a = a+1
                        elif doc['status'] == 'rejected':
                            r = r+1
                        else:
                            p = p+1
                    nol_list.append(a)
                    nol_list.append(p)
                    nol_list.append(r)
                    nol_json = json.dumps(nol_list)
                    context = {
                        'user': reply,
                        'leaves': leavetable.find({'email': request.session.get('username')}).sort('from_date', pymongo.DESCENDING),
                        'nol_json': nol_json
                    }
                    return render(request, 'faculty.html', context)

            tatble = db['ta info']
            reply = tatble.find_one({'email': username})

            if reply:
                if check_password(password, reply['password']):
                    request.session['username'] = username
                    messages.success(
                        request, "You have been logged in successfully as TA!")
                    # leavetable = db['leaveTable']
                    cursor = tatble.find(
                        {'email': request.session.get('username')})
                    cursor1 = leavetable.find(
                        {'email': request.session.get('username')})
                    nol_list = []
                    for doc in cursor:
                        nol_list.append(doc['nol'])
                    a, p, r = 0, 0, 0
                    for doc in cursor1:
                        if doc['status'] == 'approved':
                            a = a+1
                        elif doc['status'] == 'rejected':
                            r = r+1
                        else:
                            p = p+1
                    nol_list.append(a)
                    nol_list.append(p)
                    nol_list.append(r)
                    nol_json = json.dumps(nol_list)
                    context = {
                        'user': reply,
                        'leaves': leavetable.find({'email': request.session.get('username')}).sort('from_date', pymongo.DESCENDING),
                        'nol_json': nol_json
                    }

                    return render(request, 'ta.html', context)

            messages.error(request, "Please Enter Valid Details!")
            return render(request, 'index.html', {'form': form, 'msg': msg})
    # response = JsonResponse({}, status=401)
    # render(request, 'index.html', {'form': form, 'msg': msg})
    # return response
    return render(request, 'index.html', {'form': form, 'msg': msg})


def leaveform(request):
    if request.method == 'POST':
        studenttable = db['student info']
        facultytable = db['faculty info']
        tatble = db['ta info']

        leave_type = request.POST.get('leave-type')
        leave_duration = request.POST.get('leave-duration')
        from_date = request.POST.get('from-date')
        to_date = request.POST.get('to-date')
        reason = request.POST.get('reason')

        if from_date > to_date:
            messages.error(request, 'From date cannot be greater than to date')
            return render(request, 'leaveform-student.html')

        leavetable = db['leaveTable']
        check = list(leavetable.find(
            {'email': request.session.get('username')}))
        # print(check)
        if check:
            for i in check:
                print(i['to_date'], i['from_date'])
                if i['to_date'] >= from_date and i['from_date'] <= to_date:
                    messages.error(
                        request, 'You have already applied for leave in this duration')
                    reply = studenttable.find_one(
                        {'email': request.session.get('username')})
                    if reply:
                        context = {
                            'user': reply,
                        }
                        return render(request, 'leaveform-student.html', context)
                    reply = tatble.find_one(
                        {'email': request.session.get('username')})
                    if reply:
                        context = {
                            'user': reply,
                        }
                        return render(request, 'leaveform.html', context)
                    reply = facultytable.find_one(
                        {'email': request.session.get('username')})
                    if reply:
                        context = {
                            'user': reply,
                        }
                        return render(request, 'leaveform.html', context)

        username = request.session.get('username')

        reply = studenttable.find_one({'email': username})

        if reply:
            emailList = []
            emailList.append(username)
            for i in reply['faculties']:
                emailList.append(i)

            for i in reply['tas']:
                emailList.append(i)
            role = "student"
            name = reply['name']
            email = reply['email']
            id = reply['id']
            nols = reply['nol']

        reply = facultytable.find_one({'email': username})

        if reply:
            emailList = []
            emailList.append(username)
            for i in reply['faculties']:
                emailList.append(i)

            for i in reply['tas']:
                emailList.append(i)
            role = "faculty"
            name = reply['name']
            email = reply['email']
            id = reply['id']
            nols = reply['nol']

        reply = tatble.find_one({'email': username})

        if reply:
            emailList = []
            emailList.append(username)
            for i in reply['faculties']:
                emailList.append(i)

            for i in reply['tas']:
                emailList.append(i)
            role = "ta"
            name = reply['name']
            email = reply['email']
            id = reply['id']
            nols = reply['nol']
        leaveTableEntry = {
            'leave_type': leave_type,
            'leave_duration': leave_duration,
            'from_date': from_date,
            'to_date': to_date,
            'reason': reason,
            'emailList': emailList,
            'status': 'pending',
            'role': role,
            'name': name,
            'email': email,
            'id': id,
            'nols': nols,
        }

        # if len(from_date) == 0 or len(to_date) == 0 or len(reason) == 0:
        #     messages.error(
        #         request, "Please fill all the details before submitting!")
        #     return render(request, 'leaveform.html')

        leaveTable = db['leaveTable']
        leaveTable.insert_one(leaveTableEntry)

        if leaveTableEntry is not None:
            messages.success(
                request, "You have successfully applied for leave!")
            return redirect('/')
        else:
            messages.error(request, "Error in applying for leave!")
        

    else:
        print(request.session.get('username'))
        facultytable = db['faculty info']
        reply = facultytable.find_one(
            {'email': request.session.get('username')})

        if reply:
            context = {
                'user': reply,
            }
            return render(request, 'leaveform.html', context)

        studenttable = db['student info']
        reply = studenttable.find_one(
            {'email': request.session.get('username')})

        if reply:
            context = {
                'user': reply,
            }
            return render(request, 'leaveform-student.html', context)

        tatble = db['ta info']
        reply = tatble.find_one({'email': request.session.get('username')})

        if reply:
            context = {
                'user': reply,
            }
            return render(request, 'leaveform.html', context)


def admin_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('enter-password')
        # check_password = request.POST.get('confirm-password')

        # if password != check_password:
        #     messages.error(request, "Passwords do not match!")
        #     return redirect(admin_page)

        role = request.POST.get('role')
        id = request.POST.get('id')
        id = int(id)
        courses = request.POST.get('courses')
        tas = request.POST.get('tas')
        faculties = request.POST.get('faculties')
        courses_list = courses.split(',')
        tas_list = tas.split(',')
        faculties_list = faculties.split(',')

        password = make_password(password)
        # if password != check_password:
        #     messages.error(request, "Passwords do not match!")
        #     return redirect('admin_page')

        if role == 'student':
            studenttable = db['student info']
            studenttable.insert_one(
                {'name': name, 'email': email, 'password': password, 'faculties': faculties_list, 'courses': courses_list, 'tas': tas_list, 'id': id, 'nol': 0})
            messages.success(request, "Student added successfully!")

        elif role == 'faculty':
            facultytable = db['faculty info']
            facultytable.insert_one(
                {'name': name, 'email': email, 'password': password, 'faculties': faculties_list, 'courses': courses_list, 'tas': tas_list, 'id': id, 'nol': 0})
            messages.success(request, "Faculty added successfully!")

        elif role == 'ta':
            tatble = db['ta info']
            tatble.insert_one(
                {'name': name, 'email': email, 'password': password, 'faculties': faculties_list, 'courses': courses_list, 'tas': tas_list, 'id': id, 'nol': 0})
            messages.success(request, "TA added successfully!")

    if request.session.get('username'):
        adminTablte = db['adminTable']
        reply = adminTablte.find_one(
            {'email': request.session.get('username')})
        if reply:
            leavetable = db['leaveTable']
            cursor1 = leavetable.find()
            nol_list = []
            a, p, r = 0, 0, 0
            for doc in cursor1:
                if doc['status'] == 'approved':
                    a = a+1
                elif doc['status'] == 'rejected':
                    r = r+1
                else:
                    p = p+1
            nol_list.append(a)
            nol_list.append(p)
            nol_list.append(r)
            nol_json = json.dumps(nol_list)

            # if reply:
            context = {
                'user': reply,
                'nol_json': nol_json
            }
            return render(request, 'admin_page.html', context)


def leave_status_approved(request):
    if request.session.get('username'):
        leaveTable = db['leaveTable']
        reply = leaveTable.find().sort('from_date', pymongo.ASCENDING)
        reply = list(reply)   # convert cursor to list
        # reason for converting cursor to list is that cursor is not iterable
        # and we need to iterate over it to change the values

        for i in reply:
            i['oid'] = str(ObjectId(i['_id']))  # convert ObjectId to string
            # so that it can be used in html

        return render(request, 'leave_status_approved.html', {'reply': reply})


def leave_status_pending(request):
    if request.session.get('username'):
        leaveTable = db['leaveTable']
        reply = leaveTable.find().sort('from_date', pymongo.ASCENDING)
        reply = list(reply)
        # studenttable = db['student info']

        for i in reply:
            i['oid'] = str(ObjectId(i['_id']))
            if i['role'] == 'student':
                studenttable = db['student info']
                reply1 = studenttable.find_one({'email': i['email']})
                i['nols'] = reply1['nol']

            elif i['role'] == 'ta':
                tatble = db['ta info']
                reply1 = tatble.find_one({'email': i['email']})
                i['nols'] = reply1['nol']

            elif i['role'] == 'faculty':
                facultytable = db['faculty info']
                reply1 = facultytable.find_one({'email': i['email']})
                i['nols'] = reply1['nol']

        return render(request, 'leave_status_pending.html', {'reply': reply})


def leave_status_rejected(request):
    if request.session.get('username'):
        leaveTable = db['leaveTable']
        reply = leaveTable.find().sort('from_date', pymongo.ASCENDING)
        reply = list(reply)

        for i in reply:
            i['oid'] = str(ObjectId(i['_id']))

        return render(request, 'leave_status_rejected.html', {'reply': reply})


def pending_to_approved(request, oid):
    if request.session.get('username'):

        # convert id to object id
        # convert string to ObjectId so that it can be used in query to find the object in db using id as a key in db collection (table)
        id = ObjectId(oid)

        # string is only needed for html to use it as a parameter in url
        leaveTable = db['leaveTable']
        reply = leaveTable.find_one({'_id': id})
        email = reply['email']

        to_date = reply['to_date']
        from_date = reply['from_date']

        date1 = datetime.strptime(to_date, "%Y-%m-%d")
        date2 = datetime.strptime(from_date, "%Y-%m-%d")

        delta = date1 - date2
        # print(delta)
        studenttable = db['student info']
        document = studenttable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) + (delta.days + 1)
            studenttable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        facultytable = db['faculty info']
        document = facultytable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) + (delta.days + 1)
            facultytable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        tatable = db['ta info']
        document = tatable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) + (delta.days + 1)
            tatable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        leaveTable = db['leaveTable']
        reply = leaveTable.find_one({'_id': id})

        # upadte status and insert leave table

        status = 'approved'
        leaveTable.update_one({'_id': id}, {  # update status of leave in leave table
            '$set': {'status': status}})

        # redirect to pending page using url
        # to pass updated reply to html page we need to use redirect instead of render

        role = reply['role']
        name = reply['name']
        id = reply['id']
        leave_type = reply['leave_type']
        from_date = reply['from_date']
        to_date = reply['to_date']
        reason = reply['reason']
        emaillist = reply['emailList']
        # print(emaillist)
        substring = str(id) + " " + "Leave got Approved"

        bodystring_to_leave_applier = "Dear " + str(role) + " " + str(name) + " " + str(id) + ",\n\nYour " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the Reason: " + str(reason) + " " + " has been approved." + "\n\nRegards,\nLeave Management System"

        bodystring_to_emaillist = str(role) + " " + str(name) + " " + str(id) + " has applied for " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the reason: " + str(reason) + " " + "has been approved." + "\n\nRegards,\nLeave Management System"

        own_email = emaillist[0]
        own_email_list = [own_email]
        send_mail(substring, bodystring_to_leave_applier,
                  'leavemanagement91@gmail.com', own_email_list)
        del emaillist[0]
        send_mail(substring, bodystring_to_emaillist,
                  'leavemanagement91@gmail.com', emaillist)

        messages.success(request, "Leave approved successfully!")
        return redirect('/leave_status_pending')


def pending_to_rejected(request, oid):
    if request.session.get('username'):

        id = ObjectId(oid)

        leaveTable = db['leaveTable']
        reply = leaveTable.find_one({'_id': id})

        status = 'rejected'
        leaveTable.update_one({'_id': id}, {
            '$set': {'status': status}})

        role = reply['role']
        name = reply['name']
        id = reply['id']
        leave_type = reply['leave_type']
        from_date = reply['from_date']
        to_date = reply['to_date']
        reason = reply['reason']
        emaillist = reply['emailList']
        # print(emaillist)
        substring = str(id) + " " + "Leave got Rejected"

        bodystring_to_leave_applier = "Dear " + str(role) + " " + str(name) + " " + str(id) + ",\n\nYour " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the reason: " + str(reason) + " " + " has been rejected." + "\n\nRegards,\nLeave Management System"

        bodystring_to_emaillist = str(role) + " " + str(name) + " " + str(id) + " has applied for " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the reason: " + str(reason) + " " + " has been rejected." + "\n\nRegards,\nLeave Management System"

        own_email = emaillist[0]
        own_email_list = [own_email]
        send_mail(substring, bodystring_to_leave_applier,
                  'leavemanagement91@gmail.com', own_email_list)
        del emaillist[0]
        send_mail(substring, bodystring_to_emaillist,
                  'leavemanagement91@gmail.com', emaillist)

        messages.success(request, "Leave rejected successfully!")
        return redirect('/leave_status_pending')


def approved_to_rejected(request, oid):
    if request.session.get('username'):

        id = ObjectId(oid)

        leaveTable = db['leaveTable']
        reply = leaveTable.find_one({'_id': id})
        email = reply['email']

        to_date = reply['to_date']
        from_date = reply['from_date']

        date1 = datetime.strptime(to_date, "%Y-%m-%d")
        date2 = datetime.strptime(from_date, "%Y-%m-%d")

        delta = date1 - date2
        studenttable = db['student info']
        document = studenttable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) - (delta.days + 1)
            studenttable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        facultytable = db['faculty info']
        document = facultytable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) - (delta.days + 1)
            facultytable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        tatable = db['ta info']
        document = tatable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) - (delta.days + 1)
            tatable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        leaveTable = db['leaveTable']
        reply = leaveTable.find_one({'_id': id})

        status = 'rejected'
        leaveTable.update_one({'_id': id}, {
            '$set': {'status': status}})

        role = reply['role']
        name = reply['name']
        id = reply['id']
        leave_type = reply['leave_type']
        from_date = reply['from_date']
        to_date = reply['to_date']
        reason = reply['reason']
        emaillist = reply['emailList']
        # print(emaillist)
        substring = str(id) + " " + "Leave got Rejected"

        bodystring_to_leave_applier = "Dear " + str(role) + " " + str(name) + " " + str(id) + ",\n\nYour " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the reason: " + str(reason) + " " + " has been rejected." + "\n\nRegards,\nLeave Management System"

        bodystring_to_emaillist = str(role) + " " + str(name) + " " + str(id) + " has applied for " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the reason: " + str(reason) + " " + " has been rejected." + "\n\nRegards,\nLeave Management System"

        own_email = emaillist[0]
        own_email_list = [own_email]
        send_mail(substring, bodystring_to_leave_applier,
                  'leavemanagement91@gmail.com', own_email_list)
        del emaillist[0]
        send_mail(substring, bodystring_to_emaillist,
                  'leavemanagement91@gmail.com', emaillist)
        messages.success(request, "Leave rejected successfully!")
        return redirect('/leave_status_approved')


def rejected_to_approved(request, oid):
    if request.session.get('username'):

        id = ObjectId(oid)

        leaveTable = db['leaveTable']
        reply = leaveTable.find_one({'_id': id})
        email = reply['email']

        to_date = reply['to_date']
        from_date = reply['from_date']

        date1 = datetime.strptime(to_date, "%Y-%m-%d")
        date2 = datetime.strptime(from_date, "%Y-%m-%d")

        delta = date1 - date2

        studenttable = db['student info']
        document = studenttable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) + (delta.days + 1)
            studenttable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        facultytable = db['faculty info']
        document = facultytable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) + (delta.days + 1)
            facultytable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        tatable = db['ta info']
        document = tatable.find_one({'email': email})

        if document:
            leaves = document['nol']
            leaves = int(leaves) + (delta.days + 1)
            tatable.update_one({'email': email}, {
                '$set': {'nol': leaves}})

        leaveTable = db['leaveTable']
        reply = leaveTable.find_one({'_id': id})

        status = 'approved'
        leaveTable.update_one({'_id': id}, {
            '$set': {'status': status}})

        role = reply['role']
        name = reply['name']
        id = reply['id']
        leave_type = reply['leave_type']
        from_date = reply['from_date']
        to_date = reply['to_date']
        reason = reply['reason']
        emaillist = reply['emailList']
        # print(emaillist)
        substring = str(id) + " " + "Leave got Approved"

        bodystring_to_leave_applier = "Dear " + str(role) + " " + str(name) + " " + str(id) + ",\n\nYour " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the reason: " + str(reason) + " " + " has been approved." + "\n\nRegards,\nLeave Management System"

        bodystring_to_emaillist = str(role) + " " + str(name) + " " + str(id) + " has applied for " + str(leave_type) + " leave from " + str(
            from_date) + " to " + str(to_date) + " for the reason: " + str(reason) + " " + " has been approved." + "\n\nRegards,\nLeave Management System"

        own_email = emaillist[0]
        own_email_list = [own_email]
        send_mail(substring, bodystring_to_leave_applier,
                  'leavemanagement91@gmail.com', own_email_list)
        del emaillist[0]
        send_mail(substring, bodystring_to_emaillist,
                  'leavemanagement91@gmail.com', emaillist)

        messages.success(request, "Leave approved successfully!")
        return redirect('/leave_status_rejected')


def approved_leave_data(request):
    if request.session.get('username'):

        leavetable = db['leaveTable']
        facultytable = db['faculty info']
        reply = facultytable.find_one(
            {'email': request.session.get('username')})

        if reply:  # if the user is a faculty

            query = {
                'status': 'approved',
                'emailList': {'$in': [request.session.get('username')]},
                '$or': [
                    {'role': 'student'},
                    {'role': 'ta'}
                ]
            }
            reply2 = list(leavetable.find(query))

            context = {
                'leave_data': reply2,
            }

            return render(request, 'approvedleave_faculty.html', context)

        tatable = db['ta info']
        reply = tatable.find_one(
            {'email': request.session.get('username')})

        if reply:  # if the user is a ta

            query = {
                'status': 'approved',
                'emailList': {'$in': [request.session.get('username')]},
                'role': 'student'
            }
            reply3 = list(leavetable.find(query))

            context = {
                'leave_data': reply3,
            }

            # print(reply2)

            return render(request, 'approvedleave_ta.html', context)


def student_data(request):

    if request.session.get('username'):
        studenttable = db['student info']
        reply = studenttable.find()

        if reply:
            context = {
                'student_data': reply,
            }

        return render(request, 'student_data.html', context)


def faculty_data(request):
    if request.session.get('username'):
        facultytable = db['faculty info']
        reply = facultytable.find()

        if reply:
            context = {
                'faculty_data': reply,
            }

        return render(request, 'faculty_data.html', context)


def ta_data(request):
    if request.session.get('username'):
        tatable = db['ta info']
        reply = tatable.find()

        if reply:
            context = {
                'ta_data': reply,
            }

        return render(request, 'ta_data.html', context)
    
def change_pass(request):
    if request.session.get('username'):
        if request.method == 'POST':
            old_password = request.POST.get('old-pass')
            new_password = request.POST.get('enter-pass')

            facultytable = db['faculty info']
            reply = facultytable.find_one(
                {'email': request.session.get('username')})

            if reply:
                if check_password(old_password, reply['password']) == False:
                    messages.error(request, "Old Password is incorrect!")
                    return render(request, 'change_pass.html')
                else:
                    new_password = make_password(new_password)
                    facultytable.update_one({'email': reply['email']}, {
                    '$set': {'password': new_password}})
                    messages.success(request, "Password changed successfully!")
                    # return render(request, 'faculty-profile.html',{'user':reply})
                    return redirect('/profile_page')

            studenttable = db['student info']
            reply = studenttable.find_one(
                {'email': request.session.get('username')})

            if reply:
                if check_password(old_password, reply['password']) == False:
                    messages.error(request, "Old Password is incorrect!")
                    return render(request, 'change_pass.html')
                else:
                    new_password = make_password(new_password)
                    studenttable.update_one({'email': reply['email']}, {
                    '$set': {'password': new_password}})
                    messages.success(request, "Password changed successfully!")
                    # return render(request, 'student-profile.html',{'user':reply})
                    return redirect('/profile_page')

            tatble = db['ta info']
            reply = tatble.find_one({'email': request.session.get('username')})

            if reply:
                if check_password(old_password, reply['password']) == False:
                    messages.error(request, "Old Password is incorrect!")
                    return render(request, 'change_pass.html')
                else:
                    new_password = make_password(new_password)
                    tatble.update_one({'email': reply['email']}, {
                    '$set': {'password': new_password}})
                    messages.success(request, "Password changed successfully!")
                    # return render(request, 'ta-profile.html',{'user':reply})
                    return redirect('/profile_page')
            
        else:
            return render(request, 'change_pass.html')

def change_password(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        password = request.POST.get('enter-pass')

        admin = db['adminTable']
        reply = admin.find_one(
            {'email': email})

        if reply:
            password = make_password(password)
            admin.update_one({'email': reply['email']}, {
            '$set': {'password': password}})
            messages.success(request, "Password changed successfully!")
            # return render(request, 'faculty-profile.html',{'user':reply})
            return redirect('/admin_page')

        facultytable = db['faculty info']
        reply = facultytable.find_one(
                {'email': email})
        
        if reply:
            password = make_password(password)
            facultytable.update_one({'email': reply['email']}, {
            '$set': {'password': password}})
            messages.success(request, "Password changed successfully!")
            # return render(request, 'faculty-profile.html',{'user':reply})
            return redirect('/admin_page')

        studenttable = db['student info']
        reply = studenttable.find_one(
                {'email': email})
        
        if reply:
            password = make_password(password)
            studenttable.update_one({'email': reply['email']}, {
            '$set': {'password': password}})
            messages.success(request, "Password changed successfully!")
            # return render(request, 'faculty-profile.html',{'user':reply})
            return redirect('/admin_page')


        tatble = db['ta info']
        reply = tatble.find_one({'email': email})

        if reply:
            password = make_password(password)
            tatble.update_one({'email': reply['email']}, {
            '$set': {'password': password}})
            messages.success(request, "Password changed successfully!")
            # return render(request, 'faculty-profile.html',{'user':reply})
            return redirect('/admin_page')
        
        return render(request,'change_password.html')

    else:
        return render(request,'change_password.html')



