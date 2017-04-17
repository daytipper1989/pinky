from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'pinky.core.views.home', name='home'),
    url(r'^application/new/', 'pinky.core.views.newApplication', name='newApplication'),
    url(r'^application/renew/', 'pinky.core.views.renewApplication', name='renewApplication'),
    url(r'^application/pause/', 'pinky.core.views.pauseApplication', name='pauseApplication'),
    url(r'^application/all/', 'pinky.core.views.allApplication', name='allApplication'),
    url(r'^order/new/', 'pinky.core.views.newOrder', name='newOrder'),
    url(r'^order/all/', 'pinky.core.views.allOrder', name='allOrder'),
    url(r'^class/new/', 'pinky.core.views.newClass', name='newClass'),
    url(r'^classtype/new/', 'pinky.core.views.newClassType', name='newClassType'),
    url(r'^class/all/', 'pinky.core.views.allClass', name='allClass'),
    url(r'^trainer/new/', 'pinky.core.views.newTrainer', name='newTrainer'),
    url(r'^trainer/all/', 'pinky.core.views.allTrainer', name='allTrainer'),
    url(r'^general/attendance/', 'pinky.core.views.attendanceGeneral', name='attendanceGeneral'),
    url(r'^class/attendance/', 'pinky.core.views.attendanceClass', name='attendanceClass'),
    url(r'^spa/attendance/', 'pinky.core.views.attendanceSpa', name='attendanceSpa'),
    url(r'^machine/attendance/', 'pinky.core.views.attendanceMachine', name='attendanceMachine'),
    url(r'^exercise/counter/', 'pinky.core.views.counterExercise', name='counterExercise'),
    url(r'^customer/progress/', 'pinky.core.views.customerProgress', name='customerProgress'),
    url(r'^customer/data/', 'pinky.core.views.customerData', name='customerData'),
    url(r'^logout/', 'pinky.core.views.logoutView', name='logoutView'),
)
