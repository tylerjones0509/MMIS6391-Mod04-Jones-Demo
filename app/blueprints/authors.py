from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

authors = Blueprint('authors', __name__)

# Route to display and add authors
@authors.route('/author', methods=['GET', 'POST'])
def authors_list():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new author
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Insert the new author into the database
        cursor.execute('INSERT INTO authors (first_name, last_name) VALUES (%s, %s)', (first_name, last_name))
        db.commit()

        flash('New author added successfully!', 'success')
        return redirect(url_for('authors.authors_list'))

    # Handle GET request to display all authors
    cursor.execute('SELECT * FROM authors')
    all_authors = cursor.fetchall()
    return render_template('authors.html', all_authors=all_authors)

# Route to update an author
@authors.route('/update_author/<int:author_id>', methods=['GET', 'POST'])
def update_author(author_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the author's details
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        cursor.execute('UPDATE authors SET first_name = %s, last_name = %s WHERE author_id = %s', (first_name, last_name, author_id))
        db.commit()

        flash('Author updated successfully!', 'success')
        return redirect(url_for('authors.authors_list'))

    # GET method: fetch author's current data for pre-populating the form
    cursor.execute('SELECT * FROM authors WHERE author_id = %s', (author_id,))
    current_author = cursor.fetchone()
    return render_template('update_author.html', current_author=current_author)

# Route to delete an author
@authors.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the author
    cursor.execute('DELETE FROM authors WHERE author_id = %s', (author_id,))
    db.commit()

    flash('Author deleted successfully!', 'danger')
    return redirect(url_for('authors.authors_list'))
