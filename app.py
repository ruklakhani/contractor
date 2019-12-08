from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/ClownStore')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

clowns = db.clowns

@app.route('/')
def clowns_index():
    ''' home page - lists all of the clown product options '''
    return render_template('clowns_index.html', clowns=clowns.find())


@app.route('/clowns/<clown_id>')
def clowns_show(clown_id):
    ''' display info for one individual product '''
    clown = clowns.find_one({'_id': ObjectId(clown_id)})
    return render_template('clowns_show.html', clown=clown)


@app.route('/clowns/new')
def clowns_new():
    ''' form to create a product listing '''
    return render_template('clowns_new.html', clown={}, title='Add a Clown Product!')


@app.route('/clowns', methods=['POST'])
def clowns_submit():
    ''' add new product to the database and redirect to that product's page '''
    clown = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'image': request.form.get('image')
    }
    clown_id = clowns.insert_one(clown).inserted_id
    return redirect(url_for('clowns_show', clown_id=clown_id))


@app.route('/clowns/<clown_id>/edit')
def plans_edit(clown_id):
    ''' form to edit a product's listing '''
    clown = clowns.find_one({'_id': ObjectId(clown_id)})
    return render_template('clowns_edit.html', clown=clown, title='Edit Listing')


@app.route('/clowns/<clown_id>', methods=['POST'])
def clowns_update(clown_id):
    ''' add updated info of a product to the database and redirect to that product's page '''
    updated_clown = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'image': request.form.get('image')
    }
    clowns.update_one(
        {'_id': ObjectId(clown_id)},
        {'$set': updated_clown})
    return redirect(url_for('clowns_show', clown_id=clown_id))


@app.route('/clowns/<clown_id>/delete', methods=['POST'])
def clowns_delete(clown_id):
    ''' delete a product from the database, redirect to the home page '''
    clowns.delete_one({'_id': ObjectId(clown_id)})
    return redirect(url_for('clowns_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))