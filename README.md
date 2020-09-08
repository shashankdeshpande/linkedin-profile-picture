
# LinkedIn Profile Picture Search
## [Prerequisites](#prerequisites)

To be able to use this library, you need to enable Google Custom Search API, generate API key credentials and set a project:
 -   Visit [https://console.developers.google.com](https://console.developers.google.com) and create a project.
 -   Visit [https://console.developers.google.com/apis/library/customsearch.googleapis.com](https://console.developers.google.com/apis/library/customsearch.googleapis.com) and enable "Custom Search API" for your project.
 -   Visit [https://console.developers.google.com/apis/credentials](https://console.developers.google.com/apis/credentials) and generate API key credentials for your project.
 -   Visit [https://cse.google.com/cse/all](https://cse.google.com/cse/all) and in the web form where you create/edit your custom search engine. 
Enable "Image search" and "Search the entire web" options.
Add specific page url as [www.linkedin.com](www.linkedin.com) in "Sites to search" option.

After setting up your Google developers account and project, you should have been provided with developers API key and project CX.

## [Installation](#installation)
Install directly from the GitHub repository
```bash
pip install git+https://github.com/shashankdeshpande/linkedin-profile-picture.git
```
## [Usage](#usage)
```python
> from linkedin_profile_picture import ProfilePicture
> lp = ProfilePicture("your_dev_key","your_project_cx")
```
```python
> params = {"q": "linkedin_id"}
> res = lp.search(params)
> res.link
"https://media-exp1.licdn.com/dms/image/C5103AQFg0lOJGLL5nQ/profile-displayphoto-shrink_200_200/0?e=1605139200&v=beta&t=ezcdygbf8i6Hz7DLdZ2xbKkzpbpPlFHryQ_uUJ2XW-8"
```
