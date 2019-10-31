from algorithms.cg import CG
import tkinter as tk
from tkinter import messagebox, ttk
from tests.cs_class import *
from math import floor
# 683 --> x

# 438 --> y
class App():

    def __init__(self, master=None):
        self.center_x = master.winfo_screenwidth()/2
        self.center_y = master.winfo_screenheight()/2
        
        print(self.center_x)
        print(self.center_y)

        self.canvas = None
        #passa o master Tk()
        self.master = master
        self.casa = CG()
        #define o menubar
        self.menu = tk.Menu(self.master) 
        self.master.config(menu=self.menu)

        #define os itens do menu bar
        self.line = tk.Menu(self.menu)
        self.circ = tk.Menu(self.menu)
        self.house = tk.Menu(self.menu)
        self.cs = tk.Menu(self.menu)

        #adiciona os elementos aos itens de menu
        self.line.add_command(label='Novo', command=self.call_draw_line)
        self.circ.add_command(label='Novo', command=self.call_draw_circ)
        self.house.add_command(label='Novo', command=self.call_reset_house)
        self.house.add_command(label='Escala Local', command=self.dialog_escala)
        self.house.add_command(label='Escala Global', command=self.dialog_escala_global)
        self.house.add_command(label='Translação', command=self.dialog_translacao)
        self.house.add_command(label='Rotação', command=self.dialog_rotacao)
        self.house.add_command(label='Cisalhamento', command=self.dialog_shearing)
        self.house.add_command(label='Projeção Cavaleira', command=self.call_cavaleira)
        self.house.add_command(label='Projeção Ortogonal', command=self.dialog_projecao)
        self.house.add_command(label='Projeção Cabinet', command=self.call_cabinet)

        self.cs.add_command(label='Nova Janela', command = self.call_cohen_sutherland)
        
        #adiciona os itens de menu ao menubar
        self.menu.add_cascade(label='Linha', menu=self.line)
        self.menu.add_cascade(label='Circunferência', menu=self.circ)
        self.menu.add_cascade(label='Casa', menu=self.house)
        self.menu.add_cascade(label='Cohen-Sutherland', menu=self.cs)

        # self.dialog_master         = tk.Toplevel(self.master)
        # self.dialog_master_rotacao = tk.Toplevel(self.master)
        self.dialog_master         = None
        self.dialog_master_rotacao = None
        

    
# ----------INIÍCIO MÉTODOS DE MONITORAMENTO DE EVENTOS DE MOUSE-------------- #

    def mouse_click_line(self, event):
       
        print("Mouse position: (%s %s)" % (event.x, event.y))
        self.x1 = event.x
        self.y1 = event.y
        
    
    def mouse_release_line(self, event):
        
        print("Mouse position: (%s %s)" % (event.x, event.y))
        self.x2 = event.x
        self.y2 = event.y
        CG.line_breasenham(self.x1, self.y1, self.x2, self.y2, self.canvas)


    def mouse_click_circ(self, event):
       
        print("Mouse position: (%s %s)" % (event.x, event.y))
        self.x1 = event.x
        self.y1 = event.y
        
    
    def mouse_release_circ(self, event):
        
        print("Mouse position: (%s %s)" % (event.x, event.y))
        self.x2 = event.x
        self.y2 = event.y
        
        # input()
        r = floor(((self.x2-self.x1)**2 + (self.y2-self.y1)**2)**(1/2))
        CG.circunferencia(self.x1, self.y1, r, self.canvas)


# ----------FIM MÉTODOS DE MONITORAMENTO DE EVENTOS DE MOUSE-------------- #

