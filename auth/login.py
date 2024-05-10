import pandas as pd

file_path = "Resource/Brix Student Users.csv"
filedf = pd.read_csv(file_path)

def valid_login(username, password):
    found = filedf.loc[filedf['Matric Number'] == username]
    
    for _, f in found.iterrows():
        # print(f)
        if f['Password'] == password:
            return f
    
if __name__ == '__main__':
	print(valid_login("2019_8479", "SS1234@4"))