import os
import customtkinter as tkinter
import ffmpeg
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

padX = 20
padY = 20

class App(tkinter.CTk):
    def __init__(self):
        super().__init__()

        #not the best way?
        global path, outpath, resMethod, resList, resSelected, state, Xvar, Yvar, presetframe, resframe, presetframe

        self.title("Discordipy")
        self.geometry("1000x500")
        self.minsize(1000,500)

        self.grid_rowconfigure([0,1,2,3], weight=1)
        self.grid_columnconfigure(0, weight=1)

        path = tkinter.StringVar()
        path.set("")
        outpath = tkinter.StringVar()
        outpath.set("")
        resMethod = tkinter.IntVar()
        resMethod.set(1)
        resList = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        resSelected = tkinter.StringVar()
        state = tkinter.StringVar()
        state.set("disabled")
        Xvar = tkinter.IntVar()
        Xvar.set(0)
        Yvar = tkinter.IntVar()
        Yvar.set(0)

        #Input Frame
        self.inputfileframe = InputFileFrame(self, header_name="InputFileFrame")
        self.inputfileframe.grid(padx=padX, pady=10, row=0, column=0, columnspan=3, sticky="new")

        #Preset Frame
        presetframe = PresetFrame(self, header_name="PresetFrame")
        presetframe.grid(padx=padX, pady=10, row=1, column=0)

        #Resolution Frame
        resframe = ResolutionFrame(self, header_name="ResolutionFrame")
        resframe.grid(padx=padX, pady=10, row=2, column=0)

        #Save Frame
        self.savefileframe = SaveFileFrame(self, header_name="SaveFileFrame")
        self.savefileframe.grid(padx=padX, pady=10, row=3, column=0, columnspan=3, sticky="sew")

        #Discordify Button
        self.discordify = Discordify(self, header_name="Discordify")
        self.discordify.grid(padx=padX, pady=10, row=4, column=0, columnspan=3)

    def fileselect():
        global vwidth, vheight, vlength, vbitrate, abitrate, newRate
        select = askopenfilename()
        if select:
            path.set(select)
            file_name, file_ext = os.path.splitext(select)
            newName = (file_name+" - Discord"+file_ext)
            outpath.set(newName)
            probe = ffmpeg.probe(select)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            vwidth = int(video_stream["width"])
            vheight = int(video_stream["height"])
            vlength = float(round((float(video_stream["duration"]))/60, 1))
            vbitrate = int(video_stream["bit_rate"])
            abitrate = int(audio_stream["bit_rate"])
            Xvar.set(vwidth)
            Yvar.set(vheight)
            newRate = int((8/(vlength*0.0000075))-abitrate)
            resMethod.set(1)
        else:
            pass

    def savefileselect():
        save = asksaveasfilename(initialfile=outpath.get(), filetypes=[("mp4",".mp4")], defaultextension=".mp4")
        if save:
            outpath.set(save)
        else:
            pass

    def radiostate():
        match resMethod.get():
            case 1:
                print(resMethod.get())
                state.set("disabled")
                resframe.setres()
                presetframe.setpreset()
            case 2:
                print(resMethod.get())
                state.set("normal")
                resframe.setres()
                presetframe.setpreset()

    def discordify():
        match resMethod.get():
            case 1:
                match resSelected.get():
                    case "1080p":
                        Xvar.set(1920)
                        Yvar.set(1080)
                    case "720p":
                        Xvar.set(1280)
                        Yvar.set(720)
                    case "480p":
                        Xvar.set(854)
                        Yvar.set(480)
                    case "360p":
                        Xvar.set(640)
                        Yvar.set(360)
                    case "240p":
                        Xvar.set(426)
                        Yvar.set(240)
                    case "144p":
                        Xvar.set(256)
                        Yvar.set(144)
                input_stream = ffmpeg.input(path.get())
                video = input_stream.video.filter("scale", Xvar.get(), Yvar.get())
                audio = input_stream.audio
                concat = ffmpeg.concat(video, audio, v=1, a=1).node
                video_out = concat[0]
                audio_out = concat[1]
                out = ffmpeg.output(video_out, audio_out, outpath.get(), video_bitrate=newRate, audio_bitrate=abitrate, format="mp4")
                out.run()
            case 2:
                input_stream = ffmpeg.input(path.get())
                video = input_stream.video.filter("scale", Xvar.get(), Yvar.get())
                audio = input_stream.audio
                concat = ffmpeg.concat(video, audio, v=1, a=1).node
                video_out = concat[0]
                audio_out = concat[1]
                out = ffmpeg.output(video_out, audio_out, outpath.get(), video_bitrate=newRate, audio_bitrate=abitrate, format="mp4")
                out.run()

class InputFileFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="InputFileFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #File Input
        self.file = tkinter.CTkLabel(master=self, text="Input File:")
        self.file.grid(padx=padX, pady=padY, row=0, column=0)

        self.path = tkinter.CTkLabel(master=self, textvariable=path, width=500)
        self.path.grid(padx=padX, pady=padY, row=0, column=1, sticky="ew")

        self.pickfile = tkinter.CTkButton(master=self, text="Select File/Folder", command=App.fileselect)
        self.pickfile.grid(padx=padX, pady=padY, row=0, column=2)

class PresetFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="PresetFrame", **kwargs):
        super().__init__(*args, **kwargs)

        #Preset Select
        self.radio = tkinter.CTkRadioButton(master=self, text="Preset:", variable=resMethod, value=1, command=App.radiostate)
        self.radio.grid(padx=padX, pady=padY, row=2, column=0)

        self.presetmenu = tkinter.CTkComboBox(master=self, state="normal", justify="center", values=resList, variable=resSelected)
        self.presetmenu.grid(padx=padX, pady=padY, row=2, column=1)

    def setpreset(self):
        match state.get():
            case "disabled":
                self.presetmenu.configure(state="normal")
            case "normal":
                self.presetmenu.configure(state="disabled")

class ResolutionFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ResolutionFrame", **kwargs):
        super().__init__(*args, **kwargs)

        #Resolution
        self.radio2 = tkinter.CTkRadioButton(master=self, text="Resolution:", variable=resMethod, value=2, command= App.radiostate)
        self.radio2.grid(padx=padX, pady=padY, row=3, column=0)

        self.resX = tkinter.CTkEntry(master=self, state="disabled", textvariable=Xvar)
        self.resX.grid(padx=padX, pady=padY, row=3, column=1)

        self.x = tkinter.CTkLabel(master=self, text="X")
        self.x.grid(padx=0, pady=0, row=3, column=2)

        self.resY = tkinter.CTkEntry(master=self, state="disabled", textvariable=Yvar)
        self.resY.grid(padx=padX, pady=padY, row=3, column=3)

    def setres(self):
        match state.get():
            case "disabled":
                self.resX.configure(state="disabled")
                self.resY.configure(state="disabled")
            case "normal":
                self.resX.configure(state="normal")
                self.resY.configure(state="normal")

class SaveFileFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="SaveFileFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #File Save
        self.outfile = tkinter.CTkLabel(master=self, text="Save As:")
        self.outfile.grid(padx=padX, pady=padY, row=0, column=0)

        self.outpath = tkinter.CTkLabel(master=self, textvariable=outpath, width=500)
        self.outpath.grid(padx=padX, pady=padY, row=0, column=1, sticky="ew")

        self.pickoutfile = tkinter.CTkButton(master=self, text="Browse", command=App.savefileselect)
        self.pickoutfile.grid(padx=padX, pady=padY, row=0, column=2)

class Discordify(tkinter.CTkFrame):
    def __init__(self, *args, header_name="Discordify", **kwargs):
        super().__init__(*args, **kwargs)

        self.savebutton = tkinter.CTkButton(master=self, text="Discordify", command=App.discordify, width=250, height=100)
        self.savebutton.grid(padx=0, pady=0, row=0, column=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()