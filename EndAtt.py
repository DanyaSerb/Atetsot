import tkinter as tk
from tkinter import messagebox
import json
import requests  # Не забудьте: pip install requests

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("700x500")
        
        self.favorites_file = "favorites.json"
        self.favorites = self.load_favorites()
        self.current_user_data = None  # Храним полные данные текущего пользователя
        
        self.setup_ui()
        
    def setup_ui(self):
        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Username:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        # Привязываем Enter к поиску
        self.search_entry.bind('<Return>', lambda e: self.search_user())
        
        tk.Button(search_frame, text="Поиск", command=self.search_user).pack(side=tk.LEFT, padx=5)
        
        # Results display
        self.result_text = tk.Text(self.root, height=8, width=60)
        self.result_text.pack(pady=10)
        
        # Favorites frame
        favorites_frame = tk.LabelFrame(self.root, text="Избранные")
        favorites_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.favorites_listbox = tk.Listbox(favorites_frame, height=10)
        self.favorites_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="В избранное", command=self.add_to_favorites).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Удалить", command=self.remove_from_favorites).pack(side=tk.LEFT, padx=5)
        
        self.refresh_favorites()
        
    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showwarning("Ошибка", "Введите Username")
            return
            
        try:
            # Запрос к реальному API GitHub
            response = requests.get(f"https://github.com/{username}")
            
            if response.status_code == 200:
                user = response.json()
                # Сохраняем данные для добавления в избранное
                self.current_user_data = {
                    "login": user.get("login"),
                    "name": user.get("name") or "N/A",
                    "repos": user.get("public_repos"),
                    "followers": user.get("followers")
                }
                
                # Вывод в текстовое поле
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Логин: {self.current_user_data['login']}\n")
                self.result_text.insert(tk.END, f"Имя: {self.current_user_data['name']}\n")
                self.result_text.insert(tk.END, f"Репозитории: {self.current_user_data['repos']}\n")
                self.result_text.insert(tk.END, f"Подписчики: {self.current_user_data['followers']}\n")
                self.result_text.insert(tk.END, f"Ссылка: {user.get('html_url')}")
            
            elif response.status_code == 404:
                messagebox.showerror("Ошибка", f"Пользователь {username} не найден")
            else:
                messagebox.showerror("Ошибка API", f"Статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка сети", f"Не удалось подключиться: {e}")

    def add_to_favorites(self):
        if self.current_user_data:
            login = self.current_user_data['login']
            if login not in self.favorites:
                self.favorites[login] = self.current_user_data
                self.save_favorites()
                self.refresh_favorites()
            else:
                messagebox.showinfo("Инфо", "Уже в списке")
        else:
            messagebox.showwarning("Внимание", "Сначала найдите пользователя")
            
    def remove_from_favorites(self):
        selection = self.favorites_listbox.curselection()
        if selection:
            username = self.favorites_listbox.get(selection[0])
            if username in self.favorites:
                del self.favorites[username]
                self.save_favorites()
                self.refresh_favorites()
        else:
            messagebox.showwarning("Ошибка", "Выберите пользователя из списка")
            
    def refresh_favorites(self):
        self.favorites_listbox.delete(0, tk.END)
        for username in self.favorites:
            self.favorites_listbox.insert(tk.END, username)
            
    def load_favorites(self):
        try:
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
        
    def save_favorites(self):
        with open(self.favorites_file, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
