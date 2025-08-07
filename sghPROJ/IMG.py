import matplotlib.pyplot as plt
import matplotlib.patches as patches
import menu as menu

fig, ax = plt.subplots(figsize=(14, 8))
dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

horarios = [
    '07:10 - 08:00', '08:00 - 08:50', '08:50 - 09:40', '09:55 - 10:45',
    '10:45 - 11:35', '11:35 - 12:25', '12:25 - 13:50', '13:50 - 14:40',
    '14:40 - 15:30', '15:50 - 16:40', '16:40 - 17:30', '17:30 - 19:00',
    '19:00 - 19:50', '19:50 - 20:40', '20:50 - 21:40', '21:40 - 22:30'
]

for i in range(len(dias)):
    for t in range(len(horarios)):
        ax.add_patch(patches.Rectangle((i, t),1, 1, edgecolor='black', facecolor='white'))


plt.show()