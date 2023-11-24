DROP TABLE IF EXISTS lié_à, Benne_la_plus_proche, Est_dans_la_collecte, Provient_de,
    Vetements,Collecte, Vente, Récupération, Benne, Client, Categorie;

CREATE TABLE Categorie (
   Categorie_ID INT AUTO_INCREMENT,
   Nom_categorie VARCHAR(50),
   Prix_au_kilo DECIMAL(15,2),
   PRIMARY KEY (Categorie_ID)
);

CREATE TABLE Client (
   Client_id INT AUTO_INCREMENT,
   Nom_client VARCHAR(50),
   Prenom_client VARCHAR(50),
   Points_fidelites INT,
   PRIMARY KEY(Client_id)
);

CREATE TABLE Benne (
   Benne_id INT AUTO_INCREMENT,
   Coordonnees VARCHAR(50),
   Remplie BOOLEAN,
   Distance_avec_magasin_km DECIMAL(15,2),
   PRIMARY KEY(Benne_id)
);


CREATE TABLE Récupération(
   id_récupération INT AUTO_INCREMENT,
   Quantitée_récoltée_kg DECIMAL(15,2),
   PRIMARY KEY(id_récupération)
);

CREATE TABLE Vente (
   Vente_id INT AUTO_INCREMENT,
   Date_vente DATE,
   Client_id INT NOT NULL,
   PRIMARY KEY(Vente_id),
   FOREIGN KEY(Client_id) REFERENCES Client(Client_id)
);

CREATE TABLE Collecte (
   Collecte_id INT AUTO_INCREMENT,
   Date_collecte DATE,
   PRIMARY KEY(Collecte_id)
);

CREATE TABLE Vetements (
   Vetement_id INT AUTO_INCREMENT,
   En_stock BOOLEAN,
   Offert_collecte VARCHAR(50),
   Poids_kg DECIMAL(15,2),
   Collecte_id INT NOT NULL,
   Vente_id INT NOT NULL,
   Categorie_ID INT NOT NULL,
   PRIMARY KEY(Vetement_id),
   FOREIGN KEY(Collecte_id) REFERENCES Collecte(Collecte_id),
   FOREIGN KEY(Vente_id) REFERENCES Vente(Vente_id),
   FOREIGN KEY(Categorie_ID) REFERENCES Categorie(Categorie_ID)
);

CREATE TABLE Provient_de (
   Benne_id INT,
   Collecte_id INT,
   PRIMARY KEY(Benne_id, Collecte_id),
   FOREIGN KEY(Benne_id) REFERENCES Benne(Benne_id),
   FOREIGN KEY(Collecte_id) REFERENCES Collecte(Collecte_id)
);

CREATE TABLE Est_dans_la_collecte (
   Categorie_ID INT,
   Collecte_id INT,
   Quantite_vetement_kg DECIMAL(15,2),
   PRIMARY KEY(Categorie_ID, Collecte_id),
   FOREIGN KEY(Categorie_ID) REFERENCES Categorie(Categorie_ID),
   FOREIGN KEY(Collecte_id) REFERENCES Collecte(Collecte_id)
);

CREATE TABLE Benne_la_plus_proche (
   Benne_id INT,
   Benne_id_1 INT,
   Distance_km DECIMAL(15,2),
   PRIMARY KEY(Benne_id, Benne_id_1),
   FOREIGN KEY(Benne_id) REFERENCES Benne(Benne_id),
   FOREIGN KEY(Benne_id_1) REFERENCES Benne(Benne_id)
);

CREATE TABLE lié_à(
   Categorie_ID INT,
   id_récupération INT,
   PRIMARY KEY(Categorie_ID, id_récupération),
   FOREIGN KEY(Categorie_ID) REFERENCES Categorie(Categorie_ID),
   FOREIGN KEY(id_récupération) REFERENCES Récupération(id_récupération)
);


-- jeu de test fait grâce à ChatGPT

-- Insérer des valeurs dans la table Categorie
INSERT INTO Categorie (Nom_categorie, Prix_au_kilo) VALUES
   ('Vêtements pour hommes', 10.50),
   ('Vêtements pour femmes', 12.75),
   ('Chaussures', 15.00);

-- Insérer des valeurs dans la table Client
INSERT INTO Client (Nom_client, Prenom_client, Points_fidelites) VALUES
   ('Dupont', 'Jean', 50),
   ('Martin', 'Marie', 30),
   ('Dubois', 'Pierre', 20);

-- Insérer des valeurs dans la table Benne
INSERT INTO Benne (Coordonnees, Remplie, Distance_avec_magasin_km) VALUES
   ('45.123, -73.456', TRUE, 2.5),
   ('46.789, -74.012', FALSE, 1.8),
   ('44.567, -72.345', TRUE, 3.2);

-- Insérer des valeurs dans la table Récupération
INSERT INTO Récupération (Quantitée_récoltée_kg) VALUES
   (25.75),
   (15.30),
   (30.50);

-- Insérer des valeurs dans la table Vente
INSERT INTO Vente (Date_vente, Client_id) VALUES
   ('2023-01-15', 1),
   ('2023-02-20', 2),
   ('2023-03-10', 3);

-- Insérer des valeurs dans la table Collecte
INSERT INTO Collecte (Date_collecte) VALUES
   ('2023-01-20'),
   ('2023-02-25'),
   ('2023-03-15');

-- Insérer des valeurs dans la table Vetements
INSERT INTO Vetements (En_stock, Offert_collecte, Poids_kg, Collecte_id, Vente_id, Categorie_ID) VALUES
   (TRUE, 'Oui', 5.20, 1, 1, 1),
   (FALSE, 'Non', 8.75, 2, 2, 2),
   (TRUE, 'Oui', 3.50, 3, 3, 3);

-- Insérer des valeurs dans la table Provient_de
INSERT INTO Provient_de (Benne_id, Collecte_id) VALUES
   (1, 1),
   (2, 2),
   (3, 3);

-- Insérer des valeurs dans la table Est_dans_la_collecte
INSERT INTO Est_dans_la_collecte (Categorie_ID, Collecte_id, Quantite_vetement_kg) VALUES
   (1, 1, 15.00),
   (2, 2, 10.50),
   (3, 3, 20.25);

-- Insérer des valeurs dans la table Benne_la_plus_proche
INSERT INTO Benne_la_plus_proche (Benne_id, Benne_id_1, Distance_km) VALUES
   (1, 2, 3.0),
   (2, 3, 1.5),
   (3, 1, 2.8);

-- Insérer des valeurs dans la table lié_à
INSERT INTO lié_à (Categorie_ID, id_récupération) VALUES
   (1, 1),
   (2, 2),
   (3, 3);

-- Modifier certaines valeurs
UPDATE Client SET Points_fidelites = 40 WHERE Client_id = 1;
UPDATE Vetements SET En_stock = FALSE WHERE Vetement_id = 2;

-- Sélectionner des valeurs avec jointures
SELECT V.Vetement_id, V.Poids_kg, C.Nom_categorie, R.Quantitée_récoltée_kg
FROM Vetements V
JOIN Categorie C ON V.Categorie_ID = C.Categorie_ID
JOIN Récupération R ON V.Collecte_id = R.id_récupération;

