#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="xgousset",
            password="mdp",
            database="BDD_xgousset",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/vetements/show')
def show_vetements():
    mycursor = get_db().cursor()
    sql = '''SELECT Vetement_id, En_stock, Offert_collecte, Poids, Vente.Date_vente, Categorie.Nom_categorie, Collecte.Date_collecte
             FROM Vetements
             JOIN Vente ON Vetements.Vente_id = Vente.Vente_id
             JOIN Categorie ON Vetements.Categorie_ID = Categorie.Categorie_ID
             JOIN Collecte ON Vetements.Collecte_id = Collecte.Collecte_id'''
    mycursor.execute(sql)
    vetements = mycursor.fetchall()
    return render_template('vetements/show_vetements.html', vetements=vetements)

@app.route('/vetements/add', methods=['GET'])
def add_vetements():
    mycursor1 = get_db().cursor()
    sql = ''' SELECT * FROM vetements'''
    mycursor1.execute(sql)
    vetements = mycursor1.fetchall()
    mycursor2 = get_db().cursor()
    sql = ''' SELECT * FROM categorie'''
    mycursor2.execute(sql)
    categorie = mycursor2.fetchall()
    mycursor3 = get_db().cursor()
    sql = ''' SELECT * FROM collecte'''
    mycursor3.execute(sql)
    collecte = mycursor3.fetchall()
    return render_template('vetements/add_vetements.html', vetements=vetements, collecte=collecte, categorie=categorie)

@app.route('/vetements/add', methods=['POST'])
def valid_add_vetement():
    mycursor = get_db().cursor()
    offert = request.form.get('offert', '')
    poids = request.form.get('poids', '')
    categorie = request.form.get('Categorie_ID', '')
    collecte = request.form.get('Collecte_id', '')
    tuple_insert = ('oui', offert, poids, 1, categorie, collecte)
    sql = '''INSERT INTO Vetements(en_stock,Offert_collecte,Poids,Vente_id,Categorie_ID, Collecte_id) VALUES (%s,%s,%s,%s,%s,%s)'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'vetement ajouté, offert:', offert, ' - poids:', poids, ' - categorie:', categorie, ' - collecte:', collecte)
    message = u'vetement ajouté,  offert:' + offert + ' - poids:' + poids + ' - categorie:' + categorie + ' - collecte:' + collecte
    flash(message, 'alert-success')
    return redirect('/vetements/show')

@app.route('/vetements/delete', methods=['GET'])
def delete_vetements():
    mycursor = get_db().cursor()
    id_vet = request.args.get('id', 0)
    print("Valeur de id_vet :", id_vet)
    tuple_del = (id_vet,)
    sql = '''DELETE FROM Vetements WHERE Vetement_id = %s;'''
    mycursor.execute(sql, tuple_del)
    get_db().commit()
    id_vet = request.args.get('id', 0)
    message = u'un vetement supprimé, id : ' + id_vet
    flash(message, 'alert-warning')
    return redirect('/vetements/show')


@app.route('/vetements/edit', methods=['GET'])
def edit_vetement():
    id = request.args.get('id', '')
    id = int(id)
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM Vetements
             JOIN Categorie ON Vetements.Categorie_ID = Categorie.Categorie_ID
             JOIN Collecte ON Vetements.Collecte_id = Collecte.Collecte_id
             JOIN Vente ON Vetements.Vente_id = Vente.Vente_id
             WHERE Vetements.Vetement_id = %s'''
    mycursor.execute(sql, (id,))
    vetement = mycursor.fetchone()

    # Assurez-vous que get_db().cursor() retourne un curseur
    cursor = get_db().cursor()

    cursor.execute('''SELECT * FROM categorie''')
    categorie = cursor.fetchall()

    cursor.execute('''SELECT * FROM collecte''')
    collecte = cursor.fetchall()

    cursor.execute('''SELECT * FROM vente''')
    ventes = cursor.fetchall()

    return render_template('vetements/edit_vetement.html', vetement=vetement, categorie=categorie, collecte=collecte,
                           ventes=ventes)


@app.route('/vetements/edit', methods=['POST'])
def valid_edit_vetement():
    vetement_id = request.form.get('vetement_id', '')
    stock = request.form.get('stock', '')
    offert = request.form.get('offert', '')
    poids = request.form.get('poids', '')
    vente = request.form.get('vente', '')
    categorie = request.form.get('categorie', '')
    collecte = request.form.get('collecte', '')

    mycursor = get_db().cursor()
    sql = '''UPDATE Vetements
             SET En_stock=%s, Offert_collecte=%s, Poids=%s, Vente_id=%s, Categorie_ID=%s, Collecte_id=%s
             WHERE Vetement_id=%s'''
    mycursor.execute(sql, (stock, offert, poids, vente, categorie, collecte, vetement_id))
    get_db().commit()

    message = u'vetement modifié, - stock:' + stock + ' - offert:' + offert + ' - poids:' + poids + ' - vente:' + vente + ' - categorie:' + categorie + ' - collecte:' + collecte
    flash(message, 'alert-success')
    return redirect('/vetements/show')



@app.route('/vetements/etat')
def vetement_etat():
    mycursor = get_db().cursor()

    # Récupérer le nombre total de vêtements
    mycursor.execute('''SELECT COUNT(*) FROM Vetements''')
    total_vetements = mycursor.fetchone()
    total_vetements = total_vetements['COUNT(*)'] if total_vetements is not None else 0

    # Récupérer le nombre de vêtements par catégorie
    mycursor.execute('''SELECT Categorie.Categorie_ID, 
                               COUNT(*) AS count_items, 
                               SUM(Categorie.Prix * Vetements.Poids / 1000) AS valeur_totale_categorie 
                        FROM Vetements 
                        JOIN Categorie ON Vetements.Categorie_ID = Categorie.Categorie_ID 
                        GROUP BY Categorie.Categorie_ID''')
    vetements_par_categorie = mycursor.fetchall()

    # Récupérer le nom de la catégorie pour chaque résultat
    categories = {}
    for row in vetements_par_categorie:
        categorie_id = row['Categorie_ID']
        mycursor.execute('''SELECT Nom_categorie FROM Categorie WHERE Categorie_ID = %s''', (categorie_id,))
        nom_categorie = mycursor.fetchone()['Nom_categorie']
        valeur_totale_categorie = round(row['valeur_totale_categorie'], 2) if 'valeur_totale_categorie' in row else 0
        categories[nom_categorie] = {'count_items': row['count_items'], 'valeur_totale_categorie': valeur_totale_categorie}

    return render_template('vetements/etat_vetements.html', total_vetements=total_vetements, categories=categories)


if __name__ == '__main__':
    app.run(debug=True)
