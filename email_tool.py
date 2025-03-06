import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(to, subject, text, from_name=None):
    """
    Send an email using Mailgun API.
    
    Args:
        to (str): Recipient email address
        subject (str): Email subject
        text (str): Email body content
        from_name (str, optional): Sender name. Defaults to None.
    
    Returns:
        dict: Response from Mailgun API
    """
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_DOMAIN")
    
    if not api_key or not domain:
        return {"error": "Mailgun API key or domain not configured in .env file"}
    
    from_email = f"{from_name} <mailgun@{domain}>" if from_name else f"mailgun@{domain}"
    
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": from_email,
                "to": to,
                "subject": subject,
                "text": text
            }
        )
        
        if response.status_code == 200:
            return {"success": True, "message": "Email sent successfully"}
        else:
            return {"error": f"Failed to send email: {response.text}"}
    except Exception as e:
        return {"error": f"Error sending email: {str(e)}"}