from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('mybook/', views.LoanedBooksByUserListView.as_view(), name='all-borrowed'),# CHANGE MEEE
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

]
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('bookinstances/', views.BookInstanceListView.as_view(), name='bookinstances'),
    path('bookinstance/<uuid:pk>', views.BookInstanceDetailView.as_view(), name='bookinstance-detail'),
    path('bookinstance/<uuid:pk>/update/', views.BookInstanceUpdate.as_view(), name='bookinstance-update'),
    path('bookinstance/<uuid:pk>/delete/', views.BookInstanceDelete.as_view(), name='bookinstance-delete'),
    path('bookinstance/create/', views.BookInstanceCreate.as_view(), name='bookinstance-create'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
]
