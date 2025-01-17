import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageDraw
import random
from tensorflow.keras.models import load_model

model = load_model('cnn_model.keras')

class DrawingCanvas:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=200, height=200, bg='white')
        self.canvas.pack()
        self.image = Image.new('L', (200, 200), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind('<B1-Motion>', self.paint)

    def paint(self, event):
        x, y = event.x, event.y
        r = 5
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='black', outline='black')
        self.draw.ellipse([x-r, y-r, x+r, y+r], fill='black')

    def clear(self):
        self.canvas.delete('all')
        self.draw.rectangle([0, 0, 200, 200], fill='white')

    def get_image(self):
        image = self.image.resize((28, 28)).convert('L')
        image = np.array(image)
        image = 255 - image
        return image / 255.0


class MathGame:
    def __init__(self, root):
        self.root = root
        self.canvas = DrawingCanvas(root)
        self.equation_label = tk.Label(root, text="", font=("Arial", 24))
        self.equation_label.pack()
        self.answer_button = tk.Button(root, text="Check Answer", command=self.check_answer)
        self.answer_button.pack()
        self.clear_button = tk.Button(root, text="Clear", command=self.canvas.clear)
        self.clear_button.pack()

        self.generate_equation()

    def generate_equation(self):
        self.num1 = random.randint(0, 5)
        self.num2 = random.randint(0, 5)
        self.operator = random.choice(['+'])
        self.solution = eval(f"{self.num1} {self.operator} {self.num2}")
        self.equation_label.config(text=f"{self.num1} {self.operator} {self.num2} = ?")

    def check_answer(self):
        image = np.array(self.canvas.get_image()).reshape(1, 28, 28, 1)

        prediction = model.predict(image)
        predicted_digit = np.argmax(prediction)
        
        print(predicted_digit)

        if predicted_digit == self.solution:
            messagebox.showinfo("Correct!", "Well done!")
        else:
            messagebox.showerror("Incorrect", f"The correct answer was {self.solution}. Try again!")

        self.canvas.clear()
        self.generate_equation()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Write2Solve")
    game = MathGame(root)
    root.mainloop()
