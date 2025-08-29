from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from jinja2 import Environment, FileSystemLoader
import tempfile
# import pdfkit
# from playwright.sync_api import sync_playwright

app = FastAPI()
env = Environment(loader=FileSystemLoader("templates"))

@app.get("/", response_class=HTMLResponse)
async def form():
    template = env.get_template("form_inputs.html")
    return template.render()

@app.post("/generate", response_class=HTMLResponse)
async def generate(
    name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    job_title: str = Form(""),
    location: str = Form(""),
    summary: str = Form(""),
    portfolio: str = Form(""),
    other_links: str = Form(""),
    experience: str = Form(""),
    education: str = Form(""),
    projects: str = Form(""),
    certificates: str = Form(""),
    export_pdf: str = Form("no")
):
    portfolio_links = [x.strip() for x in portfolio.splitlines() if x.strip()]
    other_links_list = [x.strip() for x in other_links.splitlines() if x.strip()]
    experience_list = [x.strip() for x in experience.splitlines() if x.strip()]
    education_list = [x.strip() for x in education.splitlines() if x.strip()]
    projects_list = [x.strip() for x in projects.splitlines() if x.strip()]
    certificates_list = [x.strip() for x in certificates.splitlines() if x.strip()]

    template = env.get_template("resume.html")
    html_content = template.render(
        resume={
            "name": name,
            "email": email,
            "mobile": mobile,
            "job_title": job_title,
            "location": location,
            "summary": summary,
            "portfolio_links": portfolio_links,
            "other_links": other_links_list,
            "experience": experience_list,
            "education": education_list,
            "projects": projects_list,
            "certificates": certificates_list
        }
    )

    if export_pdf.lower() == "yes":
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdfkit.from_string(html_content, tmp_file.name)
        return FileResponse(tmp_file.name, media_type="application/pdf", filename="resume.pdf")

    return HTMLResponse(content=html_content)


# def html_to_pdf(html_content, output_file):
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         page.set_content(html_content)
#         page.pdf(path=output_file, format="A4")
#         browser.close()