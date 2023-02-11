from gettext import install
from json.tool import main
from datetime import datetime
from multiprocessing.sharedctypes import Value
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import os
import tempfile
from time import strftime
import xlsxwriter
import numpy as np
import pandas as pd
import openpyxl
import time


# Bill Receipt Generation Based some Number (to be done)

class Bill_App:
    def __init__(self,root):
        self.root=root
        
        width= root.winfo_screenwidth()               
        height= root.winfo_screenheight()
        self.root.geometry("%dx%d"%(width,height))
        self.root.title('Billing Software')

        # ===========================Variables=========================
        self.C_name=StringVar()
        self.C_name.set("")
        self.C_phon=StringVar()
        self.C_phon.set("")
        self.bill_no=StringVar()
        self.bill_generated = False
        self.card_upi=''
        self.Cash=''
        self.printed = False

        self.card_transaction = False
        self.cash_transaction = False

        bill_no_format=strftime('%H:%M:%S %p')
        bill_no_format = bill_no_format.split(' ')
        bill_no_format=''.join(bill_no_format[0].split(':'))

        self.bill_no.set(bill_no_format)

        self.search_bill=StringVar()
        self.product=StringVar()
        self.prices=IntVar()
        self.qty=IntVar()
        self.sub_total=StringVar()
        self.tax_input=StringVar()
        self.total=StringVar()

        # Item Category List
        self.Category=['Select Option','Lassi','ThickShakes','Mocktails','Veg SandWich','Non-Veg SandWich',
                    'Spl. SandWich','Falooda','Special IceCream','Cold Coffee','Veg Nachos',
                    'Non-Veg Nachos','Snack','Juice & Fruit Salad','Pasta','Combos for 1','Combos for 2','Special Items','Biryani','Add Ons']

        self.SubCatAdd_Ons=['Select Item','Water Bottle','Extra Mayonnaise']

        self.wb = 20
        self.Em = 20

        self.SubCatBiryani = ['Select Item','Chicken Biryani']
        self.Chick_Bir = 259

        self.SubCatSpl_Items = ['Select Item','Chicken Jumbo Nuggets','Chicken Wings','Chicken Garlic Fingers','Chicken Hot & Spicy Seekh Kebab',
                                'Veg Fingers']
        
        self.Chick_Jumbo_Nuggets = 179
        self.Chicken_Wings = 179
        self.Chicken_Garlic_Fingers = 169
        self.Chick_Hot_Spicy_Seekh_Kebab = 129
        self.Veg_Fingers = 129

        self.SubCatCombos_for_1=['Select Item','Veg Sandwich+Vanilla ThickShake','Paneer SandWich+Pista ThickShake','Chicken Sandwich + ButterScotch ThickShake',
                            'Cheese & Jalapeno Chicken Sandwich+Kitkat ThickShake','Veg Sandwich+Peri Peri French Fries+Virgin Mojito',
                            'Paneer Sandwich+Peri Peri French Fries+Virgin Mojito','Chicken Sandwich+Chicken Nuggets+Virgin Mojito',
                            'Cheese & Jalapeno Chicken Sandwich+Chicken Nuggets+Virgin Mojito','Loaded Chicken Nachos+Virgin Mojito',
                            'Baked Vegetable Nachos+Virgin Mojito']

        self.vegsw_Vts=259
        self.Psw_Pts=329
        self.Csw_BSts=319
        self.CJCsw_KKts=339
        self.Vsw_PPff_Vm=329
        self.Psw_PPff_Vm=369
        self.Csw_Cn_Vm=389
        self.CJCsw_Cn_Vm=409
        self.CLn_Vm=299
        self.BVn_Vm=259

        self.SubCatCombos_for_2 = ['Select Item','2 VegSandwich+2 Virgin Mojito+Peri Peri French Fries',
                                    '2 Chicken Sandwich+2 Virgin Mojito+Chicken Nuggets',
                                    'Paneer Sandwich+Chicken Sandwich+2Virgin Mojito+Peri Peri French Fries',
                                    'Paneer Sandwich+Chicken Sandwich+2Virgin Mojito+Chicken Nuggets']

        self.Vsw2_2Vm_PPff = 579
        self.Csw2_2Vm_Cn = 659
        self.Psw_Csw_2Vm_PPff = 649
        self.Psw_Csw_2Vm_Cn = 679
        
        self.SubCatPasta=['Select Item','Creamy Mushroom Chicken Pasta','Creamy Mushroom Veg Pasta',
                        'Creamy Mushroom Paneer Pasta',
                        'Creamy Mushroom Pasta',
                        'Creamy Mushroom Egg Pasta']

        self.Creamy_Mushroom_Chicken_Pasta=269
        self.Creamy_Mushroom_Veg_Pasta=229
        self.Creamy_Mushroom_Paneer_Pasta=269
        self.Creamy_Mushroom_Pasta=219
        self.Creamy_Mushroom_Egg_Pasta=229

        self.SubCatLassi=['Select Item','Sweet Lassi',
                            'Butter Scotch Lassi',
                            'Mango Lassi',
                            'Banana Lassi',
                            'Strawberry Lassi',
                            'Pista Lassi',
                            'Kiwi Lassi',
                            'Chocolate Lassi',
                            'Kesar Lassi',
                            'Royal Lassi',
                            'Dry Fruit Lassi',
                            'Fruit & Cream Lassi']

        self.Sweet_Lassi=79
        self.Butter_Scotch_Lassi=119
        self.Mango_Lassi=119
        self.Banana_Lassi=119
        self.Strawberry_Lassi=119
        self.Pista_Lassi=119
        self.Kiwi_Lassi=129
        self.Chocolate_Lassi=129
        self.Kesar_Lassi=139
        self.Royal_Lassi=199
        self.Dry_Fruit_Lassi=169
        self.Fruit_Cream_Lassi=169

        self.SubCatJuiceFruit = ['Select Item','ABC (Apple, BeetRoot, Carrot)','Carrot-BeetRoot Juice',
                                'BeetRoot Juice','Apple Smoothie','Carrot Banana Smoothie',
                                'Fruit Salad','Fruit Salad With IceCream']
        self.ABC=149
        self.Carrot_Beetroot_Juice=129
        self.Beetroot_Juice=129
        self.Apple_Smoothie=149
        self.Carrot_Banana_Smoothie=149
        self.Fruit_Salad=149
        self.Fruit_Salad_With_Icecream=199

        self.SubCatSplSandwich = ['Select Item','Nutella Banana Sandwich','Peanut Butter Sandwich','Chocolate Sandwich']

        self.Nutella_Banana_Sandwich=149
        self.Peanut_Butter_Sandwich=149
        self.Chocolate_Sandwich=169


        self.SubCatThickShakes=['Select Item','Very Berry Strawberry Thick Shake',
                                'Vanilla Thick Shake',
                                'Body Cooler Shake',
                                'Oreo Thick Shake',
                                'Mango Alphanso Thick Shake',
                                'Chocolate Thick Shake',
                                'Banana Bonkers Thick Shake',
                                'Pista Thick Shake',
                                'Shake Shake Caramel Thick Shake',
                                'Kesar Pista Thick Shake',
                                'Choco Chip Cookies Thick Shake',
                                'Hopscotch Butterscotch Thick Shake',
                                'Sharjah Thick Shake',
                                'Arabian Night Thick Shake',
                                'Dry Fruit Thick Shake',
                                'Kaju Anjeer Thick Shake',
                                'Dry Anjeer Thick Shake',
                                'Belgian Chocolate Thick Shake',
                                'Kitkat Thick Shake',
                                'Snickers Thick Shake',
                                'Chocko Dry Fruit Thick Shake',
                                'Nutella Thick Shake',
                                'Lassiday Twister Thick Shake',
                                'Ferraro Rocher Thick Shake',
                                'Brownie Thick Shake',
                                'Mississippi Mud Thick Shake',
                                'Black Current Thick Shake',
                                'Blue Berry Thick Shake']



        self.Very_Berry_Strawberry_Thick_Shake=159
        self.Vanilla_Thick_Shake=159
        self.Body_Cooler_Shake=159
        self.Oreo_Thick_Shake=179
        self.Mango_Alphanso_Thick_Shake=189
        self.Chocolate_Thick_Shake=189
        self.Banana_Bonkers_Thick_Shake=189
        self.Pista_Thick_Shake=189
        self.Shake_Shake_Caramel_Thick_Shake=189
        self.Kesar_Pista_Thick_Shake=199
        self.Choco_Chip_Cookies_Thick_Shake=199
        self.Hopscotch_Butterscotch_Thick_Shake=199
        self.Sharjah_Thick_Shake=199
        self.Arabian_Night_Thick_Shake=199
        self.Dry_Fruit_Thick_Shake=199
        self.Kaju_Anjeer_Thick_Shake=199
        self.Dry_Anjeer_Thick_Shake=199
        self.Belgian_Chocolate_Thick_Shake=209
        self.Kitkat_Thick_Shake=209
        self.Snickers_Thick_Shake=209
        self.Chocko_Dry_Fruit_Thick_Shake=209
        self.Nutella_Thick_Shake=209
        self.Lassiday_Twister_Thick_Shake=209
        self.Ferraro_Rocher_Thick_Shake=209
        self.Brownie_Thick_Shake=209
        self.Black_Current_Thick_Shake=199
        self.Blue_Berry_Thick_Shake=209
        self.Mississippi_Mud_Thick_shake=239

        self.SubCatMocktails=['Select Item','Virgin Mojito',
                                'Blue Blast',
                                'Black Moon Lagoon',
                                'Green Punch',
                                'Berry Lagoon',
                                'Fresh Lime Soda',
                                'Fresh Lime Soda Sweet & Salt']

        self.Virgin_Mojito=129
        self.Blue_Blast=129
        self.Black_Moon_Lagoon=129
        self.Green_Punch=129
        self.Berry_Lagoon=159
        self.Fresh_Lime_Soda=109
        self.Fresh_Lime_Soda_Sweet_Salt=119

        self.SubCatVegSandwich=['Select Item','Grilled Veg Club Sandwich',
                                'Grilled Veg Sandwich',
                                'Grilled Spicy Aloo Tikka Sandwich',
                                'Grilled Mushroom & Vegetable Sandwich',
                                'Grilled Veg Mexican Sandwich',
                                'Cheese & Corn Sandwich',
                                'Fresh Cut Cucumber Mint Sandwich',
                                'Chilli & Cheese Sandwich',
                                'Bombay Veg Grill Sandwich',
                                'Grilled Veg Club Paneer Sandwich',
                                'Grilled Veg Paneer Sandwich']


        self.Grilled_Veg_Club_Sandwich=149
        self.Grilled_Spicy_Aloo_Tikka_Sandwich=139
        self.Grilled_Mushroom_Vegetable_Sandwich=139
        self.Grilled_Veg_Mexican_Sandwich=139
        self.Grilled_Veg_Sandwich=129
        self.Cheese_Corn_Sandwich=139
        self.Fresh_Cut_Cucumber_Mint_Sandwich=139
        self.Chilli_Cheese_Sandwich=139
        self.Bombay_Veg_Grill_Sandwich=149
        self.Grilled_Veg_Club_Paneer_Sandwich=209
        self.Grilled_Veg_Paneer_Sandwich=169


        self.SubCatNonVegSandwich=['Select Item','Grilled Egg Sandwich',
                                    'Grilled Chicken Club Sandwich',
                                    'Grilled Mexican Chicken Sandwich',
                                    'Cheese & Jalapeno Chicken Sandwich',
                                    'Grilled Chicken Sandwich',
                                    'Grilled Chicken Overloaded Sandwich']

        self.Grilled_Egg_Sandwich=139
        self.Grilled_Chicken_Club_Sandwich=199
        self.Grilled_Mexican_Chicken_Sandwich=169
        self.Cheese_Jalapeno_Chicken_Sandwich=179
        self.Grilled_Chicken_Sandwich=149
        self.Grilled_Chicken_Overloaded_Sandwich=209
            
        self.SubCatFalooda = ['Select Item','Falooda With Ice Cream',
                                'Kulfi Falooda',
                                'Pista Falooda',
                                'Fruity Falooda',
                                'Royal Falooda',
                                'Kashmiri Falooda']
        self.Falooda_With_Ice_Cream=169
        self.Kulfi_Falooda=189
        self.Pista_Falooda=189
        self.Fruity_Falooda=209
        self.Royal_Falooda=209
        self.Kashmiri_Falooda=209



        self.SubCatSplIceCream = ['Select Item','Chocolate Fudge',
                                'Butterscotch Fudge',
                                'Nutella Fudge',
                                'Black Current Fudge',
                                'Gudbud',
                                'Royal Day Sunday',
                                'Death By Chocolate',
                                'Banana Split',
                                'Strawberry Passion',
                                'Dry Fruit Sundae',
                                'Almond Fudge',
                                'Brownie Fudge',
                                'Brownie Bomber',
                                'Nutella Brownie']


        self.Chocolate_Fudge=159
        self.Butterscotch_Fudge=159
        self.Nutella_Fudge=159
        self.Black_Current_Fudge=159
        self.Gudbud=179
        self.Royal_Day_Sunday=179
        self.Death_By_Chocolate=189
        self.Banana_Split=179
        self.Strawberry_Passion=179
        self.Dry_Fruit_Sundae=199
        self.Almond_Fudge=199
        self.Brownie_Fudge=169
        self.Brownie_Bomber=179
        self.Nutella_Brownie=189

        self.SubCatColdCoffe=['Select Item','Cold Coffee',
                                'Chocolate Coffee',
                                'ButterScotch Coffee',
                                'Mud Coffee']

        self.Cold_Coffee=169
        self.Chocolate_Coffee=179
        self.Butterscotch_Coffee=179
        self.Mud_Coffee=199

        self.SubCatVegNachos=['Select Item','Plain Nachos', 'Peri-Peri Nachos', 'Cheese Nachos', 'Jalapeno & Herb Nachos','Baked Vegetables Nachos']

        self.Plain_Nachos=119
        self.Peri_Peri_Nachos=129
        self.Cheese_Nachos=149
        self.Jalapeno_Herb_Nachos=159
        self.Baked_Vegetables_Nachos=159

        self.SubCatNonVegNachos=['Select Item','Chicken Loaded Nachos',
                                'Peri Peri Chicken Nachos',
                                'Cheese Chicken Nachos',
                                'Jalapeno Chicken Nachos',
                                'Baked Chicken Nachos']
        self.Chicken_Loaded_Nachos=199
        self.Peri_Peri_Chicken_Nachos=199
        self.Cheese_Chicken_Nachos=199
        self.Jalapeno_Chicken_Nachos=219
        self.Baked_Chicken_Nachos=219

        self.SubCatSnack = ['Select Item','Plain French Fries',
                            'Peri- Peri French Fries',
                            'Spicy French Fries',
                            'Peri- Peri Chicken French Fries',
                            'Veg Nuggets',
                            'Chicken Nuggets',
                            'Jalapeno Cheesy Bites',
                            'Potato Wedges',
                            'Cheese & Corn Nuggets',
                            'Chicken Fingers',
                            'Cheese Potato Shots',
                            'Cheese French Fries']

        self.Plain_French_Fries=99
        self.Peri_Peri_French_Fries=109
        self.Spicy_French_Fries=109
        self.Peri_Peri_Chicken_French_Fries=139
        self.Veg_Nuggets=109
        self.Chicken_Nuggets=149
        self.Jalapeno_Cheesy_Bites=139
        self.Potato_Wedges=139
        self.Chicken_fingers=149
        self.Cheese_Corn_Nuggets=129
        self.Cheese_Potato_Shots=139
        self.Cheese_French_Fries=139

        img=Image.open('logo.jpg')
        img=img.resize((100,80))

        self.photoimg=ImageTk.PhotoImage(img)

        lbl_title=Label(self.root,text="Welcome To The LassiDay",font=('times new roman',35,"bold italic"),bg='black',fg='white')
        lbl_title.place(x=0,y=0,width=1520,height=100)

        lbl_img = Label(self.root,image=self.photoimg)
        lbl_img.place(x=1050,y=10,width=100,height=80)

        Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg='white')
        Main_Frame.place(x=0,y=100,width=1530,height=700)

        def time():
            string=strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000,time)

        lbl=Label(Main_Frame,font=('times new roman',16,'bold'),background='white',fg='blue')
        lbl.place(x=0,y=0,width=120,height=50)
        time()

        # Customer LabelFrame
        Cust_Frame=LabelFrame(Main_Frame,text='Customer',font=('arial',14,"bold"),bg='white',fg='red')
        Cust_Frame.place(x=100,y=45,width=660,height=140)

        self.lbl_name=Label(Cust_Frame,text='Name',font=('arial',12,"bold"),bg='white',fg='black')
        self.lbl_name.grid(row=0,column=0,sticky=W,padx=5,pady=10)

        self.entry_name=ttk.Entry(Cust_Frame,textvariable=self.C_name,font=('arial',12,"bold"),width=24)
        self.entry_name.grid(row=0,column=1)

        self.lbl_mob=Label(Cust_Frame,text='Mobile No.',font=('arial',12,"bold"),bg='white',fg='black')
        self.lbl_mob.grid(row=1,column=0,sticky=W,padx=5,pady=10)

        self.entry_mob=ttk.Entry(Cust_Frame,textvariable=self.C_phon,font=('arial',12,"bold"),width=24)
        self.entry_mob.grid(row=1,column=1)

        # Product LabelFrame
        Prod_Frame=LabelFrame(Main_Frame,text='Items',font=('arial',14,"bold"),bg='white',fg='red')
        Prod_Frame.place(x=100,y=200,width=660,height=140)

        # Item Category
        self.lblCategory=Label(Prod_Frame,font=('arial',12,"bold"),bg='white',text='Select Category',bd=4)
        self.lblCategory.grid(row=0,column=0,sticky=W,padx=5,pady=10)

        self.Combo_Category=ttk.Combobox(Prod_Frame,state='readonly',value=self.Category,font=('arial',12,"bold"),width=24)
        self.Combo_Category.current(0)
        self.Combo_Category.grid(row=0,column=1,sticky=W,padx=5,pady=10)

        self.Combo_Category.bind("<<ComboboxSelected>>",self.Categories)


        # Item Sub Category
        self.lblSubCategory=Label(Prod_Frame,font=('arial',12,"bold"),bg='white',text='Select Sub Category',bd=4)
        self.lblSubCategory.grid(row=1,column=0,sticky=W,padx=5,pady=10)

        self.ComboSubCategory=ttk.Combobox(Prod_Frame,textvariable=self.product,state='readonly',font=('arial',12,"bold"),width=24)
        self.Combo_Category.current(0)
        self.ComboSubCategory.grid(row=1,column=1,sticky=W,padx=5,pady=10)

        self.ComboSubCategory.bind("<<ComboboxSelected>>",self.price)

        # Price
        self.lblPrice=Label(Prod_Frame,font=('arial',12,"bold"),bg='white',text='Price',bd=4)
        self.lblPrice.grid(row=0,column=2)

        self.ComboPrice=ttk.Combobox(Prod_Frame,state='readonly',textvariable=self.prices,font=('arial',12,"bold"),width=10)
        self.ComboPrice.grid(row=0,column=3,sticky=W,padx=5,pady=10)

        #Qty
        self.lblQty=Label(Prod_Frame,font=('arial',12,"bold"),bg='white',text='Quantity',bd=4)
        self.lblQty.grid(row=1,column=2)

        self.ComboQty=ttk.Entry(Prod_Frame,textvariable=self.qty,font=('arial',12,"bold"),width=12)
        self.ComboQty.grid(row=1,column=3,sticky=W,padx=5,pady=10)


        # Add To Cart and Remove from Cart in Main_Frame
        self.AddtoCart=Button(Main_Frame,command=self.AddItem,width=20,height=3,text='Add to Cart',font=('arial',12,"bold"),bg='green',fg='white',cursor='hand2')
        self.AddtoCart.place(x=150,y=380)

        self.RemoveFromList=Button(Main_Frame,command=self.Remove_Items,width=20,height=3,text='Remove From List',font=('arial',12,"bold"),bg='red',fg='white',cursor='hand2')
        self.RemoveFromList.place(x=500,y=380)

        # Bill Area (Extreme Right)
        RightLabelFrame=LabelFrame(Main_Frame,text="Bill Area",font=('arial',14,"bold"),bg='white',fg='red')
        RightLabelFrame.place(x=900,y=45,width=380,height=450)

        scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
        self.textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg="white",fg='blue',font=('arial',12))
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)

        # Bill Counter LabelFrame
        Bottom_Frame=LabelFrame(Main_Frame,text='Bill Counter',font=('arial',12,"bold"),bg='white',fg='red')
        Bottom_Frame.place(x=0,y=500,width=1520,height=120)

        self.lblSubTotal=Label(Bottom_Frame,font=('arial',10,"bold"),bg='white',text='Sub Total',bd=4)
        self.lblSubTotal.grid(row=0,column=1)

        self.EntrySubTotal=ttk.Entry(Bottom_Frame,textvariable=self.sub_total,font=('arial',10,"bold"),width=20)
        self.EntrySubTotal.grid(row=0,column=2,sticky=W,padx=5,pady=2)

        self.lbl_tax=Label(Bottom_Frame,font=('arial',10,"bold"),bg='white',text='Govt. Tax',bd=4)
        self.lbl_tax.grid(row=1,column=1)

        self.txt_tax=ttk.Entry(Bottom_Frame,textvariable=self.tax_input,font=('arial',10,"bold"),width=20)
        self.txt_tax.grid(row=1,column=2,sticky=W,padx=5,pady=2)

        self.lblAmountTotal=Label(Bottom_Frame,font=('arial',10,"bold"),bg='white',text='Total Amount',bd=4)
        self.lblAmountTotal.grid(row=2,column=1)

        self.txtAmountTotal=ttk.Entry(Bottom_Frame,textvariable=self.total,font=('arial',10,"bold"),width=20)
        self.txtAmountTotal.grid(row=2,column=2,sticky=W,padx=5,pady=2)

        # Button Frame
        Btn_Frame=Frame(Bottom_Frame,bd=2,bg='white')
        Btn_Frame.place(x=320,y=0)

        self.BtnGenerateBill=Button(Btn_Frame,command=self.gen_bill,width=14,height=2,text='Generate Bill',font=('arial',12,"bold"),bg='black',fg='white',cursor='hand2')
        self.BtnGenerateBill.grid(row=0,column=0,padx=15,pady=15)

        self.BtnUPI=Button(Btn_Frame,command=self.Card_UPI,width=14,height=2,text='Card/UPI',font=('arial',12,"bold"),bg='black',fg='white',cursor='hand2')
        self.BtnUPI.grid(row=0,column=2,padx=15,pady=15)

        self.BtnCash=Button(Btn_Frame,width=14,command=self.Cash_Payment,height=2,text='Cash',font=('arial',12,"bold"),bg='black',fg='white',cursor='hand2')
        self.BtnCash.grid(row=0,column=3,padx=15,pady=15)

        self.BtnPrint=Button(Btn_Frame,command=self.iprint,width=14,height=2,text='Print',font=('arial',12,"bold"),bg='black',fg='white',cursor='hand2')
        self.BtnPrint.grid(row=0,column=4,padx=15,pady=15)

        self.BtnClear=Button(Btn_Frame,command=self.clear,width=14,height=2,text='Clear',font=('arial',12,"bold"),bg='black',fg='white',cursor='hand2')
        self.BtnClear.grid(row=0,column=5,padx=15,pady=15)

        self.BtnExit=Button(Btn_Frame,command=self.cancel,width=18,height=2,text='Change Payment-Mode',font=('arial',11,"bold"),bg='Red',fg='white',cursor='hand2')
        self.BtnExit.grid(row=0,column=6,padx=15,pady=15)


        # Developer Info
        Developer_lbl_title=Label(Main_Frame,text="Developer Info: Team ihtihaS (Anand - 7389536536, Gokul - 9010203030)",font=('times new roman',18,"bold"),bg='black',fg='white')
        Developer_lbl_title.place(x=0,y=640,width=1520,height=40)

        self.welcome()

        self.Ordered_Items = []
        self.list_tot_prices=[]
        self.Tax=0
        self.Tax_List =[]
        self.Total_Prices=[]
    
    #====================== Function Declaration =========================

    def welcome(self):
        self.textarea.delete(1.0,END)
        self.textarea.insert(END,"\t           The LassiDay\n")
        self.textarea.insert(END,"\n           3rd Floor, Atrium Mall,Gachibowli")
        self.textarea.insert(END,"\n              Hyderabad, Telangana, 500081")
        self.textarea.insert(END,"\n                     Contact:8885022099 ")

        self.textarea.insert(END,f"\n\nDate : {str((datetime.today().strftime('%d-%m-%Y')))}\t\t\t  Time : {str((datetime.today().strftime('%H:%M')))}")


        self.textarea.insert(END,f"\n\nBill No : {self.bill_no.get()}")

        self.textarea.insert(END,"\n\n======================================")

        gap=' '*3
        self.textarea.insert(END,f"\n{'   Item Name'}\t{gap}{gap}{gap}{gap}{gap}{'Qty':3s}{gap}{'Rate':3s}{gap}{'Price':4s}")
        self.textarea.insert(END,"\n======================================\n")
        
    def AddItem(self):
        
        self.n=self.prices.get()
        self.m=self.qty.get()*self.n
        self.list_tot_prices.append(self.m)

        if self.product.get()=="" or self.prices.get()==0:
            messagebox.showerror('Error','Please Select Any Item')
        else:
            self.Ordered_Items.append(self.product.get())
            gap=" "*3

            self.textarea.insert(END,f"\n{self.product.get()}\n")
            self.textarea.insert(END,f"\t\t\t{self.qty.get():3d}{gap}{self.prices.get():3d}{gap}{self.m:4}\n")


            self.sub_total.set(str('Rs.%.2f'%(sum(self.list_tot_prices))))

            tot_tax = sum(self.list_tot_prices)*self.Tax/100
            self.Tax_List.append(tot_tax)
            self.tax_input.set(str('%.2f'%(tot_tax)))

            tot_price = max(self.Tax_List) + sum(self.list_tot_prices)
            self.total.set(str('Rs.%.2f'%(tot_price)))

        self.prices.set(0)
        self.qty.set(0)


    def Remove_Items(self):

        if len(self.list_tot_prices)==0 or len(self.Tax_List)==0 or len(self.Ordered_Items)==0:
            messagebox.showerror("Error","No Items in the Cart")

        else:
            self.list_tot_prices.pop()
            self.Tax_List.pop()
            self.Ordered_Items.pop()

            self.sub_total.set(str('Rs.%.2f'%(sum(self.list_tot_prices))))

            tot_tax = sum(self.list_tot_prices)*self.Tax/100
            self.Tax_List.append(tot_tax)
            self.tax_input.set(str('Rs.%.2f'%(tot_tax)))

            tot_price = self.Tax_List[-1] + sum(self.list_tot_prices)
            self.total.set(str('Rs.%.2f'%(tot_price)))
   
            self.textarea.delete("end-2l","end-1l")
            self.textarea.delete("end-2l","end-1l")
            self.textarea.delete("end-2l","end-1l")

    def gen_bill(self):
        if self.product.get()=="" or self.total.get()=="":
            messagebox.showerror('Error','Please Add any Item To Cart')
        else:
            text=self.textarea.get(15.0,(30.0+float(len(self.Ordered_Items)+4.0)*2))
            self.welcome()
            self.textarea.insert(END,"\n"+text)
            
            self.textarea.insert(END,"\n\n======================================")

            self.textarea.insert(END,f"\nSub Amount:\t\t{self.sub_total.get()}")

            gst_amt = float(self.tax_input.get())/2
            gst_amt = str(gst_amt).split(".")
            gst_amt = gst_amt[0] + "."+gst_amt[1][:2]
            self.textarea.insert(END,f"\nTax Amount\nSGST (2.5%):\t\tRs.{gst_amt}")
            self.textarea.insert(END,f"\nCGST (2.5%):\t\tRs.{gst_amt}")
            self.textarea.insert(END,f"\n\nTot Amount:\t\t{self.total.get()}")

            if len(self.C_name.get())>1 and len(self.C_phon.get())>1:
                tot_pr = self.total.get()[3:]
                total_after_disc = float(tot_pr) - (0.10*float(tot_pr))
                self.total.set(str('Rs.%.2f'%(total_after_disc)))

                self.textarea.insert(END,f"\nDiscount(10%):\t\t{str('Rs%.2f'%(0.10*float(tot_pr)))}")
                self.textarea.insert(END,f"\n\nTot Amount:\t\t{self.total.get()}")


            self.textarea.insert(END,'\n')
            self.bill_generated = True

    def Card_UPI(self):

        if len(self.Ordered_Items)>0:

            if self.bill_generated:

                if self.cash_transaction==False:

                    self.card_upi='Card/UPI'

                    self.card_transaction=True
                    
                    self.textarea.insert(END,f"\nPayment Mode:\t\t{self.card_upi}")
                    self.textarea.insert(END,'\n')

                else:
                    messagebox.showerror("Error",'Payment Mode is already Cash.Try Changing the Mode')

                
            else:
                messagebox.showerror("Error",'Bill is not yet Generated')


        else:
            messagebox.showerror("Error",'No Items in the Cart')


    def Cash_Payment(self):

        if len(self.Ordered_Items)>0:
            if self.bill_generated:
                if self.card_transaction==False:
                    self.Cash='Cash'

                    self.cash_transaction=True
                    
                    
                    self.textarea.insert(END,f"\nPayment Mode:\t\t{self.Cash}")
                    self.textarea.insert(END,'\n')

                else:
                    messagebox.showerror("Error",'Payment Mode is already Card/UPI.Try Changing the Mode')

            else:
                messagebox.showerror("Error",'Bill is not yet Generated')

        else:
            messagebox.showerror("Error",'No Items in the Cart')

    def iprint(self):

        if len(self.Ordered_Items)>0:
            if (self.cash_transaction==True or self.card_transaction==True):

                if self.cash_transaction==True:
                    year = str((datetime.date(datetime.now()))).split('-')[0]
                    month = str((datetime.date(datetime.now()))).split('-')[1] 
                    datetime_object = datetime.strptime(month, "%m")
                    month = datetime_object.strftime("%b")

                    lis = str((datetime.date(datetime.now()))).split('-')
                    req_name = lis[2]+'-'+lis[1]+'-'+lis[0]

                    req_path_for_excel = 'Bills/'+year+'/'+month+'/'+req_name+'/'+req_name+' Cash.xlsx'

                    df = pd.read_excel(req_path_for_excel)
                    df.drop(df.tail(3).index,inplace=True)
                    df.to_excel(req_path_for_excel, index=False)

                    bill_amt = round(float(self.total.get()[3:]),2)

                    data={'Name':[self.C_name.get(),np.NaN,np.NaN],'Contact':[self.C_phon.get(),np.NaN,np.NaN],'Items':[self.Ordered_Items,np.NaN,np.NaN],
                        'Bill No':[self.bill_no.get(),np.NaN,np.NaN],'Bill Amount':[bill_amt,np.NaN,np.NaN],'Mode of Payment':[self.Cash,np.NaN,np.NaN]}

                    new_df = pd.DataFrame(data)
                    tot = {'Bill No':['Total Amount'],
                        'Bill Amount':[np.sum(df['Bill Amount'].dropna(how='all'))+np.sum(new_df['Bill Amount'].dropna(how='all'))]}

                    new_df=pd.concat([new_df,pd.DataFrame(tot)])
                    new_df.fillna('',inplace=True)

                    df_excel = pd.read_excel(req_path_for_excel)
                    result = pd.concat([df_excel, new_df], ignore_index=True)
                    result.fillna("",inplace=True)
                    result.to_excel(req_path_for_excel, index=False)

                if self.card_transaction==True:
                    year = str((datetime.date(datetime.now()))).split('-')[0]
                    month = str((datetime.date(datetime.now()))).split('-')[1] 
                    datetime_object = datetime.strptime(month, "%m")
                    month = datetime_object.strftime("%b")

                    lis = str((datetime.date(datetime.now()))).split('-')
                    req_name = lis[2]+'-'+lis[1]+'-'+lis[0]
                    req_path_for_excel = 'Bills/'+year+'/'+month+'/'+req_name+'/'+req_name+' Card (or) UPI.xlsx'

                    df = pd.read_excel(req_path_for_excel)
                    df.drop(df.tail(3).index,inplace=True)
                    df.to_excel(req_path_for_excel, index=False)

                    bill_amt = round(float(self.total.get()[3:]),2)

                    data={'Name':[self.C_name.get(),np.NaN,np.NaN],'Contact':[self.C_phon.get(),np.NaN,np.NaN],'Items':[self.Ordered_Items,np.NaN,np.NaN],
                        'Bill No':[self.bill_no.get(),np.NaN,np.NaN],'Bill Amount':[bill_amt,np.NaN,np.NaN],'Mode of Payment':[self.card_upi,np.NaN,np.NaN]}

                    new_df = pd.DataFrame(data)
                    tot = {'Bill No':['Total Amount'],
                        'Bill Amount':[np.sum(df['Bill Amount'].dropna(how='all'))+np.sum(new_df['Bill Amount'].dropna(how='all'))]}

                    new_df=pd.concat([new_df,pd.DataFrame(tot)])
                    new_df.fillna('',inplace=True)

                    df_excel = pd.read_excel(req_path_for_excel)
                    result = pd.concat([df_excel, new_df], ignore_index=True)
                    result.fillna("",inplace=True)
                    result.to_excel(req_path_for_excel, index=False)



                self.textarea.insert(END,"\n======================================")
                self.textarea.insert(END,"\n                     Thank You & Visit Again")
                self.textarea.insert(END,"\n======================================")
                self.textarea.insert(END,"\n                  Developer Info:Team ihtihaS")
                self.textarea.insert(END,"\n          Anand-7389536536,Gokul-9010203030")


                self.printed=True

                self.bill_data=self.textarea.get(1.0,END)

                year = str((datetime.date(datetime.now()))).split('-')[0]
                month = str((datetime.date(datetime.now()))).split('-')[1] 
                datetime_object = datetime.strptime(month, "%m")
                month = datetime_object.strftime("%b")

                lis = str((datetime.date(datetime.now()))).split('-')
                req_name = lis[2]+'-'+lis[1]+'-'+lis[0]
                req_path = 'Bills/'+year+'/'+month+'/'+req_name

                f1=open(req_path+'/'+str(self.bill_no.get())+'.txt','w')
                f1.write(self.bill_data)
                f1.close()

                q=self.textarea.get(1.0,END)
                filename=tempfile.mktemp('.txt')
                open(filename,'w').write(q)
                os.startfile(filename,'Print')

                ## Our Copy
                f1_our = open(req_path+'/'+str(self.bill_no.get())+'_self.txt','w')
                f1_our.write("\t           The LassiDay\n")
                f1=open(req_path+'/'+str(self.bill_no.get())+'.txt','r')
                lines = f1.readlines()
                for i in lines[6:]:
                    if 'Sub' in i:
                        break
                    else:
                        f1_our.write(i)
                f1.close()
                f1_our.close()

                f1_our = open(req_path+'/'+str(self.bill_no.get())+'_self.txt','r')
                filename = tempfile.mktemp('.txt')
                f1_our=f1_our.read()
                open(filename,'w').write(f1_our)
                os.startfile(filename,'Print')

                req_path_for_excel = 'Bills/'+year+'/'+month+'/'+req_name+'/'+req_name+' Daily SettleMent.xlsx'

                df = pd.read_excel(req_path_for_excel)
                df.drop(df.tail(3).index,inplace=True)
                df.to_excel(req_path_for_excel, index=False)

                bill_amt = round(float(self.total.get()[3:]),2)

                if self.cash_transaction==True:
                    data={'Name':[self.C_name.get(),np.NaN,np.NaN],'Contact':[self.C_phon.get(),np.NaN,np.NaN],'Items':[self.Ordered_Items,np.NaN,np.NaN],
                        'Bill No':[self.bill_no.get(),np.NaN,np.NaN],'Bill Amount':[bill_amt,np.NaN,np.NaN],'Mode of Payment':[self.Cash,np.NaN,np.NaN]}
                elif self.card_transaction==True:
                    data={'Name':[self.C_name.get(),np.NaN,np.NaN],'Contact':[self.C_phon.get(),np.NaN,np.NaN],'Items':[self.Ordered_Items,np.NaN,np.NaN],
                        'Bill No':[self.bill_no.get(),np.NaN,np.NaN],'Bill Amount':[bill_amt,np.NaN,np.NaN],'Mode of Payment':[self.card_upi,np.NaN,np.NaN]}

                new_df = pd.DataFrame(data)
                tot = {'Bill No':['Total Amount'],
                    'Bill Amount':[np.sum(df['Bill Amount'].dropna(how='all'))+np.sum(new_df['Bill Amount'].dropna(how='all'))]}

                new_df=pd.concat([new_df,pd.DataFrame(tot)])
                new_df.fillna('',inplace=True)

                df_excel = pd.read_excel(req_path_for_excel)
                result = pd.concat([df_excel, new_df], ignore_index=True)
                result.fillna("",inplace=True)
                result.to_excel(req_path_for_excel, index=False)

                self.clear()

            else:
                messagebox.showerror('Error','Select the Payment Mode')
            
        else:
            messagebox.showerror('Error','No Items in the Cart')

    def clear(self):

        self.Ordered_Items=[]
        self.list_tot_prices=[]
        self.Tax=0
        self.Tax_List =[]
        self.Total_Prices=[]
        self.bill_generated=False
        self.cash_transaction=False
        self.card_transaction=False
        self.printed=False
        self.textarea.delete(1.0,END)
        self.C_name.set("")
        self.C_phon.set("")
        bill_no_format=strftime('%H:%M:%S %p')
        bill_no_format = bill_no_format.split(' ')
        bill_no_format=''.join(bill_no_format[0].split(':'))
        self.bill_no.set(bill_no_format)
        self.search_bill.set("")
        self.product.set("")
        self.prices.set(0)
        self.qty.set(0)
        self.l=[0]
        self.total.set("")
        self.sub_total.set("")
        self.tax_input.set("")
        self.Cash=''
        self.card_upi=''
        self.welcome()
    
    def cancel(self):

        if (self.cash_transaction==True or self.card_transaction==True):
            if self.printed==False:
                self.card_transaction=False
                self.cash_transaction=False
            
                self.textarea.delete("end-2l","end-1l")

            else:
                messagebox.showerror('Error','Bill Already Printed or Bill Not Generated')
        else:
            messagebox.showerror('Error','Bill Already Printed or Bill Not Generated')



    def Categories(self,event=""):

        if self.Combo_Category.get()=='Juice & Fruit Salad':
            self.ComboSubCategory.config(value=self.SubCatJuiceFruit)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Pasta':
            self.ComboSubCategory.config(value=self.SubCatPasta)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Lassi':
            self.ComboSubCategory.config(value=self.SubCatLassi)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='ThickShakes':
            self.ComboSubCategory.config(value=self.SubCatThickShakes)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Mocktails':
            self.ComboSubCategory.config(value=self.SubCatMocktails)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Veg SandWich':
            self.ComboSubCategory.config(value=self.SubCatVegSandwich)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Non-Veg SandWich':
            self.ComboSubCategory.config(value=self.SubCatNonVegSandwich)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Falooda':
            self.ComboSubCategory.config(value=self.SubCatFalooda)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Special IceCream':
            self.ComboSubCategory.config(value=self.SubCatSplIceCream)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Cold Coffee':
            self.ComboSubCategory.config(value=self.SubCatColdCoffe)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Veg Nachos':
            self.ComboSubCategory.config(value=self.SubCatVegNachos)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Non-Veg Nachos':
            self.ComboSubCategory.config(value=self.SubCatNonVegNachos)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Snack':
            self.ComboSubCategory.config(value=self.SubCatSnack)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Spl. SandWich':
            self.ComboSubCategory.config(value=self.SubCatSplSandwich)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Combos for 1':
            self.ComboSubCategory.config(value=self.SubCatCombos_for_1)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Combos for 2':
            self.ComboSubCategory.config(value=self.SubCatCombos_for_2)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Add Ons':
            self.ComboSubCategory.config(value=self.SubCatAdd_Ons)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Biryani':
            self.ComboSubCategory.config(value=self.SubCatBiryani)
            self.ComboSubCategory.current(0)

        if self.Combo_Category.get()=='Special Items':
            self.ComboSubCategory.config(value=self.SubCatSpl_Items)
            self.ComboSubCategory.current(0)
        
        
    def price(self,event=""):

        # Special Items
        if self.ComboSubCategory.get()=='Chicken Jumbo Nuggets':
            self.ComboPrice.config(value=self.Chick_Jumbo_Nuggets)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chicken Wings':
            self.ComboPrice.config(value=self.Chicken_Wings)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chicken Garlic Fingers':
            self.ComboPrice.config(value=self.Chicken_Garlic_Fingers)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chicken Hot & Spicy Seekh Kebab':
            self.ComboPrice.config(value=self.Chick_Hot_Spicy_Seekh_Kebab)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Veg Fingers':
            self.ComboPrice.config(value=self.Veg_Fingers)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Biryani
        if self.ComboSubCategory.get()=='Chicken Biryani':
            self.ComboPrice.config(value=self.Chick_Bir)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Add Ons
        if self.ComboSubCategory.get()=='Water Bottle':
            self.ComboPrice.config(value=self.wb)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Extra Mayonnaise':
            self.ComboPrice.config(value=self.Em)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Combos for 1
        if self.ComboSubCategory.get()=='Veg Sandwich+Vanilla ThickShake':
            self.ComboPrice.config(value=self.vegsw_Vts)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Paneer SandWich+Pista ThickShake':
            self.ComboPrice.config(value=self.Psw_Pts)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chicken Sandwich + ButterScotch ThickShake':
            self.ComboPrice.config(value=self.Csw_BSts)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Cheese & Jalapeno Chicken Sandwich+Kitkat ThickShake':
            self.ComboPrice.config(value=self.CJCsw_KKts)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Veg Sandwich+Peri Peri French Fries+Virgin Mojito':
            self.ComboPrice.config(value=self.Vsw_PPff_Vm)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Paneer Sandwich+Peri Peri French Fries+Virgin Mojito':
            self.ComboPrice.config(value=self.Psw_PPff_Vm)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Chicken Sandwich+Chicken Nuggets+Virgin Mojito':
            self.ComboPrice.config(value=self.Csw_Cn_Vm)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Cheese & Jalapeno Chicken Sandwich+Chicken Nuggets+Virgin Mojito':
            self.ComboPrice.config(value=self.CJCsw_Cn_Vm)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Loaded Chicken Nachos+Virgin Mojito':
            self.ComboPrice.config(value=self.CLn_Vm)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Baked Vegetable Nachos+Virgin Mojito':
            self.ComboPrice.config(value=self.BVn_Vm)
            self.ComboPrice.current(0)
            self.qty.set(1)


        # Combos for 2

        if self.ComboSubCategory.get()=='2 VegSandwich+2 Virgin Mojito+Peri Peri French Fries':
            self.ComboPrice.config(value=self.Vsw2_2Vm_PPff)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='2 Chicken Sandwich+2 Virgin Mojito+Chicken Nuggets':
            self.ComboPrice.config(value=self.Csw2_2Vm_Cn)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Paneer Sandwich+Chicken Sandwich+2Virgin Mojito+Peri Peri French Fries':
            self.ComboPrice.config(value=self.Psw_Csw_2Vm_PPff)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Paneer Sandwich+Chicken Sandwich+2Virgin Mojito+Chicken Nuggets':
            self.ComboPrice.config(value=self.Psw_Csw_2Vm_Cn)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Juices And Fruit Salad
        if self.ComboSubCategory.get()=='ABC (Apple, BeetRoot, Carrot)':
            self.ComboPrice.config(value=self.ABC)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Carrot-BeetRoot Juice':
            self.ComboPrice.config(value=self.Carrot_Beetroot_Juice)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='BeetRoot Juice':
            self.ComboPrice.config(value=self.Beetroot_Juice)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Apple Smoothie':
            self.ComboPrice.config(value=self.Apple_Smoothie)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Carrot Banana Smoothie':
            self.ComboPrice.config(value=self.Carrot_Banana_Smoothie)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Fruit Salad':
            self.ComboPrice.config(value=self.Fruit_Salad)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Fruit Salad With IceCream':
            self.ComboPrice.config(value=self.Fruit_Salad_With_Icecream)
            self.ComboPrice.current(0)
            self.qty.set(1)



        # Pasta
        if self.ComboSubCategory.get()=='Creamy Mushroom Chicken Pasta':
            self.ComboPrice.config(value=self.Creamy_Mushroom_Chicken_Pasta)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Creamy Mushroom Veg Pasta':
            self.ComboPrice.config(value=self.Creamy_Mushroom_Veg_Pasta)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Creamy Mushroom Paneer Pasta':
            self.ComboPrice.config(value=self.Creamy_Mushroom_Paneer_Pasta)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Creamy Mushroom Pasta':
            self.ComboPrice.config(value=self.Creamy_Mushroom_Pasta)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Creamy Mushroom Egg Pasta':
            self.ComboPrice.config(value=self.Creamy_Mushroom_Egg_Pasta)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Lassi
        if self.ComboSubCategory.get()=='Sweet Lassi':
            self.ComboPrice.config(value=self.Sweet_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Butter Scotch Lassi':
            self.ComboPrice.config(value=self.Butter_Scotch_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Mango Lassi':
            self.ComboPrice.config(value=self.Mango_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Banana Lassi':
            self.ComboPrice.config(value=self.Banana_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Strawberry Lassi':
            self.ComboPrice.config(value=self.Strawberry_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Pista Lassi':
            self.ComboPrice.config(value=self.Pista_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Kiwi Lassi':
            self.ComboPrice.config(value=self.Kiwi_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chocolate Lassi':
            self.ComboPrice.config(value=self.Chocolate_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Kesar Lassi':
            self.ComboPrice.config(value=self.Kesar_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Royal Lassi':
            self.ComboPrice.config(value=self.Royal_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Dry Fruit Lassi':
            self.ComboPrice.config(value=self.Dry_Fruit_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Fruit & Cream Lassi':
            self.ComboPrice.config(value=self.Fruit_Cream_Lassi)
            self.ComboPrice.current(0)
            self.qty.set(1)

        
        # Spl SandWich
        if self.ComboSubCategory.get()=='Nutella Banana Sandwich':
            self.ComboPrice.config(value=self.Nutella_Banana_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Peanut Butter Sandwich':
            self.ComboPrice.config(value=self.Peanut_Butter_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chocolate Sandwich':
            self.ComboPrice.config(value=self.Chocolate_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)


        # ThickShakes
        if self.ComboSubCategory.get()=='Very Berry Strawberry Thick Shake':
            self.ComboPrice.config(value=self.Very_Berry_Strawberry_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Vanilla Thick Shake':
            self.ComboPrice.config(value=self.Vanilla_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Body Cooler Shake':
            self.ComboPrice.config(value=self.Body_Cooler_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Oreo Thick Shake':
            self.ComboPrice.config(value=self.Oreo_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Mango Alphanso Thick Shake':
            self.ComboPrice.config(value=self.Mango_Alphanso_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chocolate Thick Shake':
            self.ComboPrice.config(value=self.Chocolate_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Banana Bonkers Thick Shake':
            self.ComboPrice.config(value=self.Banana_Bonkers_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Pista Thick Shake':
            self.ComboPrice.config(value=self.Pista_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Shake Shake Caramel Thick Shake':
            self.ComboPrice.config(value=self.Shake_Shake_Caramel_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Kesar Pista Thick Shake':
            self.ComboPrice.config(value=self.Kesar_Pista_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Choco Chip Cookies Thick Shake':
            self.ComboPrice.config(value=self.Choco_Chip_Cookies_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Hopscotch Butterscotch Thick Shake':
            self.ComboPrice.config(value=self.Hopscotch_Butterscotch_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Sharjah Thick Shake':
            self.ComboPrice.config(value=self.Sharjah_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Arabian Night Thick Shake':
            self.ComboPrice.config(value=self.Arabian_Night_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Dry Fruit Thick Shake':
            self.ComboPrice.config(value=self.Dry_Fruit_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Kaju Anjeer Thick Shake':
            self.ComboPrice.config(value=self.Kaju_Anjeer_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Dry Anjeer Thick Shake':
            self.ComboPrice.config(value=self.Dry_Anjeer_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Belgian Chocolate Thick Shake':
            self.ComboPrice.config(value=self.Belgian_Chocolate_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Kitkat Thick Shake':
            self.ComboPrice.config(value=self.Kitkat_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Snickers Thick Shake':
            self.ComboPrice.config(value=self.Snickers_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chocko Dry Fruit Thick Shake':
            self.ComboPrice.config(value=self.Chocko_Dry_Fruit_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Nutella Thick Shake':
            self.ComboPrice.config(value=self.Nutella_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Lassiday Twister Thick Shake':
            self.ComboPrice.config(value=self.Lassiday_Twister_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Ferraro Rocher Thick Shake':
            self.ComboPrice.config(value=self.Ferraro_Rocher_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Brownie Thick Shake':
            self.ComboPrice.config(value=self.Brownie_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Blue Berry Thick Shake':
            self.ComboPrice.config(value=self.Blue_Berry_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Black Current Thick Shake':
            self.ComboPrice.config(value=self.Black_Current_Thick_Shake)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Mississippi Mud Thick Shake':
            self.ComboPrice.config(value=self.Mississippi_Mud_Thick_shake)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Mocktails
        if self.ComboSubCategory.get()=='Virgin Mojito':
            self.ComboPrice.config(value=self.Virgin_Mojito)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Blue Blast':
            self.ComboPrice.config(value=self.Blue_Blast)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Black Moon Lagoon':
            self.ComboPrice.config(value=self.Black_Moon_Lagoon)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Green Punch':
            self.ComboPrice.config(value=self.Green_Punch)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Berry Lagoon':
            self.ComboPrice.config(value=self.Berry_Lagoon)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Fresh Lime Soda':
            self.ComboPrice.config(value=self.Fresh_Lime_Soda)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Fresh Lime Soda Sweet & Salt':
            self.ComboPrice.config(value=self.Fresh_Lime_Soda_Sweet_Salt)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Veg SandWich
        if self.ComboSubCategory.get()=='Grilled Veg Club Sandwich':
            self.ComboPrice.config(value=self.Grilled_Veg_Club_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Spicy Aloo Tikka Sandwich':
            self.ComboPrice.config(value=self.Grilled_Spicy_Aloo_Tikka_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Mushroom & Vegetable Sandwich':
            self.ComboPrice.config(value=self.Grilled_Mushroom_Vegetable_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Veg Mexican Sandwich':
            self.ComboPrice.config(value=self.Grilled_Veg_Mexican_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Veg Sandwich':
            self.ComboPrice.config(value=self.Grilled_Veg_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)

        if self.ComboSubCategory.get()=='Cheese & Corn Sandwich':
            self.ComboPrice.config(value=self.Cheese_Corn_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Fresh Cut Cucumber Mint Sandwich':
            self.ComboPrice.config(value=self.Fresh_Cut_Cucumber_Mint_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chilli & Cheese Sandwich':
            self.ComboPrice.config(value=self.Chilli_Cheese_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Bombay Veg Grill Sandwich':
            self.ComboPrice.config(value=self.Bombay_Veg_Grill_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Veg Club Paneer Sandwich':
            self.ComboPrice.config(value=self.Grilled_Veg_Club_Paneer_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Veg Paneer Sandwich':
            self.ComboPrice.config(value=self.Grilled_Veg_Paneer_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Non-Veg SandWich
        if self.ComboSubCategory.get()=='Grilled Egg Sandwich':
            self.ComboPrice.config(value=self.Grilled_Egg_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Chicken Club Sandwich':
            self.ComboPrice.config(value=self.Grilled_Chicken_Club_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Mexican Chicken Sandwich':
            self.ComboPrice.config(value=self.Grilled_Mexican_Chicken_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Cheese & Jalapeno Chicken Sandwich':
            self.ComboPrice.config(value=self.Cheese_Jalapeno_Chicken_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Chicken Overloaded Sandwich':
            self.ComboPrice.config(value=self.Grilled_Chicken_Overloaded_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Grilled Chicken Sandwich':
            self.ComboPrice.config(value=self.Grilled_Chicken_Sandwich)
            self.ComboPrice.current(0)
            self.qty.set(1)

        #Falooda
        if self.ComboSubCategory.get()=='Falooda With Ice Cream':
            self.ComboPrice.config(value=self.Falooda_With_Ice_Cream)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Kulfi Falooda':
            self.ComboPrice.config(value=self.Kulfi_Falooda)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Pista Falooda':
            self.ComboPrice.config(value=self.Pista_Falooda)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Fruity Falooda':
            self.ComboPrice.config(value=self.Fruity_Falooda)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Royal Falooda':
            self.ComboPrice.config(value=self.Royal_Falooda)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Kashmiri Falooda':
            self.ComboPrice.config(value=self.Kashmiri_Falooda)
            self.ComboPrice.current(0)
            self.qty.set(1)

        # Special IceCreams
        if self.ComboSubCategory.get()=='Chocolate Fudge':
            self.ComboPrice.config(value=self.Chocolate_Fudge)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Butterscotch Fudge':
            self.ComboPrice.config(value=self.Butterscotch_Fudge)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Nutella Fudge':
            self.ComboPrice.config(value=self.Nutella_Fudge)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Black Current Fudge':
            self.ComboPrice.config(value=self.Black_Current_Fudge)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Gudbud':
            self.ComboPrice.config(value=self.Gudbud)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Royal Day Sunday':
            self.ComboPrice.config(value=self.Royal_Day_Sunday)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Death By Chocolate':
            self.ComboPrice.config(value=self.Death_By_Chocolate)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Banana Split':
            self.ComboPrice.config(value=self.Banana_Split)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Strawberry Passion':
            self.ComboPrice.config(value=self.Strawberry_Passion)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Dry Fruit Sundae':
            self.ComboPrice.config(value=self.Dry_Fruit_Sundae)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Almond Fudge':
            self.ComboPrice.config(value=self.Almond_Fudge)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Brownie Fudge':
            self.ComboPrice.config(value=self.Brownie_Fudge)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Brownie Bomber':
            self.ComboPrice.config(value=self.Brownie_Bomber)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Nutella Brownie':
            self.ComboPrice.config(value=self.Nutella_Brownie)
            self.ComboPrice.current(0)
            self.qty.set(1)
        
        #Cold Coffee
        if self.ComboSubCategory.get()=='Cold Coffee':
            self.ComboPrice.config(value=self.Cold_Coffee)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chocolate Coffee':
            self.ComboPrice.config(value=self.Chocolate_Coffee)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='ButterScotch Coffee':
            self.ComboPrice.config(value=self.Butterscotch_Coffee)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Mud Coffee':
            self.ComboPrice.config(value=self.Mud_Coffee)
            self.ComboPrice.current(0)
            self.qty.set(1)


        #Veg Nachos
        if self.ComboSubCategory.get()=='Plain Nachos':
            self.ComboPrice.config(value=self.Plain_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Peri-Peri Nachos':
            self.ComboPrice.config(value=self.Peri_Peri_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Cheese Nachos':
            self.ComboPrice.config(value=self.Cheese_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Jalapeno & Herb Nachos':
            self.ComboPrice.config(value=self.Jalapeno_Herb_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Baked Vegetables Nachos':
            self.ComboPrice.config(value=self.Baked_Vegetables_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
    
        # Non Veg Nachos
        if self.ComboSubCategory.get()=='Chicken Loaded Nachos':
            self.ComboPrice.config(value=self.Chicken_Loaded_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Peri Peri Chicken Nachos':
            self.ComboPrice.config(value=self.Peri_Peri_Chicken_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Cheese Chicken Nachos':
            self.ComboPrice.config(value=self.Cheese_Chicken_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Jalapeno Chicken Nachos':
            self.ComboPrice.config(value=self.Jalapeno_Chicken_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Baked Chicken Nachos':
            self.ComboPrice.config(value=self.Baked_Chicken_Nachos)
            self.ComboPrice.current(0)
            self.qty.set(1)
            
        #Snack
        if self.ComboSubCategory.get()=='Plain French Fries':
            self.ComboPrice.config(value=self.Plain_French_Fries)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Peri- Peri French Fries':
            self.ComboPrice.config(value=self.Peri_Peri_French_Fries)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Spicy French Fries':
            self.ComboPrice.config(value=self.Spicy_French_Fries)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Peri- Peri Chicken French Fries':
            self.ComboPrice.config(value=self.Peri_Peri_Chicken_French_Fries)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Veg Nuggets':
            self.ComboPrice.config(value=self.Veg_Nuggets)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chicken Nuggets':
            self.ComboPrice.config(value=self.Chicken_Nuggets)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Jalapeno Cheesy Bites':
            self.ComboPrice.config(value=self.Jalapeno_Cheesy_Bites)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Potato Wedges':
            self.ComboPrice.config(value=self.Potato_Wedges)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Cheese & Corn Nuggets':
            self.ComboPrice.config(value=self.Cheese_Corn_Nuggets)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Chicken Fingers':
            self.ComboPrice.config(value=self.Chicken_fingers)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Cheese French Fries':
            self.ComboPrice.config(value=self.Cheese_French_Fries)
            self.ComboPrice.current(0)
            self.qty.set(1)
        if self.ComboSubCategory.get()=='Cheese Potato Shots':
            self.ComboPrice.config(value=self.Cheese_Potato_Shots)
            self.ComboPrice.current(0)
            self.qty.set(1)


if __name__ == '__main__':

    if not os.path.isdir('Bills'):
        os.mkdir('Bills')
        
    year = str((datetime.date(datetime.now()))).split('-')[0]
    month = str((datetime.date(datetime.now()))).split('-')[1] 
    datetime_object = datetime.strptime(month, "%m")
    month = datetime_object.strftime("%b")

    yearly_path = 'Bills/%s'%(year)
    yearly_dir = os.path.isdir(yearly_path)

    if not yearly_dir:
        os.mkdir(yearly_path)

    monthly_path = yearly_path+'/'+month
    monthly_dir = os.path.isdir(monthly_path)

    if not monthly_dir:
        os.mkdir(yearly_path+'/'+month)

    lis = str((datetime.date(datetime.now()))).split('-')
    req_name = lis[2]+'-'+lis[1]+'-'+lis[0]

    daily_dir_path = yearly_path+'/'+month+'/'+req_name

    if not os.path.isdir(daily_dir_path):
        os.mkdir(daily_dir_path)

        excel_files = [' Card (or) UPI.xlsx',' Cash.xlsx',' Daily SettleMent.xlsx']

        for i in excel_files:
            path=daily_dir_path+'/'+req_name+i
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'Name')
            worksheet.write('B1','Contact')
            worksheet.write('C1','Items')
            worksheet.write('D1', 'Bill No')
            worksheet.write('E1','Bill Amount')
            worksheet.write('F1','Mode of Payment')
            workbook.close()

    root=Tk()
    img=PhotoImage(file="logo.png")
    root.iconphoto(True,img)
    obj=Bill_App(root)
    root.mainloop()
