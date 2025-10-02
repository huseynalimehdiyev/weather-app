from tkinter import ttk
import requests
from tkinter import messagebox
from tkinter import *
import time
from PIL import Image, ImageTk
import pygame
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime
datahis = []
current_background = None


def update_background(weather_description1):
    global current_background
    if "clouds" in weather_description1:
        background_image = "images/overcastclouds.webp"
    elif "Fog" in weather_description1 or "Mist" in weather_description1 or "Haze" in weather_description1:
        background_image = "images/foggyweather.jpg"
    elif "rain" in weather_description1 or "Drizzle" in weather_description1 or " Rain drizzle" in weather_description1:
        background_image = "images/rainpict.jpg"
    elif "snow" in weather_description1:
        background_image = "images/snowimage.jpg"
    elif "clear" in weather_description1:
        background_image = "images/weathericon.png"
    elif "Thunderstorm" in weather_description1:
        background_image = "images/thunderstorm.jpg"
    else:
        background_image = "images/weathericon.png"


    try:
        if current_background != background_image:
            img = Image.open(background_image)
            img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            pfoto = ImageTk.PhotoImage(img)
            label_foto.config(image=pfoto)
            label_foto.image = pfoto
            current_background = background_image
    except FileNotFoundError:
        print(f"Arxa fon şəkli tapılmadı: {background_image}")


frame = None


def weather(event=None):
    global response, frame

    if frame is not None:
        try:
            frame.destroy()
        except AttributeError:
            pass

    city = Importante.get().capitalize()
    api_key = 'xxxxxxxxxxxxxxxxxxxxxx' #api key
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}"
    )
    response = requests.get(url)

    global data
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        weather_description1 = weather_description.capitalize()
        update_background(weather_description1)

        frame = Frame(root, bg="#677f83", bd=2)
        frame.grid(row=4, column=1, pady=15)

        columns = ["Parameter", "Description"]
        for i, col in enumerate(columns):
            label = Label(frame, text=col, fg="white", bg="#677f83", font=("Arial", 16, "bold", "underline"), padx=20)
            label.grid(row=0, column=i, pady=5)

        data = [
            ("Weather Description", weather_description1),
            ("Temperature", f"{data['main']['temp'] - 273.15:.1f}°C"),
            ("Feels Like", f"{data['main']['feels_like'] - 273.15:.1f}°C"),
            ("Relative Humidity", f"{data['main']['humidity']}%"),
            ("Wind Speed", f"{data['wind']['speed']} m/sec."),
        ]

        for row_idx, (param, val1) in enumerate(data, start=1):
            Label(frame, text=param, fg="white", bg="#677f83", font=("Arial", 16, "bold")).grid(row=row_idx, column=0,
                                                                                                pady=2)
            Label(frame, text=val1, fg="white", bg="#677f83", font=("Arial", 16, "bold")).grid(row=row_idx, column=1,
                                                                                               pady=2)

    else:
        if frame is not None:
            try:
                frame.destroy()
            except AttributeError:
                pass

        Importante.delete(0, END)
        messagebox.showerror("Error", "Please enter the city name correctly!")

    button_click()


def Ötür(event=None):
    city = seçim_menyu.get().capitalize()
    Importante.delete(0, END)
    Importante.insert(0, city)
    weather()


def clear_combobox(event=None):
    seçim_menyu.set("")


def add_to_history(action):
    history_list.append(action)

    history_text.config(state="normal")
    history_text.delete(1.0, END)

    for i, entry in enumerate(history_list, 1):
        history_text.insert(END, f"{i}. {entry}\n")

    history_text.config(state="disabled")


def button_click():
    global response
    if response.status_code == 200:
        add_to_history(
            (Importante.get()).capitalize() + " " + time.strftime("%d-%m-%Y") + "," + time.strftime("%H-%M-%S"))
    else:
        add_to_history('Error 404 not found')


pygame.mixer.init()

pygame.mixer.music.load("music/project_music.mp3")

