from fastapi.templating import Jinja2Templates

# All HTML templates live in app/templates; every web router imports this object
templates = Jinja2Templates(directory="app/templates")