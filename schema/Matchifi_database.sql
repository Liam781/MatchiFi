CREATE TABLE clients (
company_id SMALLINT UNSIGNED AUTO_INCREMENT,
company_name VARCHAR(20),
company_type ENUM('sole','part'),
PRIMARY KEY(company_id)
)ENGINE=INNODB;

CREATE TABLE sectors (
sector_id SMALLINT UNSIGNED,
sector_name VARCHAR(20),
asset_turnover float(5,1),
net_pm float(5,1),
debt_to_eq float(5,1),
PRIMARY KEY(sector_id)
)ENGINE=INNODB;

CREATE TABLE client_detail (
company_id SMALLINT UNSIGNED,
sector_id SMALLINT UNSIGNED,
debt_to_eq FLOAT(3,1),
gross_pm float(5,1),
net_pm float(5,1),
return_on_assets float(5,1),
return_on_equity float(5,1),
interest_coverage INT,

FOREIGN KEY (company_id)
REFERENCES clients(company_id),

FOREIGN KEY (sector_id)
REFERENCES sectors(sector_id)
)ENGINE=INNODB;

CREATE TABLE loan_products (
    product_id SMALLINT UNSIGNED AUTO_INCREMENT,
    product_name VARCHAR(50) NOT NULL,
    min_amount DECIMAL(10, 2) NOT NULL,
    max_amount DECIMAL(10, 2) NOT NULL,
    min_term_months SMALLINT UNSIGNED NOT NULL,
    max_term_months SMALLINT UNSIGNED NOT NULL,
    typical_interest_rate FLOAT(4, 2),
    target_sector_id SMALLINT UNSIGNED, -- Optional: Link to sectors table for specific products
    required_min_credit_score INT,
    PRIMARY KEY(product_id),
    FOREIGN KEY (target_sector_id) REFERENCES sectors(sector_id) -- Link to your existing sectors table
) ENGINE=INNODB;

CREATE TABLE loan_applications (
    application_id INT UNSIGNED AUTO_INCREMENT,
    company_id SMALLINT UNSIGNED NOT NULL,
    product_id SMALLINT UNSIGNED NOT NULL,
    loan_amount DECIMAL(10, 2) NOT NULL,
    loan_term_months SMALLINT UNSIGNED NOT NULL,
    loan_status ENUM('Approved', 'Rejected') NOT NULL, -- Your target variable
    application_date DATE,
    PRIMARY KEY(application_id),
    FOREIGN KEY (company_id) REFERENCES clients(company_id),
    FOREIGN KEY (product_id) REFERENCES loan_products(product_id)
) ENGINE=INNODB;


	
