"""
Collection of functions to help establish the database
"""
import mysql.connector


# Connect to MySQL and the task database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


# Setup for the Database
#   Will erase the database if it exists
def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        f""" 
        CREATE TABLE library_patrons
        (
            account_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            account_type ENUM('STUDENT', 'PROFESSOR', 'STAFF'),
            CONSTRAINT pk_library_members PRIMARY KEY (account_id)
        );
        """
    )
    cursor.execute(
        f""" 
        CREATE TABLE books
        (
            book_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            title VARCHAR(50),
            author_fname VARCHAR(50),
            author_lname VARCHAR(50),
            publication_year YEAR,
            checked_out_to SMALLINT UNSIGNED,
            CONSTRAINT fk_check_out FOREIGN KEY (checked_out_to)
            REFERENCES library_members (account_id),
            CONSTRAINT pk_books PRIMARY KEY (book_id)
        );
        """
    )
    cursor.execute(
        f""" 
        CREATE TABLE classes
        (
            class_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            course_title VARCHAR(50),
            reference_book SMALLINT UNSIGNED,
            CONSTRAINT fk_reference_book FOREIGN KEY (reference_book)
            REFERENCES books (book_id),
            CONSTRAINT pk_classes PRIMARY KEY (class_id)
        );
        """
    )
    cursor.execute(
        f""" 
        CREATE TABLE class_members
        (
            account_id SMALLINT UNSIGNED,
            class_id SMALLINT UNSIGNED,
            CONSTRAINT fk_account_ID FOREIGN KEY (account_id)
            REFERENCES library_members (account_id),
            CONSTRAINT fk_class_ID FOREIGN KEY (class_id)
            REFERENCES classes (class_id),
            CONSTRAINT pk_class_members PRIMARY KEY (account_id, class_id)
        );
        """
    )
    cursor.close()
    conn.close()
