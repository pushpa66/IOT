from Tkinter import *
from PIL import Image, ImageTk
import json
import tkMessageBox

print('GUI APPLICATION MANAGER')
#-------------------FOR CHILD-----------------------------
variable_calibrate = ""
om_variable_type = ''
om_variable_id = ''
om_variable_port = ''

current_ids = []
available_ids =[]
current_ports = []
available_ports =[]

varBackUp = ''
option_1 = ''

ids = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']
ports = ['A01', 'A02', 'A03', 'A04', 'A05', 'D01', 'D02', 'D03', 'D04', 'D05']
#-------------------------------------------
data = {}
selected_id = ""

val_Broker = ""
val_API_Key = ""
val_Port = ""
val_Terminal_ID = ""


val_auto = ""
val_interval = ""

#-----------Update the json file------------
def update():
    jsonFile = open("Settings.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
#-----------Read the json file--------------
def read():
    jsonFile = open("Settings.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    return data
#-----------Display some of json values-----
def startUp():
    global data
    data = read()
    broker.delete(0, END)
    broker.insert(0, data['settings']['broker'])
    API_Key.delete(0, END)
    API_Key.insert(0, data['terminal']['apikey'])
    port.delete(0, END)
    port.insert(0, data['settings']['port'])
    terminal_ID.delete(0, END)
    terminal_ID.insert(0, data['terminal']['id'])

    if(data['settings']['auto'] == '1'):
        auto.set("true")
    else:
        auto.set("false")

    uploading_interval.delete(0, END)
    uploading_interval.insert(END, data['settings']['interval'])
#-----------Setup available ports and ids---
def createOption(child):
    global variable_calibrate, om_variable_type, om_variable_id, om_variable_port
    global data, current_ids, current_ports, available_ids, available_ports
    x = 0

    om_variable_type = StringVar(child)
    om_variable_type.set("Temperature")
    om_type = OptionMenu(child, om_variable_type, "Temperature", "Salinity", "Light", "Wind")
    om_type.config(width=10)
    om_type.grid(row=x, column=2)

    label_id = Label(child, text="Sensor ID:")
    label_id.grid(row=x+1, sticky=E)
    om_variable_id = StringVar(child)
    om_variable_id.set(available_ids[0])
    om_id = OptionMenu(child, om_variable_id, *available_ids)
    om_id.config(width=10)
    om_id.grid(row=x+1, column=2)

    label_port = Label(child, text="Connected Port:")
    label_port.grid(row=x+2, sticky=E)
    om_variable_port = StringVar(child)
    om_variable_port.set(available_ports[0])
    om_port = OptionMenu(child, om_variable_port, *available_ports)
    om_port.config(width=10)
    om_port.grid(row=x+2, column=2)
#-------------------------------------------
def setup():
    global data, current_ids, current_ports, available_ids, available_ports

    current_ids = []
    available_ids = []
    current_ports = []
    available_ports = []

    for i in data['sensors']:
        current_ids.append(i['id'])
        current_ports.append(i['port'])

    for i in ids:
        if(i not in current_ids):
            available_ids.append(i)
    for i in ports:
        if(i not in current_ports):
            available_ports.append(i)
#-----------Popup window for adding sensors--
def popupWindow(event):
    global variable_calibrate, om_variable_type, om_variable_id, om_variable_port
    global data, current_ids, current_ports, available_ids, available_ports

    child = Tk()
    child.lift()
    child.resizable(height=False, width=False )
    child.title('Add Sensor Panel')
    # child.iconbitmap('R2D2.ico')
    x = 0
    #------------------------------------------------
    label_type = Label(child, text="Sensor Type:")
    label_type.grid(row=x, sticky=E)

    setup()
    createOption(child)

    #-----------------------------------------------
    label_calib = Label(child, text="Calibrate Value:")
    label_calib.grid(row=x+3, sticky=E)
    variable_calibrate = Entry(child)
    variable_calibrate.insert(END, "100")
    variable_calibrate.config(width=10)
    variable_calibrate.grid(row=x+3, column=2)
    #-----------------------------------------------
    add_Sensor_Submit = Button(child, text="Conform", width=15)
    add_Sensor_Submit.bind("<Button-1>", submit)
    add_Sensor_Submit.grid(row=x+4, column=2)

    child.mainloop()
#-----------Submit the added sensor details--
def submit(event):
    global data, listbox
    sensor = {}

    parentName = event.widget.winfo_parent()
    parent = event.widget._nametowidget(parentName)

    try:
        cali = variable_calibrate.get()
        cali = int(cali)
        sensor['calib'] = str(cali)
        x = om_variable_type.get()
        id = om_variable_id.get()
        port = om_variable_port.get()

        if(x == 'Temperature'):
            x = 'TEMP'
        elif(x == 'Salinity'):
            x = 'SALI'
        elif(x == 'Light'):
            x = 'LIGH'
        elif(x == 'Wind'):
            x = 'WIND'

        sensor['type'] = x
        sensor['id'] = id
        sensor['port'] = port
        data['sensors'].append(sensor)

        update()
        startUp()
        updateCurrentSensors()
        setup()
        createOption(parent)
        tkMessageBox.showinfo("Successful", "Successfully Updated..")
        parent.lift()
    except:
        tkMessageBox.showinfo("Error", "Calibrate Value must be a number..")
        parent.lift()
#-----------Update the current sensor panel--
def updateCurrentSensors():
    global listbox
    readed = read()

    listbox.delete(0, END)
    for i in readed['sensors']:
        x = i['type']
        y = i['id']
        if(x == 'TEMP'):
            listbox.insert(END, y+'_Temperature')
        elif(x == 'SALI'):
            listbox.insert(END, y+'_Salinity')
        elif(x == 'LIGH'):
            listbox.insert(END, y+'_Light')
        elif(x == 'WIND'):
            listbox.insert(END, y+'_Wind')
#-----------Update data we provided----------
def updateData(event):
    global data
    val_Broker = broker.get()
    val_API_Key = API_Key.get()
    val_Port = port.get()
    val_Terminal_ID = terminal_ID.get()

    data['settings']['broker'] = val_Broker
    data['terminal']['apikey'] = val_API_Key
    data['settings']['port'] = val_Port
    data['terminal']['id'] = val_Terminal_ID
    update()
    startUp()
#--------------------Show data of selected sensor------------
def submitData(event):

    try:
        val_auto = auto.get()
        val_interval = int(uploading_interval.get())

        if(val_auto == "true"):
            val_auto = "1"
        else:
            val_auto = "0"

        data['settings']['auto'] = val_auto
        data['settings']['interval'] = str(val_interval)
        update()
        startUp()
        tkMessageBox.showinfo("Successful", "Successfully Submitted..")
    except:
        tkMessageBox.showinfo("Error", "Uploading Interval must be a number..")

def showMyDetails(event):
    global listbox, data, selected_id, varBackUp
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])

    temp = value.split('_')

    selected_id = temp[0]

    for i in data['sensors']:
        if(i['id'] == selected_id):

            port = i['port']
            varBackUp = port

            calibrate.delete(0, END)
            calibrate.insert(END, i['calib'])

    parentName = event.widget.winfo_parent()
    parent = event.widget._nametowidget(parentName)
    editPorts(parent)