music_time = 0
is_playing = False


def music():
    global is_playing , music_time
    if not is_playing:
        pygame.mixer.music.play(start=max(0,music_time))
        is_playing = True
        music_button.config(image=play_icon)
    else:
        music_time += pygame.mixer.music.get_pos() / 1000
        pygame.mixer.music.stop()
        is_playing = False
        music_button.config(image=stop_icon)

root = Tk()
root.geometry("800x850")
root.title("Weather Forecast")
root.config(bg="Light Blue")
root.iconbitmap(r"images/sunicon.ico")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=0)

foto = Image.open(r"images/weathericon.png")
foto = foto.resize((1920, 1080), Image.Resampling.LANCZOS)
pfoto = ImageTk.PhotoImage(foto)

label_foto = Label(root, image=pfoto)
label_foto.place(x=0, y=0, relwidth=1, relheight=1)

cercive = Frame(root, bg="Black", bd=2)
cercive.grid(row=1, column=1, pady=4, padx=10)

seçim_Frame = Frame(root, bg="Black", bd=2, )
seçim_Frame.grid(row=2, column=1)

vaxt = Label(root, fg="Light Blue", font=("OCR", 16,"bold"), bg="White")
vaxt.grid(row=0, column=0, padx=10, pady=25)

Question = Label(root, text="Which city's weather forecast would you like to know?", fg="black",
                 font=("Times New Roman", 16), bg="Light Blue")
Question.grid(row=0, column=1, pady=15)

Entry_Dəyişən = StringVar()

Importante = Entry(cercive, bg="#D3D3D3", textvariable=Entry_Dəyişən, font=("Times New Roman", 16))
Importante.grid(row=1, column=1)

baton = Button(root, text="Predict", fg="black", command=weather, width=12, height=1, relief="raised",
               font=("Times New Roman", 16))
baton.grid(row=3, column=1, pady=60)

history_list = []

history_label = Label(root, text="History:", font=("Times New Roman", 15, "bold"), bg="#FFFFFF")
history_label.place(x=150, rely=0.73, anchor="sw")

history_text = Text(root, height=8, state="disabled", bg="#f0f0f0", wrap="word", width=40)
history_text.place(x=15, rely=0.9, anchor="sw")

seçimlər = ['Baku', 'Nakhchivan', 'Shusha', 'New York', 'Moscow', 'Sydney', 'Istanbul', 'Ankara', 'Tabriz', 'Ottawa',
            "Reykjavik", 'Berlin']
seçim_menyu = ttk.Combobox(seçim_Frame, values=seçimlər, state="readonly", font=("Arial"), width=10)
seçim_menyu.set('Baku')
seçim_menyu.grid()

seçim_menyu.bind("<<ComboboxSelected>>", Ötür)


def times():
    try:
        city = Importante.get().capitalize()
        api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx' #api key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            lat = data['coord']['lat']
            lon = data['coord']['lon']

            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lng=lon, lat=lat)

            if timezone_str:
                tz = pytz.timezone(timezone_str)
                now = datetime.now(tz)
                tarix = now.strftime("%d-%m-%Y")
                saat = now.strftime("%H:%M:%S")
                vaxt.config(text=f"{tarix} \n {saat}")
            else:
                vaxt.config(text="Timezone not found")
        else:
            vaxt.config(text="City not found")

    except Exception as e:
        vaxt.config(text="Xəta baş verdi")

    root.after(1000, times)


times()

stop = Image.open("Cimages/stoppictureproject.jpg")
play = Image.open("images/starticonproject.jpg")

play = play.resize((30,30))
stop = stop.resize((30,30))

play_icon = ImageTk.PhotoImage(play)
stop_icon = ImageTk.PhotoImage(stop)

music_button = Button(root,image=play_icon,command=music)
music_button.place(relx=0.97, rely=0.9, anchor="se", width=35, height=35)

Importante.bind("<Key>", clear_combobox)
Importante.bind("<Return>", weather)
root.mainloop()
