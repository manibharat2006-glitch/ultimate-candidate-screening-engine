import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from skills import SKILLS, SKILL_WEIGHTS

# ------------------ ENGINE LOGIC ------------------ #
def match_skills(resume_text):
    matched = {"core": [], "soft": [], "optional": []}
    missing = {"core": [], "soft": [], "optional": []}
    for category, skills in SKILLS.items():
        for skill in skills:
            if skill in resume_text:
                matched[category].append(skill)
            else:
                missing[category].append(skill)
    total_score = 0
    for cat in SKILLS:
        cat_score = (len(matched[cat]) / len(SKILLS[cat])) * SKILL_WEIGHTS[cat] * 100
        total_score += cat_score
    return matched, missing, total_score

def experience_score(resume_text):
    points = 0
    if "internship" in resume_text:
        points += 5
    if "project" in resume_text:
        points += 10
    if "experience" in resume_text or "worked" in resume_text or "developed" in resume_text:
        points += 20
    return min(points, 30)

def keyword_density(resume_text, job_text):
    keywords = job_text.split()
    count = sum(1 for word in keywords if word in resume_text)
    density = (count / len(keywords)) * 100 if keywords else 0
    return min(density, 20)

def strength_highlight(resume_text):
    highlights = []
    if "problem solving" in resume_text:
        highlights.append("Strong problem-solving skills")
    if "communication" in resume_text:
        highlights.append("Good communication")
    if "leadership" in resume_text:
        highlights.append("Leadership potential")
    if "teamwork" in resume_text:
        highlights.append("Teamwork skills")
    return highlights

def final_score(skill_score, exp_score, keyword_score):
    return skill_score + exp_score + keyword_score

def decision(score):
    if score >= 80:
        return "SHORTLISTED", "green"
    elif score >= 60:
        return "NEEDS REVIEW", "orange"
    else:
        return "REJECTED", "red"

# ------------------ RUN ENGINE ON ONE RESUME ------------------ #
def run_screening_gui(resume_text, job_text, output_widget):
    matched, missing, skill_score = match_skills(resume_text)
    exp_score = experience_score(resume_text)
    keyword_score = keyword_density(resume_text, job_text)
    highlights = strength_highlight(resume_text)
    total_score = final_score(skill_score, exp_score, keyword_score)
    final_decision, color = decision(total_score)

    output_widget.config(state='normal')
    output_widget.delete(1.0, tk.END)

    # Title
    output_widget.insert(tk.END, "--- Candidate Screening Result ---\n\n", "title")

    # Matched Skills
    output_widget.insert(tk.END, "Matched Skills:\n", "header")
    for cat in matched:
        output_widget.insert(tk.END, f"{cat.capitalize()}: {', '.join(matched[cat])}\n", "matched")

    # Missing Skills
    output_widget.insert(tk.END, "\nMissing Skills:\n", "header")
    for cat in missing:
        output_widget.insert(tk.END, f"{cat.capitalize()}: {', '.join(missing[cat])}\n", "missing")

    # Scores
    output_widget.insert(tk.END, f"\nSkill Score: {skill_score:.2f}\n")
    output_widget.insert(tk.END, f"Experience Score: {exp_score}\n")
    output_widget.insert(tk.END, f"Keyword Score: {keyword_score:.2f}\n")
    output_widget.insert(tk.END, f"Resume Strength Score: {total_score:.2f}\n")
    output_widget.insert(tk.END, f"Final Decision: {final_decision}\n", color)

    # Strength Highlights
    if highlights:
        output_widget.insert(tk.END, "\nStrength Highlights:\n", "header")
        for h in highlights:
            output_widget.insert(tk.END, f"- {h}\n", "highlight")

    # Suggestions
    if any(missing.values()):
        output_widget.insert(tk.END, "\nSuggestions:\n", "header")
        for cat in missing:
            if missing[cat]:
                output_widget.insert(tk.END, f"Learn {cat} skills first: {', '.join(missing[cat])}\n", "suggestion")

    output_widget.config(state='disabled')

# ------------------ GUI ------------------ #
def browse_file(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)

def screen_resume():
    resume_path = resume_entry.get()
    job_path = job_entry.get()
    if resume_path.endswith(".txt"):
        with open(resume_path, "r") as f:
            resume_text = f.read().lower()
    else:
        resume_text = resume_path.lower()

    if job_path.endswith(".txt"):
        with open(job_path, "r") as f:
            job_text = f.read().lower()
    else:
        job_text = job_path.lower()

    run_screening_gui(resume_text, job_text, output_box)

def save_results():
    text = output_box.get(1.0, tk.END)
    if text.strip() == "":
        messagebox.showwarning("Warning", "No results to save!")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
    if filename:
        with open(filename, "w") as f:
            f.write(text)
        messagebox.showinfo("Saved", f"Results saved to {filename}")

# ------------------ MAIN WINDOW ------------------ #
root = tk.Tk()
root.title("Ultimate Candidate Screening Engine")
root.geometry("900x650")

# Title banner
title_label = tk.Label(root, text="Ultimate Candidate Screening Engine", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Resume input
tk.Label(root, text="Resume (paste text or choose file):").pack()
resume_entry = tk.Entry(root, width=100)
resume_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(resume_entry)).pack(pady=2)

# Job description input
tk.Label(root, text="Job Description (paste text or choose file):").pack()
job_entry = tk.Entry(root, width=100)
job_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(job_entry)).pack(pady=2)

# Run and save buttons
tk.Button(root, text="Run Screening", bg="green", fg="white", command=screen_resume).pack(pady=5)
tk.Button(root, text="Save Results", bg="blue", fg="white", command=save_results).pack(pady=2)

# Output box
output_box = scrolledtext.ScrolledText(root, width=105, height=25)
output_box.pack(pady=10)

# Text tags for colors
output_box.tag_config("title", font=("Helvetica", 12, "bold"))
output_box.tag_config("header", font=("Helvetica", 11, "bold"))
output_box.tag_config("matched", foreground="green")
output_box.tag_config("missing", foreground="red")
output_box.tag_config("highlight", foreground="goldenrod")
output_box.tag_config("suggestion", foreground="orange")
output_box.tag_config("green", foreground="green", font=("Helvetica", 11, "bold"))
output_box.tag_config("orange", foreground="orange", font=("Helvetica", 11, "bold"))
output_box.tag_config("red", foreground="red", font=("Helvetica", 11, "bold"))

root.mainloop()
