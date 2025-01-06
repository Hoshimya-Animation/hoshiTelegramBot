from apiget.mangapi import MangaApp
#Instantiation class AnimeApp
rand_manga = MangaApp()
#Change language to spanish
rand_manga.changeLanguage('en')
#Change option to random
rand_manga.getOption('randmanga')
#print the data
print(rand_manga.getMangaData())
#Instantiation class AnimeApp
source_manga = MangaApp()
#Change language to japanese
source_manga.changeLanguage('ja')
#Give the name of anime. Input is available on english japanese and romaji without special characters.
source_manga.changemangaSource('めぞん一刻')
#Change option to username input
source_manga.getOption('usermanga')
#print the data 
print(source_manga.getMangaData())
#Instantiation class AnimeApp
recomendation_gender = MangaApp()
#Change language to spanish
recomendation_gender.changeLanguage('es')
#Search and print recomendation
print(recomendation_gender.getSuggestbyGenre('Fantasy'))