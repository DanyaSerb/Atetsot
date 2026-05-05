import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Файл для сохранения избранного
FAVORITES_FILE = "favorites.json"

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("400x500")

        # 1. Поле ввода
        self.search_label = tk.Label(root, text="Введите имя пользователя GitHub:")
        self.search_label.pack(pady=5)
        
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        self.search_button = tk.Button(root, text="Найти", command=self.search_user)
        self.search_button.pack(pady=5)

        # 2. Список результатов
        self.results_list = tk.Listbox(root, width=50, height=10)
        self.results_list.pack(pady=10)

        # 3. Кнопка добавления в избранное
        self.fav_button = tk.Button(root, text="Добавить в избранное", command=self.add_to_favorites)
        self.fav_button.pack(pady=5)

    def search_user(self):
        username = self.entry.get().strip()
        
        # 5. Проверка корректности ввода
        if not username:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым.")
            return

        response = requests.get(f"https://github.com{username}")
        
        self.results_list.delete(0, tk.END)
        if response.status_code == 200:
            user_data = response.json()
            self.results_list.insert(tk.END, f"Логин: {user_data['login']}")
            self.results_list.insert(tk.END, f"ID: {user_data['id']}")
            self.results_list.insert(tk.END, f"Репозитории: {user_data['public_repos']}")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def add_to_favorites(self):
        # 4. Сохранение в JSON
        username = self.entry.get().strip()
        if not username: return

        favorites = []
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r") as f:
                favorites = json.load(f)

        if username not in favorites:
            favorites.append(username)
            with open(FAVORITES_FILE, "w") as f:
                json.dump(favorites, f, indent=4)
            messagebox.showinfo("Успех", f"{username} добавлен в избранное!")
        else:
            messagebox.showinfo("Инфо", "Пользователь уже в списке.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
