import psycopg2
import csv
from typing import List, Tuple, Optional, Dict, Any

class PhoneBook:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="lab11",
            user="postgres",
            password="abilkosha",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()
        self.create_tables()
        self.create_functions()

    def create_tables(self):
        """Create the phonebook table if it doesn't exist"""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                phone VARCHAR(20) NOT NULL UNIQUE
            )
        """)
        self.conn.commit()

    def create_functions(self):
        """Create all necessary functions and procedures"""
        # Procedure to insert/update user
        self.cur.execute("""
            CREATE OR REPLACE PROCEDURE insert_or_update_user(
                p_first_name VARCHAR,
                p_last_name VARCHAR,
                p_phone VARCHAR
            ) AS $$
            BEGIN
                IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_phone) THEN
                    UPDATE phonebook
                    SET first_name = p_first_name,
                        last_name = p_last_name
                    WHERE phone = p_phone;
                ELSE
                    INSERT INTO phonebook (first_name, last_name, phone)
                    VALUES (p_first_name, p_last_name, p_phone);
                END IF;
            END;
            $$ LANGUAGE plpgsql;
        """)


        # Function for pagination
        self.cur.execute("""
            CREATE OR REPLACE FUNCTION get_paginated_contacts(
                p_limit INTEGER,
                p_offset INTEGER
            )
            RETURNS TABLE (
                id INTEGER,
                first_name VARCHAR,
                last_name VARCHAR,
                phone VARCHAR
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT p.id, p.first_name, p.last_name, p.phone
                FROM phonebook p
                ORDER BY p.id
                LIMIT p_limit
                OFFSET p_offset;
            END;
            $$ LANGUAGE plpgsql;
        """)

        # Procedure to delete by username or phone
        self.cur.execute("""
            CREATE OR REPLACE PROCEDURE delete_by_username_or_phone(
                p_username VARCHAR DEFAULT NULL,
                p_phone VARCHAR DEFAULT NULL
            ) AS $$
            BEGIN
                IF p_username IS NOT NULL THEN
                    DELETE FROM phonebook WHERE first_name = p_username;
                ELSIF p_phone IS NOT NULL THEN
                    DELETE FROM phonebook WHERE phone = p_phone;
                END IF;
            END;
            $$ LANGUAGE plpgsql;
        """)

        self.conn.commit()

    def insert_from_csv(self, filename: str):
        """Insert data from CSV file"""
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 2:
                        first_name, phone = row[0], row[1]
                        last_name = row[2] if len(row) > 2 else None
                        self.insert_contact(first_name, last_name, phone)
            print("Data imported successfully from CSV")
        except Exception as e:
            print(f"Error importing from CSV: {e}")

    def insert_contact(self, first_name: str, phone: str, last_name: Optional[str] = None):
        """Insert a single contact"""
        try:
            self.cur.execute(
                "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)",
                (first_name, last_name, phone)
            )
            self.conn.commit()
            print(f"Contact {first_name} added successfully")
        except psycopg2.IntegrityError:
            print(f"Phone number {phone} already exists")
        except Exception as e:
            print(f"Error adding contact: {e}")

    def update_contact(self, phone: str, new_first_name: Optional[str] = None, new_phone: Optional[str] = None):
        """Update contact information"""
        try:
            if new_first_name:
                self.cur.execute(
                    "UPDATE phonebook SET first_name = %s WHERE phone = %s",
                    (new_first_name, phone)
                )
            if new_phone:
                self.cur.execute(
                    "UPDATE phonebook SET phone = %s WHERE phone = %s",
                    (new_phone, phone)
                )
            self.conn.commit()
            print("Contact updated successfully")
        except Exception as e:
            print(f"Error updating contact: {e}")

    def query_contacts(self, first_name: Optional[str] = None, phone: Optional[str] = None):
        """Query contacts with optional filters"""
        try:
            query = "SELECT * FROM phonebook WHERE 1=1"
            params = []
            
            if first_name:
                query += " AND first_name ILIKE %s"
                params.append(f"%{first_name}%")
            if phone:
                query += " AND phone ILIKE %s"
                params.append(f"%{phone}%")
            
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except Exception as e:
            print(f"Error querying contacts: {e}")
            return []

    def delete_contact(self, first_name: Optional[str] = None, phone: Optional[str] = None):
        """Delete contact by first name or phone"""
        try:
            if first_name:
                self.cur.execute("DELETE FROM phonebook WHERE first_name = %s", (first_name,))
            elif phone:
                self.cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
            self.conn.commit()
            print("Contact deleted successfully")
        except Exception as e:
            print(f"Error deleting contact: {e}")

    def insert_or_update_user(self, first_name: str, phone: str, last_name: Optional[str] = None):
        """Insert new user or update if exists"""
        try:
            self.cur.execute("CALL insert_or_update_user(%s, %s, %s)", (first_name, last_name, phone))
            self.conn.commit()
            print("User inserted/updated successfully")
        except Exception as e:
            print(f"Error inserting/updating user: {e}")



    def get_paginated_contacts(self, limit: int, offset: int) -> List[Tuple]:
        """Get contacts with pagination"""
        try:
            self.cur.callproc('get_paginated_contacts', (limit, offset))
            return self.cur.fetchall()
        except Exception as e:
            print(f"Error getting paginated contacts: {e}")
            return []

    def delete_by_username_or_phone(self, username: Optional[str] = None, phone: Optional[str] = None):
        """Delete contact by username or phone"""
        try:
            self.cur.callproc('delete_by_username_or_phone', (username, phone))
            self.conn.commit()
            print("Contact(s) deleted successfully")
        except Exception as e:
            print(f"Error deleting contact: {e}")

    def close(self):
        """Close the database connection"""
        self.cur.close()
        self.conn.close()

def main():
    phonebook = PhoneBook()
    
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert contact from console")
        print("2. Import contacts from CSV")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Insert/Update user")
        print("7. Get paginated contacts")
        print("8. Exit")
        
        choice = input("Enter your choice (1-10): ")
        
        if choice == "1":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name (optional): ")
            phone = input("Enter phone number: ")
            phonebook.insert_contact(first_name, phone, last_name if last_name else None)
            
        elif choice == "2":
            filename = input("Enter CSV filename: ")
            phonebook.insert_from_csv(filename)
            
        elif choice == "3":
            phone = input("Enter phone number of contact to update: ")
            new_first_name = input("Enter new first name (press Enter to skip): ")
            new_phone = input("Enter new phone number (press Enter to skip): ")
            phonebook.update_contact(phone, new_first_name if new_first_name else None, new_phone if new_phone else None)
            
        elif choice == "4":
            first_name = input("Enter first name to search (press Enter to skip): ")
            phone = input("Enter phone number to search (press Enter to skip): ")
            contacts = phonebook.query_contacts(first_name if first_name else None, phone if phone else None)
            for contact in contacts:
                print(f"ID: {contact[0]}, Name: {contact[1]} {contact[2] if contact[2] else ''}, Phone: {contact[3]}")
                
        elif choice == "5":
            delete_by = input("Delete by (1) first name or (2) phone number? (1/2): ")
            if delete_by == "1":
                first_name = input("Enter first name: ")
                phonebook.delete_contact(first_name=first_name)
            else:
                phone = input("Enter phone number: ")
                phonebook.delete_contact(phone=phone)

        
        elif choice == "6":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name (optional): ")
            phone = input("Enter phone number: ")
            phonebook.insert_or_update_user(first_name, phone, last_name if last_name else None)


        elif choice == "7":
            limit = int(input("Enter number of records per page: "))
            offset = int(input("Enter page number (starting from 0): ")) * limit
            contacts = phonebook.get_paginated_contacts(limit, offset)
            for contact in contacts:
                print(f"ID: {contact[0]}, Name: {contact[1]} {contact[2] if contact[2] else ''}, Phone: {contact[3]}")
                
        elif choice == "8":
            break
            
        else:
            print("Invalid choice. Please try again.")
    
    phonebook.close()

if __name__ == "__main__":
    main() 