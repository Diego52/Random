#Carga de datos a través de la función open de python para datasets excesivamente grandes
#Crea un for que lee linea por linea del fichero y elimina aquellas que termina de processar para no quedarse sin memoria
def downloadFromUrl (url, filename, path, sep =",", delim = "\n", encoding = "utf-8"):

    import pandas as pd
    import os
    import urllib3

    #medals_url = "http://winterolympicsmedals.com/medals.csv"
    #data = pd.read_csv(medals_url)
    #print(data.head())
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    #print(r.status)
    #print(r.data)
    response = r.data

    str_data = response.decode(encoding)
    #print(str_data)
    lines = str_data.split(delim)
    #print(lines)
    col_names = lines[0].split(sep)
    n_col = len(col_names)
    #print(col_names)
    counter = 0
    main_dict = {}
    for col in col_names:
        main_dict[col] = []
    for line in lines:
        if(counter > 0):
            values = line.strip().split(",")
            for i in range (len(col_names)):
                main_dict[col_names[i]].append(values[i])
        counter += 1
    #print("El dataset tiene %d columnas y %d filas"%(n_col,counter))
    df = pd.DataFrame(main_dict)
    #print(df.head())
    #mainpath = "C:/Users/d.soriano.morales/Music/Documents/Data science y machine learning course/python-ml-course-master/datasets"
    #filepath = "athletes/Mydownload"
    fullpath = os.path.join(path, filename)

    df.to_csv(fullpath + ".csv")
    df.to_excel(fullpath + ".xlsx")
    df.to_json(fullpath + ".json")
    return df

print(downloadFromUrl("http://winterolympicsmedals.com/medals.csv","Mydownload",
    "C:/Developer/Data science y machine learning course/python-ml-course-master/datasets/athletes"))

