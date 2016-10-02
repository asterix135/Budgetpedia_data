create table expense_categories (
    variable_name text primary key,
    schedule integer,
    line integer
    column integer,
    column_description text,
    variable_line_description text
);

create table expense_data (
    variable_name text,
    mun_id integer,
    year integer,
    amount integer,
    foreign key (variable_name) references expense_categories(variable_name)
);
