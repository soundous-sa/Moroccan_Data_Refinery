from app.services.discovery.url_manager import URLManager

print()

print(URLManager.join(
    "https://www.hcp.ma",
    "/Publications_r.html"
))

print()

print(URLManager.join(
    "https://www.hcp.ma",
    "Publications_r.html"
))

print()

print(URLManager.is_absolute(
    "https://www.hcp.ma"
))

print()

print(URLManager.is_absolute(
    "/publication.pdf"
))