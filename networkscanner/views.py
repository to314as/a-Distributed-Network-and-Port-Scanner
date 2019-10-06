from django.shortcuts import render


def output(request):
	print("works so far")
	return(request,'index.html',{'data':"data"})
