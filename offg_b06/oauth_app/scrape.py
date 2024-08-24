# Legacy Code used to test scraping only use for reference
# Scraping occurs in admin.py


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
#
# # initialize dataframe
# df = pd.DataFrame(columns = ['title', 'rent','location', 'bed','bath', 'footage', 'imgadd', 'link','description'])
#
# # header settings
# # https://stackoverflow.com/questions/51154114/python-request-get-fails-to-get-an-answer-for-a-url-i-can-open-on-my-browser/51154676
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
#
# #iterate 6 times to get through 6 pages of apartments.com data for charlottesville
# # n=0 #counter for dataframe row
# # for i in range(6):
# #     try:
# #         housingEndpoint = 'https://www.apartments.com/charlottesville-va/%s/'%(i)
# #         response = requests.get(housingEndpoint,headers=headers)
# #         print(response) #confirm endpoint works
# #         soup = BeautifulSoup(response.text, "html.parser")
# #
# #         for item in soup.find_all('li', class_='mortar-wrapper'):
# #             try:
# #                 item_link = item.find('a', class_='property-link')['href']
# #                 df.loc[n, 'link'] = item_link
# #                 n += 1
# #             except Exception as e:
# #                 print('error')
# #     except Exception as e:
# #         print('too many requests from same ip')
#
# # Test Data Frame Population to prevent IP throttling during development
# # df.loc[0, 'link'] = "https://www.apartments.com/2307-jefferson-park-ave-charlottesville-va/t0blm49/"
# df.loc[0, 'link'] = "https://www.apartments.com/the-reserve-at-belvedere-charlottesville-va/2jqt3db/"
#
# # # Go through each row in the dataframe and populate it with data
# # for index, row in df.iterrows(): # for loop synthax from https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
# #     response = requests.get(row['link'], headers=headers)
# #     soup = BeautifulSoup(response.text, "html.parser")
# #     try:
# #         # title field
# #         item_title = soup.find(id='propertyName')
# #         df.loc[index, 'title'] = item_title.text
# #
# #         # location field - requires some string manipulation because link stored as background in style in div
# #         for div in soup.find('div', class_='propertyAddressContainer').find("span"):
# #             df.loc[index, 'location'] = div
# #         #Source for getting stlye: https://stackoverflow.com/questions/54933923/url-of-background-image-embeded-in-a-div-class-of-a-bs4-element
# #         itemAddress = soup.select_one('div.aspectRatioImage')
# #         itemAddress = itemAddress['style']
# #         #Source for string manipulation: https://www.geeksforgeeks.org/python-ways-to-split-a-string-in-different-ways/
# #         itemAddress = itemAddress.replace("background-image: url('", "", 1)
# #         itemAddress = itemAddress.replace("');", "", 1)
# #         df.loc[index, 'imgadd'] = itemAddress
# #
# #         # description field
# #         for desc in soup.find('section', class_='descriptionSection').find("p"):
# #             df.loc[index, 'description'] = desc
# #
# #         # rent, bed, bath, footage fields
# #         # grabs all p tags and iterates through, the modding is because the fields info is always in the same order
# #         b=1
# #         for item in soup.find_all('p', class_='rentInfoDetail'):
# #             if b % 4 == 2:
# #                 itemBed = item.text.replace(" bd", "", 1)
# #                 itemBed = itemBed.split(' -')[0]
# #                 df.loc[index, 'bed'] = itemBed
# #             if b % 4 == 3:
# #                 itemBath = item.text.replace(" ba", "", 1)
# #                 itemBath = itemBath.split(' -')[0]
# #                 df.loc[index, 'bath'] = itemBath
# #             if b % 4 == 0:
# #                 itemFootage = item.text.replace("sq ft", "", 1)
# #                 itemFootage = itemFootage.replace(",", "", 2)
# #                 itemFootage = itemFootage.split(' -')[0]
# #                 df.loc[index, 'footage'] = itemFootage
# #             if b % 4 == 1:
# #                 itemRent = item.text.replace("$", "", 2)
# #                 itemRent = itemRent.replace(",", "", 2)
# #                 itemRent = itemRent.split(' -')[0]
# #                 try:
# #                     df.loc[index, 'rent'] = int(itemRent)
# #                 except Exception as e:
# #                     df=df.drop([df.index[index]])
# #             b+=1
# #     except Exception as e:
# #         # print('error')
# #         # drop any dataframes with a null field to prevent blanks NaN when populating database
# #         df=df.drop([df.index[index]])
# #         # may occur on legacy pages or more likely pages that don't have rent info because they are structured differently
# # print(df.to_markdown())
# #
# # # Not able to iterate directly over the DataFrame
# # # df_records = df.to_dict('records')
# # # model_instances = [models.Housing(
# # #     title = record['title'],
# # #     rent = record['rent'],
# # #     location = record['location'],
# # #     footage = record['footage'],
# # #     bed = record['bed'],
# # #     bath = record['bath'],
# # #     description =record['description'],
# # #     link = record['link'],
# # #     imgadd = record['imgadd'],
# # # ) for record in df_records]
# # #
# # # models.Housing.objects.bulk_create(model_instances)
# #
