from django.http import HttpResponse
from django.shortcuts import render
from .services import (format_file_tree, get_dependency_file, generate_roast_and_readme, generate_full_readme, get_repo_details, fetch_file_tree, parse_ai_response)

def home_view(request):
    return render(request, 'a_home/home.html')

def roast_repo_view(request):
    if request.htmx:
        
        repo_url = request.POST.get('repo_url')
        owner, project = get_repo_details(repo_url)
        
        if not owner or not project:
            context = {'roast': "That doesn't look like a valid Github Link."}
            return render(request, 'a_home/partials/roast_partial', context)

        files = fetch_file_tree(owner, project)
        
        if not files:
            context = {'roast': "Could not find that repository. It is private?"}
            return render(request, 'a_home/partials/roast_partial.html', context)

        tree_string = format_file_tree(files)
        dependencies = get_dependency_file(owner, project, files)

        ai_response = generate_roast_and_readme(tree_string, dependencies)
        cleaned_data = parse_ai_response(ai_response)

        context = {'url': repo_url, 'roast': cleaned_data['roast'], 'readme_title': cleaned_data['title']}

        return render(request, 'a_home/partials/roast_partial.html', context)

    return HttpResponse("Wrong request for the endpoint...", status=400)

def generate_readme_view(request):
    if request.htmx:
        repo_url = request.POST.get("repo_url")
        owner, repo_name = get_repo_details(repo_url)

        files = fetch_file_tree(owner, repo_name)
        tree_string = format_file_tree(files)
        dependencies = get_dependency_file(owner, repo_name, files)
        readme_content = generate_full_readme(tree_string, dependencies)

        context = {'readme': readme_content}
        return render(request, 'a_home/partials/readme_result.html', context)

    return HttpResponse("Wrong request...", status=400)

