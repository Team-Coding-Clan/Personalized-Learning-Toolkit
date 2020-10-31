import pandas as pd
df = pd.read_csv("profiles.csv", sep=";")
df1 = pd.read_csv("dataset1.csv", sep=",")
df2 = pd.read_csv("Dataset2.csv", sep=",")

for i in df.index:
    course = df['course'][i]
    Payment = df['Payment'][i]
    crs = df1[df1['Language/Topic'] == course]
    course1 = crs[crs['Payment'] == Payment]
    df3 = course1[course1['Platform'] != 'YouTube']
    df3.sort_values(['Ratings'], ascending = False, inplace = True)

    print('Courses available-\n', df3.head())
    df4 = course1[course1['Platform'] == 'YouTube']
    df4.sort_values(['Views'] , ascending = False , inplace = True)
    print(df4.head())
    df[['skill1','skill2','skill3']] = df.skill.apply(lambda x: pd.Series(str(x).split(",")))
    skill1 = df['skill1'][i]
    skill2 = df['skill2'][i]
    skill3 = df['skill3'][i]
    projects1 = df2[df2['Language/Topic'] == skill1]
    projects2 = df2[df2['Language/Topic'] == skill2]
    projects3 = df2[df2['Language/Topic'] == skill3]
    projects1.sort_values(['Ratings'], ascending = False , inplace = True)
    projects2.sort_values(['Ratings'], ascending = False, inplace = True)
    projects3.sort_values(['Ratings'], ascending = False, inplace = True)
    print('Projects based on your skills:\n',projects1.head(),projects2.head(),projects3.head())

    
