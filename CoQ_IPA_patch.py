#!/usr/bin/env python
# coding: utf-8

# In[16]:


import tkinter as tk
from tkinter import messagebox, filedialog, font
import subprocess
import os
import threading

class IPAPatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IPA 패치 도구")
        self.root.geometry("400x300")  # 창 크기 키움

        # 폰트 설정
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.button_font_f = font.Font(family="Helvetica", size=10)
        self.button_font = font.Font(family="Helvetica", size=15, weight="bold")
        
        # 기본 경로
        self.default_path = r"C:\Program Files (x86)\Steam\steamapps\common\Caves of Qud"
        
        # 경로 입력 프레임
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=10)

        # 경로 라벨
        tk.Label(path_frame, text="Caves of Qud 경로:", font=self.button_font_f).pack(side=tk.LEFT)

        # 경로 입력 필드 (너비 줄임)
        self.path_var = tk.StringVar(value=self.default_path)
        self.path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=20, font=self.button_font_f)
        self.path_entry.pack(side=tk.LEFT, padx=10)

        # 폴더 선택 버튼
        tk.Button(path_frame, text="폴더 선택", font=self.button_font_f, command=self.select_folder).pack(side=tk.LEFT)

        # 메인 라벨
        tk.Label(self.root, text="Caves of Qud IPA 패치", font=self.title_font).pack(pady=3)

        # 패치 적용 버튼
        tk.Button(self.root, text="패치 적용", font=self.button_font, width=15, height=2, command=self.apply_patch).pack(pady=3)

        # 패치 해제 버튼
        tk.Button(self.root, text="패치 해제", font=self.button_font, width=15, height=2, command=self.remove_patch).pack(pady=3)

        # 종료 버튼
        tk.Button(self.root, text="종료", font=self.button_font, width=15, height=2, command=self.root.quit).pack(pady=3)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Caves of Qud 폴더 선택")
        if folder:
            self.path_var.set(folder)

    def get_paths(self):
        base_path = self.path_var.get()
        ipa_path = os.path.join(base_path, "IPA.exe")
        coq_path = os.path.join(base_path, "CoQ.exe")
        original_path = os.path.join(base_path, "CoQ_Data", "Managed", "UnityEngine.dll")
        backup_path = os.path.join(base_path, "CoQ_Data", "Managed", "UnityEngine.dll.bak")
        return ipa_path, coq_path, original_path, backup_path

    def rename_unity_file(self, case):
        _, _, original_path, backup_path = self.get_paths()
        if case == "backup":
            try:
                if os.path.exists(original_path):
                    os.rename(original_path, backup_path)
                    return True
                else:
                    messagebox.showerror("오류", "UnityEngine.dll 파일을 찾을 수 없습니다.")
                    return False
            except PermissionError:
                messagebox.showerror("오류", "파일 접근 권한이 없습니다. 프로그램을 관리자 권한으로 실행하세요.")
                return False
            except Exception as e:
                messagebox.showerror("오류", f"파일 이름 변경 실패: {str(e)}")
                return False
        elif case == "restore":
            try:
                if os.path.exists(backup_path):
                    os.rename(backup_path, original_path)
                    return True
                else:
                    messagebox.showerror("오류", "UnityEngine.dll.bak 파일을 찾을 수 없습니다.")
                    return False
            except PermissionError:
                messagebox.showerror("오류", "파일 접근 권한이 없습니다. 프로그램을 관리자 권한으로 실행하세요.")
                return False
            except Exception as e:
                messagebox.showerror("오류", f"파일 복원 실패: {str(e)}")
                return False
        else:
            messagebox.showerror("오류", "잘못된 case 값입니다.")
            return False

    def run_apply_patch(self):
        ipa_path, coq_path, _, _ = self.get_paths()
        working_dir = os.path.dirname(ipa_path)
        
        if self.rename_unity_file("backup"):
            try:
                subprocess.run(
                    f'"{ipa_path}" "{coq_path}"',
                    shell=True,
                    check=True,
                    cwd=working_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if self.rename_unity_file("restore"):
                    messagebox.showinfo("성공", "패치가 완료되었습니다!")
                else:
                    messagebox.showerror("오류", "파일 복원에 실패했습니다.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("오류", f"패치 실행 실패: {e.stderr}")
                self.rename_unity_file("restore")
            except Exception as e:
                messagebox.showerror("오류", f"패치 실패: {str(e)}")
                self.rename_unity_file("restore")

    def apply_patch(self):
        threading.Thread(target=self.run_apply_patch, daemon=True).start()

    def run_remove_patch(self):
        ipa_path, coq_path, _, _ = self.get_paths()
        working_dir = os.path.dirname(ipa_path)
        
        if self.rename_unity_file("backup"):
            command = f'"{ipa_path}" "{coq_path}" --revert'
            process = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=working_dir
            )
            stdout, stderr = process.communicate(input="\n")
            if self.rename_unity_file("restore"):
                messagebox.showinfo("성공", "패치가 해제되었습니다!")
            else:
                messagebox.showerror("오류", "파일 백업에 실패했습니다.")

    def remove_patch(self):
        threading.Thread(target=self.run_remove_patch, daemon=True).start()

# GUI 실행
root = tk.Tk()
app = IPAPatcherApp(root)
root.mainloop()


# In[ ]:





# In[ ]:




