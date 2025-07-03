#!/usr/bin/env python3

from ollama import chat
import glob
import sys
import day1
from markdown_it import MarkdownIt
from rich.console import Console
from rich.markdown import Markdown
import webbrowser
import tempfile
import os


def gather_context(directory):
    past_projects_files = glob.glob(directory)
    past_projects_string = ""
    for project_file in past_projects_files:
        with open(project_file, "r") as file:
            past_projects_string += "* " + file.read().strip() + "\n"

    todays_request = input("What kind of project are we feeling today?\n")
    return todays_request, past_projects_string
        
 
def generate(todays_request, past_projects_context, greeting=None):
    stream = chat(
            model='llama3.2',
            messages=[{'role':'user', 'content':f'Omit the Preamble. Do not explicitly code. Any code generated should be esoteric or pseudo code. Now, suggest a simple python coding projects that covers this request: {todays_request}. It must also build off the following projects: {past_projects_context}.'}],
            stream=True,
            )
    console = Console()
    # Print greeting and context once at the top
    if greeting:
        console.print(f"[bold green]{greeting}[/bold green]")
    if past_projects_context:
        console.print(f"[bold blue]Past Projects:[/bold blue]\n{past_projects_context}")
    console.print(f"[bold magenta]Today's Request:[/bold magenta] {todays_request}\n")
    # Now print the markdown as it streams in, fluidly
    accumulated_markdown = ""
    for chunk in stream:
        accumulated_markdown += chunk['message']['content']
        # Stream the raw markdown text
        print(f"{chunk['message']['content']}", end="", flush=True)
    # Print a newline at the end to finish the output
    print()
    
    # Now render the complete markdown to HTML and open in browser
    md = MarkdownIt()
    html_content = md.render(accumulated_markdown)
    
    # Create a complete HTML dashboard
    dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Project Generator Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            border-radius: 10px;
            background: #f8f9fa;
        }}
        .section h2 {{
            color: #667eea;
            margin-top: 0;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .greeting {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .request {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .projects {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
        }}
        .generated-content {{
            background: #f1f8e9;
            border-left: 4px solid #4caf50;
        }}
        .generated-content h1, .generated-content h2, .generated-content h3 {{
            color: #2e7d32;
        }}
        .generated-content code {{
            background: #e8f5e8;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        .generated-content pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            font-style: italic;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Project Generator</h1>
            <p>Your personalized coding project suggestions</p>
        </div>
        
        <div class="content">
            <div class="greeting">
                <h2>👋 Greeting</h2>
                <p>{greeting if greeting else "Welcome!"}</p>
            </div>
            
            <div class="request">
                <h2>🎯 Today's Request</h2>
                <p>{todays_request}</p>
            </div>
            
            <div class="section projects">
                <h2>📚 Past Projects Context</h2>
                <div>{past_projects_context if past_projects_context else "No past projects found."}</div>
            </div>
            
            <div class="section generated-content">
                <h2>💡 Generated Project Suggestion</h2>
                <div>{html_content}</div>
            </div>
            
            <div class="timestamp">
                Generated on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    # Create temporary HTML file and open in browser
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(dashboard_html)
        temp_file = f.name
    
    # Open in default browser
    webbrowser.open(f'file://{temp_file}')
    console.print(f"\n[bold green]✅ Dashboard opened in browser![/bold green]")
    console.print(f"[dim]HTML file: {temp_file}[/dim]")

if __name__ == "__main__":
    greeting = day1.greet()
    request, context = gather_context("./*.md")
    generate(request, context, greeting=greeting) 

