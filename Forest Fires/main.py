import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk as itk
import time
import matplotlib.pyplot as plt
import random

# graphical code
# parameters (lattice size, growth parameter, lightning strike frequency)
N, p, f = 256, 0.01, 0.2

res = 500   # Animation resolution
tk = Tk()
tk.geometry( str(int(res*1.1)) + 'x' + str(int(res*1.3)) )
tk.configure(background='white')

canvas = Canvas(tk, bd=2)            # Generate animation window
tk.attributes('-topmost', 0)
canvas.place(x=res/20, y=res/20, height=res, width=res)
color = ['#0008FF', '#DB0000', '#12F200']

growth = Scale(tk, from_=0, to=0.03, orient=HORIZONTAL, label='Growth probability', font=("Helvetica", 8), resolution=0.001)
growth.place(relx=.12, rely=.85, relheight=0.12, relwidth=0.33)
growth.set(p)            # Parameter slider for growth rate

p_lightning = Scale(tk, from_=0, to=1, orient=HORIZONTAL, label='Lightning rate', font=("Helvetica", 8), resolution=0.01)
p_lightning.place(relx=.57, rely=.85, relheight=0.12, relwidth=0.33)
p_lightning.set(f)          # Parameter slider for lightning rate

S = np.zeros((N, N))   # status array, 0 = no tree, 1 = tree, 2 = burned, 3 = on fire
forest = np.zeros((N, N, 3))
fire_count = 0
randomForest_fire_array = []
fire_size_array = []

timestep = 10000
# for T in range(timestep):
while fire_count < 5000:
    growth_rate = growth.get()
    LP = p_lightning.get()
    # tree growth happens with probability of growth rate --- check lecture note
    S[(np.random.rand(N, N) < growth_rate) & (S == 0)] = 1
    # lightning strike location selected
    lightning_location = (np.random.rand(2)*N).astype(int)
    # if lightning strikes a tree
    if (S[lightning_location[0], lightning_location[1]] == 1) and (np.random.rand() < LP):
        # start a fire event, increment fire_count
        fire_count += 1
        # generate random forest with same number of trees, start a fire and record size
        nTrees = sum(sum(S))
        S_rand = np.zeros((N, N))
        while sum(sum(S_rand)) <= nTrees:
            S_rand[(np.random.rand(N, N) < growth_rate) & (S_rand == 0)] = 1

        # lightning probability test until something is set on fire
        while np.not_equal(S_rand, 3):
            lightning_location1 = (np.random.rand(2) * N).astype(int)
            if S_rand[lightning_location1[0], lightning_location1[1]] == 1:
                S_rand[lightning_location1[0], lightning_location1[1]] = 3

        # expand fire
        random_fire_size = 0
        while sum(sum(S_rand == 3)) > 0:
            x = zip(np.where(S_rand == 3)[0], np.where(S == 3)[1])
            for i, j in x:
                if S_rand[min(i+1, N-1), j] == 1:
                    S_rand[min(i+1, N-1), j] = 3
                    random_fire_size += 1
                if S_rand[max(i-1, 0), j] == 1:
                    S_rand[max(i-1, 0), j] = 3
                    random_fire_size += 1
                if S_rand[i, min(j+1, N-1)] == 1:
                    S_rand[i, min(j+1, N-1)] = 3
                    random_fire_size += 1
                if S_rand[i, max(j-1, 0)] == 1:
                    S_rand[i, max(j-1, 0)] = 3
                    random_fire_size += 1
                S_rand[i, j] = 2
        randomForest_fire_array.append(random_fire_size)

        # expand fire by checking adjacent tiles
        S[lightning_location[0], lightning_location[1]] = 3   # location struck set on fire
        # check directions right, left, up, down
        fire_size = 0
        while sum(sum(S == 3)) > 0:
            x = zip(np.where(S == 3)[0], np.where(S == 3)[1])
            for i, j in x:
                if S[min(i+1, N-1), j] == 1:
                    S[min(i+1, N-1), j] = 3
                    fire_size += 1
                if S[max(i-1, 0), j] == 1:
                    S[max(i-1, 0), j] = 3
                    fire_size += 1
                if S[i, min(j+1, N-1)] == 1:
                    S[i, min(j+1, N-1)] = 3
                    fire_size += 1
                if S[i, max(j-1, 0)] == 1:
                    S[i, max(j-1, 0)] = 3
                    fire_size += 1
                S[i, j] = 2
        fire_size_array.append(fire_size)

    # create image of forest, black background
    forest[:, :, :] = 0
    # burned trees are red
    forest[:, :, 0] = (S == 2) * 255
    # grown tree are green
    forest[:, :, 1] = (S == 1) * 255
    # image update
    img = itk.PhotoImage(Image.fromarray(np.uint8(forest), 'RGB').resize((res, res)))
    # recreate canvas
    canvas.create_image(0, 0, anchor=NW, image=img)
    tk.title('Fires:' + str(fire_count))
    tk.update()
    # if there are trees burning, add time delay
    if sum(sum(S == 2)) > 0:
        time.sleep(0.03)
    # set burning trees, 2 -> 0
    S[S == 2] = 0
Tk.mainloop(canvas)  # closes window and finish

plt.hist(fire_size_array, bins=100)
plt.show()
# np.savetxt('fire1c.csv', fire_size_array, delimiter=',')  #N=256
# np.savetxt('fire4a.csv', fire_size_array, delimiter=',')  #N=16
# np.savetxt('fire4b.csv', fire_size_array, delimiter=',')  #N=256
# np.savetxt('fire5a1.csv', fire_size_array, delimiter=',')  #original
# np.savetxt('fire5a2.csv', randomForest_fire_array, delimiter=',')  #randomly generated forest

