from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os 
from stegano import lsb

root=Tk()
root.title("Steganography - Hide secret Text message in an Image")
root.geometry("700x500+250+180")
root.resizable(False,False)
root.configure(bg="#2f4155")


def encrypt(msg, pr):
    msg_ascii = [ord(char) for char in msg]
    msgE = []
    j = 0
    for k in range(len(msg_ascii)):
        ascii_byte = bin(msg_ascii[k])[2:].zfill(8)  # Convert ASCII to 8-bit binary string
        pr_byte = pr[j % len(pr)]  # Repeat pattern if necessary
        pr_byte = bin(pr_byte)[2:].zfill(8)  # Convert pattern element to 8-bit binary string
        xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(ascii_byte, pr_byte))  # XOR operation
        msgE.append(int(xor_result, 2))  # Convert binary back to integer
        j += 1
    return msgE

def decrypt(encrypted_msg, pr):
    decrypted_msg = []
    j = 0
    for byte in encrypted_msg:
        pr_byte = pr[j % len(pr)]  # Repeat pattern if necessary
        pr_byte = bin(pr_byte)[2:].zfill(8)  # Convert pattern element to 8-bit binary string
        encrypted_byte = bin(byte)[2:].zfill(8)  # Convert encrypted byte to 8-bit binary string
        decrypted_byte = ''.join(str(int(a) ^ int(b)) for a, b in zip(encrypted_byte, pr_byte))  # XOR operation
        decrypted_msg.append(int(decrypted_byte, 2))  # Convert binary back to integer
        j += 1
    decrypted_msg = ''.join(chr(byte) for byte in decrypted_msg)  # Convert integers back to characters
    return decrypted_msg

def showimage():
    global filename
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                        title='Selext Image File',
                                        filetype=(("PNG file",'*.png'),
                                                  ("JPG file",'*.jpg')
                                                  ))
    img=Image.open(filename)
    img=ImageTk.PhotoImage(img)
    lbl.configure(image=img,width=250,height=250)
    lbl.image=img


def Hide():
    global secret
    message = text1.get(1.0, END)
    pr = [1, 0, 1, 0]  # Example pattern, you may adjust this as needed
    encrypted_msg = encrypt(message, pr)  # Encrypt the message using your encrypt function
    binary_msg = ''.join(format(byte, '08b') for byte in encrypted_msg)  # Convert the encrypted message to a binary string
    secret = lsb.hide(filename, binary_msg)



def Show():
    global filename
    binary_msg = lsb.reveal(filename)  # Extract the hidden binary message from the image
    encrypted_msg = [int(binary_msg[i:i+8], 2) for i in range(0, len(binary_msg), 8)]  # Convert binary message to list of integers
    pr=[1,0,1,0]
    decrypted_msg = decrypt(encrypted_msg, pr)  # Decrypt the encrypted message using your decrypt function
    text1.delete(1.0, END)
    text1.insert(END, decrypted_msg)

def save():
    secret.save("hidden.png")


image_icon=PhotoImage(file="logo.jpg")
root.iconphoto(False,image_icon)

logo=PhotoImage(file="logo.png")
Label(root,image=logo,bg="#2f4155").place(x=10,y=0)
Label(root,text="DSP PROJECT",bg="#2d4155",fg="white",font="arial 25 bold").place(x=100,y=20)

#first frame
f=Frame(root,bd=3,bg="black",width=340,height=280,relief=GROOVE)
f.place(x=10,y=80)

lbl=Label(f,bg="black")
lbl.place(x=40,y=10)

#second frame
#white panel
frame2=Frame(root,bd=3,width=340,height=280,bg="white",relief=GROOVE)
frame2.place(x=350,y=80)

#text editor in white frame
text1=Text(frame2,font="Robote 20",bg="white",fg="black",relief=GROOVE,wrap=WORD)
text1.place(x=0,y=0,width=320,height=295)

#setting scrollbar for larger messages
scrollbar1=Scrollbar(frame2)
scrollbar1.place(x=320,y=0,height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

#third frame left bottom frame
frame3=Frame(root,bd=3,bg="#2f4155",width=330,height=100,relief=GROOVE)
frame3.place(x=10,y=370)

#defining buttons
Button(frame3,text="Open Image",width=10,height=2,font="arial 14 bold",command=showimage).place(x=20,y=30)
Button(frame3,text="Save Image",width=10,height=2,font="arial 14 bold",command=save).place(x=180,y=30)
Label(frame3,text="Picture, Image, Photo file",bg="#2f4155",fg="yellow").place(x=20,y=5)

#third frame
frame4=Frame(root,bd=3,bg="#2f4155",width=330,height=100,relief=GROOVE)
frame4.place(x=360,y=370)
Button(frame4,text="Hide Data",width=10,height=2,font="arial 14 bold",command=Hide).place(x=20,y=30)
Button(frame4,text="Show Data",width=10,height=2,font="arial 14 bold",command=Show).place(x=180,y=30)
Label(frame4,text="Picture, Image, Photo file",bg="#2f4155",fg="yellow").place(x=20,y=5)

root.mainloop()
