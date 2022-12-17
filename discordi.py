import os
import threading
import customtkinter as tkinter
import ffmpeg
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

padX = 15
padY = 15

class App(tkinter.CTk):
    def __init__(self):
        super().__init__()

        global inpath, outpath, resOption, Xvar, Yvar

        self.title("Discordipy")
        self.geometry("1000x800")
        self.resizable(False, False)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure([0,1,2,3,4,5], weight=1)

        inpath= tkinter.StringVar()
        inpath.set("")
        outpath= tkinter.StringVar()
        outpath.set("")
        resOption = tkinter.IntVar()
        resOption.set(1)
        Xvar = tkinter.IntVar()
        Xvar.set(0)
        Yvar = tkinter.IntVar()
        Yvar.set(0)

        self.fileframe = FileFrame(self, header_name="FileFrame")
        self.fileframe.grid(padx=padX, pady=padY, column=0, columnspan=6, row=0, sticky="ew")

        self.nochangeframe = NoChangeFrame(self, header_name="NoChangeFrame")
        self.nochangeframe.grid(padx=padX, pady=padY, column=2, row=1)

        self.presetframe = PresetFrame(self, header_name="PresetFrame")
        self.presetframe.grid(padx=0, pady=padY, column=3, row=1)

        self.resolutionframe = ResolutionFrame(self, header_name="ResolutionFrame")
        self.resolutionframe.grid(padx=0, pady=padY, columnspan=6, column=0, row=2)

        self.saveframe = SaveFrame(self, header_name="SaveFrame")
        self.saveframe.grid(padx=padX, pady=padY, column=0, columnspan=6, row=3, sticky="ew")

        self.buttonframe = ButtonFrame(self, header_name="ButtonFrame")
        self.buttonframe.grid(padx=padX, pady=padY, column=0, columnspan=6, row=4)

        self.consoleframe = ConsoleFrame(self, header_name="ConsoleFrame")
        self.consoleframe.grid(padx=padX, pady=padY, column=0, columnspan=6, row=5, sticky="news")


class FileFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="FileFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(1, weight=1)

        self.filelabel = tkinter.CTkLabel(self, text="Input File:")
        self.filelabel.grid(padx=padX, pady=padY, column=0, row=0)

        self.filepathlabel = tkinter.CTkLabel(self, textvariable=inpath)
        self.filepathlabel.grid(padx=padX, pady=padY, column=1, row=0)

        self.pickfilebtn = tkinter.CTkButton(self, text="Select File/Folder", command=Discordipy.fileselect)
        self.pickfilebtn.grid(padx=padX, pady=padY, column=2, row=0)


class NoChangeFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="NoChangeFrame", **kwargs):
        super().__init__(*args, **kwargs)

        nochange = tkinter.CTkRadioButton(self, variable=resOption, value=1, command=Discordipy.radiostate, text="     Keep Resolution", height=29, width=150)
        nochange.grid(padx=padX, pady=padY, column=0, columnspan=2, row=0)


class PresetFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="PresetFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global listSelection, presetcombo

        self.preset = tkinter.CTkRadioButton(self, variable=resOption, value=2, command=Discordipy.radiostate, text="     Preset:")
        self.preset.grid(padx=padX, pady=padY, column=2, row=0)

        comboList = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        listSelection = tkinter.StringVar()
        listSelection.set("1080p")

        presetcombo = tkinter.CTkComboBox(self, justify="center", values=comboList, variable=listSelection, state="disabled")
        presetcombo.grid(padx=padX, pady=padY, column=3, row=0)


class ResolutionFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ResolutionFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global customX, customY

        custom = tkinter.CTkRadioButton(self, variable=resOption, value=3, command=Discordipy.radiostate, text="     Resolution:")
        custom.grid(padx=padX, pady=padY, column=0, row=1)

        customX = tkinter.CTkEntry(self, state="disabled", textvariable=Xvar)
        customX.grid(padx=padX, pady=padY, column=1, row=1)

        self.X = tkinter.CTkLabel(self, text="X")
        self.X.grid(padx=0, pady=0, column=2, row=1)

        customY = tkinter.CTkEntry(self, state="disabled", textvariable=Yvar)
        customY.grid(padx=padX, pady=padY, column=3, row=1)

        
class SaveFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="SaveFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(1, weight=1)

        self.savelabel = tkinter.CTkLabel(self, text="Save As:")
        self.savelabel.grid(padx=padX, pady=padY, column=0, row=0)

        self.savepathlabel = tkinter.CTkLabel(self, textvariable=outpath)
        self.savepathlabel.grid(padx=padX, pady=padY, column=1, row=0, sticky="ew")

        self.savefilebtn = tkinter.CTkButton(self, text="Browse", command=Discordipy.savefileselect)
        self.savefilebtn.grid(padx=padX, pady=padY, column=2, row=0)


class ButtonFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ButtonFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.button = tkinter.CTkButton(self, text="Discordipy", command=Discordipy.optionset, width=250, height=100)
        self.button.grid(padx=0, pady=0, column=0, row=0)


class ConsoleFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ConsoleFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global console

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        console = tkinter.CTkTextbox(self)
        console.grid(padx=0, pady=0, column=0, row=0, sticky="news")


class Discordipy:
    def __init__(self):
        pass

    def fileselect():

        global newRate, abitrate , vframes

        select = askopenfilename()
        if select:
            inpath.set(select)
            file_name, file_ext = os.path.splitext(select)
            newName = (file_name+" - Discordipy"+file_ext)
            outpath.set(newName)
            probe = ffmpeg.probe(select)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            vwidth = int(video_stream["width"])
            vheight = int(video_stream["height"])
            vframes = int(video_stream["nb_frames"])
            vlength = float(round((float(video_stream["duration"]))/60, 1))
            # vbitrate = int(video_stream["bit_rate"])
            abitrate = int(audio_stream["bit_rate"])
            Xvar.set(vwidth)
            Yvar.set(vheight)
            newRate = int((8/(vlength*0.0000075))-abitrate)
            resOption.set(1)
        else:
            pass

    def savefileselect():
        save = asksaveasfilename(initialfile=outpath.get(), filetypes=[("mp4",".mp4")], defaultextension=".mp4")
        if save:
            outpath.set(save)
        else:
            pass

    def radiostate():
        match resOption.get():
            case 1:
                presetcombo.configure(state="disabled")
                customX.configure(state="disabled")
                customY.configure(state="disabled")
            case 2:
                presetcombo.configure(state="normal")
                customX.configure(state="disabled")
                customY.configure(state="disabled")
            case 3:
                presetcombo.configure(state="disabled")
                customX.configure(state="normal")
                customY.configure(state="normal")
    
    def optionset():
        match resOption.get():
            case 1:
                pass
            case 2:
                match listSelection.get():
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
            case 3:
                pass
        Discordipy.threadstart()

    def threadstart():
        threading.Thread(target=Discordipy.runff).start()

    def runff():

        global process

        input_stream = ffmpeg.input(inpath.get())
        video = input_stream.video.filter("scale", Xvar.get(), Yvar.get())
        audio = input_stream.audio
        concat = ffmpeg.concat(video, audio, v=1, a=1).node
        video_out = concat[0]
        audio_out = concat[1]
        ffout = ffmpeg.output(video_out, audio_out, outpath.get(), video_bitrate=newRate, audio_bitrate=abitrate, format="mp4")
        process = ffout.run_async(pipe_stdout=True, pipe_stderr=True)
        threading.Thread(target=Discordipy.consoleout).start()
        process.stderr

    def consoleout():
        while True:
            stderr = process.stderr.readline()
            if not (stderr):
                console.insert(tkinter.END, "Finished Discordipying your video!")
                break
            console.insert(tkinter.END, stderr)
            console.see(tkinter.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()