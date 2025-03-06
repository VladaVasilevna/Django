from django.urls import path
from .views import ClientCreateView, ClientListView, ClientDeleteView, \
    MessageCreateView, MessageListView, MessageUpdateView, MessageDeleteView, \
    MailingCreateView, MailingListView, MailingUpdateView, MailingDeleteView, send_mailing, index, ClientEditView, \
    ClientSaveView, ClientCancelView

app_name = 'mailing'

urlpatterns = [
    path('', index, name='index'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/<int:pk>/edit/', ClientEditView.as_view(), name='client_edit'),
    path('clients/<int:pk>/save/', ClientSaveView.as_view(), name='client_save'),
    path('clients/<int:pk>/cancel/', ClientCancelView.as_view(), name='client_cancel'),



    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/send/', send_mailing, name='send_mailing'),
]
