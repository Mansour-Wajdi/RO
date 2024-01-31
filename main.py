import os
import customtkinter
from PIL import Image
from customtkinter import CTkButton, CTkFont, CTk
from Frames.homeFrame import home
from Frames.frame1 import MyFrame1
from Frames.frame2 import MyFrame2
from Frames.frame3 import MyFrame3
from Frames.frame4 import MyFrame4
from Frames.frame5 import MyFrame5
from Frames.frame6 import MyFrame6
from Frames.frame7 import MyFrame7
from Frames.frame8 import MyFrame8
from Frames.frame9 import MyFrame9

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("PROJET RECHERCHE OPERATIONALE")
        self.geometry("1200x900")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))

        # Navigation Frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        for i in range(11): # Assuming there are 10 buttons plus one label
            self.navigation_frame.grid_rowconfigure(i, weight=1 if i == 10 else 0) # Adjust weights as needed
        self.navigation_frame.grid_columnconfigure(0, weight=1)

        frames_classes = [home, MyFrame1, MyFrame2, MyFrame3, MyFrame4, MyFrame5, MyFrame6, MyFrame7, MyFrame8, MyFrame9]
        self.frames = {frame.__name__.lower(): frame(master=self) for frame in frames_classes}

        frame_names = [
            "Home",
            "PL 1: Gestion optimale d'une zone agricole",
            "PL 2: Mixage en production",
            "PL 3: Planification des besoins en RH",
            "PL 4: Gestion de la production",
            "PL 5: La production d'électricité",
            "PL 6: Distribution de produit",
            "PL 7: Affectation optimale de ressources",
            "PL 8: Remplacement d'équipement",
            "PL 9: Planification logistique"
        ]

        for i, name in enumerate(frame_names):
            frame_key = "home" if i == 0 else f"myframe{i}"
            button = CTkButton(
                self.navigation_frame, corner_radius=0, height=40, width=350, border_spacing=10, text=name,
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                font=CTkFont(size=16, weight="bold"),
                anchor="w", command=lambda key=frame_key: self.select_frame_by_name(key))
            button.grid(row=i, column=0, sticky="nw")
            setattr(self, f"frame_{i}_button", button)

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        for frame in self.frames.values():
            frame.grid_forget()

        self.frames[name].grid(row=0, column=1, sticky="nsew")

        for i in range(10):
            button = getattr(self, f"frame_{i}_button")
            button.configure(fg_color=("gray75", "gray25") if f"myframe{i}" == name or (i == 0 and name == "home") else "transparent")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
