import json
import requests
from threading import Thread, Lock
from typing import List

class Test:
    lock = Lock()
    print_lock = Lock()
    
    count = 0
    right = 0
    lines = []
    num_threads = 0
    num_finished = 0
    
    def __init__(self, thread_num: int):
        self.thread_num = thread_num
        thread = Thread(target=self.run)
        thread.start()
        
    def run(self):
        try:
            for i in range(len(self.lines)):
                if (i % self.num_threads) != self.thread_num:
                    continue
                    
                line = self.lines[i]
                line = line.replace("  ", " ")
                
                # Parse JSON line directly instead of using string manipulation
                data = json.loads(line)
                question = data["question"]
                choices = data["choices"]
                answer_index = str(data["answer"])
                
                answers = ""
                for j, choice in enumerate(choices):
                    answers += f"\n{j}\t{choice}"
                
                thought_prompt = "How should you best think about this? Explain your thought process step by step."
                thoughts = self.generate(thought_prompt, question + "\n" + answers, 4096, 0)
                
                output_format = "Output only a single digit representing your choice (with no additional commentary)"
                choice = self.generate(output_format, 
                                     question + "\n" + answers + "\n\n--- Thoughts ---\n" + thoughts,
                                     1024, 0)
                choice = ''.join(filter(str.isdigit, choice))
                
                with self.lock:
                    self.__class__.count += 1
                    if choice == answer_index:
                        self.__class__.right += 1
                
                with self.print_lock:
                    print("===============")
                    print(question + "\n" + answers)
                    print("\n" + thoughts + "\n")
                    print(f"[RESULT {i}] {answer_index}\t{choice}")
                    print(f"{self.count}\t{(self.right * 100.0) / self.count:.2f}%")
                    
        except Exception as e:
            print(f"Error: {str(e)}")
            
        with self.lock:
            self.__class__.num_finished += 1
            if self.num_finished == self.num_threads:
                print(f"{self.count}\t{(self.right * 100.0) / self.count:.2f}%")
    
    @staticmethod
    def generate(system: str, user: str, max_response_characters: int, temp: float) -> str:
        MAX_CONTEXT_LENGTH = 128000
        
        system = system.strip()
        user = user.strip()
        
        if max_response_characters > MAX_CONTEXT_LENGTH:
            max_response_characters = MAX_CONTEXT_LENGTH
            
        payload = {
            "model": "/home/ubuntu/Chicago/code/models/Meta-Llama-3.1-405B-Instruct-AWQ-INT4",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": temp,
            "max_tokens": int(max_response_characters / 4.4),
            "stop": ["<|eot_id|>"]
        }
        
        response = requests.post(
            "http://127.0.0.1:8000/v1/chat/completions",
            json=payload
        )
        
        content = response.json()
        response_text = content["choices"][0]["message"]["content"].strip()
        
        # Remove markdown-style bold markers
        response_text = response_text.replace("**", "")
        
        return response_text.strip()

def main():
    try:
        import sys
        Test.num_threads = int(sys.argv[1])
        
        with open("mmlu_scrambled.jsonl", "r") as f:
            Test.lines = f.readlines()
            
        threads = [Test(i) for i in range(Test.num_threads)]
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
