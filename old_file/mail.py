import webbrowser
import os

# Your email content in HTML format
html_content = """
<html>
  <head>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
      }
      .container {
        width: 80%;
        margin: 0 auto;
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      }
      .header {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px 10px 0 0;
      }
      .header h1 {
        margin: 0;
        font-size: 24px;
      }
      .content {
        margin: 20px 0;
        font-size: 16px;
        line-height: 1.6;
      }
      .table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
      }
      .table th,
      .table td {
        padding: 12px;
        border: 1px solid #ddd;
        text-align: center;
      }
      .table th {
        background-color: #f2f2f2;
      }
      .footer {
        margin-top: 20px;
        text-align: center;
        font-size: 12px;
        color: #777;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>Analysis Report</h1>
      </div>
      <div class="content">
        <p>Hello,</p>
        <p>Here is the latest analysis report generated from the recent PDF files:</p>
        <table class="table">
          <thead>
            <tr>
              <th>Stock Name</th>
              <th>Ticker</th>
              <th>Action Taken</th>
              <th>Quantity</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Apple</td>
              <td>AAPL</td>
              <td>Buy</td>
              <td>100</td>
              <td>$15,000</td>
            </tr>
            <tr>
              <td>Tesla</td>
              <td>TSLA</td>
              <td>Sell</td>
              <td>50</td>
              <td>$30,000</td>
            </tr>
            <tr>
              <td>Amazon</td>
              <td>AMZN</td>
              <td>Hold</td>
              <td>---</td>
              <td>---</td>
            </tr>
          </tbody>
        </table>
        <p>If you have any questions, feel free to contact us.</p>
      </div>
      <div class="footer">
        <p>© 2024 Your Company | Confidential Information | Unsubscribe</p>
      </div>
    </div>
  </body>
</html>
"""

# Save the HTML content to a file
html_file_path = os.path.abspath("email_preview.html")
with open(html_file_path, 'w') as f:
    f.write(html_content)

# Open the HTML file in the default web browser
webbrowser.open(f'file://{html_file_path}')