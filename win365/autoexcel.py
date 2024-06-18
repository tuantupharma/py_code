import openpyxl
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import smtplib
from email.message import EmailMessage

# Authentication and file retrieval
url = 'https://your_sharepoint_site_url'
username = 'your_username'
password = 'your_password'
ctx_auth = AuthenticationContext(url)
if ctx_auth.acquire_token_for_user(username, password):
    ctx = ClientContext(url, ctx_auth)
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print("Web title: {0}".format(web.properties['Title']))

file_url = '/sites/YourSite/Documents/YourFile.xlsx'
response = File.open_binary(ctx, file_url)
with open('./YourFile.xlsx', 'wb') as local_file:
    local_file.write(response.content)

# Processing the Excel file
wb = openpyxl.load_workbook('./YourFile.xlsx')
sheet = wb.active

# Example: Increment all values in the first column by 1
for row in sheet.iter_rows(min_row=2, max_col=1):
    for cell in row:
        cell.value += 1

wb.save('./YourFile.xlsx')

# Upload the file back to SharePoint
with open('./YourFile.xlsx', 'rb') as content_file:
    file_content = content_file.read()

target_file = ctx.web.get_folder_by_server_relative_url('/sites/YourSite/Documents').upload_file('YourFile.xlsx', file_content)
ctx.execute_query()

# Send email notification
msg = EmailMessage()
msg['Subject'] = 'Updated Excel File'
msg['From'] = 'your_email@example.com'
msg['To'] = 'recipient@example.com'
msg.set_content('The Excel file has been updated and uploaded.')

with open('./YourFile.xlsx', 'rb') as f:
    file_data = f.read()
    file_name = f.name

msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

with smtplib.SMTP('smtp.example.com', 587) as server:
    server.starttls()
    server.login('your_email@example.com', 'your_email_password')
    server.send_message(msg)

print("Email sent successfully.")
