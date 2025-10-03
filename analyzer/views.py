import re
import os
import google.generativeai as genai
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from .forms import CodeSubmissionForm

load_dotenv()
genai.configure(api_key="AIzaSyCOFLWIJMpNLKhhmz1eEh9xiip062cu6Go")
model = genai.GenerativeModel("gemini-2.5-pro")


def parse_gemini_response(response_text):
    sections = {"issues": [], "fixes": [], "resources": []}

    # Enhanced pattern to handle different markdown variations
    pattern = r"(?i)\*\*(issues|fixes|resources)\*\*:\s*(.*?)(?=\n\*\*|\Z)"
    matches = re.findall(pattern, response_text, re.DOTALL)

    for match in matches:
        section_type = match[0].lower()
        content = match[1].strip()

        items = []
        for line in content.split("\n"):
            line = line.strip()
            # Handle different list markers and whitespace
            if re.match(r"^[-*•]\s+", line):
                items.append(re.sub(r"^[-*•]\s+", "", line))

        if section_type == "issues":
            sections["issues"] = items
        elif section_type == "fixes":
            sections["fixes"] = items
        elif section_type == "resources":
            sections["resources"] = items

    return sections


def analyze_code(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]

            prompt = f"""Analyze this code for issues, provide fixes, and learning resources:
            {code}

            Format your response EXACTLY like this:
            **Issues**:
            - [list issues with emojis]
            
            **Fixes**:
            - [list fixes with emojis]
            
            **Resources**:
            - [description](full_url)
            """

            try:
                response = model.generate_content(prompt)
                analysis = parse_gemini_response(response.text)

                # Ensure code preservation
                preserved_code = "\n".join([line.rstrip() for line in code.split("\n")])

                return render(
                    request,
                    "result.html",
                    {"analysis": analysis, "code": preserved_code},
                )

            except Exception as e:
                error = f"Analysis Error: {str(e)}"
                return render(request, "index.html", {"form": form, "error": error})

    return render(request, "index.html", {"form": CodeSubmissionForm()})