#------------------------------------------------------------
def modifySelected(event):
    global selected_id, data, var
    try:
        cali = int(calibrate.get())
        if(selected_id != "None"):
            for i in data['sensors']:
                if(i['id'] == selected_id):
                    new_port = var.get()
                    i['port'] = new_port
                    i['calib'] = str(cali)

            update()
            updateCurrentSensors()
            autoReset()
        selected_id = 'None'
        tkMessageBox.showinfo("Successful", "Successfully Modified..")
    except:
        tkMessageBox.showinfo("Error", "Check the Calibrate Value again..")

#------------------------------------------------------------
def removeSelected(event):
    global selected_id, data

    try:
        if(selected_id != "None"):
            for i in data['sensors']:
                if(i['id'] == selected_id):
                    del data['sensors'][data['sensors'].index(i)]
            update()
            updateCurrentSensors()
            autoReset()
        selected_id = 'None'
        tkMessageBox.showinfo("Successful", "Successfully Removed..")
    except:
        tkMessageBox.showinfo("Error", "Unable to remove.Please try again..")

#------------------------------------------------------------
def autoReset():
    var.set("None")
    calibrate.delete(0, END)
    calibrate.insert(END, "None")
#------------------------------------------------------------
def editPorts(root):
    global var, option_1, available_ports

    setup()
    var = StringVar(root)
    if(varBackUp == ''):
        var.set("None")
    else:
        var.set(varBackUp)
    option_1 = OptionMenu(root, var, "None", *available_ports)
    option_1.config(width=14)
    option_1.grid(row=12, column=3)

root = Tk()

root.resizable(height=False, width=False)
root.title('Terminal Config')
# root.iconbitmap('R2D2.ico')

