from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import pandas as pd
from pytrends.request import TrendReq
from .models import TrendName, Trend


def home(request):
    not_found = False
    keyword = ""
    # when submit the search form
    if request.GET :
        #  get the search type if region=>interest_by_region or historical=>get_historical_interest
        choice = request.GET.get('trend_type')
        # Connect to Google
        pytrend = TrendReq(hl='en-US', tz=360)
        # get the search keyword
        keyword = request.GET['keyword']
        # interest_by_region search
        if choice == "region" :

            # check for keywords number to meet requirements ( 2 keywords)
            keywords = keyword.split(',')
            if len(keywords) > 2 or len(keywords) < 2:
                print("error")
            elif keyword == "":
                print("error")
            else:
                counter =  0
                for i in keywords:
                    # Build Payload for pytrends
                    pytrend.build_payload(kw_list=[i])
                    # get the data from the api
                    data = pytrend.interest_by_region()
                    data = data.to_dict()[i]


                    # check if the trends is already in the database or not by searching by the search_type and keywords
                    previous_trend_name_region =TrendName.objects.filter(search_type="interest_by_region")
                    if previous_trend_name_region :
                        previous_trend_name_name =previous_trend_name_region.filter(name=i)
                        if previous_trend_name_name:
                            trend_name = previous_trend_name_name
                        else :
                            not_found = True
                    else :
                        not_found = True

                    # if the search didn't exist .. create a new object for the results and save it in the database
                    if not_found : 
                        trend_name = TrendName.objects.create(name=i, search_type="interest_by_region")
                        print(trend_name)     
                        for k,v in data.items():
                            print(counter)
                            if counter == 10:
                                counter = 0
                                break
                            Trend.objects.create(name=trend_name, region=str(k).split(" ")[0], interest=v) 
                            counter += 1

                # redirect us to the search results view with the data
                trend_name1 = keywords[0]
                trend_name2 = keywords[1]
                search_type = "interest_by_region"
                return redirect(reverse("search_results", kwargs={"trend_name1": trend_name1, "trend_name2":trend_name2, "search_type":search_type}))

        # get_historical_interest search
        elif  choice == "historical":
            # check for the requirments of the search ( 1 keyword only )
            keywords = keyword.split(',')
            if len(keywords) > 1 :
                print("error")
            elif keyword == "":
                print("error")
            else:
                # connect to google
                pytrend = TrendReq(hl='en-US', tz=360)
                counter = 0
                for i in keywords:
                    pytrend.build_payload(
                        kw_list=[i],
                        cat=0,
                        timeframe='today 3-m',
                        geo='',
                        gprop='')
                    # getting the data from the api
                    data = pytrend.get_historical_interest([i])
                    data = data.to_dict()[i]
                    
                    # check for previous searchs results in the database
                    previous_trend_name_historical =TrendName.objects.filter(search_type="get_historical_interest")
                    if previous_trend_name_historical :
                        previous_trend_name_name =previous_trend_name_historical.filter(name=i)
                        if previous_trend_name_name:
                            trend_name = previous_trend_name_name
                        else :
                            not_found = True
                    else :
                        not_found = True

                    # create a new result in the database
                    if not_found: 
                        trend_name = TrendName.objects.create(name=i, search_type="get_historical_interest")
                        print(trend_name)     
                        for k,v in data.items():
                            print(counter)
                            if counter == 10:
                                counter = 0
                                break
                            Trend.objects.create(name=trend_name, date=str(k).split(" ")[0], interest=v) 
                            counter += 1

            
                trend_name1 = keywords[0]
                trend_name2 = "none"
                search_type = "get_historical_interest"
                return redirect(reverse("search_results", kwargs={"trend_name1": trend_name1,"trend_name2":trend_name2, "search_type":search_type}))    
    return render(request, "home.html")



def search_results(request, trend_name1, search_type, trend_name2):
    # render the to the results page
    trend2 = ""
    new_trend_name1 = get_object_or_404(TrendName, name=trend_name1, search_type=search_type)
    trend1 = Trend.objects.filter(name=new_trend_name1)
    if trend_name2 == "none":
        pass
    else:
        new_trend_name2 = get_object_or_404(TrendName, name=trend_name2, search_type=search_type)
        trend2 = Trend.objects.filter(name=new_trend_name2)
    context = {"trendData1": trend1,"trendData2": trend2}
    return render(request, "search_results.html", context)

