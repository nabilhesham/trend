from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import TrendName
from .utils import get_data, get_from_api, save_to_database


def home(request):
    if request.GET:
        choice = request.GET.get('trend_type')
        keyword = request.GET.get('keyword').lower()

        if choice == "intereset_by_region":
            keywords = [i.lstrip(' ') for i in keyword.split(',') if i.startswith(' ') or i]
            is_exist = TrendName.objects.filter(name=keywords[0], search_type="interest_by_region")
            is_exist2 = TrendName.objects.filter(name=keywords[1], search_type="interest_by_region")
            if not is_exist and not is_exist2:
                data = get_data(keywords, choice)
                save_to_database(keywords[:2], data, choice)
            return redirect(reverse("search_results", kwargs={"trend_name1": keywords[0],
                                        "trend_name2":keywords[1], "search_type":choice}))  

        elif choice == "get_historical_interest":
            is_exist = TrendName.objects.filter(name=keyword, search_type="get_historical_interest")
            if not is_exist:
                data = get_data(keyword, choice)
                save_to_database(keyword, data, choice)
            return redirect(reverse("search_results", kwargs={"trend_name1": keyword,
                                             "trend_name2":None, "search_type":choice}))
   
    return render(request, "home.html")



def search_results(request, trend_name1, search_type, trend_name2):
    context = {}
    if search_type == "intereset_by_region":
        trens_names = [trend_name1, trend_name2]
        data = get_from_api(trens_names, search_type)
        context['trend_1_json_data'] = data[0]
        context['trend_2_json_data'] = data[1]

    elif search_type == "get_historical_interest":
        data = get_from_api(trend_name1, search_type)
        context['trend_1_json_data'] = data

    return render(request, "search_results.html", context)

