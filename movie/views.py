from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse("<h1>Welcome to home page</h1>")
    #return render(request, 'home.html')
    #return render(request, 'home.html', {"name": "Emmanuel Alvarez Castrillon"})
    searchTerm = request.GET.get("SearchMovie")
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {"name": "Emmanuel Alvarez Castrillon", "searchTerm": searchTerm, "movies": movies})
def about(request):
    #return HttpResponse("<h1>Welcome to about page</h1>")
    return render(request, 'about.html')
def signup(request):
    email = request.GET.get("email")
    return render(request, 'signup.html', {"email": email})

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    # Diccionario: películas por año
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    # ----- Nueva parte: películas por género -----
    movie_counts_by_genre = {}
    for movie in all_movies:
        if movie.genre:  # asegurarse que no esté vacío
            # Suponemos que los géneros están separados por coma, ej: "Action, Adventure"
            first_genre = movie.genre.split(",")[0].strip()
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1
        else:
            movie_counts_by_genre["None"] = movie_counts_by_genre.get("None", 0) + 1

    # -------- Gráfica por año --------
    plt.clf()  # limpiar figura anterior
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # -------- Gráfica por género --------
    plt.clf()
    bar_positions = range(len(movie_counts_by_genre))
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=0.5, align='center', color="orange")
    plt.title('Movies per genre (first genre only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla con las 2 gráficas
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })