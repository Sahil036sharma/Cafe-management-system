from tkinter import *
import time
from tkinter import messagebox
import math as mt
import pymysql  # type: ignore
from PIL import Image,ImageTk # type: ignore
from PIL import Image # type: ignore


# Establish database connection
db = pymysql.connect(
    user='root',
    password='root',
    host='localhost',
    database='cafe_db'
)

cur = db.cursor()

# Create the order_info table if it doesn't exist
cur.execute(
    "CREATE TABLE IF NOT EXISTS order_info (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200), email VARCHAR(200), mobile_no VARCHAR(30), order_no INT, order_text TEXT, total_amount DECIMAL(10, 2), order_time TEXT)")

root = Tk()
root.geometry("1400x1000+150+300")
root.resizable(width=True, height=True)
root.title("Cafe Management System")
# # root.iconbitmap("\restlogo.ico")
# photo = ImageTk.PhotoImage(Image.open(r"C:/Users/HP/Downloads/SEMINAIR/SEMINAIR/sahil.png"))
# label=Label(root,text="label1",image=photo,height=2500,width=1700)


# Top
Tops = Frame(root, width=1600, height=50, relief=SUNKEN)
Tops.pack(side=TOP)

# Time
localtime = time.asctime(time.localtime(time.time()))

# Info
lblt = Label(Tops, font=('algerian', 30, 'bold'), text="Cafe Management System", fg="crimson", bg=None, bd=10, anchor='w')
lblt.grid(row=0, column=0)
lblt = Label(Tops, font=('algerian', 25), text=localtime, fg="purple", bg=None, anchor=W)
lblt.grid(row=1, column=0)

# Items
lbit = Label(root, font=('algerian', 30, 'bold'), text="Menu", fg="dark orange", bd=10)
lbit.place(x=100, y=140)
lbit = Label(root, font=('algerian', 18, 'bold'), text="Quantity", fg="black", bd=10)
lbit.place(x=340, y=150)

lbit = Label(root, font=('arial black', 18), text="Burger", fg="sky blue", bd=1)
lbit.place(x=20, y=200)
lbit = Label(root, font=('arial black', 18), text="Tea", fg="sky blue", bd=1)
lbit.place(x=20, y=250)
lbit = Label(root, font=('arial black', 18), text="Coffie", fg="sky blue", bd=1)
lbit.place(x=20, y=300)
lbit = Label(root, font=('arial black', 18), text="Pizza", fg="sky blue", bd=1)
lbit.place(x=20, y=350)
lbit = Label(root, font=('arial black', 18), text="Cold Drink", fg="sky blue", bd=1)
lbit.place(x=20, y=400)
lbit = Label(root, font=('arial black', 18), text="Cakes", fg="sky blue", bd=1)
lbit.place(x=20, y=450)
lbit = Label(root, font=('arial black', 18), text="Maggie", fg="sky blue", bd=1)
lbit.place(x=20, y=500)

# Price
lbit = Label(root,font=( 'arial black' ,18,  ),text="₹ 49",fg="sky blue",bd=1)
lbit.place(x=220,y=200)
lbit = Label(root,font=( 'arial black' ,18,  ),text="₹ 34",fg="sky blue",bd=1)
lbit.place(x=220,y=250)
lbit = Label(root,font=( 'arial black' ,18,  ),text="₹ 32",fg="sky blue",bd=1)
lbit.place(x=220,y=300)
lbit = Label(root,font=( 'arial black' ,18,  ),text="₹ 79",fg="sky blue",bd=1)
lbit.place(x=220,y=350)
lbit = Label(root,font=( 'arial black' ,18,  ),text="₹ 47",fg="sky blue",bd=1)
lbit.place(x=220,y=400)
lbit = Label(root,font=( 'arial black' ,18,  ),text="₹ 222",fg="sky blue",bd=1)
lbit.place(x=220,y=450)
lbit = Label(root,font=( 'arial black' ,18,  ),text="₹ 37",fg="sky blue",bd=1)
lbit.place(x=220,y=500)

# Order
lbit = Label(root, font=('algerian', 30, 'bold'), text="Order", fg="crimson", bd=1)
lbit.place(x=650, y=140)

order = []

def order_add(item, quantity_entry):
    quantity = quantity_entry.get()  # Get the quantity entered by the user
    if quantity:  # Check if quantity is not empty
        order.append(f"{item} x{quantity}")  # Append item name and quantity to the order list
        order_text.delete("1.0", END)  # Clear the text box
        order_text.insert(END, '\n'.join(order))  # Display the updated order
    else:
        messagebox.showwarning("Warning", "Please enter a quantity for the item.")

#cancel order

def order_cancel():
    order.clear()
    order_text.delete("1.0", END)

# Text box
order_text = Text(root, height=10, width=20, fg="purple", font=('arial black', 20))
order_text.place(x=550, y=200)

#validation
def validation():
    order_no = entry_order_no.get()
    name = entry_name.get()
    mobile_no = entry_mobile_no.get()
    email = entry_email.get()

    # Check if any field is empty
    if not (order_no and name and order and mobile_no or email):
        messagebox.showerror("Error", "Please fill in all fields.")
        return False

    # Check email format
    if email:
        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return False

    # Check mobile number format
    if mobile_no:
        if not mobile_no.isdigit() or len(mobile_no) != 10:
            messagebox.showerror("Error", "Please enter a valid 10-digit mobile number.")
            return False

    # Check if name contains only alphabets
    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Error", "Name should contain only alphabets.")
        return False
    
    if not order_no.isdigit() or len(order_no)  <1:
            messagebox.showerror("Error", "Please enter a valid digits in order number.")
            return False
    

    return True


