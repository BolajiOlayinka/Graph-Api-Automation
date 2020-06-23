
import json
import facebook

graph=facebook.GraphAPI(access_token='EAAD9mIfgmCwBAK3UHDOAW1zvAcF5Wqjq5WCq8Q1wEHpkz5TG2F0GJXqTBtUYweeuOtiP3LbyafjWyAb6A02sZCTMAEJ1uZCMYKh3y0SMkulsCHnvij3WCuZCIdJanZC8P2wf0ky5DlL2U6ZBX0vjUKROZBDe0AvZCaZCoU77DON2jqV1neZCo9EQP9karPi4PgWGFPvWbi0qGqPuxZAcbCs8KPOs1zIMeFBdQDuFXiHDlxyAZDZD')
fields=['email, birthday,posts']
f_book=graph.get_object('me', fields=fields)

# print(json.dumps(f_book, indent=4))
with open('data.txt', 'w') as outfile:
    json.dump(f_book, outfile )










# def graph():
#     facebook.GraphAPI(access_token='EAAD9mIfgmCwBAEOyIohL8caq9QZAlVWJYekyEpFHVAVSmnZCL8kenk5awneY2cOolveBr4v8TRONoE0G6TNcE2rjbbqy6pENr6pZAjj0IwWabsFbpjCFjiflDM5RHupUmypE4k1ItSNvXuAddtlxZAQTODhkDrtJB0yInkZBSdbQbuatvYgujST0KdtZAU3H3rQIYfAyC9vTrikfNpZCfbV6fL4TP7R20HpGDlZCXGAOWeBLvP9AKZAl9')
   

# fields=['email, birthday, posts']

# profile = graph.get_object('me', fields=fields)

# print(json.dumps(profile, indent=4))


# if __name__=="__main__":
#        main()
