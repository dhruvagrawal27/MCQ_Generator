# MCQ_Generator

1. File Input:  
   - Upload a document or file containing the content.  
   - The file will serve as the source for question generation.  

2. Specify Number of MCQs:  
   - Enter the desired number of multiple-choice questions (MCQs) to generate.  

3. Choose Difficulty Level:  
   - Select the complexity level of the questions: easy, medium, or hard.  

4. Technology Stack:  
   - Utilize LangChain for seamless chaining of tasks.  
   - Implement LLM models (e.g., OpenAI, Hugging Face) to process the content.  
   - Use Streamlit for an interactive web application interface.  

5. Automated Workflow:  
   - The LLM extracts data from the uploaded file.  
   - Reads and analyzes the content to identify key points.  
   - Forms MCQs with corresponding answers tailored to the selected difficulty level.  

6. Output:  
   - Displays generated MCQs and answers on the Streamlit interface.  
   - Options to download the questions for offline use.  .

Demo
[![Watch the video](https://raw.githubusercontent.com/dhruvagrawal27/MCQ_Generator/main/demothumbnail.jpg)](https://raw.githubusercontent.com/dhruvagrawal27/MCQ_Generator/main/demorun.mp4)


```
F:

cd MCQ_Generator

conda create -p env python=3.11 -y

 conda activate F:\MCQ_Generator\env

code . 

pip list
conda list...

git status
   
git add .
git status

git commit -m "folder structure updated"
git push -f origin main
git add remote origin https://github.com/dhruvagrawal27/MCQ_Generator.git

git push -f origin main

pip install -r requirements.txt
pip list

git add .
git commit -m "second commit"
git push -f origin main
```


```
source activate ./env
pip list
pip show langchain_nvidia_ai_endpoints
```