# Function to save order details to the database
def save_order_to_database():
    name = entry_name.get()
    mobile_no = entry_mobile_no.get()
    email = entry_email.get()
    order_no = entry_order_no.get()
    order_text_data = order_text.get("1.0", "end-1c")
    order_time = time.asctime(time.localtime(time.time()))

    if not email:
        email = "not provided"
    if not mobile_no:
        mobile_no = "not provided"

    total_amount = 0
    for item in order:
        item_name, quantity_str = item.split(' x')
        quantity = int(quantity_str)
        price = 0
        if item_name == "Burger":
            price = 49
        elif item_name == "Tea":
            price = 34
        elif item_name == "Coffie":
            price = 32
        elif item_name == "Pizza":
            price = 79
        elif item_name == "Cold Drink":
            price = 47
        elif item_name == "Cakes":
            price = 222
        elif item_name == "Maggie":
            price = 37
        total_amount += price * quantity

    sgst = total_amount * 0.06
    cgst = total_amount * 0.06
    s_tax = total_amount * 0.12
    total_amount += sgst + cgst + s_tax

    try:
        cur.execute(
            "INSERT INTO order_info (name, email, mobile_no, order_no, order_text, total_amount, order_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, email, mobile_no, order_no, order_text_data, total_amount, order_time))
        db.commit()
        messagebox.showinfo("Success", "Order details saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred while saving order details: {str(e)}")
        db.rollback()


#generate bill
def generate_bill():
    if not order_text.get("1.0", END).strip():
        messagebox.showerror("Error", "Please order first to generate the bill.")
        return

    if not validation():
        return

    save_order_to_database()

    # Close the database connection
    db.close()

    total_amount = 0
    for item in order:
        item_name, quantity_str = item.split(' x')
        quantity = int(quantity_str)
        if item_name == "Burger":
            total_amount += 49 * quantity
        elif item_name == "Tea":
            total_amount += 34 * quantity
        elif item_name == "Coffie":
            total_amount += 32 * quantity
        elif item_name == "Pizza":
            total_amount += 79 * quantity
        elif item_name == "Cold Drink":
            total_amount += 47 * quantity
        elif item_name == "Cakes":
            total_amount += 222 * quantity
        elif item_name == "Maggie":
            total_amount += 37 * quantity

    order_no = entry_order_no.get()
    name = entry_name.get()
    mobile_no = entry_mobile_no.get()
    email = entry_email.get()
    order_time = time.asctime(time.localtime(time.time()))

    # Create a new window for the bill
    bill_window = Toplevel(root)
    bill_window.title("Bill")
    bill_window.geometry("500x900")
    bill_window.config(bg='black')

    bill_name = Label(bill_window, font=("Times New Roman", 20, 'bold'), bg='black', fg='white', text="Cafe Bill")
    bill_name.pack()
    bill_time = Label(bill_window, text=order_time, font=("Times New Roman", 20, 'bold'), bg='black', fg='white')
    bill_time.pack()
    bill_no = Label(bill_window, font=("Times New Roman", 15, 'bold'), bg='black', fg='white', text=f"\nBill no : {order_no}")
    bill_no.pack()
    bill_csn = Label(bill_window, font=("Times New Roman", 15, 'bold'), bg='black', fg='white', text=f"Name : {name}")
    bill_csn.pack()
    bill_phone = Label(bill_window, font=("Times New Roman", 15, 'bold'), bg='black', fg='white', text=f"Phone No: {mobile_no}")
    bill_phone.pack()
    bill_email = Label(bill_window, font=("Times New Roman", 15, 'bold'), bg='black', fg='white', text=f"Email id : {email}\n")
    bill_email.pack()

    bill_label = Label(bill_window, font=("Times New Roman", 15, 'bold'), bg='black', fg='white', text="----------------------------------------------------\nItem\t\tQty\t\tPrice\n-----------------------------------------------------")
    bill_label.pack()

    for item in order:
        item_name, quantity_str = item.split(' x')
        quantity = int(quantity_str)
        price = 0
        if item_name == "Burger":
            price = 49
        elif item_name == "Tea":
            price = 34
        elif item_name == "Coffie":
            price = 32
        elif item_name == "Pizza":
            price = 79
        elif item_name == "Cold Drink":
            price = 47
        elif item_name == "Cakes":
            price = 222
        elif item_name == "Maggie":
            price = 37
        total_price = price * quantity
        item_label = Label(bill_window, font=("Times New Roman", 15,), fg='white', bg='black', text=f"\n{item_name}\t\t{quantity}\t\t₹{total_price}")
        item_label.pack()

    sgst = (total_amount * 6) / 100
    cgst = (total_amount * 6) / 100
    S_tax = (total_amount * 12) / 100
    total_bill = total_amount + sgst + cgst + S_tax
    total_bill = mt.ceil(total_bill * 100) / 100

    sub_total_label = Label(bill_window, font=("Times New Roman", 15,), fg='white', bg='black', text=f"\n---------------------------------------------------------\nSub Total:\t\t\t₹{total_amount}")
    sub_total_label.pack()

    gst_label = Label(bill_window, font=("Times New Roman", 15,), fg='white', bg='black', text=f"CGST (6%):\t\t\t₹{cgst}")
    gst_label.pack()

    cgst_label = Label(bill_window, font=("Times New Roman", 15,), fg='white', bg='black', text=f"SGST (6%):\t\t\t₹{sgst}")
    cgst_label.pack()

    stax_label = Label(bill_window, font=("Times New Roman", 15,), fg='white', bg='black', text=f"S.Tax:\t\t\t \t₹{S_tax}")
    stax_label.pack()

    total_bill_label = Label(bill_window, font=("Times New Roman", 16, 'bold'), bg='black', fg='white', text=f"Total Amount:\t\t₹{total_bill}")
    total_bill_label.pack()

    order.clear()
    order_text.delete("1.0", END)
# Quantity

quantity1 = Entry(root, font=('arial black', 18), fg="purple", bd=1, width=3)
quantity1.place(x=360, y=200)

quantity2 = Entry(root, font=('arial black', 18), fg="purple", bd=1, width=3)
quantity2.place(x=360, y=250)

quantity3 = Entry(root, font=('arial black', 18), fg="purple", bd=1, width=3)
quantity3.place(x=360, y=300)

quantity4 = Entry(root, font=('arial black', 18), fg="purple", bd=1, width=3)
quantity4.place(x=360, y=350)

quantity5 = Entry(root, font=('arial black', 18), fg="purple", bd=1, width=3)
quantity5.place(x=360, y=400)

quantity6 = Entry(root, font=('arial black', 18), fg="purple", bd=1, width=3)
quantity6.place(x=360, y=450)

quantity7 = Entry(root, font=('arial black', 18), fg="purple", bd=1, width=3)
quantity7.place(x=360, y=500)



# Add buttons
btn1 = Button(root, text="Add", fg="red",cursor='hand2', font=('arial black', 10), command=lambda: order_add("Burger",quantity1))
btn1.place(x=450, y=200)

btn2 = Button(root, text="Add", fg="red",cursor='hand2', font=('arial black', 10), command=lambda: order_add("Tea",quantity2))
btn2.place(x=450, y=250)

btn3 = Button(root, text="Add", fg="red",cursor='hand2', font=('arial black', 10), command=lambda: order_add("Coffie",quantity3))
btn3.place(x=450, y=300)

btn4 = Button(root, text="Add", fg="red",cursor='hand2', font=('arial black', 10), command=lambda: order_add("Pizza",quantity4))
btn4.place(x=450, y=350)

btn5 = Button(root, text="Add", fg="red",cursor='hand2', font=('arial black', 10), command=lambda: order_add("Cold Drink",quantity5))
btn5.place(x=450, y=400)

btn6 = Button(root, text="Add", fg="red",cursor='hand2', font=('arial black', 10), command=lambda: order_add("Cakes",quantity6))
btn6.place(x=450, y=450)

btn7 = Button(root, text="Add", fg="red",cursor='hand2', font=('arial black', 10), command=lambda: order_add("Maggie",quantity7))
btn7.place(x=450, y=500)
#cencle_btn
btncncl=Button(root,text='Cancel Order',cursor='hand2',font=('algerian', 20, 'bold'), fg="blue", bd=1,command=lambda:order_cancel())
btncncl.place(x=620,y=600)

#bill_btn
btnbill=  Button(root,text='  Bill  ',cursor='hand2',font=('algerian', 20, 'bold'),bg="lightgreen", fg="black", bd=1,command=lambda:generate_bill())
btnbill.place(x=950,y=700)

lbl_order_no =Label(root,text='Order number',cursor='hand2',font=('algerian', 30, 'bold'), fg="red", bd=1,)
lbl_order_no.place(x=300,y=700)

entry_order_no = Entry(root,font=('algerian', 30, 'bold'), fg="black",bg='white',bd=1,relief="groove",width=10)
entry_order_no.place(x=650,y=700)
#customer details

lbl_details = Label(root,font=('algerian', 30, 'bold'), fg="black", text="Customer Details", bd=1)
lbl_details.place(x=1000, y=140)

lbl_name = Label(root,font=('algerian', 20, 'bold'), fg="purple", text="Name:", bd=1)
lbl_name.place(x=1000, y=200)

entry_name = Entry(root, font=('arial black', 18, ), fg="green", bd=1)
entry_name.place(x=1000, y=250)

lbl_mobile_no = Label(root,font=('arial black', 20, 'bold'), fg="purple", text="Phone no:", bd=1)
lbl_mobile_no.place(x=1000, y=300)

entry_mobile_no = Entry(root, font=('algerian', 20, ), fg="green", bd=1)
entry_mobile_no.place(x=1000, y=350)

lbl_email = Label(root,font=('algerian', 20, ), fg="grey", text="Or", bd=1)
lbl_email.place(x=1000, y=400)

lbl_email = Label(root,font=('algerian', 20, 'bold'), fg="purple", text="Email:", bd=1)
lbl_email.place(x=1000, y=450)

entry_email = Entry(root, font=('arial black', 18, ), fg="green", bd=1)
entry_email.place(x=1000, y=500)

root.mainloop()
