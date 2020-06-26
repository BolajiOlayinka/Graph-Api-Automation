
import json
# import facebook

# graph=facebook.GraphAPI(access_token='EAAD9mIfgmCwBAK3UHDOAW1zvAcF5Wqjq5WCq8Q1wEHpkz5TG2F0GJXqTBtUYweeuOtiP3LbyafjWyAb6A02sZCTMAEJ1uZCMYKh3y0SMkulsCHnvij3WCuZCIdJanZC8P2wf0ky5DlL2U6ZBX0vjUKROZBDe0AvZCaZCoU77DON2jqV1neZCo9EQP9karPi4PgWGFPvWbi0qGqPuxZAcbCs8KPOs1zIMeFBdQDuFXiHDlxyAZDZD')
# fields=['email, birthday,posts']
# f_book=graph.get_object('me', fields=fields)

# # print(json.dumps(f_book, indent=4))
# with open('data.txt', 'w') as outfile:
#     json.dump(f_book, outfile )




dict_list=[
  [
      {
      "name":"AAAAA",
      "age":"12",
      "class":"box"
      },
      {
      "name":"AAAAA",
      "age":"12",
      "class":"box"
      },
      {
      "name":"AAAAA",
      "age":"12",
      "class":"box"
      }
  ],
  [
      {
          "name":"DDDD",
      "age":"10",
      "class":"parce"
      },
      {
          "name":"AAAAA",
      "age":"12",
      "class":"box"
      },
      {
          "name":"AAAAA",
      "age":"12",
      "class":"box"
      }
  ],
  [
      {
          "name":"BBBB",
       "age":"16",
      "class":"cage"
      },
      {
          "name":"AAAAA",
      "age":"12",
      "class":"box"
      },
      {
          "name":"AAAAA",
      "age":"12",
      "class":"box"
      }
  ],
  [
      {
          "name":"EEEE",
      "age":"12",
      "class":"sage"
      },
      {
          "name":"AAAAA",
      "age":"12",
      "class":"box"
      },
      {
          "name":"AAAAA",
      "age":"12",
      "class":"box"
      }
  ],

]


age_list = [] 
for l in dict_list:
    temp_dict = l[0]
    age_list.append(temp_dict["age"])
print(age_list)
c=json.dumps(l)
# get set of duplicates in age list
dup_ages = set([x for x in c if c.count(x) > 1])
print(dup_ages)
for index, age in enumerate(age_list):
    for dup_age in dup_ages:            # do something for a given duplicate age
        if dup_age == age:
            print('Hello')


# [
#     [
#         {
#             "id":"8uih8o9",
#             "name":"ggeujd",
#             "city":"lag lag"
#         }
#         {
#             "id":"8uih8o9",
#             "name":"ggeujd",
#             "city":"lag lag"
#         }
#         {
#             "id":"8uih8o9",
#             "name":"ggeujd",
#             "city":"lag lag"
#         }
#     ]
#     [
#         {
#             "id":"8uih8o9",
#             "name":"ggeujd",
#             "city":"lag lag"
#         }
#         {
#             "id":"90h8o9",
#             "name""mbjgeujd",
#             "city":"lag lag"
#         }
#         {
#             "id":"0u008o9",
#             "name":"poieujd",
#             "city":"lag lag"
#         }
#     ],
#     [
#         {
#             "id":"898990o9",
#             "name":"jjjsiujd",
#             "city":"lag lag"
#         }
#         {
#             "id":"8uih8o9",
#             "name":"ggeujd",
#             "city":"lag lag"
#         }
#         {
#             "id":"8uih8o9",
#             "name":"qwerjd",
#             "city":"lag lag"
#         }
#     ]
# ]








# def graph():
#     facebook.GraphAPI(access_token='EAAD9mIfgmCwBAEOyIohL8caq9QZAlVWJYekyEpFHVAVSmnZCL8kenk5awneY2cOolveBr4v8TRONoE0G6TNcE2rjbbqy6pENr6pZAjj0IwWabsFbpjCFjiflDM5RHupUmypE4k1ItSNvXuAddtlxZAQTODhkDrtJB0yInkZBSdbQbuatvYgujST0KdtZAU3H3rQIYfAyC9vTrikfNpZCfbV6fL4TP7R20HpGDlZCXGAOWeBLvP9AKZAl9')
   

# fields=['email, birthday, posts']

# profile = graph.get_object('me', fields=fields)

# print(json.dumps(profile, indent=4))


# if __name__=="__main__":
#        main()



# age_list = [] 

# for l in dict_list:
#     temp_dict = l[0]
#     age_list.append(temp_dict["age"])

# # get set of duplicates in age list
# dup_ages = set([x for x in l if l.count(x) > 1])

# for index, age in enumerate(age_list):
#     for dup_age in dup_ages:            # do something for a given duplicate age
#         if dup_age == age:
#             dict_list[index]   
