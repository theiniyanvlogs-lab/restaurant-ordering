import os
import json

import gspread
from datetime import datetime
from zoneinfo import ZoneInfo
from google.oauth2.service_account import Credentials

# =====================================================
# GOOGLE SHEETS CONFIGURATION
# =====================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "RestaurantDB"

google_credentials = os.environ.get("GOOGLE_CREDENTIALS")

if google_credentials:
    creds = Credentials.from_service_account_info(
        json.loads(google_credentials),
        scopes=SCOPES
    )
else:
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

client = gspread.authorize(creds)

spreadsheet = client.open(SHEET_NAME)

# =====================================================
# CURRENT INDIAN TIME
# =====================================================

def current_time():

    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%d-%m-%Y %I:%M:%S %p")


# =====================================================
# GENERATE ORDER ID
# =====================================================

def generate_order_id():

    sheet = spreadsheet.worksheet("Orders")

    values = sheet.get_all_values()

    # Only Header Exists
    if len(values) <= 1:
        return "ORD1001"

    last_order = values[-1][0]

    try:
        number = int(last_order.replace("ORD", ""))
    except:
        number = 1000

    return f"ORD{number + 1}"


# =====================================================
# MENU
# =====================================================

def get_menu():

    sheet = spreadsheet.worksheet("Menu")

    rows = sheet.get_all_records()

    menu = []

    for row in rows:

        menu.append({

            "id": int(row["ID"]),
            "name": row["Name"],
            "category": row["Category"],
            "price": float(row["Price"]),
            "rating": float(row["Rating"]),
            "image": row["Image"],
            "description": row["Description"],
            "prep_time": row["Prep_Time"],
            "popular": str(row["Popular"]).upper() == "TRUE"

        })

    return menu


def get_menu_item(item_id):

    menu = get_menu()

    return next(
        (item for item in menu if item["id"] == item_id),
        None
    )


# =====================================================
# USERS
# =====================================================

def get_users():

    sheet = spreadsheet.worksheet("Users")

    return sheet.get_all_records()


def add_user(name, email, password):

    sheet = spreadsheet.worksheet("Users")

    sheet.append_row([
        name,
        email,
        password
    ])


# =====================================================
# ORDERS
# =====================================================



def add_order(
    order_id,
    customer,
    phone,
    email,
    address,
    payment,
    total
):

    sheet = spreadsheet.worksheet("Orders")

    sheet.append_row([

        order_id,
        customer,
        phone,
        email,
        address,
        payment,
        total,
        current_time(),
        "Preparing"

    ])


# =====================================================
# ORDER ITEMS
# =====================================================

def get_order_items():

    sheet = spreadsheet.worksheet("OrderItems")

    return sheet.get_all_records()


def add_order_item(
    order_id,
    item_name,
    quantity,
    price
):

    sheet = spreadsheet.worksheet("OrderItems")

    sheet.append_row([

        order_id,
        item_name,
        quantity,
        price

    ])


# =====================================================
# ORDER SUMMARY
# =====================================================

def add_order_summary(

    order_id,
    customer_name,
    phone,
    email,
    address,
    payment,
    items,
    total

):

    sheet = spreadsheet.worksheet("OrderSummary")

    sheet.append_row([

        order_id,
        customer_name,
        phone,
        email,
        address,
        payment,
        items,
        total,
        current_time(),
        "Preparing"

    ])


# =====================================================
# CONTACT
# =====================================================

def get_contacts():

    sheet = spreadsheet.worksheet("Contact")

    return sheet.get_all_records()


def add_contact(
    name,
    email,
    message
):

    sheet = spreadsheet.worksheet("Contact")

    sheet.append_row([

        name,
        email,
        message,
        current_time()

    ])