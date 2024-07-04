# from django.shortcuts import render
# from django.views.generic import View
# from watchlist_app.models import Movie
# from django.http import JsonResponse


# ####### function based view
# def movie_list(request):
#     movies=Movie.objects.all()
#     data={
#         'movies':list(movies.values())
#     }
    
#     return JsonResponse(data)


# def movie_detail(request,pk):
#     movie=Movie.objects.get(pk)
#     data={
#         'name':movie.name,
#         'description':movie.description,
#         'active':movie.active
#     }
#     return JsonResponse(data)
    
    
    
# class MovieListview(View):
#     def get(self,request):
#         qs=Movie.objects.all()
#         data={'movie':list(qs.values())}
#         return JsonResponse(data)
    
    
        
    
    