from helper.MysqlClient import *


class BaseClass:
    __conn = None

    def __init__(self):
        conn = MysqlClient()
        self.__conn = conn

    def check_user_exist(self, data_list):
        sql_query = "select first_name from Customer where first_name = %s and last_name = %s and" \
                    " email_address = %s and date_of_birth = %s"
        account = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        if len(account) > 0:
            return True
        return False

    def check_email_exist(self, data_list):
        sql_query = "select customer_id, email_address from Customer where lower(email_address) = %s"
        account = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        if len(account) > 0:
            return True
        return False

    def insert_new_user(self, data_list):
        sql_query = """INSERT INTO Customer (first_name, middle_name, last_name, email_address, date_of_birth,
         client_ip, country_code, country_name, contact_number_extension, contact_number, password, driver_license_number,
         driver_license_state, driver_license_state_code, driver_license_expiry, status, creation_datetime, mod_datetime)
          VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'approved', current_timestamp(),current_timestamp())"""
        row_inserted = self.__conn.execute_insert(sql_query, data_list, raise_no_data_error=False)
        if row_inserted > 0:
            return True
        return False

    def insert_new_user_fedrated(self, data_list):
        sql_query = """INSERT INTO Customer (first_name, middle_name, last_name, email_address, date_of_birth,
         client_ip, country_code, country_name, contact_number_extension, contact_number, driver_license_number,
         driver_license_state, driver_license_state_code, driver_license_expiry, status, creation_datetime, mod_datetime)
          VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'google-approved', current_timestamp(),current_timestamp())"""
        row_inserted = self.__conn.execute_insert(sql_query, data_list, raise_no_data_error=False)
        if row_inserted > 0:
            return True
        return False

    def insert_customer_login(self, data_list):
        sql_query = """INSERT INTO Customer_Login (email_address, client_geo_ip, client_location, device_type, operating_system,
         login_type, creation_datetime, mod_datetime)
          VALUES(%s, %s, %s, %s, %s, %s, current_timestamp(),current_timestamp())"""
        row_inserted = self.__conn.execute_insert(sql_query, data_list, raise_no_data_error=False)
        if row_inserted > 0:
            return True
        return False

    def get_login_data(self, data_list):
        sql_query = "select customer_id, first_name, password, status from Customer where email_address = %s"
        account = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return account

    def update_password(self, data_list):
        sql_query = "update Customer set password = %s, mod_datetime=current_timestamp() where email_address = %s"
        row_updated = self.__conn.execute_update(sql_query, data_list, raise_no_affected_row_error=False)
        if row_updated > 0:
            return True
        return False

    def get_vehicle_data(self, data_list):
        sql_query = """SELECT vehicle_id, vehicle_description, vehicle_company_name, per_day_rent,per_hour_rent,
                        per_month_rent , vehicle_image_url
                         FROM whygo.Vehicle """
        vehicle_data = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return vehicle_data

    def get_vehicle_data_id(self, data_list):
        sql_query = """SELECT vehicle_id, vehicle_company_name, vehicle_description, vehile_mileage,
         vehile_transmission, max_number_of_seats, vehicle_luggage_capacity, fuel, aircondition_flag, 
         child_seat_flag, gps_flag, music_flag, seat_belt_flag, sleeping_bed_flag, water_level_flag, bluetooth_flag,
          on_board_computer_flag, audio_input_flag, long_term_trip_flag, medical_kit_flag,
           remote_cental_locking_flag, climate_control, car_description, per_hour_rent, per_day_rent,
            per_month_rent, vehicle_image_url FROM Vehicle where vehicle_id = %s"""
        vehicle_data = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return vehicle_data

    def get_related_vehicle_data(self, data_list):
        sql_query = """SELECT vehicle_id, vehicle_description, vehicle_company_name, per_day_rent, vehicle_image_url
                     FROM whygo.Vehicle ORDER BY RAND() LIMIT 3;"""
        vehicle_data = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return vehicle_data

    def insert_car_reviews(self, data_list):
        sql_query = """INSERT INTO Ratings (vehicle_id, driver_id, customer_id, vehicle_rating, comment,
         cleanliness_rating, comfort_rating, pickup_rating, overall_rating, creation_datetime, mod_datetime)
          VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, current_timestamp(),current_timestamp())"""
        row_inserted = self.__conn.execute_insert(sql_query, data_list, raise_no_data_error=False)
        if row_inserted > 0:
            return True
        return False

    def get_ratings_data(self, data_list):
        sql_query = """SELECT DISTINCT r.customer_id, c.first_name, c.middle_name, c.last_name, r.vehicle_rating,
                        r.comment, DATE_FORMAT(r.creation_datetime, '%%d %%M %%Y') AS creation_datetime
                        FROM whygo.Customer c
                        INNER JOIN whygo.Ratings r ON c.customer_id = r.customer_id
                        WHERE r.comment IS NOT NULL
                        and r.vehicle_id = %s
                        ORDER BY creation_datetime;"""
        rating_data = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return rating_data

    def get_ratings_data_percentage(self, data_list):
        sql_query = """SELECT 
                          COUNT(*) AS total_reviews, 
                          SUM(CASE WHEN vehicle_rating = 5 THEN 1 ELSE 0 END) AS five_star_reviews, 
                          SUM(CASE WHEN vehicle_rating = 4 THEN 1 ELSE 0 END) AS four_star_reviews, 
                          SUM(CASE WHEN vehicle_rating = 3 THEN 1 ELSE 0 END) AS three_star_reviews, 
                          SUM(CASE WHEN vehicle_rating = 2 THEN 1 ELSE 0 END) AS two_star_reviews, 
                          SUM(CASE WHEN vehicle_rating = 1 THEN 1 ELSE 0 END) AS one_star_reviews, 
                          CONCAT(ROUND(SUM(CASE WHEN vehicle_rating = 5 THEN 1 ELSE 0 END)/COUNT(*) * 100)) AS five_star_percentage,
                          CONCAT(ROUND(SUM(CASE WHEN vehicle_rating = 4 THEN 1 ELSE 0 END)/COUNT(*) * 100)) AS four_star_percentage,
                          CONCAT(ROUND(SUM(CASE WHEN vehicle_rating = 3 THEN 1 ELSE 0 END)/COUNT(*) * 100)) AS three_star_percentage,
                          CONCAT(ROUND(SUM(CASE WHEN vehicle_rating = 2 THEN 1 ELSE 0 END)/COUNT(*) * 100)) AS two_star_percentage,
                          CONCAT(ROUND(SUM(CASE WHEN vehicle_rating = 1 THEN 1 ELSE 0 END)/COUNT(*) * 100)) AS one_star_percentage
                        FROM whygo.Ratings r
                        WHERE r.vehicle_id = %s"""
        rating_data_percentage = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return rating_data_percentage


    def get_ratings_data_base(self, data_list):
        sql_query = """SELECT DISTINCT r.customer_id, c.first_name, c.middle_name, c.last_name, r.vehicle_rating,
                        r.comment, DATE_FORMAT(r.creation_datetime, '%%d %%M %%Y') AS creation_datetime
                        FROM whygo.Customer c
                        INNER JOIN whygo.Ratings r ON c.customer_id = r.customer_id
                        WHERE r.comment IS NOT NULL and r.vehicle_rating = 5
                        ORDER BY creation_datetime;"""
        rating_data = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return rating_data


    def get_total_customer_count(self, data_list):
        sql_query = """select count(1) as customer_count from Customer;"""
        customer_count = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return customer_count

    def get_total_cars_count(self, data_list):
        sql_query = """select count(1) as cars_count from Vehicle;"""
        cars_count = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return cars_count

    def get_trending_cars(self, data_list):
        sql_query = """SELECT vehicle_id, vehicle_description, vehicle_company_name, per_day_rent, vehicle_image_url
                     FROM whygo.Vehicle where vehicle_id in %s"""
        trending_data = self.__conn.execute_fetch_all_dict(sql_query, data_list, raise_no_data_error=False)
        return trending_data