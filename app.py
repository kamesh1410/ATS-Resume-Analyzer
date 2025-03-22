import PyPDF2
import re
import gradio as gr

# Predefined IT job roles and skills (expanded with more roles and skills)
JOB_ROLES = {
    "Data Scientist": ["python", "machine learning", "statistics", "sql", "data analysis", "r", "pandas", "numpy", "data visualization", "scikit-learn", "probability", "mathematics", "jupyter", "matplotlib", "seaborn", "big data", "hadoop", "spark", "dask", "statsmodels", "plotly"],
    "Software Engineer": ["python", "java", "c++", "software development", "git", "javascript", "agile", "debugging", "oop", "api development", "unit testing", "design patterns", "spring", "hibernate", "maven", "gradle", "docker", "sql", "golang", "kotlin", "tdd"],
    "Project Manager": ["project management", "leadership", "communication", "budgeting", "scheduling", "agile", "scrum", "risk management", "stakeholder management", "ms project", "team coordination", "pmp", "prince2", "jira", "confluence", "kanban", "waterfall", "resource allocation"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js", "typescript", "responsive design", "webpack", "rest api", "frontend", "backend", "ui/ux", "sass", "less", "bootstrap", "graphql", "next.js", "express", "svelte", "gatsby", "web accessibility"],
    "DevOps Engineer": ["aws", "docker", "kubernetes", "ci/cd", "linux", "jenkins", "terraform", "ansible", "cloud", "bash", "monitoring", "infrastructure", "gitlab", "prometheus", "grafana", "nginx", "azure devops", "helm", "vault", "istio", "argocd"],
    "Cybersecurity Analyst": ["network security", "penetration testing", "firewall", "siem", "incident response", "cryptography", "vulnerability assessment", "ethical hacking", "ids/ips", "soc", "wireshark", "kali linux", "metasploit", "owasp", "cissp", "nessus", "burp suite", "splunk"],
    "Database Administrator": ["sql", "mysql", "oracle", "mongodb", "database design", "backup", "recovery", "performance tuning", "data modeling", "etl", "indexing", "postgresql", "nosql", "redis", "data warehousing", "pl/sql", "cassandra", "dynamodb", "high availability"],
    "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "computer vision", "scikit-learn", "data preprocessing", "model deployment", "keras", "xgboost", "lightgbm", "feature engineering", "hyperparameter tuning", "fastai", "onnx", "mlflow"],
    "Cloud Engineer": ["aws", "azure", "google cloud", "cloud architecture", "virtualization", "serverless", "iam", "networking", "cost management", "migration", "ec2", "s3", "lambda", "cloudformation", "gcp", "load balancing", "cloud security", "azure functions", "terraform"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node.js", "express", "mongodb", "sql", "rest api", "git", "authentication", "deployment", "angular", "vue.js", "django", "flask", "jwt", "mysql", "laravel", "redis", "graphql"],
    "Mobile App Developer": ["flutter", "react native", "swift", "kotlin", "android", "ios", "mobile ui", "api integration", "debugging", "app store", "cross-platform", "dart", "xcode", "android studio", "firebase", "push notifications", "jetpack compose", "swiftui"],
    "UI/UX Designer": ["ui design", "ux research", "figma", "adobe xd", "wireframing", "prototyping", "user testing", "interaction design", "visual design", "usability", "sketch", "invision", "user personas", "accessibility", "design systems", "zeplin", "motion design", "user flows"],
    "Business Analyst": ["requirements gathering", "data analysis", "sql", "stakeholder management", "uml", "process modeling", "agile", "jira", "documentation", "business process", "bpmn", "visio", "power bi", "tableau", "gap analysis", "use case diagrams", "swot analysis"],
    "Network Engineer": ["cisco", "routing", "switching", "firewall", "tcp/ip", "vpn", "lan/wan", "ospf", "bgp", "network troubleshooting", "ccna", "ccnp", "wireshark", "sd-wan", "mpls", "vlan", "juniper", "palo alto", "netflow"],
    "System Administrator": ["linux", "windows server", "active directory", "vmware", "powershell", "backup", "disaster recovery", "networking", "security", "monitoring", "hyper-v", "sccm", "dns", "dhcp", "group policy", "exchange server", "sharepoint", "itil"],
    "Quality Assurance Engineer": ["testing", "selenium", "automation", "manual testing", "jira", "test cases", "bug tracking", "regression testing", "api testing", "performance testing", "cypress", "postman", "jmeter", "testrail", "load testing", "appium", "browserstack", "test automation frameworks"],
    "AI Engineer": ["python", "tensorflow", "pytorch", "ai", "deep learning", "nlp", "computer vision", "reinforcement learning", "data preprocessing", "model optimization", "onnx", "hugging face", "bert", "gans", "model evaluation", "tflite", "coreml", "ai ethics"],
    "Data Engineer": ["python", "sql", "etl", "big data", "hadoop", "spark", "kafka", "data pipelines", "data warehousing", "cloud", "snowflake", "airflow", "databricks", "redshift", "data lakes", "dbt", "apache nifi", "data integration", "data quality"],
    "Game Developer": ["unity", "unreal engine", "c#", "c++", "game design", "3d modeling", "animation", "physics", "multiplayer", "vr/ar", "optimization", "blender", "maya", "shader programming", "gameplay mechanics", "godot", "photon", "playfab"],
    "Blockchain Developer": ["solidity", "ethereum", "smart contracts", "web3", "blockchain", "cryptography", "dapps", "truffle", "metamask", "security", "decentralized", "ipfs", "hyperledger", "chaincode", "nft", "polkadot", "cardano", "defi"],
    "IoT Developer": ["python", "c", "iot", "networking", "sensors", "cloud", "mqtt", "embedded systems", "data processing", "security", "raspberry pi", "arduino", "zigbee", "bluetooth", "edge computing", "aws iot", "azure iot", "lora"],
    "IT Support Specialist": ["troubleshooting", "technical support", "windows", "linux", "networking", "customer service", "it support", "ticketing systems", "hardware", "software installation", "remote desktop", "itil", "helpdesk", "ms office", "voip", "zendesk", "servicenow", "sla management"],
    "Embedded Systems Engineer": ["c", "c++", "embedded systems", "microcontrollers", "rtos", "hardware design", "firmware", "debugging", "sensors", "iot", "arm", "i2c", "spi", "uart", "pcb design", "stm32", "freertos", "keil"],
    "AR/VR Developer": ["unity", "unreal engine", "c#", "c++", "ar/vr", "3d modeling", "animation", "spatial computing", "vr headsets", "augmented reality", "oculus", "hololens", "webxr", "motion tracking", "immersive design", "arkit", "arcore", "vr optimization"],
    "Robotics Engineer": ["robotics", "python", "c++", "ros", "control systems", "sensors", "automation", "machine learning", "embedded systems", "mechanical design", "slam", "path planning", "gazebo", "opencv", "actuators", "ros2", "lidar", "kinematics"],
    "Site Reliability Engineer": ["aws", "azure", "linux", "monitoring", "automation", "python", "bash", "incident response", "sre", "scalability", "prometheus", "grafana", "elk stack", "chaos engineering", "high availability", "opentelemetry", "runbooks", "slo/sli"],
    "Frontend Developer": ["html", "css", "javascript", "react", "vue.js", "angular", "typescript", "sass", "responsive design", "webpack", "es6", "ui frameworks", "tailwind css", "babel", "jest", "storybook", "accessibility", "vite", "lit", "web components"],
    "Backend Developer": ["node.js", "python", "java", "ruby", "php", "sql", "mongodb", "rest api", "graphql", "authentication", "server management", "microservices", "redis", "rabbitmq", "nginx", "orm", "kafka", "nestjs", "fastapi", "spring boot", "golang"],
    "Data Analyst": ["sql", "excel", "python", "r", "tableau", "power bi", "data visualization", "statistics", "data cleaning", "dashboards", "business intelligence", "google analytics", "looker", "pandas", "numpy", "a/b testing", "qlikview", "data storytelling"],
    "Technical Writer": ["technical writing", "documentation", "markdown", "api documentation", "user manuals", "communication", "research", "editing", "content management", "version control", "dita", "xml", "confluence", "sphinx", "readthedocs", "asciidoc", "gitbook", "technical diagrams"],
    "IT Consultant": ["it strategy", "business analysis", "project management", "cloud solutions", "cybersecurity", "network design", "vendor management", "client communication", "problem solving", "it audits", "digital transformation", "erp systems", "crm", "it governance", "change management", "it roadmapping"],
    "ERP Consultant": ["sap", "oracle erp", "microsoft dynamics", "erp implementation", "business process", "data migration", "training", "customization", "integration", "support", "abap", "sap hana", "dynamics 365", "netsuite", "odoo", "erp testing", "workflow automation"],
    "Solutions Architect": ["system design", "aws", "azure", "microservices", "scalability", "integration", "cloud architecture", "security", "performance optimization", "stakeholder collaboration", "togaf", "uml", "enterprise architecture", "api gateway", "serverless", "design patterns", "event-driven architecture"],
    "Product Manager": ["product management", "roadmap planning", "agile", "user stories", "market research", "stakeholder management", "prioritization", "analytics", "ux design", "cross-functional collaboration", "jira", "asana", "a/b testing", "kpis", "go-to-market strategy", "product lifecycle", "customer feedback"],
    "Scrum Master": ["scrum", "agile", "sprint planning", "facilitation", "jira", "team coaching", "conflict resolution", "velocity tracking", "retrospectives", "kanban", "safe", "burndown charts", "servant leadership", "agile metrics", "team dynamics", "scrum ceremonies", "agile transformation"],
    "Information Security Manager": ["cybersecurity", "risk management", "compliance", "iso 27001", "nist", "security policies", "incident response", "team leadership", "audits", "training", "gdpr", "soc 2", "penetration testing", "security awareness", "cism", "threat modeling", "security governance"],
    # New IT job roles and skills
    "Big Data Engineer": ["hadoop", "spark", "kafka", "big data", "python", "scala", "hive", "pig", "flink", "data pipelines", "hbase", "impala", "sqoop", "data lakes", "cloud", "aws glue", "azure data factory", "data streaming"],
    "Automation Engineer": ["automation", "python", "selenium", "ansible", "bash", "powershell", "ci/cd", "testing", "robot framework", "ui automation", "api automation", "test automation", "puppet", "chef", "scripting", "process automation", "rpa", "uipath"],
    "Network Security Engineer": ["firewall", "vpn", "ids/ips", "network security", "cisco", "palo alto", "fortinet", "siem", "threat hunting", "encryption", "ssl/tls", "ipsec", "network monitoring", "security audits", "ccnp security", "checkpoint", "zero trust"],
    "Software Architect": ["software architecture", "design patterns", "microservices", "java", "python", "system design", "scalability", "cloud", "aws", "azure", "api design", "soa", "event-driven architecture", "technical leadership", "code review", "uml", "ddd"],
    "IT Auditor": ["it audit", "risk assessment", "compliance", "cobit", "itil", "iso 27001", "security controls", "audit planning", "data analysis", "report writing", "sarbanes-oxley", "pci dss", "internal audit", "it governance", "cybersecurity", "cisa", "audit tools"],
    "Digital Transformation Specialist": ["digital transformation", "change management", "business process", "cloud adoption", "agile", "stakeholder engagement", "data analytics", "automation", "erp systems", "crm", "project management", "innovation", "technology adoption", "business strategy"],
    "E-commerce Developer": ["magento", "shopify", "woocommerce", "php", "javascript", "html", "css", "e-commerce", "payment gateways", "api integration", "mysql", "performance optimization", "seo", "user experience", "cart systems", "inventory management", "bigcommerce"],
    "API Developer": ["rest api", "graphql", "node.js", "python", "java", "api design", "authentication", "oauth", "swagger", "postman", "api testing", "microservices", "json", "xml", "api gateway", "rate limiting", "api security", "open api"],
    "Geospatial Analyst": ["gis", "arcgis", "qgis", "python", "sql", "geospatial analysis", "remote sensing", "data visualization", "esri", "map development", "spatial data", "geodatabase", "cartography", "gps", "geocoding", "raster analysis", "vector analysis"],
    "SDET (Software Development Engineer in Test)": ["selenium", "java", "python", "test automation", "ci/cd", "jenkins", "api testing", "performance testing", "unit testing", "mocking", "junit", "testng", "cucumber", "bdd", "tdd", "git", "docker", "agile"]
}

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        text = re.sub(r'[^\w\s@.-]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

def extract_experience_info(resume_text):
    text_lower = resume_text.lower()
    # Find the experience section
    experience_pattern = r"(experience|work|job|employment|professional)\b.*?(?=(education|skills|summary|objective|profile|$))"
    experience_match = re.search(experience_pattern, text_lower, re.DOTALL | re.IGNORECASE)
    
    total_years = 0
    experience_level = "Fresher"
    experience_details = "No experience section detected."

    if experience_match:
        experience_text = experience_match.group(0)
        experience_details = experience_text.strip()
        # Look for date ranges (e.g., 2020 - 2022, Jan 2021 - Present)
        date_pattern = r"(\b\d{4}\b)\s*[-–—]\s*(\b\d{4}\b|present|current)"
        dates = re.findall(date_pattern, experience_text, re.IGNORECASE)
        
        for start, end in dates:
            start_year = int(start)
            if end.lower() in ["present", "current"]:
                end_year = 2025  # Current year as of the app's context
            else:
                end_year = int(end)
            years = end_year - start_year
            if years >= 0:
                total_years += years

    if total_years > 1:
        experience_level = "Experienced"
    elif 0 < total_years <= 1:
        experience_level = "Fresher with some experience"

    return experience_level, total_years, experience_details

def extract_skills_from_resume(resume_text):
    text_lower = resume_text.lower()
    all_skills = set()
    for skills in JOB_ROLES.values():
        all_skills.update(skills)
    detected_skills = []
    for skill in all_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            detected_skills.append(skill)
    return detected_skills

def recommend_roles(detected_skills, experience_level):
    role_scores = {}
    for role, required_skills in JOB_ROLES.items():
        matched_skills = [skill for skill in detected_skills if skill in required_skills]
        score = len(matched_skills) / len(required_skills) * 100 if required_skills else 0
        # Adjust score based on experience level
        if experience_level == "Fresher" and role in ["Project Manager", "Site Reliability Engineer", "Solutions Architect", "Information Security Manager", "Software Architect", "IT Auditor"]:
            score *= 0.5  # Reduce score for senior roles if fresher
        elif experience_level == "Experienced" and role in ["IT Support Specialist"]:
            score *= 0.8  # Slightly reduce score for entry-level roles if experienced
        role_scores[role] = (score, matched_skills)
    recommended_roles = sorted(role_scores.items(), key=lambda x: x[1][0], reverse=True)[:3]
    return recommended_roles

def generate_job_links(role, experience_level):
    role_encoded = role.replace(" ", "+")
    experience_filter = ""
    if experience_level == "Fresher":
        experience_filter = "+entry+level"  # General filter for entry-level jobs
    elif experience_level == "Experienced":
        experience_filter = "+mid+senior+level"  # General filter for experienced roles

    links = {
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={role_encoded}{experience_filter}",
        "Foundit": f"https://www.foundit.in/search/{role_encoded.replace('+', '-')}-jobs",
        "Indeed": f"https://www.indeed.com/jobs?q={role_encoded}{experience_filter}",
        "Glassdoor": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={role_encoded}{experience_filter}",
        "Naukri": f"https://www.naukri.com/{role_encoded.replace('+', '-')}-jobs" + ("?experience=0" if experience_level == "Fresher" else "?experience=2")
    }
    return links

def resume_chatbot(pdf_file, job_role):
    resume_text = extract_text_from_pdf(pdf_file)
    text_lower = resume_text.lower()

    # Extract experience information
    experience_level, total_years, experience_details = extract_experience_info(resume_text)

    # Extract skills from the resume
    detected_skills = extract_skills_from_resume(resume_text)

    # Recommend roles based on detected skills and experience level
    recommended_roles = recommend_roles(detected_skills, experience_level)

    # Handle the user-specified job role
    job_role_cleaned = job_role.strip()
    job_role_lower = job_role_cleaned.lower()
    job_roles_lower = {key.lower(): key for key in JOB_ROLES.keys()}
    if job_role_lower not in job_roles_lower:
        return f"<div style='font-family: Arial, sans-serif; padding: 20px;'><p style='color: red;'>Error: Job role '{job_role}' not recognized. Available roles: {', '.join(JOB_ROLES.keys())}</p></div>"
    original_job_role = job_roles_lower[job_role_lower]
    job_skills = JOB_ROLES[original_job_role]

    # Analyze the resume for the specified job role
    mistakes = []
    if len(resume_text) < 100:
        mistakes.append("Resume is too short or text extraction failed.")

    sections = {
        "contact": r"\b(name|email|phone|github|portfolio)\b",
        "summary": r"\b(summary|objective|profile)\b",
        "skills": r"\b(skills|expertise|abilities|technologies)\b",
        "experience": r"\b(experience|work|job|employment|professional)\b",
        "education": r"\b(education|degree|university|college|school)\b"
    }
    section_positions = {}
    for section, pattern in sections.items():
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            section_positions[section] = match.start()

    structure_feedback = []
    expected_order = ["contact", "summary", "skills", "experience", "education"]
    detected_sections = list(section_positions.keys())
    missing_sections = [s for s in expected_order if s not in detected_sections]
    if missing_sections:
        structure_feedback.append(f"Missing sections: {', '.join(missing_sections)}")
    if detected_sections:
        sorted_sections = sorted(detected_sections, key=lambda x: section_positions[x])
        ideal_order = [s for s in expected_order if s in detected_sections]
        if sorted_sections != ideal_order:
            structure_feedback.append(f"Sections out of order. Detected: {', '.join(sorted_sections)}. Recommended: {', '.join(ideal_order)}")

    detected_job_skills = []
    for skill in job_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            detected_job_skills.append(skill)
    matched_skills = len(detected_job_skills)
    total_skills = len(job_skills)
    score = (matched_skills / total_skills) * 100 if total_skills > 0 else 0
    if len(re.findall(r"\b(header|footer|image|table)\b", text_lower)) > 0:
        score -= 20
    score = max(0, min(100, score))
    missing_skills = [skill for skill in job_skills if skill not in detected_job_skills]

    skill_feedback = []
    critical_skills = job_skills[:5]
    for skill in detected_job_skills:
        relevance = "Critical" if skill in critical_skills else "Supplementary"
        skill_feedback.append(f"- {skill}: {relevance} skill detected")
    if not detected_job_skills:
        skill_feedback.append("- No relevant skills detected")

    # Generate a concise summary for the specified role
    summary_text = f"Your resume scores {score:.1f}% for the {original_job_role} role. "
    if detected_job_skills:
        summary_text += f"It demonstrates strong skills in {', '.join(detected_job_skills[:3])}, "
    else:
        summary_text += "It lacks relevant skills for this role, "
    if missing_sections:
        summary_text += f"but is missing key sections like {', '.join(missing_sections)}, which are critical for ATS compatibility."
    else:
        summary_text += "and follows the recommended structure for ATS compatibility."

    # Prepare recommended roles feedback with experience-filtered job links
    recommended_roles_feedback = []
    for role, (role_score, matched_skills) in recommended_roles:
        if role_score > 0:  # Only include roles with a match
            job_links = generate_job_links(role, experience_level)
            recommended_roles_feedback.append(
                f"<strong>{role}</strong> (Match Score: {role_score:.1f}%):<br>"
                f"Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}<br>"
                f"Search for {role} jobs (filtered for {experience_level}):<br>"
                f"- <a href='{job_links['LinkedIn']}' target='_blank'>LinkedIn</a><br>"
                f"- <a href='{job_links['Foundit']}' target='_blank'>Foundit</a><br>"
                f"- <a href='{job_links['Indeed']}' target='_blank'>Indeed</a><br>"
                f"- <a href='{job_links['Glassdoor']}' target='_blank'>Glassdoor</a><br>"
                f"- <a href='{job_links['Naukri']}' target='_blank'>Naukri</a><br>"
            )

    color = "#ff4d4d" if score < 40 else "#ffcc00" if score < 70 else "#4caf50"
    circumference = 2 * 3.14159 * 50
    dash_length = (score / 100) * circumference
    combined_output = f"""
    <div class="main-container">
        <!-- ATS Score Section -->
        <div class="ats-score">
            <h3>ATS Score: {score:.1f}%</h3>
            <svg width="200" height="200" viewBox="0 0 200 200" style="filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));">
                <circle cx="100" cy="100" r="50" fill="none" stroke="#4b5563" stroke-width="10"/>
                <circle cx="100" cy="100" r="50" fill="none" stroke="{color}" stroke-width="10"
                    stroke-dasharray="{dash_length} {circumference}" stroke-dashoffset="0"
                    transform="rotate(-90 100 100)">
                    <animate attributeName="stroke-dasharray" from="0 {circumference}" to="{dash_length} {circumference}" dur="2s" fill="freeze" />
                </circle>
                <text x="100" y="105" text-anchor="middle" font-size="20">{score:.1f}%</text>
            </svg>
        </div>

        <!-- Detailed Summary Section -->
        <div class="report-box">
            <h2 class="report-title">ATS Resume Analyzer & Score Bot</h2>
            <h3 style="font-size: 22px; margin-bottom: 15px; border-bottom: 2px solid #3498db; padding-bottom: 5px;">Resume Analysis Report</h3>
            <p style="font-size: 16px; margin-bottom: 10px;"><strong>Job Role:</strong> {original_job_role}</p>
            
            <h4 style="font-size: 18px; margin-top: 20px; display: flex; align-items: center;">
                <svg style="margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Summary
            </h4>
            <p style="font-size: 15px; line-height: 1.6; margin-bottom: 20px;">{summary_text}</p>

            <h5 style="font-size: 16px; margin-top: 20px; display: flex; align-items: center;">
                <svg style="margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2">
                    <path d="M16 4h2a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/>
                    <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
                </svg>
                Resume Structure Analysis
            </h5>
            {"<p style='font-size: 15px; line-height: 1.6;'><strong>Issues Detected:</strong><br>" + "<br>".join([f"  - {f}" for f in structure_feedback]) + "</p><p style='font-size: 15px; line-height: 1.6;'><strong>Recommended Order:</strong> Contact → Summary → Skills → Experience → Education</p>" if structure_feedback else "<p style='font-size: 15px; line-height: 1.6;'><strong>Issues Detected:</strong> None (Structure follows recommended order)</p>"}
            
            {"<h5 style='font-size: 16px; margin-top: 20px; display: flex; align-items: center;'><svg style='margin-right: 8px;' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#3498db' stroke-width='2'><path d='M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'/></svg>General Issues</h5><p style='font-size: 15px; line-height: 1.6;'>" + "<br>".join([f"  - {m}" for f in mistakes]) + "</p>" if mistakes else ""}
            
            <h5 style="font-size: 16px; margin-top: 20px; display: flex; align-items: center;">
                <svg style="margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2">
                    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>
                </svg>
                Skill Relevance Summary for {original_job_role}
            </h5>
            <p style="font-size: 15px; line-height: 1.6;">{"<br>".join(skill_feedback)}</p>
            
            {"<h5 style='font-size: 16px; margin-top: 20px; display: flex; align-items: center;'><svg style='margin-right: 8px;' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#3498db' stroke-width='2'><path d='M5 13l4 4L19 7'/></svg>Suggested Skills to Add (out of " + str(total_skills) + " expected)</h5><p style='font-size: 15px; line-height: 1.6;'>" + "<br>".join([f"  - {s}" for s in missing_skills]) + "</p>" if missing_skills else "<p style='font-size: 15px; line-height: 1.6;'><strong>Suggested Skills to Add:</strong> None</p>"}

            <h5 style="font-size: 16px; margin-top: 20px; display: flex; align-items: center;">
                <svg style="margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2">
                    <path d="M12 2v4m0 12v4M2 12h4m12 0h4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/>
                </svg>
                Experience Analysis
            </h5>
            <p style="font-size: 15px; line-height: 1.6;">
                <strong>Experience Level:</strong> {experience_level}<br>
                <strong>Total Years of Experience:</strong> {total_years} years<br>
                <strong>Details:</strong> {experience_details[:200] + '...' if len(experience_details) > 200 else experience_details}
            </p>

            <h5 style="font-size: 16px; margin-top: 20px; display: flex; align-items: center;">
                <svg style="margin-right: 8px;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2">
                    <path d="M12 2a10 10 0 0110 10c0 4.5-3 8.5-7 9.5v-5h-2v-2h2v-2a2 2 0 012-2h2v-2h-2a4 4 0 00-4 4v2h-2v2h2v5c-4-1-7-5-7-9.5A10 10 0 0112 2z"/>
                </svg>
                Recommended Roles Based on Your Skills and Experience
            </h5>
            <p style="font-size: 15px; line-height: 1.6;">
                {"<br>".join(recommended_roles_feedback) if recommended_roles_feedback else "No strong matches found based on your skills and experience. Consider adding more relevant skills or experience to your resume."}
            </p>
        </div>
    </div>
    """

    return combined_output

# Embed the HTML (no mode toggle button)
content_html = """
<div class="content-wrapper">
</div>
"""

# Embed the CSS with smooth scrolling and mobile optimization
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;500&display=swap');

/* Default to dark mode with smooth scrolling */
html, body, .gradio-container {
    scroll-behavior: smooth;
    position: relative;
    min-height: 100vh;
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    color: #e2e8f0;
    font-family: 'Roboto', sans-serif;
    padding: 20px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden; /* Prevent horizontal scrolling */
}

/* Ensure Gradio's settings button is not affected */
.gradio-container .settings-button {
    display: block !important;
    visibility: visible !important;
    z-index: 1000 !important;
}

/* Main content wrapper */
.content-wrapper {
    position: relative;
    max-width: 900px;
    width: 100%;
    min-height: 40px;
    background: transparent;
    border: none;
    padding: 20px;
    margin: 0 auto;
    z-index: 10;
}

/* Polygon elements for background decoration */
.polygon {
    position: absolute;
    width: 40px;
    height: 40px;
    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
    opacity: 0.2;
    z-index: -1;
    will-change: transform;
}
.polygon:nth-child(1) {
    top: 10%;
    left: 5%;
    background: linear-gradient(45deg, #60a5fa, #a855f7);
    animation: float 30s infinite linear;
}
.polygon:nth-child(2) {
    top: 30%;
    left: 60%;
    background: linear-gradient(45deg, #a855f7, #60a5fa);
    animation: float 35s infinite linear reverse;
}
.polygon:nth-child(3) {
    top: 70%;
    left: 20%;
    background: linear-gradient(45deg, #60a5fa, #a855f7);
    animation: float 25s infinite linear;
}
.polygon:nth-child(4) {
    top: 50%;
    left: 80%;
    background: linear-gradient(45deg, #a855f7, #60a5fa);
    animation: float 28s infinite linear reverse;
}

/* Slower floating animation for polygons */
@keyframes float {
    0% {
        transform: translate(0, 0) rotate(0deg);
    }
    50% {
        transform: translate(50vw, 30vh) rotate(180deg);
    }
    100% {
        transform: translate(0, 0) rotate(360deg);
    }
}

/* Inject polygons dynamically */
.gradio-container::before,
.gradio-container::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
}
.gradio-container > div::before,
.gradio-container > div::after,
.gradio-container > div:nth-child(1)::before,
.gradio-container > div:nth-child(1)::after,
.gradio-container > div:nth-child(2)::before,
.gradio-container > div:nth-child(2)::after,
.gradio-container > div:nth-child(3)::before,
.gradio-container > div:nth-child(3)::after {
    content: '';
    position: absolute;
    width: 40px;
    height: 40px;
    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
    opacity: 0.2;
    z-index: -1;
    will-change: transform;
}
.gradio-container > div:nth-child(1)::before {
    top: 10%;
    left: 5%;
    background: linear-gradient(45deg, #60a5fa, #a855f7);
    animation: float 30s infinite linear;
}
.gradio-container > div:nth-child(1)::after {
    top: 30%;
    left: 60%;
    background: linear-gradient(45deg, #a855f7, #60a5fa);
    animation: float 35s infinite linear reverse;
}
.gradio-container > div:nth-child(2)::before {
    top: 70%;
    left: 20%;
    background: linear-gradient(45deg, #60a5fa, #a855f7);
    animation: float 25s infinite linear;
}
.gradio-container > div:nth-child(2)::after {
    top: 50%;
    left: 80%;
    background: linear-gradient(45deg, #a855f7, #60a5fa);
    animation: float 28s infinite linear reverse;
}

/* Custom heading style for Gradio title */
.gradio-container h1 {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 32px !important;
    text-align: center !important;
    margin-bottom: 40px !important;
    position: relative !important;
    color: #ffffff !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    z-index: 10 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    white-space: normal !important;
    overflow: visible !important;
    line-height: 1.2 !important;
}
.gradio-container h1::before {
    content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/%3E%3Crect x='8' y='2' width='8' height='4' rx='1' ry='1'/%3E%3Cpath d='M9 10h6m-6 4h6'/%3E%3C/svg%3E");
    display: inline-block;
    margin-right: 10px;
}
.gradio-container h1::after {
    content: '';
    position: absolute;
    width: 120px;
    height: 8px;
    background: linear-gradient(90deg, #60a5fa, #a855f7);
    bottom: -20px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

/* Style for the report title */
.report-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 24px;
    text-align: center;
    margin-bottom: 20px;
    position: relative;
    color: #e2e8f0;
}
.report-title::after {
    content: '';
    position: absolute;
    width: 100px;
    height: 6px;
    background: linear-gradient(90deg, #60a5fa, #a855f7);
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

/* Style for input fields */
input, .gr-textbox, .gr-file-upload {
    background: #2d3748 !important;
    color: #e2e8f0 !important;
    border: 1px solid #4b5563 !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-size: 16px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    width: 100% !important;
    box-sizing: border-box;
    margin-top: 20px !important;
    transition: all 0.3s ease;
}
.gr-file-upload {
    background: #2d3748 !important;
    border: 1px solid #4b5563 !important;
    border-radius: 8px !important;
    padding: 20px !important;
    text-align: center !important;
}
.gr-button {
    background: linear-gradient(90deg, #60a5fa, #a855f7) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
    transition: transform 0.2s ease, background 0.3s ease !important;
    width: 100%;
    max-width: 200px;
    margin: 20px auto;
    display: block;
}
.gr-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}

/* Input container */
.input-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 600px;
    margin: 20px auto;
}

/* Main container for output */
.main-container {
    font-family: 'Roboto', sans-serif;
    padding: 20px;
    border-radius: 10px;
    max-width: 800px;
    margin: 0 auto;
}

/* ATS Score Section */
.ats-score {
    text-align: center;
    margin-bottom: 40px;
}
.ats-score h3 {
    font-size: 24px;
    margin-bottom: 15px;
    color: #e2e8f0;
}
.ats-score text {
    fill: #e2e8f0;
}

/* Report Section */
.report-box {
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    background: #2d3748;
}
.report-box h3, .report-box h4, .report-box h5 {
    color: #e2e8f0;
}
.report-box p {
    color: #b0b7c3;
}
.report-box strong {
    color: #d1d5db;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    html, body, .gradio-container {
        padding: 10px;
    }

    .content-wrapper {
        padding: 15px;
    }

    .gradio-container h1 {
        font-size: 24px !important;
        white-space: normal !important;
        line-height: 1.2 !important;
        padding: 0 10px !important;
    }

    .gradio-container h1::before {
        content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/%3E%3Crect x='8' y='2' width='8' height='4' rx='1' ry='1'/%3E%3Cpath d='M9 10h6m-6 4h6'/%3E%3C/svg%3E");
    }

    .report-title {
        font-size: 20px;
    }

    input, .gr-textbox, .gr-file-upload {
        font-size: 14px !important;
        padding: 8px !important;
    }

    .gr-button {
        font-size: 14px !important;
        padding: 8px 16px !important;
    }

    .input-container {
        margin: 15px auto;
        gap: 15px;
    }

    .main-container {
        padding: 15px;
    }

    .ats-score h3 {
        font-size: 20px;
    }

    .report-box {
        padding: 15px;
    }

    .report-box h3 {
        font-size: 20px;
    }

    .report-box h4 {
        font-size: 16px;
    }

    .report-box h5 {
        font-size: 14px;
    }

    .report-box p {
        font-size: 14px;
    }
}

@media (max-width: 480px) {
    .gradio-container h1 {
        font-size: 20px !important;
        white-space: normal !important;
        line-height: 1.2 !important;
        padding: 0 5px !important;
    }

    .gradio-container h1::before {
        content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/%3E%3Crect x='8' y='2' width='8' height='4' rx='1' ry='1'/%3E%3Cpath d='M9 10h6m-6 4h6'/%3E%3C/svg%3E");
    }

    .report-title {
        font-size: 18px;
    }

    .input-container {
        gap: 10px;
    }
}
"""

# Create the Gradio interface with no description
interface = gr.Interface(
    fn=resume_chatbot,
    inputs=[
        gr.File(label="Upload your resume (PDF)"),
        gr.Textbox(label="Enter job role (e.g., Data Scientist, Software Engineer)")
    ],
    outputs=[
        gr.HTML(label="ATS Score and Detailed Summary")
    ],
    title="ATS Resume Analyzer & Score Bot",
    description=None,
    css=custom_css
)

interface.launch()