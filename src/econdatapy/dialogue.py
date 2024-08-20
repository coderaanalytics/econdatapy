import tkinter as tk

def econdata_credentials():
    token = None

    r = tk.Tk()
    r.title('econdata.co.za credentials')

    t = tk.Label(r, text='Enter Token Details')
    l = tk.Label(r, text='API Token')
    e = tk.Entry(r, width=25)

    def reset():
        e.delete(0, tk.END)
        return()
    def submit():
        nonlocal token
        token = e.get()
        r.destroy()
        return(token)

    b1 = tk.Button(r, text='Submit', width=25, command=submit)
    b2 = tk.Button(r, text='Reset', width=25, command=reset)

    t.grid(row=0, column=0, columnspan=2)
    l.grid(row=1, column=0, pady=10, padx=10)
    e.grid(row=1, column=1, pady=10, padx=10)
    b1.grid(row=2, column=0, pady=10, padx=10)
    b2.grid(row=2, column=1, pady=10, padx=10)

    r.mainloop()
    return(token)
