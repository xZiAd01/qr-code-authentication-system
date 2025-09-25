# Import required libraries
import pandas as pd
from datetime import date, datetime

class Validator:
    """
    Validator class
    - Loads the customer & vehicle database.
    - Validates a scanned QR code against the database.
    - Checks for customer existence & membership expiration.
    - Formats results for display.
    """
    def __init__(self):
        # Load the Excel file into a pandas DataFrame
        self.df = pd.read_excel('customers_with_vehicles.xlsx')
        print("Validator Connected to Database")
    
    def validate(self, data):
        """
        Validate the QR code data.
        Looks up the customer in the database using their customer_id.
        Returns error if not found, else checks expiration.
        """
        print("Checking if data in Database...")
        
        # Find rows where customer_id matches scanned data
        customer_rows = self.df[self.df['customer_id'].astype(str) == data]
        
        if customer_rows.empty:
            # No customer found
            return {"error": "no customer was found"}
        else:
            # Customer(s) found → convert rows to list of lists
            all_customer_data = customer_rows.values.tolist()
            print("DONE.")
            # Check expiration date next
            return self.check_exp_date(all_customer_data)

    def check_exp_date(self, customer_data):
        """
        Checks if the customer's membership is still valid.
        Looks at the expiration_date field.
        """
        print("Checking Expiration Date...")
        today = date.today()
        
        # Find the index of the 'expiration_date' column
        headers_from_df = self.df.columns.tolist()
        try:
            exp_date_col_idx = headers_from_df.index('expiration_date')
        except ValueError:
            # Column not found in Excel
            return {"error": "Expiration date column not found in database."}
        
        # Parse expiration date of first record
        exp_date_str = str(customer_data[0][exp_date_col_idx])
        exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()

        if today <= exp_date:
            # Membership is valid
            print("DONE.")
            return self.format_customer_data(customer_data)
        else:
            # Membership expired
            return {"error": "QR Code is Expired"}
        
    def format_customer_data(self, customer_data):
        """
        Formats the customer & vehicle data for rendering in HTML.
        Returns a dictionary with headers and data.
        """
        # Expected headers in display order
        headers = [
            "customer_id", "first_name", "last_name", "number of cars", "car_vin",
            "car_make", "car_model", "expiration_date", "status",
            "last_maintenance_date", "next_maintenance_due", "maintenance_requirements",
            "predictive_maintenance_alert", "remaining_useful_life"
        ]
        
        # Actual column names from the DataFrame
        df_columns = self.df.columns.tolist()
        
        formatted_data = []
        for item_list in customer_data:  # each row as list
            row_data = {}
            for header_name in headers:
                try:
                    # Map header to DataFrame column index
                    col_index = df_columns.index(header_name)
                    row_data[header_name] = str(item_list[col_index])
                except ValueError:
                    # In case header not found in DataFrame
                    row_data[header_name] = "N/A"
            formatted_data.append(row_data)
        
        # Prepare final result
        return {
            "success": True,
            "headers": [h.replace('_', ' ').title() for h in headers],  # Make headers more readable
            "data": formatted_data
        }
