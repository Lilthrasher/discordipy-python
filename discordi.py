import os
import winsound
import threading
import customtkinter as tkinter
import ffmpeg
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

padX = 24
padY = 24

class App(tkinter.CTk):
    def __init__(self):
        super().__init__()

        global inpath, outpath, resOption, Xvar, Yvar, frames, progress, progresslabel, consoleframe

        self.title("Discordipy")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure([0,1,2,3,4], weight=5)
        self.grid_columnconfigure(5, weight=1)

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
        frames = tkinter.IntVar()
        frames.set(0)
        progress = tkinter.IntVar()
        progress.set(0)
        progresslabel = tkinter.StringVar()
        progresslabel.set("Waiting")

        self.fileframe = FileFrame(self, header_name="FileFrame")
        self.fileframe.grid(padx=padX, pady=padY, column=0, columnspan=6, row=0, sticky="ew")

        self.nochangeframe = NoChangeFrame(self, header_name="NoChangeFrame")
        self.nochangeframe.grid(padx=padX, pady=(0,padY), column=0, columnspan=2, row=1, sticky="w")

        self.presetframe = PresetFrame(self, header_name="PresetFrame")
        self.presetframe.grid(padx=padX, pady=(0,padY), column=2, columnspan=2, row=1)

        self.resolutionframe = ResolutionFrame(self, header_name="ResolutionFrame")
        self.resolutionframe.grid(padx=padX, pady=(0,padY), column=4, columnspan=2, row=1, sticky="e")

        self.saveframe = SaveFrame(self, header_name="SaveFrame")
        self.saveframe.grid(padx=padX, pady=(0,padY), column=0, columnspan=5, row=2, sticky="ew")

        self.buttonframe = ButtonFrame(self, header_name="ButtonFrame", fg_color="transparent")
        self.buttonframe.grid(padx=padX, pady=(0,padY), column=5, columnspan=1, row=2, sticky="news")

        consoleframe = ConsoleFrame(self, header_name="ConsoleFrame", fg_color="transparent")
        consoleframe.grid(padx=padX, pady=(0,padY), column=0, columnspan=6, row=3, sticky="news")

        self.progressframe = ProgressFrame(self, header_name="ProgressFrame", fg_color="transparent")
        self.progressframe.grid(padx=padX, pady=(0,padY), column= 0, columnspan=6, row=4, sticky="ews")


class FileFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="FileFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global pickfilebtn

        self.columnconfigure(1, weight=1)

        self.filelabel = tkinter.CTkLabel(self, text="Input File:")
        self.filelabel.grid(padx=padX, pady=padY, column=0, row=0)

        self.filepathlabel = tkinter.CTkLabel(self, textvariable=inpath)
        self.filepathlabel.grid(padx=padX, pady=padY, column=1, row=0)

        pickfilebtn = tkinter.CTkButton(self, text="Select File/Folder", command=Discordipy.fileselect, text_color_disabled="#DCE4EE")
        pickfilebtn.grid(padx=padX, pady=padY, column=2, row=0)


class NoChangeFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="NoChangeFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global nochange

        nochange = tkinter.CTkRadioButton(self, variable=resOption, value=1, command=Discordipy.radiostate, text="     Keep Resolution", height=29, width=150)
        nochange.grid(padx=padX, pady=padY, column=0, columnspan=2, row=0)


class PresetFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="PresetFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global preset, listSelection, presetcombo

        preset = tkinter.CTkRadioButton(self, variable=resOption, value=2, command=Discordipy.radiostate, text="     Preset:")
        preset.grid(padx=padX, pady=padY, column=2, row=0)

        comboList = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        listSelection = tkinter.StringVar()
        listSelection.set("1080p")

        presetcombo = tkinter.CTkComboBox(self, justify="center", values=comboList, variable=listSelection, state="disabled", text_color_disabled="#DCE4EE")
        presetcombo.grid(padx=padX, pady=padY, column=3, row=0)


class ResolutionFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ResolutionFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global custom, customX, customY

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

        global savefilebtn

        self.columnconfigure(1, weight=1)

        self.savelabel = tkinter.CTkLabel(self, text="Save As:")
        self.savelabel.grid(padx=padX, pady=padY, column=0, row=0)

        self.savepathlabel = tkinter.CTkLabel(self, textvariable=outpath)
        self.savepathlabel.grid(padx=padX, pady=padY, column=1, row=0)

        savefilebtn = tkinter.CTkButton(self, text="Browse", command=Discordipy.savefileselect, text_color_disabled="#DCE4EE")
        savefilebtn.grid(padx=padX, pady=padY, column=2, row=0)


class ButtonFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ButtonFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global button

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        button = tkinter.CTkButton(self, text="Discordipy", command=Discordipy.optionsetff, text_color_disabled="#DCE4EE")
        button.grid(padx=0, pady=0, column=0, row=0, sticky="news")


class ConsoleFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ConsoleFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global console

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        console = tkinter.CTkTextbox(self)
        console.grid(padx=0, pady=0, column=0, row=0, sticky="news")

    def resetconsole(self):

        global console

        console.destroy()
        console = tkinter.CTkTextbox(self)
        console.grid(padx=0, pady=0, column=0, row=0, sticky="news")
        

class ProgressFrame(tkinter.CTkFrame):
    def __init__(self, *args, header_name="ProgressFrame", **kwargs):
        super().__init__(*args, **kwargs)

        global progressbar, progressbarlabel

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        progressbar = tkinter.CTkProgressBar(self, height=30, progress_color="#1F6AA5", corner_radius=15)
        progressbar.grid(padx=(0,5), pady=0, column=0, row=0, sticky="ew")
        progressbar.set(0)

        progressbarlabel = tkinter.CTkButton(self, textvariable=progresslabel, hover=False, width=100, height=30, corner_radius=15)
        progressbarlabel.grid(padx=(5,0), pady=0, column=1, row=0, sticky="e")


class Discordipy:

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
            frames.set(vframes)
            newRate = int((8/(vlength*0.0000075))-abitrate)
            resOption.set(1)
            Discordipy.resetui()
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
    
    def optionsetff():
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
        Discordipy.prepff()

    def prepff():
        
        nochange.configure(state="disabled")
        preset.configure(state="disabled")
        custom.configure(state="disabled")
        pickfilebtn.configure(state="disabled")
        savefilebtn.configure(state="disabled")
        button.configure(state="disabled")
        threading.Thread(target=Discordipy.runff).start()

    def runff():

        global process

        input_stream = ffmpeg.input(inpath.get())
        video = input_stream.video.filter("scale", Xvar.get(), Yvar.get())
        audio = input_stream.audio
        concat = ffmpeg.concat(video, audio, v=1, a=1).node
        video_out = concat[0]
        audio_out = concat[1]
        ffout = ffmpeg.output(video_out, audio_out, outpath.get(), format="mp4", progress="pipe:2", **{"b:v": newRate}, **{"b:a": abitrate})
        process = ffout.run_async(pipe_stderr=True, overwrite_output=True)
        Discordipy.consoleout()

    def consoleout():

        while True:
            stderr = process.stderr.readline().decode()
            if not (stderr):
                Discordipy.success()
                break
            if "\rframe" in stderr:
                progsplit = stderr.split("\r",1)
                # print(progsplit)
                if len(progsplit) > 1:
                    progstrip = progsplit[1].strip()
                    # print(progstrip)
                    prog = progstrip.split("=",1)
                    if len(prog) > 1:
                        # if len(prog[1]) != "0":
                            # console.delete("end -12 lines", tkinter.END)
                        currentprogress = round(round((int(prog[1])/frames.get()),2)*100)
                        currentprogresspercent = str(currentprogress)
                        progresslabel.set(currentprogresspercent+"%")
                        progressbar.set(currentprogress/100)
                        # print(currentprogress)
                    else:
                        print("weird prog line", prog)
                else:
                    print("weird progsplit line", progsplit)
            if "progress=" in stderr:
                continue
            console.insert(tkinter.END, stderr)
            console.see(tkinter.END)

    def success():

        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        progressbar.set(1)
        progresslabel.set("Completed")
        nochange.configure(state="normal")
        preset.configure(state="normal")
        custom.configure(state="normal")
        pickfilebtn.configure(state="normal")
        savefilebtn.configure(state="normal")
        button.configure(state="normal")

    def resetui():

        consoleframe.resetconsole()
        progressbar.set(0)
        progresslabel.set("Waiting")

if __name__ == "__main__":
    app = App()
    app.mainloop()