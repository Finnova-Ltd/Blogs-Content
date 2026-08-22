path = "/var/www/ecrm/index.html"
try:
    with open(path, "r") as f:
        code = f.read()

    widget_code = """  <!-- Omni Chatbot & Behavioral Cookie Scoring -->
  <script src="https://omni-agent.testcustomer2022.workers.dev/cookie-consent.js" defer></script>
  <script src="https://omni-agent.testcustomer2022.workers.dev/widget.js" defer></script>
  <script>
    window.OMNI_CHAT_CONFIG = {
      category: "CRM_PLATFORM",
      businessInfo: {
        businessName: "ECRM Australia",
        phone: "1300 050 099",
        email: "support@ecrm.com.au",
        focusAreas: "Sales Pipeline Management, Marketing Automation, Email Campaigns, Lead Scoring, and Customer Lifecycle Tracking"
      }
    };
  </script>
</body>"""

    if "cookie-consent.js" not in code:
        if "omni-agent.testcustomer2022.workers.dev/widget.js" in code:
            code = code.replace(
                '<script src="https://omni-agent.testcustomer2022.workers.dev/widget.js" defer></script>',
                '<script src="https://omni-agent.testcustomer2022.workers.dev/cookie-consent.js" defer></script>\n  <script src="https://omni-agent.testcustomer2022.workers.dev/widget.js" defer></script>'
            )
        else:
            code = code.replace("</body>", widget_code)
            
        with open(path, "w") as f:
            f.write(code)
        print("Successfully embedded cookie-consent.js and widget.js in /var/www/ecrm/index.html!")
    else:
        print("cookie-consent.js is already present in /var/www/ecrm/index.html!")
except Exception as e:
    print("Notice:", e)