# ----------INÍCIO MÉTODOS DE DIALOG-------------- #


    def dialog_get_data(self):
        status_x = self.select_x_axis.get()
        status_y = self.select_y_axis.get()
        status_z = self.select_z_axis.get()
        distance_translation_x = self.value_translation_x.get()
        distance_translation_y = self.value_translation_y.get()
        distance_translation_z = self.value_translation_z.get()
        
        if status_x and status_y and status_z:
            # passa os tres
            self.call_translacao(x=True, y=True, z=True,translacao=
            [distance_translation_x,distance_translation_y,distance_translation_z])

        elif status_x and status_y:
            # passa os dois
            self.call_translacao(x=True, y=True,translacao=
            [distance_translation_x, distance_translation_y])

        elif status_x and status_z:
            # passa os dois
            self.call_translacao(x=True,z=True,translacao=
            [distance_translation_x, distance_translation_z])

        elif status_z and status_y:
            # passa os dois
            self.call_translacao(y=True, z=True,translacao=
            [distance_translation_y, distance_translation_z])
        elif status_x:
            # passa o x
            self.call_translacao(x=True, translacao=
            [distance_translation_x])
        elif status_y:
            self.call_translacao(y=True, translacao=
            [distance_translation_y])
        elif status_z:
            self.call_translacao(z=True, translacao=
            [distance_translation_z])


    def dialog_translacao(self):
        self.init_dialog_translacao()
        self.dialog_master.lift()
        self.dialog_master.mainloop()


    def init_dialog_translacao(self):
        if self.casa == None:
            self.casa = CG()
            self.call_proj()
        
        self.dialog_master = tk.Toplevel(self.master)
        self.dialog_master.title('Selecionar translação')
        self.dialog_master.geometry('350x100+%d+%d'% 
        (self.master.winfo_screenwidth()/2,self.master.winfo_screenheight()/2))
        self.button_set_translation = Button(self.dialog_master, text="OK", command=self.dialog_get_data)
        self.button_set_translation.grid(row=10, column=1, sticky=W)
        
        tk.Label(self.dialog_master, text="Deslocamento x:").grid(row=0, sticky=W)
        tk.Label(self.dialog_master, text="Deslocamento y:").grid(row=1, sticky=W)
        tk.Label(self.dialog_master, text="Deslocamento z:").grid(row=2, sticky=W)
        
        
        self.value_translation_x = tk.Entry(self.dialog_master)
        self.value_translation_x.grid(row=0, column=1)
        self.value_translation_y = tk.Entry(self.dialog_master)
        self.value_translation_y.grid(row=1, column=1)
        self.value_translation_z = tk.Entry(self.dialog_master)
        self.value_translation_z.grid(row=2, column=1)

        self.select_x_axis = tk.BooleanVar()
        self.select_y_axis = tk.BooleanVar()
        self.select_z_axis = tk.BooleanVar()
        
        self.check_x = tk.Checkbutton(self.dialog_master, variable=self.select_x_axis, onvalue=True, offvalue=False,
         text="X")
        self.check_x.grid(row=0, column=2 , sticky=W)
        
        self.check_y = tk.Checkbutton(self.dialog_master, variable=self.select_y_axis, onvalue=True, offvalue=False,
         text="Y")
        self.check_y.grid(row=1, column=2 , sticky=W)

        self.check_z = tk.Checkbutton(self.dialog_master, variable=self.select_z_axis, onvalue=True, offvalue=False,
         text="Z")
        self.check_z.grid(row=2, column=2 , sticky=W)
        

    def dialog_rotacao(self):
        if self.casa == None:
            self.casa = CG()
            self.canvas = tk.Canvas(self.master, height=768, width=1366, background="#ffffff")
            self.canvas.grid(row=0, column=0)
        self.init_dialog_rotacao()
        self.dialog_master_rotacao.lift()
        self.dialog_master_rotacao.mainloop()


    def init_dialog_rotacao(self):
        self.dialog_master_rotacao = tk.Toplevel(self.master)
        self.dialog_master_rotacao.title('Selecionar rotação')
        self.dialog_master_rotacao.geometry('450x200+%d+%d'% 
        (self.master.winfo_screenwidth()/2,self.master.winfo_screenheight()/2))
        self.button_set_rotation = Button(self.dialog_master_rotacao, text="OK", command=self.call_rotacao)
        self.button_set_rotation.grid(row=10, column=1, sticky=W)

        tk.Label(self.dialog_master_rotacao, text="Rotação x:").grid(row=0, sticky=W)
        tk.Label(self.dialog_master_rotacao, text="Rotação y:").grid(row=1, sticky=W)
        tk.Label(self.dialog_master_rotacao, text="Rotação z:").grid(row=2, sticky=W)
        tk.Label(self.dialog_master_rotacao, text="Rotação origem:").grid(row=3, sticky=W)
        self.value_rotation_x = tk.Entry(self.dialog_master_rotacao)
        self.value_rotation_x.grid(row=0, column=1)
        self.value_rotation_y = tk.Entry(self.dialog_master_rotacao)
        self.value_rotation_y.grid(row=1, column=1)
        self.value_rotation_z = tk.Entry(self.dialog_master_rotacao)
        self.value_rotation_z.grid(row=2, column=1)
        self.value_rotation_org = tk.Entry(self.dialog_master_rotacao)
        self.value_rotation_org.grid(row=3, column=1)
        self.axis_rotation = IntVar()
        
        
        self.x_rot = tk.Radiobutton(self.dialog_master_rotacao, text='X',
         variable=self.axis_rotation, value=1).grid(row=0, column=3, sticky=W)
        self.y_rot = tk.Radiobutton(self.dialog_master_rotacao, text='Y',
         variable=self.axis_rotation, value=2).grid(row=1, column=3, sticky=W)
        self.z_rot = tk.Radiobutton(self.dialog_master_rotacao, text='Z',
         variable=self.axis_rotation, value=3).grid(row=2, column=3, sticky=W)
        self.or_rot = tk.Radiobutton(self.dialog_master_rotacao, text='Origem',
        variable=self.axis_rotation, value=4).grid(row=3, column=3, sticky=W)
        # print('finished ')


    def dialog_escala(self):
        
        self.init_dialog_escala()

        self.dialog_master_escala.lift()
        self.dialog_master_escala.mainloop()


    def init_dialog_escala(self):
        self.dialog_master_escala = tk.Toplevel(self.master)
        self.dialog_master_escala.title('Selecionar escala')
        self.dialog_master_escala.geometry('350x100+%d+%d'% 
        (self.master.winfo_screenwidth()/2,self.master.winfo_screenheight()/2))
        self.button_set_escala = Button(self.dialog_master_escala, text="OK", command=self.call_escala)
        self.button_set_escala.grid(row=10, column=1, sticky=W)

        tk.Label(self.dialog_master_escala, text="Escala x:").grid(row=0, sticky=W)
        tk.Label(self.dialog_master_escala, text="Escala y:").grid(row=1, sticky=W)
        tk.Label(self.dialog_master_escala, text="Escala z:").grid(row=2, sticky=W)
        self.value_escala_x = tk.Entry(self.dialog_master_escala)
        self.value_escala_x.grid(row=0, column=1)
        self.value_escala_y = tk.Entry(self.dialog_master_escala)
        self.value_escala_y.grid(row=1, column=1)
        self.value_escala_z = tk.Entry(self.dialog_master_escala)
        self.value_escala_z.grid(row=2, column=1)
        self.axis_escala = IntVar()
        
        
        self.x_scale = tk.Radiobutton(self.dialog_master_escala, text='X',
         variable=self.axis_escala, value=1).grid(row=0, column=3, sticky=W)
        self.y_scale = tk.Radiobutton(self.dialog_master_escala, text='Y',
         variable=self.axis_escala, value=2).grid(row=1, column=3, sticky=W)
        self.z_scale = tk.Radiobutton(self.dialog_master_escala, text='Z',
         variable=self.axis_escala, value=3).grid(row=2, column=3, sticky=W)    


    def dialog_projecao(self):
        
        self.init_dialog_proj_ortogonal()

        self.dialog_master_ortogonal.lift()
        self.dialog_master_ortogonal.mainloop() 


    def init_dialog_proj_ortogonal(self):    
        self.dialog_master_ortogonal = tk.Toplevel(self.master)
        self.dialog_master_ortogonal.title('Selecionar Plano de Projeção')
        self.dialog_master_ortogonal.geometry('350x100+%d+%d'% 
        (self.master.winfo_screenwidth()/2,self.master.winfo_screenheight()/2))
        self.button_set_ortogonal = Button(self.dialog_master_ortogonal, text="OK", command=self.call_ortogonal)
        self.button_set_ortogonal.grid(row=10, column=1, sticky=W)
        self.plano_proj = IntVar()
        self.plano_xy = tk.Radiobutton(self.dialog_master_ortogonal, text='XY',
         variable=self.plano_proj, value=1).grid(row=0, column=3, sticky=W)
        self.plano_yz = tk.Radiobutton(self.dialog_master_ortogonal, text='YZ',
         variable=self.plano_proj, value=2).grid(row=1, column=3, sticky=W)
        self.plano_xz = tk.Radiobutton(self.dialog_master_ortogonal, text='XZ',
        variable=self.plano_proj, value=3).grid(row=2, column=3, sticky=W)   

    
    def dialog_escala_global(self):
        self.init_dialog_escala_global()
        self.dialog_master_escala_global.lift()
        self.dialog_master_escala_global.mainloop() 

    
    def init_dialog_escala_global(self):
        self.dialog_master_escala_global = tk.Toplevel(self.master)
        self.dialog_master_escala_global.title('Selecionar Fator Escala Global')
        self.dialog_master_escala_global.geometry('200x100+%d+%d'% 
        (self.master.winfo_screenwidth()/2,self.master.winfo_screenheight()/2))
        self.button_set_escala_global = Button(self.dialog_master_escala_global, text="OK", command=self.call_escala_global)
        self.button_set_escala_global.grid(row=10, column=1, sticky=W)
        tk.Label(self.dialog_master_escala_global, text="Escala:").grid(row=0, column=0, sticky=W)

        self.value_escala_global = tk.Entry(self.dialog_master_escala_global)
        self.value_escala_global.grid(row=0, column=2)


    def dialog_shearing(self):
        self.init_dialog_shearing()
        self.dialog_master_shearing.lift()
        self.dialog_master_shearing.mainloop() 


    def init_dialog_shearing(self):
        self.dialog_master_shearing = tk.Toplevel(self.master)
        self.dialog_master_shearing.title('Selecionar fator e eixo de cisalhamento')
        self.dialog_master_shearing.geometry('350x100+%d+%d'% 
        (self.master.winfo_screenwidth()/2,self.master.winfo_screenheight()/2))
        self.button_set_shearing = Button(self.dialog_master_shearing, text="OK", command=self.call_shearing)
        self.button_set_shearing.grid(row=10, column=1, sticky=W)
        tk.Label(self.dialog_master_shearing, text="Shearing x:").grid(row=0, sticky=W)
        tk.Label(self.dialog_master_shearing, text="Shearing y:").grid(row=1, sticky=W)
        tk.Label(self.dialog_master_shearing, text="Shearing z:").grid(row=2, sticky=W)
        self.value_shearing_x = tk.Entry(self.dialog_master_shearing)
        self.value_shearing_x.grid(row=0, column=1)
        self.value_shearing_y = tk.Entry(self.dialog_master_shearing)
        self.value_shearing_y.grid(row=1, column=1)
        self.value_shearing_z = tk.Entry(self.dialog_master_shearing)
        self.value_shearing_z.grid(row=2, column=1)
        self.select_x_shearing = tk.BooleanVar()
        self.select_y_shearing = tk.BooleanVar()
        self.select_z_shearing = tk.BooleanVar()
        self.check_x_shear = tk.Checkbutton(self.dialog_master_shearing, variable=self.select_x_shearing, onvalue=True, offvalue=False,
         text="X")
        self.check_x_shear.grid(row=0, column=2 , sticky=W)
        self.check_y_shear = tk.Checkbutton(self.dialog_master_shearing, variable=self.select_y_shearing, onvalue=True, offvalue=False,
         text="Y")
        self.check_y_shear.grid(row=1, column=2 , sticky=W)
        self.check_z_shear = tk.Checkbutton(self.dialog_master_shearing, variable=self.select_z_shearing, onvalue=True, offvalue=False,
         text="Z")
        self.check_z_shear.grid(row=2, column=2 , sticky=W)        
                
        
# ----------FIM MÉTODOS DE DIALOG-------------- #



def main():
    
    root = tk.Tk()
    root.geometry('%dx%d+%d+%d'% (1000, 1000, root.winfo_screenheight()/2, root.winfo_screenwidth()/2))
    root.title('Trabalho de Computação Gráfica')
    App(root)
    #root.attributes('-zoomed', True)
    root.mainloop()



main()



