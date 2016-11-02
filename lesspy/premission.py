from django.contrib.auth.models import Permission, Group

add_lib = Permission.objects.get(codename='add_library')
edit_lib = Permission.objects.get(codename='change_library')
del_lib = Permission.objects.get(codename='delete_library')

add_func = Permission.objects.get(codename='add_function')
edit_func = Permission.objects.get(codename='change_function')
del_func = Permission.objects.get(codename='delete_function')

add_topic = Permission.objects.get(codename='add_topic')
edit_topic = Permission.objects.get(codename='change_topic')
del_topic = Permission.objects.get(codename='delete_topic')

add_skill = Permission.objects.get(codename='add_skill')
edit_skill = Permission.objects.get(codename='change_skill')
del_skill = Permission.objects.get(codename='delete_skill')


lib_editor = Group.objects.create(name='lib_editor')
lib_editor.permissions = [
    add_lib, edit_lib, del_lib, add_func, edit_func, del_func]

topic_editor = Group.objects.create(name='topic_editor')
topic_editor.permissions = [
    add_topic, edit_topic, del_topic, add_skill, edit_skill, del_skill]
