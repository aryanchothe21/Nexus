from client import aiProcess

print("Sending request to Gemini...")

answer = aiProcess("What is Java?")

print("Gemini responded:")
print(answer)