import os
import pandas as pd
from django.shortcuts import redirect, render
import myapp.functions.my_functions as l_reg
import myapp.misc.globals as file

def index(request):
    file.file_path = ""
    archDrv = l_reg.list_files()
    filtered_data = [{'name': item['name'], 'id': item['id']} for item in archDrv if item['mimeType'] == 'application/vnd.google-apps.spreadsheet']
    archivosServer = os.listdir("myapp/data")
    archivosDrive = filtered_data

    if request.method == "POST":
        rutaServer = request.POST.get("rutaServer")
        rutaDrive = request.POST.get("rutaDrive")
        print("reqServer", rutaServer)

        if rutaDrive == None:
            file.file_path = "myapp/data/" + rutaServer
        else:
            print("reqDrive", rutaDrive)
            file.file_path = l_reg.descargarDrive(rutaDrive, 'Ender 3 v2 - Costos')
        return redirect("home")
    return render(request, "index.html", {"archivosServer": archivosServer, "archivosDrive": archivosDrive})

def home(request):
    if request.method == "POST":
        file.Y = request.POST.get("Y").strip()
        file.X = request.POST.get("X").split(",")

        return redirect("predict")
    df = pd.read_excel(file.file_path)
    return render(request, 'home.html', {'data': df.to_html()})

def predict(request):
    if (file.X != "" and file.Y != ""):
        df = pd.read_excel(file.file_path)

        X = df[file.X]
        Y = df[file.Y]

        beta_standardized = l_reg.standardized_betas(X, Y)

        reg_pred = l_reg.my_pred(X, Y, beta_standardized)
        
        r2 = l_reg.r_squared(X, Y)

        data = l_reg.my_data(X, Y)
        plot = l_reg.my_plot(X, Y, reg_pred, r2, beta_standardized)
    else:
        r2 = "error"
        beta_standardized = "error"
        data = ""
        plot = "error"

    return render(request, 'predict.html', {'r2': r2, 'beta_standardized': beta_standardized, 'data': data, 'plot': plot})