image = Image.open("Header.png")
image = image.resize((500, 60), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)

label = Label(root, image=photo)
label.grid(columnspan=4)
label.grid(rowspan=2)
#--------------------------------------------------------
#--------------MQTT Network Settings---------------------
#--------------------------------------------------------
label_title = Label(root, text="MQTT Network Settings")
label_title.grid(row=3, sticky=W)
label_title.grid(columnspan=2, sticky=W)
#--------------------------------------------------------
x=4
label_Broker = Label(root, text="Broker")
label_API_Key = Label(root, text="API Key")
label_Broker.grid(row=x, sticky=E)
label_API_Key.grid(row=x+1, sticky=E)

broker = Entry(root)
API_Key = Entry(root)

broker.grid(row=x, column=1)
API_Key.grid(row=x+1, column=1)
#--------------------------------------------------------
label_Port = Label(root, text="Port")
label_Terminal_ID = Label(root, text="Terminal ID")
label_Port.grid(row=x, column=2, sticky=E)
label_Terminal_ID.grid(row=x+1, column=2, sticky=E)

port = Entry(root)
port.grid(row=x, column=3)

terminal_ID = Entry(root)
terminal_ID.grid(row=x+1, column=3)
#--------------------------------------------------------
button_update = Button(root, text="Update", width=15)
button_update.bind("<Button-1>", updateData)
button_update.grid(row=x+2, column=3)
#--------------------------------------------------------
#--------------Data Uploading Settings-------------------
#--------------------------------------------------------
y = 7;
label_title = Label(root, text="Data Uploading Settings")
label_title.grid(row=7, sticky=W)
label_title.grid(columnspan=2, sticky=W)
#--------------------------------------------------------
label_auto_uploading = Label(root, text="Auto Uploading")
label_auto_uploading.grid(row=y+1, column=0, sticky=E)

auto = StringVar(root)
auto.set("true")
auto_uploading = OptionMenu(root, auto, "true", "false")
auto_uploading.config(width=14)
auto_uploading.grid(row=y+1, column=1)

label_uploading_interval = Label(root, text="Uploading Interval")
label_uploading_interval.grid(row=y+1, column=2, sticky=E)

uploading_interval = Entry(root)
uploading_interval.grid(row=y+1, column=3)

button_submit = Button(root, text="Submit", width=15)
button_submit.bind("<Button-1>", submitData)
button_submit.grid(row=y+2, column=3)

#--------------------------------------------------------
#--------------Sensor Settings---------------------------
#--------------------------------------------------------
t = 10;
label_title = Label(root, text="Sensor Settings")
label_title.grid(row=t, sticky=W)
label_title.grid(columnspan=2, sticky=W)

add_Sensor = Button(root, text="Add Sensor", width=15)
add_Sensor.bind("<Button-1>",popupWindow)
add_Sensor.grid(row=t+1, column=1)
#--------------------------------------------------------
listbox = Listbox(root, height=4,width=1, bg="white")
scroll = Scrollbar(root, orient=VERTICAL)
listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)

listbox.grid(row=t+2, column=1, rowspan=4, columnspan=1, sticky=N+E+W+S)
listbox.bind("<Double-Button-1>",showMyDetails)
listbox.columnconfigure(t+2, weight=1)

scroll.grid(row=t+2, column=1, rowspan=4, sticky=N+E+S)

#--------------------------------------------------------
label_Digital_Port = Label(root, text="Analog/Digital Port")
label_Digital_Port.grid(row=t+2, column=2, sticky=E)

######################
#----------->
######################
#---------------------------------------------------------
label_Calibrate = Label(root, text="Calibrate Value")
label_Calibrate.grid(row=t+3, column=2, sticky=E)
calibrate = Entry(root)
calibrate.grid(row=t+3, column=3)
calibrate.insert(0, "None")
#----------------------------------------------------------
modify_Selected = Button(root, text="Modify Selected", width=15)
modify_Selected.bind("<Button-1>",modifySelected)
modify_Selected.grid(row=t+4, column=2)
#----------------------------------------------------------
remove_Selected = Button(root, text="Remove Selected", width=15)
remove_Selected.bind("<Button-1>",removeSelected)
remove_Selected.grid(row=t+4, column=3)
#------------------------------------------------------------------------
last = Label(root, text="", height=1)
last.grid(row=t+6, columnspan=4, sticky=E)

startUp()
setup()
editPorts(root)
updateCurrentSensors()
#---------------------------------------------------------------------
root.mainloop()