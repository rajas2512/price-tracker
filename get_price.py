from tkinter import *
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# The wishlist link
url = ' ' #Enter your Amazon's wishlist
# The headers
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
# Requesting
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')
name = []
price = []
rating = []


class App(Frame):

    def __init__(root, master):
        Frame.__init__(root, master)
        root.grid(column=1)
        root.create_widgets()

        # The label showing the project name in the window
        label = Label(root, text="price-tracker\n")
        label.grid(row=0, column=1)
        label.configure(font=("Arial", 44))

        # Defining labels begin here #
        label_ = Label(root, text="Product Name: \n\n")
        label_.grid(row=1, column=0)
        label_.configure(font=("Arial", 20))

        label_ = Label(root, text="Actual Price: \n\n")
        label_.grid(row=1, column=1)
        label_.configure(font=("Arial", 20))

        label_ = Label(root, text="Desired Price: \n\n")
        label_.grid(row=1, column=2)
        label_.configure(font=("Arial", 20))
        # Labels end here #


    def get_values(root):
        return [float(entry.get()) for entry in root.entries]

    def calc_CR(root):
        print(root.get_values())
        df = pd.DataFrame({"Product_Name": name,
                           "Prices": price,
                           "Ratings": rating,
                           "Desired_Prices": root.get_values()})

        df["Prices"] = df['Prices'].str.replace(',', '').astype(float)

        print(df)
        print("-----------------------------")
        print("csv file is created successfully!")
        print("-----------------------------")
        df.to_csv("wishlist_products.csv", index=False)
        filee = "wishlist_products.csv"
        os.system('start %s' % filee)
        app.destroy()
        root.destroy()
        root.calc_button.destroy()
        Frame.destroy()



    def create_widgets(root):
        spans = soup.find_all('span', {'class': 'a-offscreen'})
        for span in spans:
            extract_price = span.text[1:]
            price.append(extract_price)
        # print(len(price))

        spans1 = soup.find_all('h3', {'class': "a-size-base"})
        for span in spans1:
            extract_name = span.text.replace('', '').strip()
            name.append(extract_name)
        # print(len(name))

        spans2 = soup.find_all(
            'a', {'class': "a-link-normal g-visible-js reviewStarsPopoverLink"})
        for span in spans2:
            extract_rating = span.text.replace('', '').strip()
            rating.append(extract_rating)
        # print(rating)

        # Array for the desired prices
        n = len(name)
        root.entries = []
        for i in range(n):
            s = name[i].split(' ')[0:5]
            label1 = Label(root, text=f"{' '.join(map(str, s))} ", font=(
                'calibre', 15), pady=5, justify=LEFT)
            label3 = Label(root, text=f"Rs. {price[i]} ", font=(
                'calibre', 15), pady=5, justify=LEFT)
            label2 = Label(root, text="\n")
            label1.grid(row=i + 2, column=0)
            label2.grid()
            label3.grid(row=i + 2, column=1)

            entry = Entry(root)
            entry.grid(row=i + 2, column=2)
            entry.insert(0, '0.00')
            root.entries.append(entry)

        root.calc_button = Button(
            text="submit", command=root.calc_CR, height=3, width=30)
        root.calc_button.grid(row=n + 3, column=1)


    def run(root):
        root.mainloop()


root = Tk()
root.title('price-tracker')
root.minsize(width=800, height=100)

app = App(root)
app.run()
