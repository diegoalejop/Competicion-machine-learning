import pandas as pd
import xgboost
import numpy as np
import joblib
import sys

def pred_price(info):
    input = info
    #Importar datos de test para comparar campos
    dataTesting = pd.read_csv('https://raw.githubusercontent.com/davidzarruk/MIAD_ML_NLP_2023/main/datasets/dataTest_carListings.zip', index_col=0)
    
    #Para revisión de inputs
    States = list(dataTesting['State'].drop_duplicates())
    Make = list(dataTesting['Make'].drop_duplicates())
    Model = list(dataTesting['Model'].drop_duplicates())

    if type(input) != list:
        print("No se ingresó una lista")
    elif len(input) != 5:
        print("No se ingresó el número específico de parámetros")
    elif info[2] not in States:
        print("No se infgresó un Estado válido en la posición 3")
    elif info[3] not in Make:
        print("No se infgresó un fabricante válido en la posición 3")
    elif info[4] not in Model:
        print("No se infgresó un Modelo válido en la posición 3")
    else:
        
        X_test_dummies_orig = pd.get_dummies(dataTesting, columns=['State','Make','Model'])
        X_test_dummies_orig = X_test_dummies_orig[X_test_dummies_orig['Year']>2030].transpose()

        #Construcción estructura en dummies
        dict_input = {'Year':input[0],'Mileage':input[1],'State' :input[2],'Make':input[3],'Model':input[4]}
        inputDf = pd.DataFrame(dict_input, index = [0])
        X_test_dummies = pd.get_dummies(inputDf, columns=['State','Make','Model'], sparse=True).transpose() #Dummies de variables categóricas

        #Construcción nueva observación
        New_Obs = pd.merge(left=X_test_dummies_orig,
                        right=X_test_dummies,
                        right_index=True,
                        left_index=True,
                        how='left')

        New_Obs.fillna(0, inplace=True)
        New_Obs = New_Obs.transpose()

        #Importando el clasificador guardado
        clf = joblib.load("XGB_Car_Price.pkl") 

        #Predicción del modelo
        pred_final = clf.predict(X = New_Obs)

        return round(float(pred_final),2)
    
if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print('Por favor inserte información de los componentes')
        
    else:

        year = sys.argv[1]
        mileage = sys.argv[2]
        state = sys.argv[3]
        brand = sys.argv[4]
        model = sys.argv[5]

        p1 = pred_price([year,mileage,state,brand,model])
        
        print('Year: ' +str(year) +
              '\nMileage: ' + str(mileage) +
              '\nState: ' + state +
              '\nBrand: ' + brand +
              '\nModel: ' +model)
        
        print('\nPrecio automobil: ', str(p1))
            