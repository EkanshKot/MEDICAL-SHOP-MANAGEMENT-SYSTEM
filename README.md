# MEDICAL-SHOP-MANAGEMENT-SYSTEM
Hi guys This is a project i built to understand databases and explore tkinter.
Medical Shop Management System  This project is a Python-based desktop application designed to manage the day-to-day operations of a medical shop or pharmacy. It provides an integrated system for inventory management, billing, sales tracking, and reporting through a user-friendly graphical interface built using Tkinter.  


The application uses an SQLite database to persist medicine and sales data, enabling features such as real-time stock updates, low-stock alerts, bill generation with inbuilt gst(Taxes), and sales history tracking. It is designed as a single-user, offline system suitable for small to medium-sized medical stores.
The project focuses on practical software engineering concepts such as database-backed GUI applications, CRUD operations, and transactional data handling 
Here are some features of this system:
*Dashboard

Displays total number of medicines
Shows low-stock alerts
Provides daily sales summary

*Inventory Management

Add, edit, and delete medicine records
Search medicines by name, batch number, or generic name
Track expiry dates and available quantities

*Billing System
Generate bills with automatic GST calculation
Update inventory levels after each sale
Store customer and transaction details

Reports

Low stock report for inventory monitoring
Sales history report with customer and customer details

Database Integration

Persistent data storage using SQLite
Automatic database and table creation
Preloaded sample data for first-time use


What I learnt from this Prooject:

Building real-world GUI applications:
Learned how to design a multi-tab desktop application using Tkinter with a clean user flow.

Database-backed applications:
Integrated SQLite to persist data, handle relationships, and maintain consistency across sessions.

CRUD operations:
Implemented Create, Read, Update, and Delete operations for inventory and sales records.

Transaction management:
Ensured that billing updates inventory and sales records atomically to avoid inconsistencies.

Event-driven programming:
Used callbacks and GUI events to respond to user actions such as clicks, searches, and form submissions.

Data validation & error handling:
Handled invalid inputs, empty bills, and database exceptions gracefully.

Separation of concerns:
Structured the application to separate UI logic, database operations, and business logic.

Practical software engineering:
Designed a system that mirrors real operational workflows used in pharmacies.

However Ofc this is not ready for practical uses.It only stores the data locally as SQlite has been used wwhich is a problem in itself and can be deleted,
It is designed to be a single user and single system project
