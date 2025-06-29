import tkinter as tk



class App:
    def __init__(self):
        # Initialize tkinter
        self.root = tk.Tk()

        # Font settings
        self.font_settings = ("Courier",28)


    def loop(self):
        self.root.mainloop()
        
    def run(self):
        # Start up window
        self.root.geometry("700x700")
        self.root.title("Zinc -1")
        
        # Label
        label = tk.Label(self.root, text="Test GUI",font=self.font_settings)
        label.pack(pady=10)


        # Input field
        input_field = tk.Text(self.root, height=3,font=self.font_settings)
        input_field.pack(padx=20,pady=30)

        # Button frame (weight only works when full screen)
        button_frame = tk.Frame(self.root)
        button_frame.columnconfigure(0,weight=1)
        button_frame.columnconfigure(1,weight=1)
        button_frame.columnconfigure(2,weight=1)

        # Buttons
        btn1 = tk.Button(button_frame,text="Text btn1",font= self.font_settings)
        btn1.grid(row=0,column=0,sticky=tk.W+tk.E)

        btn2 = tk.Button(button_frame,text="Text btn2",font= self.font_settings)
        btn2.grid(row=0,column=1,sticky=tk.W+tk.E)

        btn3 = tk.Button(button_frame,text="Text btn3",font= self.font_settings)
        btn3.grid(row=0,column=2,sticky=tk.W+tk.E)

        # Run buttons
        button_frame.pack(fill="x")


        self.loop()

app = App()

if __name__ == "__main__":
    app.run()
