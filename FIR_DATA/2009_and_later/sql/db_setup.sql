CREATE TABLE expense_categories (
    variable_name CHAR(20) PRIMARY KEY,
    schedule INT,
    line INT,
    column INT,
    column_description VARCHAR(100),
    variable_line_description VARCHAR(100)
);

CREATE TABLE municipalities (
    mun_id INT PRIMARY KEY,
    region_code INT,
    sgc_code INT,
    lt1no INT,
    lt1type INT,
    ltrevno INT,
    sgc_cd INT,
    mun_name CHAR(255),
    mun_tier CHAR(10),
    region CHAR(25),
    website CHAR(255)
);

CREATE TABLE expense_data (
    variable_name CHAR(20),
    mun_id INT,
    year INT,
    amount INT,
    PRIMARY KEY (variable_name, mun_id, year),
    FOREIGN KEY (variable_name) REFERENCES expense_categories(variable_name),
    FOREIGN KEY (mun_id) REFERENCES municipalities(mun_id)
);

CREATE TABLE budget_categories (
    cat_code CHAR(20) PRIMARY KEY,
    cat_name CHAR(50),
    cat_type CHAR(1),
    CHECK (cat_type IN ('R', 'E', 'S', 'O'))
);

CREATE TABLE budget_expense_links (
    parent_code CHAR(20),
    child_code CHAR(20),
    parent_table CHAR(20),
    child_table CHAR(20),
    PRIMARY KEY (parent_code, child_code)
);
