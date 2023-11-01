from django.urls import path

from .apis import (
        get_taskspace_list,
        create_taskspace,
        update_taskspace,
        delete_taskspace,
        )


urlpatterns = [
        path('list', get_taskspace_list, name='taskspace_list'),
        path('create', create_taskspace, name='taskspace_create'),
        path('update/<int:taskspace_id>', update_taskspace, name='taskspace_update'),
        path('delete/<int:taskspace_id>', delete_taskspace, name='taskspace_delete'),
        ]
