-- Active: 1682683224031@@127.0.0.1@3306@diplomatiki11
CREATE TABLE Distributor (
    id_distributor INT AUTO_INCREMENT ,
    name_distributor TEXT, 
    Acceptance_Rate FLOAT,

    PRIMARY KEY (id_distributor)
);

CREATE TABLE Shift (
   date_shift DATE,
   ID_distributor_shift INT,
   acceptance_rate FLOAT(9),
   active BOOLEAN,
   hours_expected FLOAT(20),
   hours_worked FLOAT(20),
   Sinepeia BOOLEAN,
   Total_aitimata_per_shift INT,
   time_starts TIME,
   time_ends TIME,
   PRIMARY KEY (date_shift, ID_distributor_shift),
   FOREIGN KEY(ID_distributor_shift) REFERENCES Distributor(id_distributor)
);
CREATE TABLE Aitima (
    id_aitimatos INT AUTO_INCREMENT,
    id_distr INT,
    dmin FLOAT, 
    time_aitimatos TIME,
    date_aitimatos DATE,
    latitude_store DECIMAL(10, 8),
    latitude_costomer  DECIMAL(10, 8),
    longitude_store  DECIMAL(10, 8),
    longtitude_costumer  DECIMAL(10, 8),
    expected_difference_km FLOAT(7, 2),
    real_klm FLOAT(7,2),
    accepted INT,

    PRIMARY KEY (id_aitimatos),
    FOREIGN KEY (id_distr) REFERENCES Distributor (id_distributor)
);


CREATE TABLE RatingFromStore (
 id_di INT, 
 dat_shift DATE,
 id_aitim INT,
 Rating_store TINYINT UNSIGNED NOT NULL CHECK(Rating_store BETWEEN 0 AND 5 ),
FOREIGN KEY (id_di) REFERENCES Distributor (id_distributor),
FOREIGN KEY (dat_shift) REFERENCES Shift (date_shift),
FOREIGN KEY (id_aitim) REFERENCES Aitima (id_aitimatos)
);



CREATE TABLE RatingFromCostumer (
 id_rating_costumer INT, 
 dat_shif_costumer DATE,
 id_aitimatos_costumer INT,
 criterion1 TINYINT UNSIGNED NOT NULL CHECK(criterion1 BETWEEN 0 AND 5 ),
 criterion2 TINYINT UNSIGNED NOT NULL CHECK(criterion2 BETWEEN 0 AND 5 ),
 criterion3 TINYINT UNSIGNED NOT NULL CHECK(criterion3 BETWEEN 0 AND 5 ),

FOREIGN KEY (id_rating_costumer ) REFERENCES Distributor (id_distributor),
FOREIGN KEY (dat_shif_costumer) REFERENCES Shift (date_shift),
FOREIGN KEY (id_aitimatos_costumer) REFERENCES Aitima (id_aitimatos)
);



CREATE TABLE metrics (
  distributor_id INT,
  shift DATE,
  total_rate FLOAT,
  metrics_rate FLOAT,
  accepted_requests INT,
  difference_time_startshift_accepted INT,
  difference_time_endshift_accepted INT,
  overhead INT,
  average_distance INT,
  sunepeia_enarxi FLOAT,
  sunepeia_lixi FLOAT,
  overhead_real FLOAT,
  average_distance_k FLOAT,
  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)
);

CREATE TABLE metrics_costumer(
  distributor_id INT,
  shift DATE,
  total_rate_costumer FLOAT,
  criterion1 FLOAT,
  criterion2 FLOAT,
  criterion3 FLOAT,
  criterion1_b INT,
  criterion2_b INT,
  criterion3_b INT,
  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)

);

CREATE TABLE metrics_store(
  distributor_id INT,
  shift DATE,
  total_rate_store FLOAT,
  Rating_Stores_b INT,
  Rating_stores FLOAT,

  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)

);


CREATE TABLE metrics_company(
distributor_id INT,
  shift DATE,
  total_rate_company FLOAT,
  Rate_Company_b INT,
  Rate_Company FLOAT,
 
  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)

);


CREATE TABLE RatingFromCompany (
 id_di INT, 
 dat_shift DATE,
 id_aitim INT,
Rating_company TINYINT UNSIGNED NOT NULL CHECK(Rating_company BETWEEN 0 AND 5 ),
FOREIGN KEY (id_di) REFERENCES Distributor (id_distributor),
FOREIGN KEY (dat_shift) REFERENCES Shift (date_shift),
FOREIGN KEY (id_aitim) REFERENCES Aitima (id_aitimatos)
);
