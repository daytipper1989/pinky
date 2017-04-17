from forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='/')
def pauseApplication(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #integerAmountForm = IntegerAmountForm(request.POST)
        #membershipSelectForm = MembershipSelectForm(request.POST)
        # check whether it's valid:
        amount = int(request.POST['days'])
        import datetime
        dt = datetime.datetime.now()
        membership = Membership.objects.get(id = int(request.POST['membership']))
        membership.pausedTime = dt
        membership.pauser = Employee.objects.get(user=request.user)
        if amount<=0 or amount>7:
            failureMessage = "Invalid amount"
            return render_to_response('pause_application.html', locals(), context_instance = RequestContext(request))
        if membership.daysPaused>0:
            failureMessage = "Limit reached. Memerbership was paused before."
            return render_to_response('pause_application.html', locals(), context_instance = RequestContext(request))
        else:
            successMessage = "Days paused successfully."
            membership.daysPaused = membership.daysPaused + amount
            membership.endedTime = membership.endedTime + datetime.timedelta(amount)
            membership.save()
            return render_to_response('pause_application.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        membershipSelectForm = MembershipSelectForm()
        integerAmountForm = IntegerAmountForm()
    return render_to_response('pause_application.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def newApplication(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        try:
            form = MembershipForm(request.POST)
            form2 = CustomerForm(request.POST)
            # check whether it's valid:
            if form.is_valid() and form2.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                customer = form2.save(commit=False)
                customer.isGymCustomer = True
                customer.save()
                import datetime
                dt = datetime.datetime.now()
                membership = form.save(commit=False)
                membership.customer = customer
                membership.price = membership.package.price
                membership.employee = Employee.objects.get(user=request.user)
                membership.endedTime = dt + datetime.timedelta(30)
                membership.save()
                successMessage = "Membership created successfully"
                return render_to_response('new_application.html', locals(), context_instance = RequestContext(request))
            else:
                failureMessage = "Information is not valid"
                return render_to_response('new_application.html', locals(), context_instance = RequestContext(request))
        except:
            failureMessage = "Internal error occured"
            #add logs here
            return render_to_response('new_application.html', locals(), context_instance = RequestContext(request))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = MembershipForm()
        form2 = CustomerForm()

    return render_to_response('new_application.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def renewApplication(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MembershipForm(request.POST)
        form2 = CustomerSearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid() and form2.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            try:
                customer = Customer.objects.get(mobile=form2.cleaned_data['mobile'])
            except:
                failureMessage = "No such customer found"
                return render_to_response('renew_application.html', locals(), context_instance = RequestContext(request))
            import datetime
            dt = datetime.datetime.now()
            membership = form.save(commit=False)
            membership.price = membership.package.price
            membership.customer = customer
            membership.employee = Employee.objects.get(user=request.user)
            membership.endedTime = dt + datetime.timedelta(30)
            membership.save()
            successMessage = "Membership renewed successfully"
            return render_to_response('renew_application.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MembershipForm()
        form2 = CustomerSearchForm()
    return render_to_response('renew_application.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def allApplication(request):
    # if this is a POST request we need to process the form data
    import datetime
    dt = datetime.datetime.now()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        customerSearchForm = CustomerSelectForm(request.POST)
        employeeSelectForm = EmployeeSelectForm(request.POST)
        packageSelectForm = PackageSelectForm(request.POST)
        membershipPriceFilterForm = PriceFilterForm(request.POST)
        # check whether it's valid:
        if customerSearchForm.is_valid() and employeeSelectForm.is_valid() and packageSelectForm.is_valid() and membershipPriceFilterForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #membership = form.save(commit=False)
            #membership.price = membership.package.price
            #membership.save()
            filterList = []
            try:
                mobile = customerSearchForm.cleaned_data['mobile']
                if mobile:
                    customer = Customer.objects.get(mobile = mobile)
                    filterList.append(('customer' , customer))
            except:
                pass
            try:
                employee = employeeSelectForm.cleaned_data['employee']
                if employee:
                    filterList.append(('employee' , employee))
            except:
                pass
            try:
                package = packageSelectForm.cleaned_data['package']
                if package:
                    filterList.append(('package' , package))
            except:
                pass
            try:
                minimum = membershipPriceFilterForm.cleaned_data['minimum']
                if minimum:
                    filterList.append(('price__gte' , minimum ))
            except:
                pass
            try:
                maximum = membershipPriceFilterForm.cleaned_data['maximum']
                if maximum:
                    filterList.append(('price__lte', maximum ))
            except:
                pass
            if filterList:
                membershipList = Membership.objects.filter(**dict(filterList))
            else:
                membershipList = []
            return render_to_response('all_application.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        customerSearchForm = CustomerSelectForm()
        employeeSelectForm = EmployeeSelectForm()
        packageSelectForm = PackageSelectForm()
        membershipPriceFilterForm = PriceFilterForm()
        membershipList = Membership.objects.all()
    return render_to_response('all_application.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def newOrder(request):
    # if this is a POST request we need to process the form data
    productList = Product.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form2 = CustomerSelectForm(request.POST)
        locationSelectForm = LocationSelectForm(request.POST)
        addressForm = AddressForm(request.POST)
        shipmentSelectForm = ShipmentSelectForm(request.POST)
        governmentSelectForm = GovernmentSelectForm(request.POST)
        # check whether it's valid:
        if form2.is_valid() and locationSelectForm.is_valid() and shipmentSelectForm.is_valid() and governmentSelectForm.is_valid() and addressForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            product = request.POST.getlist('product')
            quantity = request.POST.getlist('quantity')
            for each in product:
                if not each:
                    failureMessage = "Please enter product"
                    return render_to_response('new_order.html', locals(), context_instance = RequestContext(request))
            for each in quantity:
                if not each:
                    failureMessage = "Please enter quantity"
                    return render_to_response('new_order.html', locals(), context_instance = RequestContext(request))
            order = Order()
            mobile = form2.cleaned_data['mobile']
            if mobile:
                try:
                    order.customer = Customer.objects.get(mobile = mobile)
                except:
                    failureMessage = "No customer found with specified mobile number"
                    return render_to_response('new_order.html', locals(), context_instance = RequestContext(request))
            order.employee = Employee.objects.get(user=request.user)
            order.location = locationSelectForm.cleaned_data['location']
            order.address = addressForm.cleaned_data['address']
            order.shipment = shipmentSelectForm.cleaned_data['shipment']
            order.government = governmentSelectForm.cleaned_data['government']
            order.price=0
            order.save()
            i=0
            while i < len(product):
                orderDetail = OrderDetail()
                orderDetail.product = Product.objects.get(id=int(product[i]))
                orderDetail.quantity = int(quantity[i])
                orderDetail.price = int(quantity[i]) * float(orderDetail.product.price)
                orderDetail.order=order
                orderDetail.save()
                order.price += orderDetail.price
                i+=1
            order.save()
            successMessage = "Order submitted successfully"
            return render_to_response('new_order.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        form2 = CustomerSelectForm()
        locationSelectForm = LocationSelectForm(req=request)
        addressForm = AddressForm()
        shipmentSelectForm = ShipmentSelectForm()
        governmentSelectForm = GovernmentSelectForm()
    return render_to_response('new_order.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def newClass(request):
    trainerList = Trainer.objects.all()
    classTypeList = ClassType.objects.all()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClassForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            import datetime
            classs = form.save(commit=False)
            if classs.startingTime<datetime.datetime.now():
                failureMessage = "Please Enter a starting time in the future"
                return render_to_response('new_class.html', locals(), context_instance = RequestContext(request))
            classs.endingTime = classs.startingTime + datetime.timedelta(hours=1)
            classs.amountPaid = classs.trainer.salary
            classs.save()
            successMessage = "Class created successfully."
            return render_to_response('new_class.html', locals(), context_instance = RequestContext(request))
        else:
            failureMessage = "An error occured."
            return render_to_response('new_class.html', locals(), context_instance = RequestContext(request))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClassForm()

    return render_to_response('new_class.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def attendanceClass(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClassSelectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #classs = form.save(commit=False)
            #classs.save()
            classs = form.cleaned_data['classs']
            attendeesCount = len(classs.attendees.all())
            mobiles = request.POST.getlist('mobile')
            count = len(mobiles)
            if count == 0:
                failureMessage = "Please enter a mobile number for customer."
                return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))
            if attendeesCount + count>15:
                failureMessage = "Could not add " + str(count) + " customers. Already " + str(attendeesCount) + " reserved."
                return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))
            successMessage = None
            failureMessage = None
            for mobile in mobiles:
                try:
                    customer = Customer.objects.get(mobile=mobile)
                    if customer in classs.attendees.all():
                        failureMessage = "Customer already reserved in this class."
                        return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))
                    classesCount = 0
                    import datetime
                    dt = datetime.datetime.now()
                    membershipList = Membership.objects.filter(customer = customer, endedTime__gte = dt).order_by("createdTime")
                    if len(membershipList) <= 0:
                        failureMessage = "No active membership found for " + mobile + "\n"
                        return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))
                    for membership in membershipList:
                        package = membership.package
                        packageDetailList = PackageDetail.objects.filter(package = package , service = Service.objects.get(name = "Class"))
                        for packageDetail in packageDetailList:
                            classesCount += packageDetail.maximumNumberAllowed
                    if classesCount <= 0:
                        failureMessage = "Customer has no membership to enter classes " + str( classesCount) + "\n"
                        return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))
                    else:
                        attendedClasses = Class.objects.filter(attendees__in=[customer],startingTime__gte=membershipList[0].createdTime)
                    if len(attendedClasses)>= classesCount:
                        failureMessage = "Classes limit reached for " + mobile + ". Customer needs a new membership."
                        return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))
                    #successMessage = str(attendedClasses)
                    classs.attendees.add(customer)
                    if not successMessage:
                        successMessage = ""
                    successMessage += str(mobile) + " added\n"
                except:
                    if not failureMessage:
                        failureMessage = ""
                    failureMessage += str(mobile) + " is not associated to a customer\n"
            return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClassSelectForm()

    return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def attendanceSpa(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = ClassSelectForm(request.POST)
        # check whether it's valid:
        if True:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #classs = form.save(commit=False)
            #classs.save()
            #classs = form.cleaned_data['classs']
            #attendeesCount = len(classs.attendees.all())
            mobiles = request.POST.getlist('mobile')
            count = len(mobiles)
            if count == 0:
                failureMessage = "Please enter a mobile number for customer."
                return render_to_response('attendance_spa.html', locals(), context_instance = RequestContext(request))
            successMessage = None
            failureMessage = None
            for mobile in mobiles:
                try:
                    customer = Customer.objects.get(mobile=mobile)
                    classesCount = 0
                    import datetime
                    dt = datetime.datetime.now()
                    membershipList = Membership.objects.filter(customer = customer, endedTime__gte = dt).order_by("createdTime")
                    if len(membershipList) <= 0:
                        failureMessage = "No active membership found for " + mobile + "\n"
                        return render_to_response('attendance_spa.html', locals(), context_instance = RequestContext(request))
                    for membership in membershipList:
                        package = membership.package
                        packageDetailList = PackageDetail.objects.filter(package = package , service = Service.objects.get(name = "Spa"))
                        for packageDetail in packageDetailList:
                            classesCount += packageDetail.maximumNumberAllowed
                    if classesCount <= 0:
                        failureMessage = "Customer has no membership to enter spa " + str( classesCount) + "\n"
                        return render_to_response('attendance_class.html', locals(), context_instance = RequestContext(request))
                    else:
                        attendedClasses = SpaUsage.objects.filter(attendees__in=[customer],startingTime__gte=membershipList[0].createdTime)
                    if len(attendedClasses)>= classesCount:
                        failureMessage = "Spa limit reached for " + mobile + ". Customer needs a new membership."
                        return render_to_response('attendance_spa.html', locals(), context_instance = RequestContext(request))
                    #successMessage = str(attendedClasses)
                    classs = SpaUsage(startingTime=dt,endingTime=dt)
                    classs.save()
                    classs.attendees.add(customer)
                    if not successMessage:
                        successMessage = ""
                    successMessage += str(mobile) + " added\n"
                except:
                    if not failureMessage:
                        failureMessage = ""
                    failureMessage += str(mobile) + " is not associated to a customer\n"
            return render_to_response('attendance_spa.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        pass

    return render_to_response('attendance_spa.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def attendanceMachine(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = ClassSelectForm(request.POST)
        # check whether it's valid:
        if True:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #classs = form.save(commit=False)
            #classs.save()
            #classs = form.cleaned_data['classs']
            #attendeesCount = len(classs.attendees.all())
            mobiles = request.POST.getlist('mobile')
            count = len(mobiles)
            if count == 0:
                failureMessage = "Please enter a mobile number for customer."
                return render_to_response('attendance_machine.html', locals(), context_instance = RequestContext(request))
            successMessage = None
            failureMessage = None
            for mobile in mobiles:
                try:
                    customer = Customer.objects.get(mobile=mobile)
                    classesCount = 0
                    import datetime
                    dt = datetime.datetime.now()
                    membershipList = Membership.objects.filter(customer = customer, endedTime__gte = dt).order_by("createdTime")
                    if len(membershipList) <= 0:
                        failureMessage = "No active membership found for " + mobile + "\n"
                        return render_to_response('attendance_machine.html', locals(), context_instance = RequestContext(request))
                    for membership in membershipList:
                        package = membership.package
                        packageDetailList = PackageDetail.objects.filter(package = package , service = Service.objects.get(name = "Machine"))
                        for packageDetail in packageDetailList:
                            classesCount += packageDetail.maximumNumberAllowed
                    if classesCount <= 0:
                        failureMessage = "Customer has no membership to enter machines " + str( classesCount) + "\n"
                        return render_to_response('attendance_machine.html', locals(), context_instance = RequestContext(request))
                    else:
                        attendedClasses = MachinesUsage.objects.filter(attendees__in=[customer],startingTime__gte=membershipList[0].createdTime)
                    if len(attendedClasses)>= classesCount:
                        failureMessage = "Machines limit reached for " + mobile + ". Customer needs a new membership."
                        return render_to_response('attendance_machine.html', locals(), context_instance = RequestContext(request))
                    #successMessage = str(attendedClasses)
                    classs = MachinesUsage(startingTime=dt,endingTime=dt)
                    classs.save()
                    classs.attendees.add(customer)
                    if not successMessage:
                        successMessage = ""
                    successMessage += str(mobile) + " added\n"
                except:
                    if not failureMessage:
                        failureMessage = ""
                    failureMessage += str(mobile) + " is not associated to a customer\n"
            return render_to_response('attendance_machine.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        pass

    return render_to_response('attendance_machine.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def newClassType(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClassTypeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            classType = form.save(commit=False)
            classType.save()
            successMessage = "Class type added successfully"
            return render_to_response('new_class_type.html', locals(), context_instance = RequestContext(request))
        else:
            failureMessage = "An error occured"
            return render_to_response('new_class_type.html', locals(), context_instance = RequestContext(request))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClassTypeForm()

    return render_to_response('new_class_type.html', locals(), context_instance = RequestContext(request))


@login_required(login_url='/')
def newTrainer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TrainerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            trainer = form.save(commit=False)
            trainer.save()
            form.save_m2m()
            successMessage="Trainer created successfully"
            return render_to_response('new_trainer.html', locals(), context_instance = RequestContext(request))
        else:
            failureMessage="An error occured"
            return render_to_response('new_trainer.html', locals(), context_instance = RequestContext(request))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainerForm()

    return render_to_response('new_trainer.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def allOrder(request):
    # if this is a POST request we need to process the form data
    orderList = Order.objects.all()
    orderDetailList = OrderDetail.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        customerSearchForm = CustomerSearchForm(request.POST)
        employeeSelectForm = EmployeeSelectForm(request.POST)
        orderPriceFilterForm = PriceFilterForm(request.POST)
        # check whether it's valid:
        if customerSearchForm.is_valid() and employeeSelectForm.is_valid() and orderPriceFilterForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #membership = form.save(commit=False)
            #membership.price = membership.package.price
            #membership.save()
            return render_to_response('all_order.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        customerSearchForm = CustomerSearchForm()
        employeeSelectForm = EmployeeSelectForm()
        orderPriceFilterForm = PriceFilterForm()
    return render_to_response('all_order.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def allClass(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = MembershipRenewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            membership = form.save(commit=False)
            membership.price = membership.package.price
            membership.save()
            return render_to_response('all_order.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        import datetime
        classList = Class.objects.filter(startingTime__gte=datetime.datetime.now()).order_by('startingTime')
        trainerList = []
        for each in classList:
            if not each.trainer in trainerList:
                trainerList.append(each.trainer)
    return render_to_response('all_class.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def allTrainer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        skillSelectForm = SkillSelectForm(request.POST)
        trainerSelectForm = TrainerSelectForm(request.POST)
        # check whether it's valid:
        if skillSelectForm.is_valid() and trainerSelectForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #membership = form.save(commit=False)
            #membership.price = membership.package.price
            #membership.save()
            filterList = []
            try:
                skill = skillSelectForm.cleaned_data['skill']
                if skill:
                    filterList.append(('skill__in' , [skill]))
            except:
                pass
            try:
                trainer = trainerSelectForm.cleaned_data['trainer']
                if trainer:
                    filterList.append(('id' , trainer.id))
            except:
                pass
            if filterList:
                trainerList = Trainer.objects.filter(**dict(filterList))
            else:
                trainerList = Trainer.objects.all()
            return render_to_response('all_trainer.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        skillSelectForm = SkillSelectForm()
        trainerSelectForm = TrainerSelectForm()
        trainerList = Trainer.objects.all()
    return render_to_response('all_trainer.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def counterExercise(request):
    # if this is a POST request we need to process the form data
    exerciseDetails = ExerciseDetail.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        customerSearchForm = CustomerSearchForm(request.POST)
        exerciseSelectForm = ExerciseSelectForm(request.POST)
        integerAmountForm = IntegerAmountForm(request.POST)
        # check whether it's valid:
        if customerSearchForm.is_valid() and exerciseSelectForm.is_valid() and integerAmountForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #membership = form.save(commit=False)
            #membership.price = membership.package.price
            #membership.save()
            amountDone = integerAmountForm.cleaned_data['amount']
            exercise = exerciseSelectForm.cleaned_data['exercise']
            customer = Customer.objects.get(mobile=customerSearchForm.cleaned_data['mobile'])
            import datetime
            customerDetail, created = CustomerDetail.objects.get_or_create(detailDate = datetime.date.today(),customer = customer)
            exerciseDetail = ExerciseDetail(customerDetail=customerDetail,exercise=exercise,amountDone=amountDone)
            exerciseDetail.save()
            return render_to_response('counter_exercise.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        customerSearchForm = CustomerSearchForm()
        exerciseSelectForm = ExerciseSelectForm()
        integerAmountForm = IntegerAmountForm()
    return render_to_response('counter_exercise.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def customerProgress(request):
    # if this is a POST request we need to process the form data
    attributeDetails = AttributeDetail.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        customerSearchForm = CustomerSearchForm(request.POST)
        customerDetailAttributeSelectForm = CustomerDetailAttributeSelectForm(request.POST)
        integerAmountForm = IntegerAmountForm(request.POST)
        # check whether it's valid:
        if customerSearchForm.is_valid() and customerDetailAttributeSelectForm.is_valid() and integerAmountForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #membership = form.save(commit=False)
            #membership.price = membership.package.price
            #membership.save()
            amount = integerAmountForm.cleaned_data['amount']
            customerDetailAttribute = customerDetailAttributeSelectForm.cleaned_data['customerDetailAttribute']
            customer = Customer.objects.get(mobile=customerSearchForm.cleaned_data['mobile'])
            import datetime
            customerDetail, created = CustomerDetail.objects.get_or_create(detailDate = datetime.date.today(),customer = customer)
            attributeDetail = AttributeDetail(customerDetail=customerDetail,customerDetailAttribute=customerDetailAttribute,amountDone=amount)
            attributeDetail.save()
            return render_to_response('progress_customer.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        customerSearchForm = CustomerSearchForm()
        customerDetailAttributeSelectForm = CustomerDetailAttributeSelectForm()
        integerAmountForm = IntegerAmountForm()
    return render_to_response('progress_customer.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def customerData(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        customerSearchForm = CustomerSearchForm(request.POST)
        # check whether it's valid:
        if customerSearchForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #membership = form.save(commit=False)
            #membership.price = membership.package.price
            #membership.save()
            try:
                customer = Customer.objects.get(mobile=customerSearchForm.cleaned_data['mobile'])
            except:
                failureMessage = "Customer not found"
                return render_to_response('data_customer.html', locals(), context_instance = RequestContext(request))
            customerDetailList = CustomerDetail.objects.filter(customer = customer)
            #displayList.sort(key=lambda x: x.startingTime, reverse=False)
            return render_to_response('data_customer.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        displayList = []
        customerSearchForm = CustomerSearchForm()
    return render_to_response('data_customer.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def attendanceGeneral(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        customerSearchForm = CustomerSearchForm(request.POST)
        # check whether it's valid:
        if customerSearchForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #membership = form.save(commit=False)
            #membership.price = membership.package.price
            #membership.save()
            try:
                customer = Customer.objects.get(mobile=customerSearchForm.cleaned_data['mobile'])
            except:
                failureMessage = "Customer not found"
                return render_to_response('attendance_general.html', locals(), context_instance = RequestContext(request))
            displayList = list(Class.objects.filter(attendees__in=[customer]))
            displayList = displayList + list(SpaUsage.objects.filter(attendees__in=[customer]))
            displayList = displayList + list(MachinesUsage.objects.filter(attendees__in=[customer]))
            displayList.sort(key=lambda x: x.startingTime, reverse=False)
            return render_to_response('attendance_general.html', locals(), context_instance = RequestContext(request))

    # if a GET (or any other method) we'll create a blank form
    else:
        displayList = []
        customerSearchForm = CustomerSearchForm()
    return render_to_response('attendance_general.html', locals(), context_instance = RequestContext(request))

def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render_to_response('home.html', locals(), context_instance = RequestContext(request))
                else:
                    failureMessage = "Login Authentication Failure"
                    return render_to_response('home.html', locals(), context_instance = RequestContext(request))
            else:
                failureMessage = "Login Failure"
                return render_to_response('home.html', locals(), context_instance = RequestContext(request))
        else:
            failureMessage = "Login Failure"
            return render_to_response('home.html', locals(), context_instance = RequestContext(request))
    else:
        form = LoginForm()
        return render_to_response('home.html', locals(), context_instance = RequestContext(request))

@login_required(login_url='/')
def logoutView(request):
    logout(request)
    form = LoginForm()
    return render_to_response('home.html', locals(), context_instance = RequestContext(request))
