# ATS Resume Analyzer & Score Bot

## Introduction

The ATS Resume Analyzer & Score Bot is a tool designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). It analyzes a resume (in PDF format) against a specified job role and provides a compatibility score along with actionable feedback to improve the resume's chances of passing ATS filters. Whether you're a recent graduate, a career changer, or a seasoned professional, this tool can help you tailor your resume to better match job requirements. The app now features an expanded list of IT job roles, enhanced skills coverage, and a mobile-optimized interface for a seamless user experience.

## Features

- **ATS Compatibility Score**: Get a percentage score indicating how well your resume matches the selected job role.
- **Detailed Feedback**: Receive insights on missing sections, skill relevance, structural issues, and experience analysis.
- **Expanded Job Role Support**: Supports a wide range of IT job roles, including Data Scientist, Software Engineer, Big Data Engineer, SDET, and more.
- **User-Friendly Interface**: Built with Gradio for an intuitive and interactive experience, now optimized for mobile devices with smooth scrolling.
- **Job Recommendations**: Provides job search links tailored to your experience level (Fresher or Experienced) for recommended roles.

## How It Works

1. **Upload Your Resume**: Provide your resume in PDF format.
2. **Specify a Job Role**: Enter the job role you're targeting (e.g., "Data Scientist", "Software Engineer").
3. **Get Your Score and Feedback**: The tool analyzes your resume and provides:
   - An ATS compatibility score (e.g., 66.7%).
   - A detailed report on resume structure, detected skills, missing skills, experience analysis, and recommended job roles with search links.
4. **Improve Your Resume**: Use the feedback to update your resume and re-run the analysis for a better score.

## Supported Job Roles

The tool currently supports the following IT job roles:

- Data Scientist
- Software Engineer
- Project Manager
- Web Developer
- DevOps Engineer
- Cybersecurity Analyst
- Database Administrator
- Machine Learning Engineer
- Cloud Engineer
- Full Stack Developer
- Mobile App Developer
- UI/UX Designer
- Business Analyst
- Network Engineer
- System Administrator
- Quality Assurance Engineer
- AI Engineer
- Data Engineer
- Game Developer
- Blockchain Developer
- IoT Developer
- IT Support Specialist
- Embedded Systems Engineer
- AR/VR Developer
- Robotics Engineer
- Site Reliability Engineer
- Frontend Developer
- Backend Developer
- Data Analyst
- Technical Writer
- IT Consultant
- ERP Consultant
- Solutions Architect
- Product Manager
- Scrum Master
- Information Security Manager
- Big Data Engineer
- Automation Engineer
- Network Security Engineer
- Software Architect
- IT Auditor
- Digital Transformation Specialist
- E-commerce Developer
- API Developer
- Geospatial Analyst
- SDET (Software Development Engineer in Test)

If your desired role is not listed, please let us know, and we can consider adding it!

## Usage Instructions

### Running Locally

1. **Clone the Repository**:

2. **Set Up a Virtual Environment** (optional but recommended):

3. **Install Dependencies**:

4. **Run the App**:
The app will launch at `http://127.0.0.1:7860`. Open this URL in your browser.

5. **Test on Mobile**:
- Find your laptop’s IP address (e.g., on Windows: `ipconfig`, on Linux/Mac: `ifconfig` or `ip addr`).
- Access the app on your mobile device using `http://<your-laptop-ip>:7860`.

### Using the Hosted Version

1. **Visit the Space**: Go to the [ATS Resume Analyzer Space](https://huggingface.co/spaces/Kamesh14/ATS-Resume-Analyzer) on Hugging Face.
2. **Upload Your Resume**: Click the "Upload your resume (PDF)" field and select your resume file in PDF format.
3. **Enter a Job Role**: In the "Enter job role" field, type the job role you're applying for (e.g., "Data Scientist").
4. **Submit**: Click the "Submit" button to analyze your resume.
5. **Review Results**: Check your ATS score, detailed feedback, and job recommendations to identify areas for improvement.
6. **Iterate**: Update your resume based on the feedback and re-run the analysis as needed.

## Example Output

After uploading a resume and selecting "Data Scientist" as the job role, you might see:

- **ATS Score**: 66.7%
- **Summary**: "Your resume scores 66.7% for the Data Scientist role. It demonstrates strong skills in Python, machine learning, and SQL, but is missing key sections like Education, which are critical for ATS compatibility."
- **Resume Structure Analysis**: Issues detected: Missing "Education" section. Recommended order: Contact → Summary → Skills → Experience → Education.
- **Skill Relevance Summary**:
- Python: Critical skill detected
- Machine learning: Critical skill detected
- SQL: Critical skill detected
- **Suggested Skills to Add**: Statistics, R, data visualization, plotly
- **Experience Analysis**:
- Experience Level: Fresher
- Total Years of Experience: 0 years
- **Recommended Roles**:
- Data Analyst (Match Score: 50.0%): Matched Skills: SQL, Python
 - Search for Data Analyst jobs (filtered for Fresher):
   - [LinkedIn](https://www.linkedin.com/jobs/search/?keywords=Data+Analyst+entry+level)
   - [Indeed](https://www.indeed.com/jobs?q=Data+Analyst+entry+level)

## Limitations

- The tool only supports resumes in PDF format.
- Analysis is limited to the predefined job roles listed above.
- The ATS score is an estimate based on common ATS criteria and may not reflect the exact behavior of all ATS systems.
- Resumes with complex formatting (e.g., headers, footers, tables) may not be parsed accurately.
- The tool currently operates in dark mode only (light mode toggle has been removed for simplicity).

## Contributing

We welcome contributions to improve the ATS Resume Analyzer! If you'd like to add new job roles, enhance the analysis algorithm, or improve the UI, please:

1. Fork the repository: [ATS Resume Analyzer GitHub](https://github.com/Kamesh14/ATS-Resume-Analyzer).
2. Create a new branch for your changes:
3. Commit your changes:
4. Push to your fork:
5. Submit a pull request with a detailed description of your updates.

You can also report issues or suggest features by opening an issue in the repository: [Issue Tracker](https://github.com/Kamesh14/ATS-Resume-Analyzer/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, feedback, or support, please open an issue in the repository: [Issue Tracker](https://github.com/Kamesh14/ATS-Resume-Analyzer/issues) or contact me at [kamesh743243@gmail.com](mailto:kamesh743243@gmail.com).

## Acknowledgements

- Built with [Gradio](https://gradio.app/) for the interactive interface.
- Uses [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction.
- Hosted on [Hugging Face Spaces](https://huggingface.co/spaces).
- Inspired by the need to help job seekers navigate ATS systems effectively.
