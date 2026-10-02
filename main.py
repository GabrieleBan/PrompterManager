import pandas as pd
import os 
import pathlib as path
import random
import datetime

lists_dir="./lists"

def main():
    os.makedirs("lists",exist_ok=True)
    exiting=False

    while(not exiting):
        opt=int(input("what to do? \n (0 - create new list) \n (1 - open list) \n (2 - exit)\n Option : " ))
        match opt:
            case 0: 
                filepath = create_new_list()
                menage_list(filepath)
                continue
            case 1:
                files_list=path.Path(lists_dir).glob("*.csv")
                files_list_name=[]

                for i, file in enumerate(files_list,0):
                        print(str(i)+ " : " +file.name)
                        files_list_name.append(file)
                        
                index = int(input("insert index : "))
                file = files_list_name[index]
                filepath=path.Path(lists_dir).joinpath(file.name)

                menage_list(filepath)
                

                continue
            case 2:
                exiting=True
                continue
            
            case _ : print("unrecognized command")

def create_new_list():
    name=None
    while not name:
        name=input("Insert new list name : ")
    filepath=path.Path(lists_dir).joinpath(name+".csv")
    if filepath.exists():
        print("list already exists")
    else:
        pd.DataFrame(columns=["prompt", "date"]).to_csv(str(filepath))
    return filepath


def menage_list(filepath):
    exiting=False
    df=pd.read_csv(str(filepath),index_col=0)
    df["date"] = df["date"].astype("str")


    while not exiting:
        print("what to do? (0 - generate suggestion) (1 - add prompt to list) (2 - read list) (3 - close list)")
        opt=int(input(""))
        match opt:
            case 0:
                unused_prompts_index=df.index[df["date"].isna()].to_list()
                if len(unused_prompts_index)==0:
                    print("no more suggestions left")
                    continue
                chosen_idx=random.randrange(0,len(unused_prompts_index))
                print("Chosen :", df.loc[unused_prompts_index[chosen_idx],"prompt"])
                committing=input("commit? y/n ")=="y"
                if committing:
                    df.loc[unused_prompts_index[chosen_idx],"date"]= str(datetime.datetime.now().date())
                    df.to_csv(filepath)
                
            case 1:
                prompt=input("insert new prompt: ")
                df.loc[len(df)]= {"prompt": prompt, "date":None}
                df.to_csv(filepath)
            case 2:
                print(df.to_string(index=True, header=False).replace("NaN","-"))
            
            case 3:
                exiting=True

            case _: print("unrecognized prompt")

                






if __name__=="__main__":
    main()


