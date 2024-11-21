from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

books = Blueprint('books', __name__)

# Route to display and add books
@books.route('/book', methods=['GET', 'POST'])
def book_list():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new book
    if request.method == 'POST':
        book_name = request.form['book_name']
        page_count = request.form['page_count']
        author_id = request.form['author_id']

        # Insert the new book into the database
        cursor.execute('INSERT INTO books (book_name, page_count, author_id) VALUES (%s, %s, %s)', (book_name, page_count, author_id))
        db.commit()

        flash('New book added successfully!', 'success')
        return redirect(url_for('books.book_list'))

    # Handle GET request to display all books
    cursor.execute('SELECT * FROM books')
    all_books = cursor.fetchall()
    return render_template('books.html', all_books=all_books)

# Route to update a book
@books.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the book's details
        book_name = request.form['book_name']
        page_count = request.form['page_count']
        author_id = request.form['author_id']

        cursor.execute('UPDATE books SET book_name = %s, page_count = %s, author_id = %s WHERE book_id = %s', (book_name, page_count, author_id, book_id))
        db.commit()

        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.book_list'))

    # GET method: fetch book's current data for pre-populating the form
    cursor.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
    current_book = cursor.fetchone()
    return render_template('update_book.html', current_book=current_book)

# Route to delete a book
@books.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the book
    cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
    db.commit()

    flash('Book deleted successfully!', 'danger')
    return redirect(url_for('books.book_list'))

